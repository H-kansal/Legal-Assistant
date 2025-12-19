from langgraph.graph import START,END,StateGraph
from stateAgent import DocuementAgentState

from nodeFunctions.parsingNode import parsingNode
from nodeFunctions.docuementPatternNode import documentPatternNode
from nodeFunctions.issueExtractionNode import issueExtractionNode
from nodeFunctions.deDupliationNode import deDupliationNode
from nodeFunctions.queryEnrichment import queryEnrichmentNode
from nodeFunctions.riskAnalysisNode import riskAnalysisNode
from nodeFunctions.riskReport import riskReportNode

graph_builder=StateGraph(DocuementAgentState)
graph_builder.add_node("parsing",parsingNode)
graph_builder.add_node("document_pattern",documentPatternNode)
graph_builder.add_node("issue_extraction",issueExtractionNode)
graph_builder.add_node("de_duplication",deDupliationNode)
graph_builder.add_node("query_enrichment",queryEnrichmentNode)
graph_builder.add_node("risk_analysis",riskAnalysisNode)
graph_builder.add_node("risk_report",riskReportNode)
# edges

graph_builder.add_edge(START,"parsing")
graph_builder.add_edge("parsing","document_pattern")
graph_builder.add_edge("document_pattern","issue_extraction")
graph_builder.add_edge("issue_extraction","de_duplication")
graph_builder.add_edge("de_duplication","query_enrichment")
graph_builder.add_edge("query_enrichment","risk_analysis")
graph_builder.add_edge("risk_analysis","risk_report")
graph_builder.add_edge("risk_report",END)

graph=graph_builder.compile()


# initial_state:DocuementAgentState={
#     "file_name":"sample_property_sale_agreement (1).pdf",
#     "document_summary":"",
#     "document_chunks":[],
#     "document_pattern":{}
# }
# final_state = None

# for state in graph.stream(initial_state, stream_mode="values"):
#     final_state = state

# print("---------------------------------------------------")
# print("Issues Found:", final_state["issues_found"])
# print("---------------------------------------------------")
# print("Enriched Questions:", final_state["enriched_questions"])
# print("---------------------------------------------------")
# print("Risk Analysis Results:", final_state["risk_analysis_results"])
# print("---------------------------------------------------")
# print("Risk Report:", final_state["risk_report"])