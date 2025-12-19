from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from dotenv import load_dotenv
from stateAgent import DocuementAgentState
import os

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")



example_prompt=PromptTemplate.from_template(
    """
        issue_summary:{issue_summary}
        affected_parties: {affected_parties}
        issue_type: {issue_type}
        \n
        output:{output}
    """
)

example_inputs = [
    {
        "issue_summary": "Termination without prior notice",
        "affected_parties": ["Employee", "Employer"],
        "issue_type": "Termination issue",
        "output": "What is the legal position in India regarding termination of an employment relationship without prior notice?"
    },
    {
        "issue_summary": "Non-payment of agreed service fees",
        "affected_parties": ["Service Provider", "Client"],
        "issue_type": "Contract dispute",
        "output": "What is the legal position in India regarding non-payment of agreed service fees under a contract?"
    },
    {
        "issue_summary": "Restriction on transfer of shares",
        "affected_parties": ["Shareholder", "Company"],
        "issue_type": "Restriction issue",
        "output": "What is the legal position in India regarding restrictions on the transfer of shares?"
    },
    {
        "issue_summary": "Possession of property without consent",
        "affected_parties": ["Property Owner", "Occupant"],
        "issue_type": "Property issue",
        "output": "How is possession of property without the owner's consent treated under Indian law?"
    },
    {
        "issue_summary": "Delay in salary payment",
        "affected_parties": ["Employee", "Employer"],
        "issue_type": "Employment issue",
        "output": "What are the legal implications in India of delayed payment of salary by an employer?"
    }
]


prefix="""
You are a legal query reformulation assistant for Indian legal matters.

You will be given:
• issue_summary: a brief description of a legal issue
• affected_parties: parties involved or impacted
• issue_type: the general category of the legal issue

Your task is to convert this information into ONE clear, neutral, stand-alone legal question.

STRICT RULES:
• Do NOT answer the question
• Do NOT cite or mention any laws, statutes, sections, or case names
• Do NOT add, infer, or assume facts not explicitly stated
• Do NOT include remedies, outcomes, or advice
• Keep the question generic and jurisdiction-neutral within India
• Use formal legal language
• Ensure the question is self-contained and understandable without context
• Output ONLY a single question as plain text
• Do NOT include explanations, bullet points, or formatting

The output must be suitable for downstream legal research and retrieval.
"""
def queryEnrichmentNode(state:DocuementAgentState)->DocuementAgentState:
    llm=ChatGroq(api_key=groq_api_key,model="openai/gpt-oss-120b",temperature=0)

    prompt=FewShotPromptTemplate(
        examples=example_inputs,
        example_prompt=example_prompt,
        input_variables=["issue_summary","affected_parties","issue_type"],
        prefix=prefix,
        suffix="issue_summary:{issue_summary}\naffected_parties: {affected_parties}\nissue_type: {issue_type}\n\noutput:",
    )
    
    chain=prompt | llm
    all_enriched_questions=[]
    issue_found=state.get("issues_found",[])
    for issue in issue_found:
        result=chain.invoke({
            "issue_summary":issue.issue_summary,
            "affected_parties":issue.affected_parties,
            "issue_type":issue.issue_type,
        })
        all_enriched_questions.append(result.content.strip()) 
    state["enriched_questions"]=all_enriched_questions
    return state