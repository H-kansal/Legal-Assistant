from langchain_groq import ChatGroq
from stateAgent import AgentState
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from structureClass import FinalAnswerOutput
import os
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

def get_final_answer(state: AgentState)-> AgentState:
    if not state["retrieved_docs"]:
        return {
            "final_answer":{}
        }

    promptMessage="""You are a highly accurate Indian legal assistant.
        
        You will be given:
        1. A user's legal question
        2. Retrieved legal excerpts from multiple Indian law databases

        Your task is to provide a clear, well-structured legal answer based ONLY on the provided material.

        ━━━━━━━━━━━━━━━━━━━
        IMPORTANT RULES
        ━━━━━━━━━━━━━━━━━━━
        • Use ONLY the provided legal excerpts as your source of truth  
        • Do NOT invent sections, punishments, or procedures  
        • If information is missing or unclear, explicitly say so  
        • Clearly distinguish between substantive law, procedural law, and evidentiary rules  
        • Maintain neutral, informative tone (not advisory or opinionated)  

        ━━━━━━━━━━━━━━━━━━━
        LEGAL HIERARCHY
        ━━━━━━━━━━━━━━━━━━━
        Follow this order when reasoning:
        1. Constitution of India
        2. Substantive Criminal Law (BNS)
        3. Special Law (IT Act, etc.)
        4. Procedural Law (CrPC / CPC)
        5. Evidence Law (Indian Evidence Act)

        ━━━━━━━━━━━━━━━━━━━
        If section or rule numbers are not explicitly present in the provided excerpts, do NOT invent or assume them.
        If the provided material is insufficient to fully answer the question, clearly state:
        "The available legal excerpts do not provide sufficient information to fully answer this question."
    """

    llm=ChatGroq(groq_api_key=groq_api_key,model="openai/gpt-oss-120b", temperature=0)
    structed_llm=llm.with_structured_output(FinalAnswerOutput,method="function_calling")

    retrieved_docs=state["retrieved_docs"]
    prompt=ChatPromptTemplate.from_messages([
        ("system", promptMessage),
        ("user","Provide a clear, well-structured legal answer based ONLY on the provided material. User query: {user_query},Retrieved legal excerpts: {retrieved_docs}"),
    ])

    chain=prompt | structed_llm
    result=chain.invoke({"user_query":state["user_query"], "retrieved_docs":retrieved_docs})

    return {
        "final_answer": result.model_dump()
    }