"""
Compliance RAG + Validator
--------------------------
Maps each user story + its test steps to likely regulatory clauses
(FDA 21 CFR Part 11, IEC 62304, ISO 13485/9001, ISO 27001),
checks for required controls (audit trail, RBAC, e-sig, data integrity),
and generates a Compliance Evidence Report (CSV/Excel).

Inputs:
  - stories.json     (your generated stories with citations/alignment)
  - testcases.csv    (ADO/Jira export; must include 'Story Id', 'Step Action', 'Step Expected')

Outputs:
  - compliance_evidence.csv
  - compliance_evidence.xlsx (optional)

Dependencies:
  pip install pandas numpy langchain-google-vertexai
  # (You already have them in your stack.)
"""

import os
import re
import json
import math
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from langchain_google_vertexai import VertexAIEmbeddings

# ------------------------------- Controls & KB -------------------------------

# Canonical control tags we care about (expandable)
CONTROL_TAGS = {
    "audit_trail": [r"\baudit trail\b", r"\blog(ging|s)?\b", r"\bimmutable\b", r"\bchange history\b"],
    "rbac": [r"\brole[- ]?based\b", r"\baccess control\b", r"\bprivilege(s)?\b", r"\bauthori[sz]ation\b"],
    "e_signature": [r"\be(-| )?sig(nature)?\b", r"\belectronic signature\b", r"\bsign[- ]off\b"],
    "data_integrity": [r"\bdata integrity\b", r"\bchecksum\b", r"\bhmac\b", r"\btimestamp(ed)?\b"],
    "encryption": [r"\bencrypt(ed|ion)\b", r"\bTLS\b", r"\bAES\b"],
    "pii_protection": [r"\bPHI\b", r"\bPII\b", r"\bde-?identif(y|ication)\b", r"\bpseudonymi[sz]ation\b"],
    "traceability": [r"\btraceab(le|ility)\b", r"\brequirement id\b", r"\blinkage\b", r"\bprovenance\b"],
    "verification_validation": [r"\bverification\b", r"\bvalidation\b", r"\bV&V\b", r"\btest evidence\b"],
    "risk_management": [r"\brisk\b", r"\bhazard\b", r"\bmitigation\b", r"\bseverity\b", r"\bprobability\b"],
}

# Lightweight compliance knowledge base.
# NOTE: Titles/summaries are HIGH-LEVEL paraphrases (not verbatim from standards).
COMPLIANCE_KB = [
    {
        "standard": "FDA 21 CFR Part 11",
        "clause": "11.10(e)",
        "title": "Audit trails for electronic records",
        "summary": "Secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions that create, modify, or delete electronic records.",
        "controls": ["audit_trail", "data_integrity", "traceability"]
    },
    {
        "standard": "FDA 21 CFR Part 11",
        "clause": "11.100",
        "title": "Electronic signatures (identity verification)",
        "summary": "Electronic signatures are unique to individuals and verified; binding equivalent to handwritten signatures.",
        "controls": ["e_signature", "rbac"]
    },
    {
        "standard": "IEC 62304",
        "clause": "5.1",
        "title": "Software development planning",
        "summary": "Define processes, activities, and tasks including verification/validation appropriate to safety class.",
        "controls": ["verification_validation", "traceability", "risk_management"]
    },
    {
        "standard": "ISO 13485",
        "clause": "4.2.5",
        "title": "Document control & records",
        "summary": "Control of documents/records to ensure data integrity, retention, and retrieval.",
        "controls": ["data_integrity", "audit_trail", "traceability"]
    },
    {
        "standard": "ISO 27001",
        "clause": "A.9",
        "title": "Access control (RBAC)",
        "summary": "Limit access to information and systems based on business/role requirements.",
        "controls": ["rbac"]
    },
    {
        "standard": "ISO 27001",
        "clause": "A.10",
        "title": "Cryptography",
        "summary": "Use of encryption to protect confidentiality and integrity.",
        "controls": ["encryption", "data_integrity"]
    },
    {
        "standard": "ISO 9001",
        "clause": "8.5.1",
        "title": "Production & service provision control",
        "summary": "Controlled conditions including monitoring and measurement to ensure conformity.",
        "controls": ["verification_validation", "traceability"]
    },
]

# Pre-compile regexes for faster detection
COMPILED_CONTROL_PATTERNS = {
    tag: [re.compile(pat, re.I) for pat in patterns]
    for tag, patterns in CONTROL_TAGS.items()
}


# ----------------------------- Embedding Utilities -----------------------------

def _cosines(query_emb, matrix: List[List[float]]) -> List[float]:
    sims = []
    q = np.array(query_emb, dtype=float)
    qn = np.linalg.norm(q)
    for v in matrix:
        v = np.array(v, dtype=float)
        vn = np.linalg.norm(v)
        sims.append(0.0 if qn == 0 or vn == 0 else float(np.dot(q, v) / (qn * vn)))
    return sims


class ComplianceRetriever:
    """
    Tiny in-memory semantic retriever over the compliance KB.
    """

    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1",
                 embedding_model: str = "text-embedding-005", use_embeddings: bool = True):
        self.use_embeddings = use_embeddings
        self.kb = COMPLIANCE_KB
        self.embedder = None
        self.kb_texts = [f"{k['standard']} {k['clause']} {k['title']} :: {k['summary']}" for k in self.kb]
        self.kb_embs = None
        if use_embeddings:
            try:
                self.embedder = VertexAIEmbeddings(model=embedding_model, project=project_id, location=location)
                self.kb_embs = self.embedder.embed_documents(self.kb_texts)
            except Exception as e:
                print(f"⚠️ Embeddings disabled (fallback to keyword-only). Reason: {e}")
                self.use_embeddings = False

    def retrieve(self, text: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Return top_k matching KB clauses with scores.
        Fallback to keyword overlap if embeddings are disabled.
        """
        if not text:
            return []
        if self.use_embeddings and self.embedder and self.kb_embs is not None:
            q = self.embedder.embed_query(text)
            sims = _cosines(q, self.kb_embs)
            idxs = np.argsort(sims)[::-1][:top_k]
            return [
                dict(self.kb[i], score=float(sims[i]))
                for i in idxs
            ]
        # keyword fallback: count control hits
        text_l = text.lower()
        scores = []
        for i, k in enumerate(self.kb):
            hits = 0
            for ctl in k["controls"]:
                for rx in COMPILED_CONTROL_PATTERNS[ctl]:
                    if rx.search(text_l):
                        hits += 1
                        break
            scores.append((i, hits))
        scores.sort(key=lambda x: x[1], reverse=True)
        idxs = [i for i, _ in scores[:top_k]]
        return [dict(self.kb[i], score=float(scores[j][1])) for j, i in enumerate(idxs)]


# ------------------------------ Control Detection ------------------------------

def detect_controls_in_text(text: str) -> List[str]:
    """
    Regex-based detection of control tags present in text.
    """
    if not text:
        return []
    present = set()
    tl = text.lower()
    for tag, patterns in COMPILED_CONTROL_PATTERNS.items():
        if any(rx.search(tl) for rx in patterns):
            present.add(tag)
    return sorted(present)


def story_full_text(story: Dict[str, Any], tc_rows: pd.DataFrame) -> str:
    """
    Combine story fields + its test steps into one blob for retrieval/detection.
    """
    parts = [story.get("user_story", "")]
    for ac in story.get("acceptance_criteria", []) or []:
        parts.append(f"GIVEN {ac.get('given','')}")
        parts.append(f"WHEN {ac.get('when','')}")
        parts.append(f"THEN {ac.get('then','')}")
    parts.extend(story.get("non_functional", []) or [])

    sid = story.get("story_id")
    if sid and not tc_rows.empty:
        sub = tc_rows[tc_rows["story_id"] == sid]
        for _, r in sub.iterrows():
            parts.append(str(r.get("Step Action", "")))
            parts.append(str(r.get("Step Expected", "")))

    return "\n".join([p for p in parts if p])


def expected_controls_from_clauses(clauses: List[Dict[str, Any]]) -> List[str]:
    exp = set()
    for c in clauses:
        for ctl in c.get("controls", []):
            exp.add(ctl)
    return sorted(exp)


def compliance_gap(expected: List[str], detected: List[str]) -> (List[str], List[str]):
    exp = set(expected)
    det = set(detected)
    return sorted(list(det)), sorted(list(exp - det))


# ------------------------------ Report Generator ------------------------------

def build_compliance_report(
    stories_path: str = "stories.json",
    testcases_path: str = "testcases.csv",
    out_csv: str = "compliance_evidence.csv",
    out_xlsx: Optional[str] = "compliance_evidence.xlsx",
    project_id: Optional[str] = None,
    location: str = "us-central1",
    use_embeddings: bool = True,
) -> pd.DataFrame:
    """
    Generate Compliance Evidence Report:
      - Likely clauses per story (RAG)
      - Detected vs expected controls (gap analysis)
      - Trace (citations pages, alignment, priority, epic)
    """
    # Load inputs
    with open(stories_path, "r", encoding="utf-8") as f:
        stories = json.load(f)
    tcs = pd.read_csv(testcases_path)

    retriever = ComplianceRetriever(project_id=project_id, location=location, use_embeddings=use_embeddings)

    rows = []
    for s in stories:
        rid = None
        src_ids = s.get("source_requirement_ids") or []
        if src_ids:
            rid = src_ids[0]
        epic = (s.get("epic") or "").strip()
        priority = (s.get("priority") or "").strip()

        # Construct evidence text
        evidence = story_full_text(s, tcs)

        # RAG: retrieve likely clauses
        top_clauses = retriever.retrieve(evidence, top_k=4)
        expected_controls = expected_controls_from_clauses(top_clauses)

        # Detected controls from actual text
        detected_controls = detect_controls_in_text(evidence)

        # Gap
        detected, missing = compliance_gap(expected_controls, detected_controls)

        pages = ";".join([str(c.get("page")) for c in (s.get("citations") or []) if c.get("page")])
        clause_labels = [f"{c['standard']} {c['clause']}" for c in top_clauses]
        clause_scores = [round(float(c.get("score", 0.0)), 3) for c in top_clauses]

        rows.append({
            "Requirement ID": rid,
            "Story Id": s.get("story_id", ""),
            "Epic": epic,
            "Priority": priority,
            "User Story": s.get("user_story", ""),
            "Pages (Citations)": pages,
            "Alignment Score": s.get("alignment_score", ""),
            "Needs Review": s.get("needs_review", ""),
            # RAG results
            "Matched Clauses": "; ".join(clause_labels),
            "Clause Scores": "; ".join(map(str, clause_scores)),
            # Controls
            "Expected Controls": "; ".join(expected_controls),
            "Detected Controls": "; ".join(detected),
            "Missing Controls": "; ".join(missing),
            # Evidence for auditor
            "Evidence (Story + Steps)": evidence[:2000],  # keep report compact
        })

    df = pd.DataFrame(rows)

    # Save
    df.to_csv(out_csv, index=False, encoding="utf-8")
    if out_xlsx:
        df.to_excel(out_xlsx, index=False)

    print(f"✅ Compliance Evidence Report: {out_csv}" + (f" and {out_xlsx}" if out_xlsx else ""))
    # Quick summary
    total = len(df)
    with_gaps = int((df["Missing Controls"].str.len() > 0).sum())
    print(f"   Stories analyzed: {total} | Stories with missing controls: {with_gaps}")
    return df
