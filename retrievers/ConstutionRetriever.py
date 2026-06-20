

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
import json
import os

load_dotenv()

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "db", "const_db")
FILE_PATH   = os.path.join(BASE_DIR, "docs", "Constitution.json")

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_documents() -> list[Document]:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc_name = data.get("document_name", "Constitution")
    docs = []

    for part in data.get("parts", []):
        part_id     = part.get("part_id", "")
        part_number = part.get("part_number", "")
        part_title  = part.get("part_title", "")

        for article in part.get("articles", []):
            content = article.get("content", "").strip()
            if not content:
                continue

            article_number = article.get("article_number", "")
            article_title  = article.get("heading", "") or article.get("article_title", "")

            # ✅ Enrich content so article number & title are searchable via embeddings
            enriched_content = (
                f"Document: {doc_name}\n"
                f"Part {part_number}: {part_title}\n"
                f"Article {article_number}: {article_title}\n\n"
                f"{content}"
            )

            metadata = {
                # Document level
                "document_name":  doc_name,
                # Part level
                "part_id":        part_id,
                "part_number":    str(part_number),
                "part_title":     part_title,
                # Article level
                "article_id":     article.get("article_id", ""),
                "article_number": str(article_number),
                "article_title":  article_title,        # ✅ now in metadata
                # Location
                "page_start":     article.get("page_start", 0),
                "page_end":       article.get("page_end", 0),
            }

            docs.append(Document(page_content=enriched_content, metadata=metadata))

    print(f"✅ Loaded {len(docs)} articles from {doc_name}")
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
