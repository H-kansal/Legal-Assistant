from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma
from langchain_core.documents import Document
import json
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH=os.path.join(BASE_DIR, "db" ,"bsc_db")
file_path = os.path.join(BASE_DIR, "docs", "bns_clean.json")
with open(file_path, "r", encoding="utf-8") as f:
    sections = json.load(f)


embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


docs=[]

def load_documents():

    for obj in sections:
        content = obj.get("section_text", "").strip()
        if not content:
            continue
        metadata = {k: v for k, v in obj.items() if k != "section_text"}

        docs.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    return docs


if  os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
    print("Loading existing Chroma database...")
    db=Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
else:
    print("Creating new Chroma database...")
    load_documents()
    db=Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=CHROMA_PATH)


def get_retriever():
    retriever=db.as_retriever(search_type="similarity", search_kwargs={"k":3})
    return retriever