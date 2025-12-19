import os
import json
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "db", "document_pattern_db")
file_path = os.path.join(BASE_DIR, "docs", "documentPattern.json")

with open(file_path, "r", encoding="utf-8") as f:
    patterns = json.load(f)

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

docs=[]
def load_documents():
    for pattern in patterns:
        docs.append(
            Document(
                id=pattern.get("id", ""),
                page_content=pattern.get("content", ""),
                metadata=pattern.get("metadata", {})
            )
        )
    return docs

if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
    print("Loading existing Chroma database...")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
else:
    print("Creating new Chroma database...")
    load_documents()
    db = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=CHROMA_PATH)

def get_retriever():
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever