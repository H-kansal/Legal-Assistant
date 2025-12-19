from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

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

Return ONLY bullet points.So that document pattern can be easily identified.
"""

def textSummary(text:str)->str:
    llm=ChatGroq(api_key=groq_api_key,model="openai/gpt-oss-20b",temperature=0)
    prompt=ChatPromptTemplate.from_messages([
        ("system", promptTemplate),
        ("user","Summarize the following legal document:\n{text}")
    ])
    chain=prompt | llm
    response=chain.invoke({"text":text})
    return response.content