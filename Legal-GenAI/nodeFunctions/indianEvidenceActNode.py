from langchain_groq import ChatGroq
from stateAgent import AgentState
from retrievers.IndianEvidenceAcrRetriever import get_retriever
from dotenv import load_dotenv
import os

load_dotenv()


def get_db_queries(sub_query) -> list:
    queries = []
    for sq in sub_query:
        if 'Indian Evidence Act' in sq.databases:
            queries.append(sq.question)
    return queries

def indianEvidenceActDocsRetriever(sub_queries) -> list:
    queries = get_db_queries(sub_queries)
    if not queries:
        return {}
    retriever = get_retriever()

    all_retrieved_docs = []
    for query in queries:
        results = retriever.invoke(query)
        all_retrieved_docs.extend([doc.page_content for doc in results])

def indianEvidenceActNode(state: AgentState) -> AgentState:
    
    return {
        "retrieved_docs": {
            "IndianEvidenceAct": indianEvidenceActDocsRetriever(state["sub_queries"])
        }
    }