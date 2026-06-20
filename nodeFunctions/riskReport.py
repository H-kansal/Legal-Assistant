from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from stateAgent import DocuementAgentState
from structureClass import FinalAnswer
from langsmith import traceable
import os

from utils.llm import getLLM
groq_api_key=os.getenv("GROQ_API_KEY")

promptTemplate="""
    You are a legal risk explanation assistant for Indian law.

You will be given individual legal issues extracted from a document.
Each issue includes:

a neutral issue overview
identified legal risk factors
an assessed risk level
affected parties

Your task is to analyze each issue independently and generate a concise, self-contained risk explanation for that issue.

For each issue, you must:
Clearly explain why the issue presents legal risk, based only on the provided details
Describe the nature and seriousness of the risk in neutral, factual terms
Reflect the provided risk level accurately, acknowledging uncertainty where outcomes depend on facts or interpretation
Identify the parties impacted by the risk

Important rules:
Do NOT state that anything is legal or illegal
Do NOT give legal advice or recommendations
Do NOT suggest corrective or preventive actions
Do NOT introduce new facts, assumptions, or external information
Do NOT merge or compare issues with each other
Always respond in valid JSON format.

Base your explanation strictly on the provided issue analysis

Maintain a neutral, explanatory, risk-focused tone
Your role is to explain and contextualize legal risk for each issue individually, not to resolve it or assess the document as a whole.
    """
@traceable(name="Risk Report Node")
def riskReportNode(state:DocuementAgentState)-> DocuementAgentState:

    llm=getLLM()
    structed_llm=llm.with_structured_output(FinalAnswer)
    prompt=ChatPromptTemplate.from_messages([
        ("system", promptTemplate),
        ("user","Given the following legal risk analysis:\n{issue}"),
    ])
    
    chain=prompt | structed_llm
    all_issue=[]
    for issue in state["risk_analysis_results"]:
        result=chain.invoke({"issue":issue})
        all_issue.append(result.model_dump())
    return {"risk_report":all_issue}



