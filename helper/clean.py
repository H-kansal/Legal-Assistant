import re

def clean_text(text: str) -> str:
    """
    Light cleanup for legal documents
    """
    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    # Remove page numbers like "Page 3 of 10"
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.I)

    # Remove repeated underscores or dashes
    text = re.sub(r"[_\-]{5,}", "", text)

    return text.strip()
