from  helper.parsed import parse_document
from helper.clean import clean_text


def process_document(file_path):
    raw_text = parse_document(file_path)
    cleaned_text = clean_text(raw_text)
    return cleaned_text