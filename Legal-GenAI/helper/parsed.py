import os
from typing import Optional
from pypdf import PdfReader
from docx import Document as DocxDocument

def parse_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    paragraphs = []

    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text)

    return "\n".join(paragraphs)

def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)

    return "\n".join(pages_text)

def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_document(file_path: str) -> str:
    """
    Detects file type and extracts text accordingly.
    Supported: PDF, DOCX, TXT
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return parse_pdf(file_path)

    elif ext == ".docx":
        return parse_docx(file_path)

    elif ext == ".txt":
        return parse_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
