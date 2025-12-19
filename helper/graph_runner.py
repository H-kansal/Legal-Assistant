from LegalQA import graph as QAGraph
from LegalDocs import graph as DocsGraph
from stateAgent import AgentState,DocuementAgentState

def run_legal_graph(question):
    initial_state:AgentState={
        "user_query":question,
        "sub_queries":[],
        "retrieved_docs":{},
        "final_answer":None
    }
    final_state = None


    for state in QAGraph.stream(initial_state, stream_mode="values"):
        final_state = state
    
    if not final_state or "final_answer" not in final_state:
        raise RuntimeError("Graph did not produce a final answer")
    print("Final Answer:", final_state["final_answer"])
    return final_state["final_answer"]

def docs_graph_runner(fileName):
    initial_state={
        "file_name":fileName,
        "document_summary":"",
        "document_chunks":[],
        "document_pattern":{}
    }
    final_state = None

    for state in DocsGraph.stream(initial_state, stream_mode="values"):
        final_state = state
    
    if not final_state or "risk_report" not in final_state:
        raise RuntimeError("Graph did not produce a final answer")
    print("Final Answer:", final_state["risk_report"])
    return final_state["risk_report"]
