from langchain_groq import ChatGroq
from stateAgent import AgentState
from retrievers.ItActRetriever import get_retriever
from dotenv import load_dotenv
import os
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

def get_db_queries(sub_query)->list:
    queries=[]
    for sq in sub_query:
        if 'IT Act' in sq.databases:
            queries.append(sq.question)
    return  queries

def itActDocsRetriever(sub_queries)->list:
    queries=get_db_queries(sub_queries)
    if not queries:
        return {}
    retriever=get_retriever()

    all_retrieved_docs=[]
    for query in queries:
        results=retriever.invoke(query)
        all_retrieved_docs.extend([doc.page_content for doc in results])
    return all_retrieved_docs


def itActNode(state:AgentState)->AgentState:
    return {
        "retrieved_docs":{
            "ITAct": itActDocsRetriever(state["sub_queries"])
        }
    }