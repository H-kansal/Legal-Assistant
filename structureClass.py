
from pydantic import BaseModel, Field
from typing import List, Optional, Dict,Literal
class SubQuery(BaseModel):
    question: str
    databases: List[str]

class DecompositionOutput(BaseModel):
    sub_queries:List[SubQuery]=Field(..., description="List of sub-queries with their corresponding databases to search.")

class ApplicableLaw(BaseModel):
    act: str
    provision: str
    context: str | None = None

class FinalAnswerOutput(BaseModel):
    Legal_Issue_Identified: Optional[str] = Field(
        default=None,
        description="Briefly restate the core legal issue(s)"
    )
    Applicable_Laws: List[ApplicableLaw] = Field(
        description="Relevant Acts and provisions used in the answer",
        example=[
            {
                "act": "Civil Procedure Code",
                "provision": "Rule 294",
                "context": "Temporary injunction"
            }
        ]
    )
    Legal_Explanation: str = Field(
        description="Explain how the law applies to the issue"
    )
    Procedure: Optional[str] = Field(
        default=None,
        description="Procedural steps, if applicable"
    )
    Evidence: Optional[str] = Field(
        default=None,
        description="Evidentiary requirements, if applicable"
    )
    Conclusion: str = Field(
        description="Concise legal conclusion"
    )


class DocumentPatternOutput(BaseModel):
    document_type:str=Field(...,description="Type of the legal document")
    jurisdiction:str=Field(...,description="Jurisdiction of the legal document")
    category:str=Field(...,description="Category of the legal document")
    parties_involved:Optional[List[str]]=Field(None,description="Main parties involved in the document")


class IssueOutput(BaseModel):
    issue_summary: str = Field(description="A brief summary of the legal issue identified.")
    affected_parties: List[str] = Field(description="List of parties affected by the legal issue.")
    issue_type: str = Field(description="Type of legal issue (e.g., contract dispute, property issue,Termination issue,Restriction issue).")
class RiskAnalysisOutput(BaseModel):
    issue_overview: str = Field(description="A clear, neutral, stand-alone legal question based on the provided issue details.")
    risk_factors: str = Field(description="Key risk factors or considerations related to the legal issue.")
    risk_level:Optional[Literal["Low", "Medium", "High", "Fact-dependent"]]= Field(None, description="An assessment of the potential risk level (e.g., low, medium, high) associated with the issue.")
    affected_parties: List[str] = Field(description="List of parties affected by the legal issue.")


class FinalAnswer(BaseModel):
    legal_explanation: str
    overall_risk_level: str
    affected_parties: List[str]