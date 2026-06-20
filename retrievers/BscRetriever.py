from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "db", "bsc_db")
FILE_PATH   = os.path.join(BASE_DIR, "docs", "Bsc.json")

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def load_documents() -> list[Document]:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc_name = data.get("document_name", "Bsc")
    docs = []

    for chapter in data.get("chapters", []):
        chapter_id     = chapter.get("chapter_id", "")
        chapter_number = chapter.get("chapter_number", "")
        chapter_title  = chapter.get("chapter_title", "")

        for section in chapter.get("sections", []):
            content = section.get("content", "").strip()
            if not content:
                continue

            section_number = section.get("section_number", "")
            section_title  = section.get("heading", "") or section.get("section_title", "")
            article_number = section.get("article_number", section_number)
            article_title  = section.get("article_title", section_title)

            # ✅ Enrich content with identifiers for better embedding matches
            enriched_content = (
                f"Document: {doc_name}\n"
                f"Chapter {chapter_number}: {chapter_title}\n"
                f"Section {article_number}: {article_title}\n\n"
                f"{content}"
            )

            metadata = {
                # Document level
                "document_name":   doc_name,
                # Chapter level
                "chapter_id":      chapter_id,
                "chapter_number":  str(chapter_number),
                "chapter_title":   chapter_title,
                # Section / Article level
                "section_id":      section.get("section_id", ""),
                "section_number":  str(section_number),
                "section_title":   section_title,
                "article_number":  str(article_number),
                "article_title":   article_title,
                # Location
                "page_start":      section.get("page_start", 0),
                "page_end":        section.get("page_end", 0),
            }

            docs.append(Document(page_content=enriched_content, metadata=metadata))

    print(f"✅ Loaded {len(docs)} sections from {doc_name}")
    return docs


# ── Load or create ChromaDB ───────────────────────────────────────────────────
if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
    print("Loading existing Chroma database...")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
else:
    print("Creating new Chroma database...")
    docs = load_documents()
    db = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=CHROMA_PATH
    )


def get_retriever():
    retriever=db.as_retriever(search_type="similarity", search_kwargs={"k":3})
    return retriever
