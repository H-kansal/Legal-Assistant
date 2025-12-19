from typing import TypedDict, List, Dict, Any,Annotated
from operator import add
from structureClass import DecompositionOutput
from langgraph.graph.message import add_messages
from structureClass import FinalAnswerOutput,IssueOutput,FinalAnswer,RiskAnalysisOutput
from operator import add

def merge_dicts(a: Dict[str, List[str]], b: Dict[str, List[str]]):
    result = dict(a)
    for k, v in b.items():
        if k in result:
            result[k].extend(v)
        else:
            result[k] = v
    return result


class AgentState(TypedDict):
    user_query: str
    sub_queries: Annotated[List[DecompositionOutput],add]
    retrieved_docs:Annotated[Dict[str, List[str]],merge_dicts]
    final_answer:FinalAnswerOutput

class DocuementAgentState(TypedDict):
    file_name:str
    document_summary: str
    document_chunks: List[str]
    document_pattern: Dict[str, Any]
    issues_found: List[IssueOutput]
    enriched_questions: List[str]
    risk_analysis_results: List[Dict[str, Any]]
    risk_report: List[FinalAnswer]
