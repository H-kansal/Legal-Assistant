from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable
from utils.llm import getLLM
import os



promptTemplate="""
You are a legal document summarization assistant for Indian legal documents.

Your task is to produce a concise, neutral summary.
Do NOT analyze legality.
Do NOT give legal advice.
Do NOT cite laws or sections.

Summarize the legal document in 5–7 bullet points.
Focus only on:
- the purpose of the document
- parties involved
- key obligations
- rights
- penalties or consequences (if any)

Return ONLY bullet points in json format.So that document pattern can be easily identified.
"""
@traceable(name="Text Summary Node")
def textSummary(text:str)->str:    

    llm=getLLM()
    prompt=ChatPromptTemplate.from_messages([
        ("system", promptTemplate),
        ("user","Summarize the following legal document:\n{text}")
    ])
    chain=prompt | llm
    response=chain.invoke({"text":text})
    return response.content