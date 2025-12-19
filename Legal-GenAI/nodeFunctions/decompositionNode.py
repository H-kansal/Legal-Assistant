from langchain_groq import ChatGroq
from stateAgent import AgentState
from dotenv import load_dotenv
from structureClass import DecompositionOutput
from typing import List
from langchain_core.prompts import ChatPromptTemplate
import os
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

def decompose_query(query):
    llm=ChatGroq(groq_api_key=groq_api_key,model="openai/gpt-oss-120b", temperature=0)
    structed_llm=llm.with_structured_output(DecompositionOutput)
    prompt=ChatPromptTemplate.from_messages([
        ("system",
          
          "You are an expert Indian legal query analyzer.Your task is to decompose a user's legal question into the minimum numberof independent, legally meaningful sub-questions and map each sub-question to the correct legal database(s).You MUST choose databases only from the following list:  - BNS (Bharatiya Nyaya Sanhita) - CrPC (Code of Criminal Procedure) - CPC (Civil Procedure Code) - IT Act - Indian Evidence Act Constitution Database usage rules: - Use BNS for offences, crimes, punishment, criminal liability. - Use CrPC for arrest, FIR, investigation, bail, trial, sentencing procedure. - Use CPC for civil suits, injunctions, decrees, appeals, execution. - Use IT Act for cyber offences, hacking, digital crimes, online misconduct. - Use Indian Evidence Act for admissibility of evidence, burden of proof,electronic evidence, confessions, presumptions. - Use Constitution for fundamental rights, writs, constitutional validity, powers of State, federal structure.Decomposition rules: 1. Each sub-question must be legally answerable on its own. 2. Do NOT invent sections or laws. 3. Do NOT over-split — prefer fewer, high-quality sub-questions. 4. If the question involves multiple legal aspects (e.g. offence + procedure), split them. 5. If only one legal issue exists, return exactly one sub-question. 6. Assign ALL relevant databases for each sub-question."
         ),
        ("user","Decompose the following user query into sub-queries along with the databases to search for each sub-query. User query: {user_query}")
    ])


    chain=prompt | structed_llm
    result=chain.invoke({"user_query":query})
    return result.sub_queries

def decompositionNode(state:AgentState)->AgentState:
    return {"sub_queries":decompose_query(state["user_query"])}