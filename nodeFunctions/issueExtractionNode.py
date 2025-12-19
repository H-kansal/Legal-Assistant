from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from stateAgent import DocuementAgentState
from structureClass import IssueOutput
from pydantic import BaseModel
from typing import List
import os

load_dotenv()

class IssueExtractionOutput(BaseModel):
    issues: List[IssueOutput]

groq_api_key=os.getenv("GROQ_API_KEY")

promptTempelate="""
You are a legal issue identification assistant for Indian legal documents.

Your task is to identify statements or clauses that may be legally significant or risky.

Follow these rules strictly:
- Identify only potential issue, not conclusions.
- Do NOT decide legality.
- Do NOT cite laws or sections.
- Do NOT give legal advice.
- Be neutral and descriptive.

"""

def issueExtractionNode(state:DocuementAgentState)->DocuementAgentState:
    llm=ChatGroq(api_key=groq_api_key,model="openai/gpt-oss-120b",temperature=0)
    structed_llm=llm.with_structured_output(IssueExtractionOutput)

    pronpt=ChatPromptTemplate.from_messages([
        ("system", promptTempelate),
        ("user","Identify potential issues in the following legal document chunk:\n{chunk}"),
    ])

    chain=pronpt | structed_llm

    all_issues=[]
    for chunk in state["document_chunks"]:
        result=chain.invoke({"chunk":chunk})
        all_issues.extend(result.issues)
    state["issues_found"]=all_issues
    return state