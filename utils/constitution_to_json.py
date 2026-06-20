"""
constitution_to_json.py
-----------------------
Converts the Constitution of India PDF into structured JSON.

Structure (chapters only, stops before Schedules at page 283):
    document
    └── parts[]
            ├── part_number   (e.g. "XVI")
            ├── part_title    (e.g. "Special Provisions Relating to Certain Classes")
            └── articles[]
                    ├── article_number  (e.g. "170")
                    ├── page_start
                    ├── page_end
                    └── content

Key behaviors:
- Footnotes (below the horizontal separator line at the bottom of each page)
  are EXCLUDED from content.
- Stops processing after page SCHEDULE_START_PAGE (1-indexed).
- Skips page headers ("THE CONSTITUTION OF INDIA"), part-reference lines,
  and other noise.
"""

import fitz   # pymupdf
import json
import os
import re

# ── Page Range ───────────────────────────────────────────────────────────────
START_PAGE = 5           # 1-indexed; start processing from this page
SCHEDULE_START_PAGE = 70   # 1-indexed; stop processing from this page onward

# ── Fraction of page height below which blocks are treated as footnotes ──────
# Constitution PDFs have footnotes in roughly the bottom 18% of the page.
FOOTNOTE_Y_RATIO = 0.82

# ── Noise lines to discard ───────────────────────────────────────────────────
NOISE_PATTERNS = [
    re.compile(r'THE CONSTITUTION OF INDIA', re.IGNORECASE),
    re.compile(r'^\s*\(Part\s+[IVXLCDM]+[\.\—]', re.IGNORECASE),  # "(Part XVI.—...)"
    re.compile(r'^\d+\s*$'),           # standalone page numbers
    re.compile(r'^\s*$'),              # blank
    re.compile(r'^\(Contd\.\)', re.IGNORECASE),
]

# ── Part header: "PART I", "PART XVI", "PART 1" ──────────────────────────────
# Allows optional space (handles "PARTI" vs "PART I")
PART_RE = re.compile(r'^PART\s*([IVXLCDM\d]+)\s*$', re.IGNORECASE)

# ── Article / section number at the start of a line ──────────────────────────
# Matches: "170.", "170A.", "3BB." etc.
ARTICLE_RE = re.compile(r'^(\d+[A-Za-z]{0,3})\.\s*(.*)', re.DOTALL)


# ─────────────────────────────────────────────────────────────────────────────
def _is_noise(line: str) -> bool:
    return any(pat.search(line) for pat in NOISE_PATTERNS)


def _is_part(line: str):
    return PART_RE.match(line.strip())


def _is_article_start(line: str):
    """Return (article_number, rest_of_line) or None."""
    m = ARTICLE_RE.match(line.strip())
    if m:
        return m.group(1), m.group(2).strip()
    return None


def find_footnote_separator_y(page):
    """
    Search for a horizontal separator line in the bottom area of the page.
    Returns the y-coordinate of the line, or None if not found.
    """
    page_height = page.rect.height
    min_y = 0.5 * page_height
    
    try:
        drawings = page.get_drawings()
        for d in drawings:
            r = d["rect"]
            # Check if the drawing is in the bottom area, is horizontal and is wide
            is_horizontal = (r.y1 - r.y0) <= 4
            is_wide = (r.x1 - r.x0) >= 40
            is_in_bottom = r.y0 > min_y
            if is_horizontal and is_wide and is_in_bottom:
                return r.y0
    except Exception:
        pass
    return None


def _page_blocks_without_footnotes(page):
    """
    Return text blocks for the page, excluding blocks that fall
    below the footnote separator line (either drawing or text underscore).
    Also skips image blocks (block_type != 0).
    """
    page_height = page.rect.height
    
    # 1. Try to find a drawing-based separator line
    sep_y = find_footnote_separator_y(page)
    
    blocks = page.get_text("blocks")
    # Sort top-to-bottom, then left-to-right
    blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
    
    valid_blocks = []
    
    # Pattern to match footnote separator lines in text
    # e.g., "______________________________________________"
    SEPARATOR_RE = re.compile(r'_{5,}|-{5,}|\u2014{5,}')
    
    for b in blocks:
        # Skip image blocks
        if b[6] != 0:
            continue
            
        x0, y0, x1, y1, text, block_no, block_type = b
        
        # If we already have a drawing-based separator, skip blocks below it
        if sep_y is not None and y0 >= (sep_y - 2):
            continue
            
        # Check if the block text contains a separator line
        has_text_separator = False
        lines = text.split("\n")
        clean_lines = []
        
        for line in lines:
            m = SEPARATOR_RE.search(line)
            if m:
                has_text_separator = True
                # Keep the part of the line before the separator, if any
                pre_text = line[:m.start()].strip()
                if pre_text:
                    clean_lines.append(pre_text)
                break  # Stop processing lines in this block/page
            else:
                clean_lines.append(line)
                
        if has_text_separator:
            # Reconstruct block text without the separator and subsequent text
            if clean_lines:
                new_text = "\n".join(clean_lines)
                valid_blocks.append((x0, y0, x1, y1, new_text, block_no, block_type))
            # Since we hit a separator, all subsequent blocks on this page are footnotes
            break
        else:
            valid_blocks.append(b)
            
    # If we didn't find any separator on the page (neither drawing nor text),
    # fallback to FOOTNOTE_Y_RATIO to filter out any blocks that are very far down.
    if sep_y is None and not any(any(SEPARATOR_RE.search(l) for l in b[4].split("\n")) for b in blocks if b[6] == 0):
        fallback_y = FOOTNOTE_Y_RATIO * page_height
        valid_blocks = [b for b in valid_blocks if b[1] < fallback_y]
        
    # Sort reading order: top-to-bottom, left-to-right
    valid_blocks = sorted(valid_blocks, key=lambda b: (round(b[1] / 10), b[0]))
    return valid_blocks


def _flush_article(current_part, current_article):
    if current_article:
        current_article["content"] = current_article["content"].strip()
        current_part["articles"].append(current_article)


def _flush_part(structured, current_part, current_article):
    if current_part:
        _flush_article(current_part, current_article)
        structured["parts"].append(current_part)


# ─────────────────────────────────────────────────────────────────────────────
def pdf_to_structured_json(pdf_path: str, doc_name: str) -> dict:
    doc = fitz.open(pdf_path)

    structured = {
        "document_name": doc_name,
        "total_pages": len(doc),
        "schedule_starts_at_page": SCHEDULE_START_PAGE,
        "parts": []
    }

    current_part: dict | None = None
    current_article: dict | None = None
    part_counter = 0
    pending_part: dict | None = None  # waiting for title on next line

    for page_num, page in enumerate(doc):
        page_number = page_num + 1

        # ── Start from START_PAGE ────────────────────────────────────────────
        if page_number < START_PAGE:
            continue

        # ── Stop before Schedules ────────────────────────────────────────────
        if page_number >= SCHEDULE_START_PAGE:
            break

        blocks = _page_blocks_without_footnotes(page)

        for block in blocks:
            raw = block[4]
            lines = [l.strip() for l in raw.split("\n")]

            for line in lines:
                if _is_noise(line):
                    continue

                clean = line.strip()
                if not clean:
                    continue

                # ── Pending part: next non-noise line is the title ───────────
                if pending_part is not None:
                    if not _is_part(clean) and not _is_article_start(clean):
                        # This line is the part title
                        # Remove leading/trailing punctuation like "—"
                        title = clean.strip("—–-. ")
                        pending_part["part_title"] = title.title()
                        current_part = pending_part
                        pending_part = None
                        continue
                    else:
                        # No title found — finalise as-is and fall through
                        current_part = pending_part
                        pending_part = None

                # ── Detect PART header ───────────────────────────────────────
                part_match = _is_part(clean)
                if part_match:
                    # Save previous part + article
                    _flush_part(structured, current_part, current_article)
                    current_article = None

                    part_counter += 1
                    pending_part = {
                        "part_id": f"{doc_name}_p{part_counter}",
                        "part_number": part_match.group(1).upper(),
                        "part_title": "",
                        "page_start": page_number,
                        "page_end": page_number,
                        "articles": []
                    }
                    continue

                # ── Detect Article number ────────────────────────────────────
                art_match = _is_article_start(clean)
                if art_match and current_part is not None:
                    art_num, rest = art_match

                    # Save previous article
                    _flush_article(current_part, current_article)

                    current_article = {
                        "article_id": f"{doc_name}_a{art_num}",
                        "article_number": art_num,
                        "page_start": page_number,
                        "page_end": page_number,
                        "content": rest
                    }
                    current_part["page_end"] = page_number
                    continue

                # ── Accumulate content ───────────────────────────────────────
                if current_article is not None:
                    sep = " " if current_article["content"] else ""
                    current_article["content"] += sep + clean
                    current_article["page_end"] = page_number
                    if current_part:
                        current_part["page_end"] = page_number

                elif current_part is not None:
                    # Text before first article in a part (preamble of part)
                    current_article = {
                        "article_id": f"{doc_name}_preamble_p{part_counter}",
                        "article_number": None,
                        "page_start": page_number,
                        "page_end": page_number,
                        "content": clean
                    }

    # ── Flush remaining ──────────────────────────────────────────────────────
    if pending_part:
        current_part = pending_part
    _flush_part(structured, current_part, current_article)

    doc.close()
    return structured


# ─────────────────────────────────────────────────────────────────────────────
def convert_constitution_pdf(pdf_path: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    doc_name = os.path.splitext(os.path.basename(pdf_path))[0]

    print(f"Converting Constitution PDF: {pdf_path}")
    print(f"Processing pages {START_PAGE} to {SCHEDULE_START_PAGE - 1} (before Schedules) ...")

    structured = pdf_to_structured_json(pdf_path, doc_name)

    output_path = os.path.join(output_folder, f"{doc_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2, ensure_ascii=False)

    total_articles = sum(len(p["articles"]) for p in structured["parts"])
    print(f"✅ Saved → {output_path}")
    print(f"   Parts    : {len(structured['parts'])}")
    print(f"   Articles : {total_articles}")



# ── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    convert_constitution_pdf("./pdfs/Industrial Disputes Act 1947.pdf", "./json_docs")
