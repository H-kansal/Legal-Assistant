"""
bsc_to_json.py
--------------
Converts the BSC (Bharatiya Sanhita Code) PDF into a structured JSON with:
    document
    └── chapters[]
            ├── chapter_number  (e.g. "XX")
            ├── chapter_title   (e.g. "REPEAL AND SAVINGS")
            └── sections[]
                    ├── section_number  (e.g. "358")
                    ├── section_heading (first sentence / inline heading if present)
                    └── content         (full accumulated text for that section)
"""

import fitz  # pymupdf
import json
import os
import re

# ─── Noise patterns to discard ───────────────────────────────────────────────
NOISE_PATTERNS = [
    re.compile(r'^Sec\.\s*\d+\]'),                          # "Sec. 1]"
    re.compile(r'THE GAZETTE OF INDIA EXTRAORDINARY', re.IGNORECASE),
    re.compile(r'^\[Part\s+II', re.IGNORECASE),             # "[Part II—"
    re.compile(r'^_{4,}'),                                  # "____..."
    re.compile(r'^\d+\s*$'),                                # standalone page numbers
    re.compile(r'^\s*$'),                                   # blank lines
    re.compile(r'[\u0900-\u097F]'),                         # Hindi/Devanagari script (page 1 noise)
    re.compile(r'^MINISTRY OF LAW', re.IGNORECASE),         # gazette header
    re.compile(r'^PUBLISHED BY AUTHORITY', re.IGNORECASE),  # gazette header
    re.compile(r'^REGISTERED NO\.', re.IGNORECASE),         # gazette registration
    re.compile(r'^NEW DELHI,', re.IGNORECASE),              # gazette dateline
    re.compile(r'^CG-DL-', re.IGNORECASE),                  # gazette reference code
    re.compile(r'^xxxGID', re.IGNORECASE),                  # gazette internal marker
    re.compile(r'^NO\.\s*\d+\s+OF\s+\d{4}', re.IGNORECASE), # "NO. 45 OF 2023"
    re.compile(r'^\[\d+th\s', re.IGNORECASE),              # "[25th December..."
]

# ─── Chapter header: CHAPTER I, CHAPTER XX, CHAPTERI, CHAPTERII etc. ────────
# \s* (zero or more spaces) handles both "CHAPTER I" and "CHAPTERI" formats
CHAPTER_RE = re.compile(r'^CHAPTER\s*([IVXLCDM\d]+)\s*$', re.IGNORECASE)

# ─── Section / rule number: "358.", "3.", "21A.", "302." at line start ───────
#     Must be followed by content OR stand alone
SECTION_RE = re.compile(r'^(\d+[A-Z]?)\.\s*(.*)', re.DOTALL)


def _is_noise(line: str) -> bool:
    return any(pat.search(line) for pat in NOISE_PATTERNS)


def _is_chapter(line: str):
    """Return re.Match if line is a chapter heading, else None."""
    return CHAPTER_RE.match(line.strip())


def _is_section_start(line: str):
    """Return (section_number, rest_of_line) if line starts a new section, else None."""
    m = SECTION_RE.match(line.strip())
    if m:
        return m.group(1), m.group(2).strip()
    return None


def _save_section(chapter: dict, current_section: dict):
    """Flush current_section into chapter['sections']."""
    if current_section:
        current_section["content"] = current_section["content"].strip()
        chapter["sections"].append(current_section)


def _save_chapter(structured: dict, current_chapter: dict, current_section: dict):
    """Flush current_section then current_chapter."""
    if current_chapter:
        _save_section(current_chapter, current_section)
        structured["chapters"].append(current_chapter)


def pdf_to_structured_json(pdf_path: str, doc_name: str) -> dict:
    doc = fitz.open(pdf_path)

    structured = {
        "document_name": doc_name,
        "total_pages": len(doc),
        "chapters": []
    }

    current_chapter: dict | None = None
    current_section: dict | None = None
    chapter_counter = 0
    section_counter = 0

    # Buffer to detect chapter subtitles (line after CHAPTER XX)
    pending_chapter: dict | None = None

    for page_num, page in enumerate(doc):
        page_number = page_num + 1

        # Use "blocks" mode for reading-order text
        blocks = page.get_text("blocks")
        blocks = sorted(blocks, key=lambda b: (round(b[1] / 10), b[0]))

        for block in blocks:
            raw_text = block[4]
            lines = [l.strip() for l in raw_text.split("\n")]

            for line in lines:
                # ── 1. Skip noise ────────────────────────────────────────────
                if _is_noise(line):
                    continue

                clean = line.strip()
                if not clean:
                    continue

                # ── 2. Pending chapter needs a subtitle on next content line ─
                if pending_chapter is not None:
                    # If line looks like an ALL-CAPS subtitle (not a section)
                    if clean.isupper() and not _is_section_start(clean) and not _is_chapter(clean):
                        pending_chapter["chapter_title"] = clean.title()
                        current_chapter = pending_chapter
                        pending_chapter = None
                        continue
                    else:
                        # No subtitle — finalise chapter as-is
                        current_chapter = pending_chapter
                        pending_chapter = None
                        # Fall through to process current line normally

                # ── 3. Detect new CHAPTER ───────────────────────────────────
                ch_match = _is_chapter(clean)
                if ch_match:
                    # Save previous chapter + section
                    if current_chapter:
                        _save_section(current_chapter, current_section)
                        current_section = None
                        structured["chapters"].append(current_chapter)

                    chapter_counter += 1
                    pending_chapter = {
                        "chapter_id": f"{doc_name}_ch{chapter_counter}",
                        "chapter_number": ch_match.group(1).upper(),
                        "chapter_title": "",
                        "page_start": page_number,
                        "page_end": page_number,
                        "sections": []
                    }
                    continue

                # ── 4. Detect new SECTION number ────────────────────────────
                sec_match = _is_section_start(clean)
                if sec_match and current_chapter is not None:
                    sec_num, rest = sec_match

                    # Save previous section
                    _save_section(current_chapter, current_section)

                    section_counter += 1
                    current_section = {
                        "section_id": f"{doc_name}_s{sec_num}",
                        "section_number": sec_num,
                        "page_start": page_number,
                        "page_end": page_number,
                        "content": rest
                    }
                    # Update chapter page_end
                    current_chapter["page_end"] = page_number
                    continue

                # ── 5. Accumulate content into current section ───────────────
                if current_section is not None:
                    sep = " " if current_section["content"] else ""
                    current_section["content"] += sep + clean
                    current_section["page_end"] = page_number
                    if current_chapter:
                        current_chapter["page_end"] = page_number

                elif current_chapter is not None:
                    # Text inside a chapter but before first section number
                    # (e.g., chapter description/preamble)
                    section_counter += 1
                    current_section = {
                        "section_id": f"{doc_name}_preamble_{chapter_counter}",
                        "section_number": None,
                        "page_start": page_number,
                        "page_end": page_number,
                        "content": clean
                    }

    # ── Flush last section + chapter ────────────────────────────────────────
    if pending_chapter:
        current_chapter = pending_chapter
    if current_chapter:
        _save_section(current_chapter, current_section)
        structured["chapters"].append(current_chapter)

    doc.close()
    return structured


def convert_bsc_pdf(pdf_path: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    doc_name = os.path.splitext(os.path.basename(pdf_path))[0]

    print(f"Converting BSC PDF: {pdf_path} ...")
    structured = pdf_to_structured_json(pdf_path, doc_name)

    output_path = os.path.join(output_folder, f"{doc_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2, ensure_ascii=False)

    total_sections = sum(len(ch["sections"]) for ch in structured["chapters"])
    print(f"✅ Saved → {output_path}")
    print(f"   Chapters : {len(structured['chapters'])}")
    print(f"   Sections : {total_sections}")


# ── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    convert_bsc_pdf("./pdf/Bsc.pdf", "./json_docs")
