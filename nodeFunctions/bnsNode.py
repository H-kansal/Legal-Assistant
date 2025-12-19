from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from stateAgent import AgentState
from retrievers.BscRetriever import get_retriever
import os
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

def get_db_queries(sub_query)->list:
    queries=[]
    for sq in sub_query:
        if 'BNS' in sq.databases:
            queries.append(sq.question)
    return  queries


def bnsDocsRetriever(sub_queries)->list:
    queries=get_db_queries(sub_queries)
    all_retrieved_docs=[]
    if not queries:
        return all_retrieved_docs
    retriever=get_retriever()

    for query in queries:
        results=retriever.invoke(query)
        all_retrieved_docs.extend([doc.page_content for doc in results])
    
    return all_retrieved_docs



def bnsNode(state:AgentState)->AgentState:
    sub_queries=state["sub_queries"]
    
    return {
        "retrieved_docs":{
            "BNS":bnsDocsRetriever(sub_queries)
        }
    }