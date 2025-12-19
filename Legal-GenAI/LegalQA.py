from langgraph.graph import START,END,StateGraph
from stateAgent import AgentState

from nodeFunctions.decompositionNode import decompositionNode
from nodeFunctions.bnsNode import bnsNode
from nodeFunctions.constitutionNode import constitutionNode
from nodeFunctions.cpcNode import cpcNode
from nodeFunctions.crpcNode import crpcNode
from nodeFunctions.indianEvidenceActNode import indianEvidenceActNode
from nodeFunctions.itActNode import itActNode
from nodeFunctions.finalAnswerNode import get_final_answer

graph_builder=StateGraph(AgentState)
graph_builder.add_node("decompose",decompositionNode)

# nodes
graph_builder.add_edge(START,"decompose")
graph_builder.add_node("bns",bnsNode)
graph_builder.add_node("constitution",constitutionNode)
graph_builder.add_node("cpc",cpcNode)
graph_builder.add_node("crpc",crpcNode)
graph_builder.add_node("indian_evidence_act",indianEvidenceActNode)
graph_builder.add_node("itAct",itActNode)
graph_builder.add_node("final_answer",get_final_answer)
# edges
graph_builder.add_edge("decompose","bns")
graph_builder.add_edge("decompose","constitution")
graph_builder.add_edge("decompose","cpc")
graph_builder.add_edge("decompose","crpc")
graph_builder.add_edge("decompose","indian_evidence_act")
graph_builder.add_edge("decompose","itAct")
graph_builder.add_edge("bns","final_answer")
graph_builder.add_edge("constitution","final_answer")
graph_builder.add_edge("cpc","final_answer")
graph_builder.add_edge("crpc","final_answer")
graph_builder.add_edge("indian_evidence_act","final_answer")
graph_builder.add_edge("itAct","final_answer")
graph_builder.add_edge("final_answer",END)


graph=graph_builder.compile()
# initial_state:AgentState={
#     "user_query":"what is criminal breach of trust?",
#     "sub_queries":[],
#     "retrieved_docs":{},
#     "final_answer":None
# }
# final_state = None


# for state in graph.stream(initial_state, stream_mode="values"):
#     final_state = state

# if not final_state or "final_answer" not in final_state:
#     raise RuntimeError("Graph did not produce a final answer")
# print("Final Answer:", final_state["final_answer"])    
