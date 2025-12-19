from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from stateAgent import AgentState
from retrievers.CpcRetriever import get_retriever
import os
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

def get_db_queries(sub_query)->list:
    queries=[]
    for sq in sub_query:
        if 'CPC' in sq.databases:
            queries.append(sq.question)
    return  queries

def cpcDocsRetriever(sub_queries)->list:
    queries=get_db_queries(sub_queries)
    if not queries:
        return {}
    retriever=get_retriever()

    all_retrieved_docs=[]
    for query in queries:
        results=retriever.invoke(query)
        all_retrieved_docs.extend([doc.page_content for doc in results])
    return all_retrieved_docs

def cpcNode(state:AgentState)->AgentState:
    
    
    return {
        "retrieved_docs":{
            "CPC": cpcDocsRetriever(state["sub_queries"])
        }
    }