"""
payment_of_wages_to_json.py
----------------------------
Converts the Payment of Wages Act, 1936 PDF into structured JSON.

Structure:
    document
    └── sections[]
            ├── section_id        (e.g. "POWA_S12A")
            ├── section_number    (e.g. "12A")
            ├── heading           (e.g. "Deductions for recovery of loans")
            ├── page_start
            ├── page_end
            └── content

Key behaviors:
- Processes pages START_PAGE to END_PAGE (1-indexed, inclusive).
- Footnote lines (numbered citation lines in bottom 35% of page) are excluded.
- Inline superscript refs like "1[" "2[" are stripped from content.
- Skips page headers, act title, standalone page numbers, and other noise.
- Each section becomes one JSON object.
"""

import pdfplumber
import json
import os
import re

# ── Page Range ────────────────────────────────────────────────────────────────
START_PAGE = 3
END_PAGE   = 19

# ── Footnote detection: Y threshold + line pattern ────────────────────────────
# A line is a footnote if BOTH conditions are true:
#   1. It's in the bottom (1 - FOOTNOTE_Y_RATIO) of the page
#   2. It matches the numbered citation pattern
FOOTNOTE_Y_RATIO = 0.60

FOOTNOTE_LINE_RE = re.compile(
    r'^\d+\.\s+'
    r'(Subs\.|Ins\.|Added|Omitted|The\s+Act|The\s+word|The\s+words|'
    r'Renumbered|See\s+Gazette|Act\s+\d+|w\.e\.f\.|ibid\.|'
    r'A\.O\.\s*\d+|Clauses?|Explanation|Section)',
    re.IGNORECASE
)

# ── Noise lines ───────────────────────────────────────────────────────────────
NOISE_PATTERNS = [
    re.compile(r'THE PAYMENT OF WAGES ACT', re.IGNORECASE),
    re.compile(r'^\s*\d+\s*$'),
    re.compile(r'^\s*$'),
    re.compile(r'^ACT NO\.\s*\d+', re.IGNORECASE),
    re.compile(r'^An Act to regulate', re.IGNORECASE),
    re.compile(r'^WHEREAS it is expedient', re.IGNORECASE),
    re.compile(r'^It is hereby enacted', re.IGNORECASE),
    re.compile(r'^\[\d{4}\.\]$'),                    # "[1936.]"
]

# ── Section start pattern ─────────────────────────────────────────────────────
SECTION_RE = re.compile(r'^(\d+[A-Za-z]?)\.\s+(.*)', re.DOTALL)

# ── Inline superscript footnote markers ──────────────────────────────────────
INLINE_REF_RE = re.compile(r'\d+\[')

# ── Known sections with their correct headings (for PDF parsing edge cases) ──
# Some headings get split across lines due to inline footnote refs in the PDF
KNOWN_HEADINGS = {
    "3":   "Responsibility for payment of wages",
    "6":   "Wages to be paid in current coin or currency notes or by cheque or crediting in bank account",
    "10":  "Deductions for damage or loss",
    "12A": "Deductions for recovery of loans",
    "13A": "Maintenance of registers and records",
    "15":  "Claims arising out of deductions from wages or delay in payment of wages and penalty for malicious or vexatious claims",
    "17A": "Conditional attachment of property of employer or other person responsible for payment of wages",
    "22A": "Protection of action taken in good faith",
    "25A": "Payment of undisbursed wages in cases of death of employed person",
}


# ─────────────────────────────────────────────────────────────────────────────
def _is_noise(line: str) -> bool:
    return any(p.search(line.strip()) for p in NOISE_PATTERNS)


def _is_footnote(line: str, y_ratio: float) -> bool:
    return y_ratio >= FOOTNOTE_Y_RATIO and bool(FOOTNOTE_LINE_RE.match(line.strip()))


def _clean(text: str) -> str:
    """Remove inline footnote markers like 1[ 2[ etc., keep the bracket content."""
    return INLINE_REF_RE.sub('[', text).strip()


def _extract_heading_and_content(sec_num: str, text: str):
    """
    Split section rest-text into (heading, content).
    Uses known headings dict first, then falls back to separator detection.
    """
    if sec_num in KNOWN_HEADINGS:
        heading = KNOWN_HEADINGS[sec_num]
        # Try to find where actual content starts after the separator
        for sep in ['.—', '.–', '—', '–']:
            idx = text.find(sep)
            if idx != -1:
                content = text[idx + len(sep):].strip()
                return heading, content
        return heading, text.strip()

    for sep in ['.—', '.–', '—', '–']:
        idx = text.find(sep)
        if idx != -1:
            heading = text[:idx].strip().rstrip('.')
            content = text[idx + len(sep):].strip()
            return heading, content

    return "", text.strip()


def _get_body_lines(page) -> list[str]:
    """
    Extract body lines from page, stopping at the first footnote line.
    """
    words = page.extract_words(keep_blank_chars=False, use_text_flow=True)
    if not words:
        return []

    lines_dict: dict[float, list] = {}
    for w in words:
        y_key = round(w['top'] / 2) * 2
        lines_dict.setdefault(y_key, []).append(w)

    result = []
    page_height = page.height

    for y in sorted(lines_dict.keys()):
        line_words = sorted(lines_dict[y], key=lambda w: w['x0'])
        line = ' '.join(w['text'] for w in line_words).strip()
        if not line:
            continue
        if _is_footnote(line, y / page_height):
            break
        result.append(line)

    return result


def _flush(sections: list, current: dict | None):
    if current:
        current['content'] = current['content'].strip()
        current['heading'] = current['heading'].strip().rstrip('.')
        sections.append(current)


# ─────────────────────────────────────────────────────────────────────────────
def pdf_to_structured_json(pdf_path: str, doc_name: str) -> dict:
    structured = {
        "document_name": "The Payment of Wages Act, 1936",
        "act_number": "Act No. 4 of 1936",
        "enacted_on": "23rd April, 1936",
        "category": "Labour & Employment",
        "document_key": doc_name,
        "pages_processed": f"{START_PAGE} to {END_PAGE}",
        "sections": []
    }

    sections = structured["sections"]
    current: dict | None = None

    # Track seen section numbers to avoid false matches
    seen_sections: set[str] = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in range(len(pdf.pages)):
            page_number = page_idx + 1
            if page_number < START_PAGE: continue
            if page_number > END_PAGE:   break

            for line in _get_body_lines(pdf.pages[page_idx]):
                if _is_noise(line):
                    continue

                clean = _clean(line.strip())
                if not clean:
                    continue

                m = SECTION_RE.match(clean)
                if m:
                    sec_num  = m.group(1)
                    sec_rest = m.group(2)

                    # Skip if this section number was already seen
                    # (avoids false re-matches from inline references)
                    if sec_num in seen_sections:
                        # Append to current section as content instead
                        if current:
                            sep = " " if current["content"] else ""
                            current["content"] += sep + clean
                            current["page_end"] = page_number
                        continue

                    _flush(sections, current)
                    seen_sections.add(sec_num)

                    heading, content = _extract_heading_and_content(sec_num, sec_rest)

                    current = {
                        "section_id":     f"{doc_name}_S{sec_num}",
                        "section_number": sec_num,
                        "heading":        heading,
                        "page_start":     page_number,
                        "page_end":       page_number,
                        "content":        content
                    }
                    continue

                if current:
                    sep = " " if current["content"] else ""
                    current["content"] += sep + clean
                    current["page_end"] = page_number

    _flush(sections, current)
    return structured


# ─────────────────────────────────────────────────────────────────────────────
def convert_pdf(pdf_path: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    doc_name = os.path.splitext(os.path.basename(pdf_path))[0]

    print(f"Converting : {pdf_path}")
    print(f"Pages      : {START_PAGE} → {END_PAGE}")
    print()

    structured = pdf_to_structured_json(pdf_path, doc_name)

    output_path = os.path.join(output_folder, f"{doc_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved   : {output_path}")
    print(f"   Sections : {len(structured['sections'])}")
    print()
    for s in structured['sections']:
        print(f"  [{s['section_number']:>4}]  p{s['page_start']}-{s['page_end']}  {s['heading'][:65]}")


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    PDF_PATH      = "./pdfs/Payment of Wages Act 1936.pdf"
    OUTPUT_FOLDER = "./json_docs"
    convert_pdf(PDF_PATH, OUTPUT_FOLDER)