from langchain_groq import ChatGroq
from stateAgent import DocuementAgentState
from helper.docuementProcessing import process_document
from helper.textChunk import chunk_text
from helper.textSummary import textSummary
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parsingNode(state: DocuementAgentState)->DocuementAgentState:
    file_name=state['file_name']
    file_path=os.path.join(BASE_DIR,"docs",file_name)
    cleaned_text = process_document(file_path)
    chunks=chunk_text(cleaned_text, max_chars=1100, min_chars=300)
    summary_input="\n\n".join(chunks[:5])
    summary=textSummary(summary_input)
    state['document_summary']=summary
    state['document_chunks']=chunks
    return state
