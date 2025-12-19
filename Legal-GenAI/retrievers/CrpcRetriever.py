from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "docs", "crpc.pdf")
CHROMA_PATH=os.path.join(BASE_DIR,  "db" ,"crpc_db")

def load_documents():
    loader=PyPDFLoader(file_path)
    documents=loader.load()

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs=text_splitter.split_documents(documents)
    return docs


embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
    print("Loading existing Chroma database...")
    db=Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
else:
    docs=load_documents()
    print("Creating new Chroma database...")
    db=Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=CHROMA_PATH)

def get_retriever():
    retriever=db.as_retriever(search_type="similarity", search_kwargs={"k":3})
    return retriever

