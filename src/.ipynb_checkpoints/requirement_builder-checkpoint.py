"""
Healthcare User Story Extractor (Vertex AI + RAG + Async + BigQuery Export)
---------------------------------------------------------------------------
Parses healthcare requirement docs and extracts validated user stories
using Google Vertex AI (Gemini + Embeddings). Optionally exports results
to BigQuery with dynamic schema inference.

Deps:
  pip install google-cloud-aiplatform langchain-google-vertexai PyPDF2 python-docx pydantic numpy tqdm
Auth:
  gcloud auth application-default login
"""

LLM_MODEL = "gemini-2.0-flash"  # e.g., "gemini-1.5-pro"

import os
import re
import json
import uuid
import asyncio
import docx
import xml.etree.ElementTree as ET
import numpy as np
from tqdm.auto import tqdm
from PyPDF2 import PdfReader
from typing import List, Iterable, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

from google.cloud import bigquery
from langchain_google_vertexai import VertexAIEmbeddings, VertexAI

# ========================== Helpers & Schema ==========================

def _story_text_for_embedding(s: dict) -> str:
    """Flatten story + ACs for richer similarity signals."""
    ac = s.get("acceptance_criteria", []) or []
    ac_text = " | ".join([f"G:{a.get('given','')} W:{a.get('when','')} T:{a.get('then','')}" for a in ac])
    return f"{s.get('user_story','')} || {ac_text}"

class AcceptanceCriteria(BaseModel):
    given: str
    when: str
    then: str

class Citation(BaseModel):
    page: int
    snippet: str

class UserStory(BaseModel):
    epic: str
    story_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_story: str
    acceptance_criteria: List[AcceptanceCriteria]
    priority: str
    dependencies: List[str] = []
    non_functional: List[str] = []
    source_requirement_ids: List[str] = []
    assumptions: List[str] = []
    open_questions: List[str] = []
    citations: List[Citation] = []   # NEW

SCHEMA = {
    "epic": "",
    "story_id": "",
    "user_story": "As a <role>, I want <capability> so that <benefit>.",
    "acceptance_criteria": [
        {"given": "", "when": "", "then": ""}
    ],
    "priority": "Must|Should|Could|Won't",
    "dependencies": [],
    "non_functional": [],
    "source_requirement_ids": [],
    "assumptions": [],
    "open_questions": [],
    "citations": [{"page": 0, "snippet": ""}]  # NEW
}

# ========================== Parsing & Normalization ==========================

BULLET_RE = re.compile(r"^\s*(?:[-*•]|[0-9]+[.)])\s+")
REQ_ID_RE  = re.compile(r"^(REQ[-\s]?\d+|[A-Z]{2,}\d+|[0-9]+(?:\.[0-9]+)*)\b")
REQ_KEYWORDS = re.compile(r"\b(system shall|shall|must|should|ability to|capability to|enable|allow)\b", re.I)

def parse_pdf_pages(path: str) -> List[Dict[str, Any]]:
    """Return list of {'page': int, 'text': str} for PDFs."""
    reader = PdfReader(path)
    pages = []
    for idx, page in enumerate(reader.pages, start=1):
        pages.append({"page": idx, "text": page.extract_text() or ""})
    return pages

def parse_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def parse_xml(path: str) -> str:
    tree = ET.parse(path)
    root = tree.getroot()
    return ET.tostring(root, encoding="unicode")

def parse_json_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return json.dumps(json.load(f), indent=2, ensure_ascii=False)

def parse_file_text_or_pages(path: str) -> Dict[str, Any]:
    """Return {'text': str} for non-PDFs, or {'pages': [{page, text}, ...]} for PDFs."""
    path_l = path.lower()
    if path_l.endswith(".pdf"):
        return {"pages": parse_pdf_pages(path)}
    if path_l.endswith(".docx"):
        return {"text": parse_docx(path)}
    if path_l.endswith(".xml"):
        return {"text": parse_xml(path)}
    if path_l.endswith(".json"):
        return {"text": parse_json_text(path)}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return {"text": f.read()}

def normalize_text(text: str) -> str:
    """Join soft-wrapped lines, preserve bullets/headings, keep paragraph breaks."""
    lines = text.splitlines()
    out = []
    buf = ""
    for raw in lines:
        line = raw.rstrip()
        # blank line => paragraph break
        if not line.strip():
            if buf:
                out.append(buf)
                buf = ""
            out.append("")
            continue
        # new bullet or heading/ID => start new requirement block
        if BULLET_RE.match(line) or REQ_ID_RE.match(line):
            if buf:
                out.append(buf)
            buf = line.strip()
            continue
        # soft wrap: if buf doesn't end sentence punctuation, join
        if buf and not buf.endswith((".", ":", ";")):
            buf += " " + line.strip()
        else:
            if buf:
                out.append(buf)
            buf = line.strip()
    if buf:
        out.append(buf)
    # collapse consecutive blanks
    cleaned = []
    for s in out:
        if s == "" and cleaned and cleaned[-1] == "":
            continue
        cleaned.append(s)
    return "\n".join(cleaned)

def normalize_page_text(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{"page": p["page"], "text": normalize_text(p["text"])} for p in pages]

import re
from typing import List, Dict

# ========================== Heading-based Epic Extraction ==========================

# ========================== Heading-based Epic Extraction ==========================

HEADING_RE = re.compile(r"^(\d+(?:\.\d+)*)(?:\s+)([A-Z][\w\s-]+.*)$")

# Generic section titles we don't want to use as epics
GENERIC_HEADINGS = {
    "introduction", "purpose", "scope",
    "functional requirements", "non-functional requirements",
    "references", "appendix"
}

def extract_headings(text: str) -> Dict[str, str]:
    """
    Extract headings like '2.1.2 Clinician Portal Development'
    Returns dict: {'2.1.2': 'Clinician Portal Development'}
    Skips generic titles.
    """
    headings = {}
    for line in text.splitlines():
        m = HEADING_RE.match(line.strip())
        if m:
            sec_id = m.group(1)
            title = m.group(2).strip()
            # Skip generic container titles
            if title.lower() not in GENERIC_HEADINGS:
                headings[sec_id] = title
    return headings

def assign_epic(req_id: str, headings: Dict[str, str]) -> str:
    """
    Assign epic based on the closest heading prefix.
    Example: req_id='2.1.2.5' → epic='Clinician Portal Development'
    Falls back to 'General' if none found.
    """
    for h in sorted(headings.keys(), key=lambda x: -len(x)):  # longest prefix first
        if req_id.startswith(h):
            return headings[h]
    return "General"



def split_requirements_with_epics(text: str) -> List[Dict[str, str]]:
    """
    Segment into atomic requirements with IDs (AUTO-n fallback),
    and attach inferred epics from document headings.
    """
    headings = extract_headings(text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    requirements = []
    cur = None

    def flush():
        nonlocal cur
        if cur and cur["text"].strip():
            cur["text"] = re.sub(r"\s+", " ", cur["text"]).strip()
            # Assign epic from headings
            cur["epic"] = assign_epic(cur["req_id"], headings)
            requirements.append(cur)
        cur = None

    for i, line in enumerate(lines):
        rid = None
        content = line
        start_new = False

        # Requirement ID pattern
        m = re.match(r"^(REQ[-\s]?\d+|[0-9]+(?:\.[0-9]+)*)\b", line)
        if m:
            rid = m.group(0)
            start_new = True
            content = line[m.end():].strip() or line.strip()
        elif re.match(r"^\s*[-*•]\s+", line):  # bullet point
            start_new = True
            content = line.strip()

        if start_new:
            flush()
            rid = rid or f"AUTO-{len(requirements)+1}"
            cur = {"req_id": rid, "text": content}
        else:
            if cur:
                cur["text"] += " " + content
            else:
                cur = {"req_id": f"AUTO-{len(requirements)+1}", "text": content}

    flush()
    return requirements


def chunked(seq: List[Any], n: int) -> Iterable[List[Any]]:
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

# ========================== RAG Index & Retrieval ==========================

def page_chunks(pages: List[Dict[str, Any]], max_chars=1500, overlap=200) -> List[Dict[str, Any]]:
    """Create sliding-window chunks with page provenance."""
    chunks = []
    for p in pages:
        t = p["text"]
        i = 0
        while i < len(t):
            j = min(len(t), i + max_chars)
            chunk = t[i:j]
            chunks.append({"page": p["page"], "text": chunk})
            if j == len(t): break
            i = j - overlap
    return chunks

def _cosines(query_emb, matrix):
    sims = []
    q = np.array(query_emb, dtype=float)
    qn = np.linalg.norm(q)
    for v in matrix:
        v = np.array(v, dtype=float)
        vn = np.linalg.norm(v)
        sims.append(0.0 if qn == 0 or vn == 0 else float(np.dot(q, v) / (qn * vn)))
    return sims

def build_retriever(embedder: VertexAIEmbeddings, chunks: List[Dict[str, Any]]):
    texts = [c["text"] for c in chunks]
    embs = embedder.embed_documents(texts)
    return {"chunks": chunks, "embs": embs}

def retrieve_context(retriever: Dict[str, Any], embedder: VertexAIEmbeddings, query: str, top_k=3):
    q_emb = embedder.embed_query(query)
    sims = _cosines(q_emb, retriever["embs"])
    idxs = np.argsort(sims)[::-1][:top_k]
    results = []
    for i in idxs:
        c = retriever["chunks"][i]
        results.append({"page": c["page"], "text": c["text"], "score": float(sims[i])})
    return results

# ========================== LLM Utils ==========================

async def safe_llm_batch_async(llm, prompts, timeout=60):
    """Run multiple LLM calls concurrently with timeout handling."""
    tasks = [llm.ainvoke(p) for p in prompts]  # VertexAI async call
    try:
        return await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=timeout)
    except asyncio.TimeoutError:
        print("⏳ Timeout reached, skipping batch.")
        return ["{}" for _ in prompts]

FENCE_OPEN_RE = re.compile(r"^```(?:json|JSON)?\s*")
FENCE_CLOSE_RE = re.compile(r"\s*```$")

def clean_response(resp) -> str:
    """Convert VertexAI response to a plain JSON string. Strips ```json fences."""
    if isinstance(resp, Exception):
        return "{}"
    if isinstance(resp, str):
        text = resp.strip()
    elif hasattr(resp, "content") and isinstance(resp.content, str):
        text = resp.content.strip()
    elif hasattr(resp, "content"):
        text = str(resp.content).strip()
    else:
        text = str(resp).strip()

    # Strip code fences
    text = FENCE_OPEN_RE.sub("", text)
    text = FENCE_CLOSE_RE.sub("", text)
    if "```" in text:
        text = text.replace("```json", "").replace("```JSON", "").replace("```", "")
    return text.strip()

def extract_json_object(text: str) -> str:
    """Try to salvage the first balanced {...} block from text."""
    start = text.find("{")
    if start == -1:
        return text
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return text[start:]  # fallback

def cosine_similarity(a, b) -> float:
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0.0:
        return 0.0
    return float(np.dot(a, b) / denom)

# ========================== Alignment Checks ==========================

STOP = set(("the","and","of","to","in","a","for","on","with","by","is","be","as","at","or","an","from"))

def key_terms(s: str):
    toks = re.findall(r"[A-Za-z0-9_]+", s.lower())
    return set(t for t in toks if t not in STOP and len(t) > 2)

def alignment_score(req_text: str, citations: List[dict]) -> float:
    req_terms = key_terms(req_text)
    ctx_terms = set()
    for c in citations or []:
        ctx_terms |= key_terms(c.get("snippet",""))
    if not req_terms or not ctx_terms:
        return 0.0
    return len(req_terms & ctx_terms) / float(len(req_terms | ctx_terms))

def validate_alignment(requirement: Dict[str, str], story: Dict[str, Any], min_score=0.15):
    score = alignment_score(requirement.get("text",""), story.get("citations", []))
    ok = score >= min_score and len(story.get("citations", [])) > 0
    return ok, score
import csv

import csv


# ========================== Extractor ==========================

class HealthcareStoryExtractor:
    def __init__(self, project_id, location="us-central1",
                 embedding_model="text-embedding-005",
                 classifier_model=LLM_MODEL):
        self.project_id = project_id
        self.location = location
        self.embedder = VertexAIEmbeddings(
            model=embedding_model,
            project=project_id,
            location=location
        )
        self.llm = VertexAI(
            model_name=classifier_model,
            temperature=0.2,   # slight diversity, still stable JSON
            top_p=0.9,
            top_k=40,
            project=project_id,
            location=location,
        )

    async def generate_user_stories_batch(
        self,
        requirements,
        glossary,
        actors,
        constraints,
        batch_size=5,
        retriever: Optional[Dict[str, Any]] = None,
    ):
        # Use dumps to avoid quote-escaping hell in long strings
        abstain = {
            "epic": "",
            "story_id": "",
            "user_story": "",
            "acceptance_criteria": [],
            "priority": "",
            "dependencies": [],
            "non_functional": [],
            "source_requirement_ids": [],
            "assumptions": ["Insufficient context"],
            "open_questions": ["Need clarification"],
            "citations": [],
        }

        system_prompt = (
            "You are a senior BA in healthcare software.\n"
            "Use ONLY the provided glossary, actors, constraints, and CONTEXT SNIPPETS.\n"
            "Cite which page(s) you used in the 'citations' field; include a short snippet from each page.\n"
            "If the context is insufficient or unrelated, return EXACTLY this JSON:\n"
            f"{json.dumps(abstain, indent=2)}\n"
            "Return ONLY valid JSON with this schema (no markdown, no commentary):\n"
            f"{json.dumps(SCHEMA, indent=2)}"
        )

        stories = []
        for i in tqdm(range(0, len(requirements), batch_size), desc="LLM batches"):
            batch_reqs = requirements[i:i + batch_size]
            prompts = []
            for req in batch_reqs:
                ctx = []
                if retriever is not None:
                    hits = retrieve_context(retriever, self.embedder, req["text"], top_k=3)
                    ctx = [{"page": h["page"], "snippet": h["text"][:500]} for h in hits]  # cap snippet

                user_prompt = (
                    f"GLOSSARY: {glossary}\n"
                    f"ACTORS: {actors}\n"
                    f"CONSTRAINTS: {constraints}\n"
                    f"CONTEXT SNIPPETS: {json.dumps(ctx, ensure_ascii=False)}\n"
                    f"REQUIREMENT (ID: {req['req_id']}): {req['text']}"
                )
                prompts.append(f"{system_prompt}\n\n{user_prompt}")

            responses = await safe_llm_batch_async(self.llm, prompts)

            for req, resp in zip(batch_reqs, responses):
                raw_text = clean_response(resp)
                try:
                    try:
                        story_json = json.loads(raw_text)
                    except json.JSONDecodeError:
                        story_json = json.loads(extract_json_object(raw_text))

                    us = UserStory(**story_json)

                    # Force unique story_id & keep provenance
                    us.story_id = str(uuid.uuid4())
                    if not us.source_requirement_ids:
                        us.source_requirement_ids = [req["req_id"]]

                    stories.append(us.model_dump())  # pydantic v2
                except (json.JSONDecodeError, ValidationError) as e:
                    print(f"❌ Invalid JSON for {req['req_id']}: {e}\nRaw output:\n{raw_text}\n")

        self._last_requirements = requirements
        return stories



    def check_duplicates(self, stories, threshold=0.99):
        """Return list of (story_id_i, story_id_j, similarity) for near-duplicates across different source reqs."""
        texts = [_story_text_for_embedding(s) for s in stories if s.get("user_story")]
        if not texts:
            return []

        embeddings = self.embedder.embed_documents(texts)
        flagged = []

        total_pairs = (len(embeddings) * (len(embeddings) - 1)) // 2
        pbar = tqdm(total=total_pairs, desc="Duplicate check")
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                # provenance-aware: skip same-source pairs
                src_i = set(stories[i].get("source_requirement_ids", []))
                src_j = set(stories[j].get("source_requirement_ids", []))
                if not (src_i & src_j):
                    sim = cosine_similarity(embeddings[i], embeddings[j])
                    if sim >= threshold:
                        flagged.append((stories[i]["story_id"], stories[j]["story_id"], sim))
                pbar.update(1)
        pbar.close()
        return flagged

    def dedupe_stories(self, stories, threshold=0.99):
        """Cluster near-duplicates and keep the best representative per cluster."""
        if not stories:
            return stories

        texts = [_story_text_for_embedding(s) for s in stories]
        embeddings = self.embedder.embed_documents(texts)

        # Union-Find with progress
        parent = list(range(len(stories)))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        total_pairs = (len(embeddings) * (len(embeddings) - 1)) // 2
        pbar = tqdm(total=total_pairs, desc="Clustering dupes")
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                src_i = set(stories[i].get("source_requirement_ids", []))
                src_j = set(stories[j].get("source_requirement_ids", []))
                if not (src_i & src_j):
                    sim = cosine_similarity(embeddings[i], embeddings[j])
                    if sim >= threshold:
                        union(i, j)
                pbar.update(1)
        pbar.close()

        clusters = {}
        for idx in range(len(stories)):
            r = find(idx)
            clusters.setdefault(r, []).append(idx)

        # pick representative: more ACs, then longer text
        def score(k):
            ac_len = len(stories[k].get("acceptance_criteria", []) or [])
            txt_len = len(texts[k])
            return (ac_len, txt_len)

        kept = []
        dropped_pairs = []  # (kept_id, dropped_id, cluster_size)
        for _, idxs in clusters.items():
            if len(idxs) == 1:
                kept.append(stories[idxs[0]])
                continue
            best = max(idxs, key=score)
            kept.append(stories[best])
            for other in idxs:
                if other != best:
                    dropped_pairs.append((stories[best]["story_id"], stories[other]["story_id"], len(idxs)))

        if dropped_pairs:
            preview = [(k, d, int(n)) for k, d, n in dropped_pairs]
            print("🧹 Dedupe kept/dropped:", preview)

        return kept


    async def extract_from_file(
        self,
        file_path,
        constraints="HIPAA, FDA 21 CFR Part 11",
        batch_llm_size=20,
        llm_inner_batch=5,
        dedupe=True,
        dup_threshold=0.99,
        min_alignment=0.15,
        TEST=False
    ):
        print("📥 Parsing document...")
        parsed = parse_file_text_or_pages(file_path)

        retriever = None
        if "pages" in parsed:
            print("🧹 Normalizing PDF pages & building RAG index...")
            norm_pages = normalize_page_text(parsed["pages"])
            chunks = page_chunks(norm_pages, max_chars=1500, overlap=200)
            retriever = build_retriever(self.embedder, chunks)
            full_text = "\n".join([p["text"] for p in norm_pages])
        else:
            full_text = parsed["text"]

        print("🧩 Segmenting requirements...")
        requirements = split_requirements_with_epics(full_text)
        print(f"📌 Found requirements: {len(requirements)}")

        # ✅ Limit for test mode
        if TEST:
            requirements = requirements[:10]
            print(f"⚡ TEST mode active → using only {len(requirements)} requirements")

        glossary = {"EHR": "Electronic Health Record", "HL7": "Data exchange standard"}
        actors = {"Doctor": "Reviews patient data", "Nurse": "Updates vitals", "Patient": "Views reports"}

        stories: List[Dict[str, Any]] = []
        print("🧠 Generating stories (LLM)...")
        for batch in tqdm(list(chunked(requirements, batch_llm_size)), desc="Requirement chunks"):
            part = await self.generate_user_stories_batch(
                batch, glossary, actors, constraints, batch_size=llm_inner_batch, retriever=retriever
            )
            stories.extend(part)

        print(f"🧾 Generated stories (pre-alignment, pre-dedupe): {len(stories)}")

        # Alignment pass
        print("🔎 Checking alignment with citations...")
        req_map = {r["req_id"]: r for r in requirements}
        aligned, needs_review = [], []
        for s in stories:
            rid = (s.get("source_requirement_ids") or [None])[0]
            req = req_map.get(rid, {"text": ""})
            ok, score = validate_alignment(req, s, min_score=min_alignment)
            s["alignment_score"] = round(score, 3)
            s["needs_review"] = not ok
            (aligned if ok else needs_review).append(s)
        print(f"✅ Aligned: {len(aligned)} | 🚩 Needs review: {len(needs_review)}")

        final_stories = aligned + needs_review
        if dedupe and final_stories:
            dups = self.check_duplicates(final_stories, threshold=dup_threshold)
            if dups:
                print("⚠️ Near-duplicate pairs:", [(a, b, round(sim, 3)) for a, b, sim in dups])
            final_stories = self.dedupe_stories(final_stories, threshold=dup_threshold)
            print(f"✅ Final stories after dedupe: {len(final_stories)}")
        else:
            print("⏭️ Skipping dedupe.")

        return final_stories
    
    
    def export_testcases_csv(
        stories,
        requirements,
        out_csv="testcases.csv",
        area_path="Healthcare\\DayHealth",
        iteration_path="Release 1",
        synth_step_on_missing_ac=True
    ):
        """
        ADO-style export.
        Writes one row per acceptance criterion.
        If a story has no ACs and synth_step_on_missing_ac=True,
        writes a single synthetic step so nothing is dropped.
        """

        if not stories:
            print("⚠️ No stories to export.")
            return

        req_map = {r["req_id"]: r for r in requirements}

        total_stories = len(stories)
        stories_with_acs = 0
        stories_without_acs = 0
        rows_written = 0

        with open(out_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "Test Case Title",
                "Step Action",
                "Step Expected",
                "Requirement ID",
                "Priority",
                "Tags",
                "Pages",
                "Story Id",
                "Epic",
                "Area Path",
                "Iteration Path",
            ])

            for s in stories:
                rid = (s.get("source_requirement_ids") or [None])[0]
                req = req_map.get(rid, {})
                epic = (s.get("epic") or req.get("epic") or "General").strip()

                # build tags
                priority = (s.get("priority") or "").strip()
                tags = []
                if priority:
                    tags.append(f"@priority_{priority}")
                if rid:
                    tags.append(f"@req_{rid}")
                nf_join = " ".join(s.get("non_functional", []) or [])
                if "HIPAA" in nf_join.upper():
                    tags.append("@HIPAA")
                if "21 CFR" in nf_join.upper() or "FDA" in nf_join.upper():
                    tags.append("@FDA21CFR11")
                tags_str = " ".join(tags)

                # pages from citations
                pages = ";".join(
                    [str(c.get("page")) for c in (s.get("citations") or []) if c.get("page")]
                )

                acs = s.get("acceptance_criteria") or []
                if acs:
                    stories_with_acs += 1
                    for ac in acs:
                        given_ = (ac.get("given") or "").strip()
                        when_  = (ac.get("when") or "").strip()
                        then_  = (ac.get("then") or "").strip()

                        step_action = " | ".join([p for p in [given_, when_] if p])
                        step_expected = then_ or "Then: expected outcome is observed."

                        w.writerow([
                            s.get("user_story","").strip(),
                            step_action,
                            step_expected,
                            rid,
                            priority,
                            tags_str,
                            pages,
                            s.get("story_id",""),
                            epic,
                            area_path,
                            iteration_path,
                        ])
                        rows_written += 1
                else:
                    stories_without_acs += 1
                    if synth_step_on_missing_ac:
                        # create a single synthetic step so the test case isn’t lost
                        title = s.get("user_story","").strip() or "User story (no AC specified)"
                        w.writerow([
                            title,
                            "Given the system is available | When I perform the described capability",
                            "Then the described outcome is achieved",
                            rid,
                            priority,
                            tags_str,
                            pages,
                            s.get("story_id",""),
                            epic,
                            area_path,
                            iteration_path,
                        ])
                        rows_written += 1
                    # else: intentionally skip writing rows for no-AC stories

        print("✅ Exported test cases to", out_csv)
        print(f"   Stories total:            {total_stories}")
        print(f"   Stories with ACs:         {stories_with_acs}")
        print(f"   Stories without ACs:      {stories_without_acs}")
        print(f"   Rows written (test steps):{rows_written}")




    # ------------------ BigQuery Export ------------------

    def _infer_bq_schema(self, sample_row: dict):
        """Infer BigQuery schema dynamically from a sample story dict."""
        schema = []
        for key, val in sample_row.items():
            if isinstance(val, list) and val and isinstance(val[0], dict):
                schema.append(bigquery.SchemaField(key, "JSON"))
            elif isinstance(val, list):
                schema.append(bigquery.SchemaField(key, "STRING", mode="REPEATED"))
            elif isinstance(val, dict):
                schema.append(bigquery.SchemaField(key, "JSON"))
            elif isinstance(val, str):
                schema.append(bigquery.SchemaField(key, "STRING"))
            else:
                schema.append(bigquery.SchemaField(key, "STRING"))
        return schema

    def export_to_bq(self, stories, dataset_id="stories_dataset", table_id="user_stories"):
        if not stories:
            print("No stories to export")
            return

        client = bigquery.Client(project=self.project_id)
        table_ref = f"{self.project_id}.{dataset_id}.{table_id}"

        schema = self._infer_bq_schema(stories[0])

        # Ensure dataset
        try:
            client.get_dataset(dataset_id)
        except Exception:
            dataset = bigquery.Dataset(f"{self.project_id}.{dataset_id}")
            dataset.location = self.location
            client.create_dataset(dataset, exists_ok=True)

        # Ensure table
        try:
            client.get_table(table_ref)
        except Exception:
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)

        # Stringify dict fields (BQ JSON is fine, but this is robust)
        rows = []
        for story in stories:
            row = story.copy()
            for k, v in row.items():
                if isinstance(v, dict):
                    row[k] = json.dumps(v, ensure_ascii=False)
            rows.append(row)

        print("⬆️ Exporting to BigQuery...")
        errors = client.insert_rows_json(table_ref, rows)
        if errors:
            print(f"❌ Errors inserting rows: {errors}")
        else:
            print(f"✅ Inserted {len(rows)} stories into {table_ref}")
