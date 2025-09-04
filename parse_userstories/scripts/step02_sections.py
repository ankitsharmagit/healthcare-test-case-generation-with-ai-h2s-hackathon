#!/usr/bin/env python3
"""
Step 2 – Sectioning (glossary, actors, constraints, epics, features, requirements)
----------------------------------------------------------------------------------

Reads the normalized text produced by Step 1 and splits it into logical sections
based on headings. Also extracts a lightweight context (glossary/actors/constraints)
that we will feed into generation later.

Inputs (derived automatically):
  artifacts/<basename>/01_normalized.txt

Outputs:
  artifacts/<basename>/02_sections.json      # raw buckets by section
  artifacts/<basename>/02_context.json       # glossary/actors/constraints dicts
  artifacts/<basename>/02_sections_preview.md# small human-readable summary

Usage:
  python step02_sections.py requirements.pdf
  (reads artifacts/requirements/01_normalized.txt)
"""

from __future__ import annotations
import argparse, json, os, re
from typing import Dict, List, Any, Optional, Tuple

# ---------- Patterns ----------
BULLET_PATTERN = re.compile(r"^\s*([\-•·◦*] |\d+\.|\([a-zA-Z0-9]\))")
HEADING_PATTERN = re.compile(r"^(?:\s{0,3})([A-Z][A-Z0-9\s\-_/]{3,})\s*$", re.MULTILINE)

SECTION_TITLES = {
    "glossary": ["glossary", "definitions"],
    "actors": ["actors", "personas", "roles", "users"],
    "constraints": ["constraints", "assumptions", "regulatory", "compliance"],
    "requirements": ["requirements", "functional requirements", "user requirements", "business requirements"],
    "epics": ["epic", "epics"],
    "features": ["feature", "features", "modules", "subsystems"],
}

# ---------- Helpers ----------

def _section_key(title: str) -> Optional[str]:
    t = title.lower().strip()
    for key, aliases in SECTION_TITLES.items():
        for a in aliases:
            if a in t:
                return key
    return None


def find_sections(text: str) -> Dict[str, Any]:
    """Split by headings and bucket into known sections. Keeps the heading line
    inside each block as context (first line)."""
    sections: Dict[str, List[str]] = {k: [] for k in SECTION_TITLES}
    sections["other"] = []

    current_key = "other"
    buf: List[str] = []

    def flush():
        if not buf:
            return
        content = "\n".join(buf).strip()
        if content:
            sections[current_key].append(content)
        buf.clear()

    for line in text.split("\n"):
        if HEADING_PATTERN.match(line.strip()):
            flush()
            key = _section_key(line) or "other"
            current_key = key
            buf.append(line.strip())
        else:
            buf.append(line)
    flush()

    return sections


def _extract_bullets(block: str) -> List[str]:
    items: List[str] = []
    for ln in block.split("\n"):
        if BULLET_PATTERN.match(ln.strip()):
            items.append(ln.strip())
    return items


def _parse_key_value(line: str) -> Optional[Tuple[str, str]]:
    # e.g., "Patient: Individual receiving care" or "Role - Description"
    m = re.match(r"^\s*([^:\-–]+)\s*[:\-–]\s*(.+)$", line)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None


def extract_context(sections: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    glossary: Dict[str, str] = {}
    actors: Dict[str, str] = {}
    constraints: Dict[str, str] = {}

    for block in sections.get("glossary", []):
        for item in _extract_bullets(block):
            kv = _parse_key_value(re.sub(BULLET_PATTERN, "", item, count=1))
            if kv:
                glossary[kv[0]] = kv[1]

    for block in sections.get("actors", []):
        for item in _extract_bullets(block):
            kv = _parse_key_value(re.sub(BULLET_PATTERN, "", item, count=1))
            if kv:
                actors[kv[0]] = kv[1]

    for block in sections.get("constraints", []):
        idx = 1
        for item in _extract_bullets(block):
            key = f"C{idx:02d}"
            constraints[key] = re.sub(BULLET_PATTERN, "", item, count=1).strip()
            idx += 1

    return {"glossary": glossary, "actors": actors, "constraints": constraints}


# ---------- CLI ----------

parser = argparse.ArgumentParser(description="Step 2 – Sectioning of normalized text")
parser.add_argument("filename", help="Original input filename (in data/), e.g. requirements.pdf")

if __name__ == "__main__":
    args = parser.parse_args()

    base = os.path.splitext(os.path.basename(args.filename))[0]
    in_path = os.path.join("artifacts", base, "01_normalized.txt")
    if not os.path.exists(in_path):
        raise FileNotFoundError(
            f"Normalized text not found: {in_path}. Run step01 first: python step01_parse_normalize.py {args.filename}"
        )

    text = open(in_path, "r", encoding="utf-8").read()
    sections = find_sections(text)
    context = extract_context(sections)

    out_dir = os.path.dirname(in_path)
    sec_path = os.path.join(out_dir, "02_sections.json")
    ctx_path = os.path.join(out_dir, "02_context.json")
    prv_path = os.path.join(out_dir, "02_sections_preview.md")

    open(sec_path, "w", encoding="utf-8").write(json.dumps(sections, ensure_ascii=False, indent=2))
    open(ctx_path, "w", encoding="utf-8").write(json.dumps(context, ensure_ascii=False, indent=2))

    # Small preview for humans
    def _count(k: str) -> int:
        return len(sections.get(k, []))

    preview = [
        f"# Step 2 Preview — {base}",
        "", 
        f"Glossary blocks:     {_count('glossary')}",
        f"Actors blocks:       {_count('actors')}",
        f"Constraints blocks:  {_count('constraints')}",
        f"Epics blocks:        {_count('epics')}",
        f"Features blocks:     {_count('features')}",
        f"Requirements blocks: {_count('requirements')}",
        f"Other blocks:        {_count('other')}",
        "",
        "## Extracted Context (top 10 each)",
        "### Glossary",
        *[f"- {k}: {v}" for k, v in list(context.get('glossary', {}).items())[:10]],
        "\n### Actors",
        *[f"- {k}: {v}" for k, v in list(context.get('actors', {}).items())[:10]],
        "\n### Constraints",
        *[f"- {k}: {v}" for k, v in list(context.get('constraints', {}).items())[:10]],
    ]

    open(prv_path, "w", encoding="utf-8").write("\n".join(preview))

    print("Saved:", sec_path)
    print("Saved:", ctx_path)
    print("Saved:", prv_path)
