
# ------------------------------
# FILE: healthstory/io_loaders.py
# ------------------------------
from __future__ import annotations
import os
from typing import Callable

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
except Exception:
    pdf_extract_text = None  # type: ignore

try:
    import docx  # python-docx
except Exception:
    docx = None  # type: ignore


def parse_pdf(path: str) -> str:
    if pdf_extract_text is None:
        raise RuntimeError("Install pdfminer.six: pip install pdfminer.six")
    return pdf_extract_text(path)


def parse_docx(path: str) -> str:
    if docx is None:
        raise RuntimeError("Install python-docx: pip install python-docx")
    d = docx.Document(path)
    lines = []
    for p in d.paragraphs:
        lines.append(p.text or "")
    return "\n".join(lines)


def detect_loader(path: str) -> Callable[[str], str]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return parse_pdf
    if ext in (".docx", ".doc"):
        return parse_docx
    # default plain text
    return lambda p: open(p, "r", encoding="utf-8").read()