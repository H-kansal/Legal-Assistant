from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from retrievers.documentPatternRetriever import get_retriever
from dotenv import load_dotenv
from stateAgent import DocuementAgentState
from structureClass import DocumentPatternOutput
import os

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

promptTempelate="""
You are a legal document classification assistant for Indian legal documents.

Your task is to identify the document pattern and provide structured information about the document.

Follow these rules strictly:
- Identify exactly ONE document type.
- Identify the main parties involved.
- State the purpose of the document in 1–2 sentences.
- Select applicable legal domains from:
  Civil, Criminal, Contract, Employment, Property, Cyber, Constitutional.
- Do NOT analyze legality.
- Do NOT cite laws or sections.
- Do NOT give legal advice.
- If the document does not clearly match a known type, choose "Other".
"""


def documentPatternNode(state: DocuementAgentState) -> DocuementAgentState:
    retriever = get_retriever()
    all_retrieved_docs=retriever.invoke(state["document_summary"])
    llm=ChatGroq(api_key=groq_api_key, model="openai/gpt-oss-120b", temperature=0)
    structed_llm=llm.with_structured_output(DocumentPatternOutput)

    prompt=ChatPromptTemplate.from_messages([
        ("system", promptTempelate),
        ("user","Classify the following legal document:\n{document_summary} on given document pattern:\n{retrieved_docs}"),
    ])

    chain=prompt | structed_llm
    result=chain.invoke({"document_summary":state["document_summary"],"retrieved_docs":all_retrieved_docs})

    return {
        "document_pattern": {
            "document_type": result.document_type,
            "category": result.category,
            "jurisdiction": result.jurisdiction,
            "parties_involved": result.parties_involved
        }
    }

