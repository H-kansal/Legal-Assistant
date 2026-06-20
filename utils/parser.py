import pdfplumber
import re
import json


PDF_PATH = r"pdfs/Minimum Wages Act 1948.pdf"
OUTPUT_JSON = r"pdfs/minimum_wages_act.json"


SECTION_START_RE = re.compile(
    r'(?m)^(\d+[A-Z]?)\.\s+([^.]+?)\.—'
)


def extract_pdf_text(pdf_path):

    pages_text = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_num in range(2, len(pdf.pages)):  # start from page 3

            text = pdf.pages[page_num].extract_text()

            if not text:
                continue

            lines = []

            for line in text.split("\n"):

                line = line.strip()

                if not line:
                    continue

                # remove page number
                if re.fullmatch(r"\d+", line):
                    continue

                # remove footnotes
                if re.match(
                    r'^\d+\.\s+(Subs\.|Ins\.|Omitted|The words|The word|Act)',
                    line,
                    re.I
                ):
                    continue

                lines.append(line)

            pages_text.append("\n".join(lines))

    text = "\n".join(pages_text)

    # remove inline refs like 1[ 2[
    text = re.sub(r'\d+\[', '[', text)

    return text


def extract_sections(text):

    matches = list(SECTION_START_RE.finditer(text))

    sections = []

    for i, match in enumerate(matches):

        start = match.start()

        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(text)
        )

        chunk = text[start:end].strip()

        section_number = match.group(1).strip()

        title = match.group(2).strip()

        first_sep = chunk.find(".—")

        description = chunk[first_sep + 2:].strip()

        description = re.sub(
            r'\s+',
            ' ',
            description
        )

        sections.append(
            {
                "section_number": section_number,
                "title": title,
                "description": description
            }
        )

    return sections


def main():

    text = extract_pdf_text(PDF_PATH)

    sections = extract_sections(text)

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            sections,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Extracted {len(sections)} sections"
    )

    print(
        f"Saved to {OUTPUT_JSON}"
    )


if __name__ == "__main__":
    main()