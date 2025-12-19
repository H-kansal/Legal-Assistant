from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from stateAgent import DocuementAgentState
from nodeFunctions.decompositionNode import decompose_query
from nodeFunctions.bnsNode import bnsDocsRetriever
from nodeFunctions.constitutionNode import constitutionDocsRetriever
from nodeFunctions.cpcNode import cpcDocsRetriever
from nodeFunctions.crpcNode import crpcDocsRetriever
from nodeFunctions.indianEvidenceActNode import indianEvidenceActDocsRetriever
from nodeFunctions.itActNode import itActDocsRetriever
from structureClass import RiskAnalysisOutput
import os
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

promptTemplate="""
You are an Indian legal risk analysis assistant.

You are given:
• A specific legal issue identified from a document
• Relevant legal materials retrieved from Indian law sources

The document has already been analyzed to identify potential issues.
Your role is NOT to decide legality or give advice.
Your role is to explain what legal risks MAY arise from the issue,
based strictly on the provided legal materials.

You must analyze the issue in a risk-focused manner and explain:
• Why this issue could pose legal risk
• What legal principles or provisions are relevant
• Where uncertainty, ambiguity, or fact-dependence exists

Important rules you MUST follow:
• Do NOT say that anything is legal or illegal
• Do NOT recommend actions or solutions
• Do NOT speculate beyond the provided legal texts
• Do NOT introduce new facts or assumptions
• Use a neutral, informational, and explanatory tone
• If the legal position depends on facts or interpretation, clearly say so

Your objective is to help the user understand
the possible legal exposure or risk areas present in the document,
not to resolve the issue or give an opinion.
you have to also analysis the risk level(e.g., low, medium, high).
Base your analysis ONLY on the supplied legal materials.
If the materials are insufficient, explicitly state that limitation.
"""

def riskAnalysisNode(state:DocuementAgentState)->DocuementAgentState:
    queries=state.get("enriched_questions",[])
    if not queries:
        return {"risk_analysis_results":[]}
    llm=ChatGroq(api_key=groq_api_key,model="openai/gpt-oss-120b",temperature=0)
    structed_llm=llm.with_structured_output(RiskAnalysisOutput)
    prompt=ChatPromptTemplate.from_messages([
        ("system", promptTemplate),
        ("user","Analyze the following legal issue and relevant legal materials to explain potential legal risks:\n\nLegal Issue:\n{query}\n\nRelevant Legal Materials:\n{retrieved_docs}")
    ])
    chain=prompt | structed_llm

    risk_analysis_results=[]
    for query in queries:
        decomposed_queries=decompose_query(query)
        retrieved_docs={}
        retrieved_docs.update({
            "BNS": bnsDocsRetriever(decomposed_queries),
            "Constitution": constitutionDocsRetriever(decomposed_queries),
            "CPC": cpcDocsRetriever(decomposed_queries),
            "CrPC": crpcDocsRetriever(decomposed_queries),
            "IndianEvidenceAct": indianEvidenceActDocsRetriever(decomposed_queries),
            "ITAct": itActDocsRetriever(decomposed_queries)
        })

        result=chain.invoke({
            "query": query,
            "retrieved_docs": retrieved_docs
        })
        risk_analysis_results.append(result)
    state["risk_analysis_results"]=[result.model_dump() for result in risk_analysis_results]
    return state








                


        

    
