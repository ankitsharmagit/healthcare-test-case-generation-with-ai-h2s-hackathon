#!/usr/bin/env python3
"""
Step 1 – Parse & Normalize
---------------------------

This script only handles parsing PDF/DOCX/text files and normalizing the content.
It is the first step in the modular pipeline.

Functions:
- parse_pdf(path) -> str
- parse_docx(path) -> str
- normalize_text(raw_text) -> str
- main() -> CLI entrypoint for Step 1

Install deps:
    pip install pdfminer.six python-docx

Usage:
    python step01_parse_normalize.py /path/to/requirements.pdf
"""

from __future__ import annotations
import argparse
import os
import re
from typing import List

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
except Exception:
    pdf_extract_text = None  # type: ignore

try:
    import docx  # python-docx
except Exception:
    docx = None  # type: ignore

# Regex patterns
BULLET_PATTERN = re.compile(r"^\s*([\-•·◦*] |\d+\.|\([a-zA-Z0-9]\))")
HEADING_PATTERN = re.compile(r"^(?:\s{0,3})([A-Z][A-Z0-9\s\-_/]{3,})\s*$")


def parse_pdf(path: str) -> str:
    if pdf_extract_text is None:
        raise RuntimeError("pdfminer.six is not installed. Install with: pip install pdfminer.six")
    return pdf_extract_text(path)


def parse_docx(path: str) -> str:
    if docx is None:
        raise RuntimeError("python-docx is not installed. Install with: pip install python-docx")
    d = docx.Document(path)
    lines: List[str] = []
    for p in d.paragraphs:
        txt = p.text or ""
        lines.append(txt)
    return "\n".join(lines)


def normalize_text(raw: str) -> str:
    if not raw:
        return ""

    text = raw.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r"\u00A0", " ", text)  # non-breaking space
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # join hyphenated breaks

    lines = text.split('\n')
    merged: List[str] = []
    buf: List[str] = []

    def flush():
        if buf:
            merged.append(" ".join(s.strip() for s in buf))
            buf.clear()

    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            flush(); merged.append(""); continue
        if BULLET_PATTERN.match(s) or HEADING_PATTERN.match(s):
            flush(); merged.append(s.strip()); continue
        buf.append(s)
    flush()

    text = "\n".join(merged)
    text = re.sub(r"\n{3,}", "\n\n", text)

    def tidy_heading(m: re.Match[str]) -> str:
        h = m.group(1).strip()
        return h if h.isupper() else h.title()

    text = re.sub(HEADING_PATTERN, lambda m: tidy_heading(m), text, flags=re.MULTILINE)
    return text.strip()


def _detect_loader(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return parse_pdf
    if ext in (".docx", ".doc"):
        return parse_docx
    return lambda p: open(p, "r", encoding="utf-8").read()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Step 1 – Parse & Normalize requirement documents")
    parser.add_argument("input", help="Path to PDF/DOCX/TXT requirements file")
    args = parser.parse_args(argv)

    loader = _detect_loader(args.input)
    raw = loader(args.input)
    text = normalize_text(raw)

    base = os.path.splitext(os.path.basename(args.input))[0]
    out_dir = os.path.join("artifacts", base)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "01_normalized.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("Saved:", out_path)


if __name__ == "__main__":
    main()
