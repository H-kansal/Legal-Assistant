import os
from dotenv import load_dotenv
from langsmith import Client
from langchain_groq import ChatGroq
from Evaluation.LegalQA_Dataset import EXAMPLES
from Evaluation.run_agent import run_legal_graph
from pydantic import BaseModel
from typing import Annotated
from utils.llm import getLLM
load_dotenv()


os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"]="true"
# ── Setup ─────────────────────────────────────────────────────────────────────

client = Client()
# ChatGroq is automatically traced by LangSmith when LANGCHAIN_TRACING_V2=true

DATASET_NAME = "Legal-Rag-Ai"


def createDataset():
    try:
        dataset = client.create_dataset(DATASET_NAME)
    except Exception:
        dataset = client.read_dataset(dataset_name=DATASET_NAME)
        print(f"Dataset '{DATASET_NAME}' already exists, reusing it.")
        return dataset
    
    client.create_examples(
        dataset_id=dataset.id,
        examples=EXAMPLES
    )

    print("Dataset formed")
    return dataset

def run_agent(inputs:dict)->dict:
    state=run_legal_graph(inputs["query"])
    print(state.keys())
    return {"answer":state["final_answer"],"docs":state["retrieved_docs"]}




# correctNess (Response vs reference answer)
class CorrectnessGrade(BaseModel):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    correct: Annotated[bool, ..., "True if the answer is correct, False otherwise."]

def correctness(inputs:dict,outputs:dict,reference_outputs:dict):
    input_test=inputs["query"]
    reference=reference_outputs["answer"]
    response=outputs["answer"]

    SYSTEM_PROMPT="""
            You are a teacher grading a quiz. 

            You will be given a QUESTION, the GROUND TRUTH (correct) ANSWER, and the STUDENT ANSWER. 

            Here is the grade criteria to follow:
            (1) Grade the student answers based ONLY on their factual accuracy relative to the ground truth answer. 
            (2) Ensure that the student answer does not contain any conflicting statements.
            (3) It is OK if the student answer contains more information than the ground truth answer, as long as it is factually accurate relative to the  ground truth answer.

            Correctness:
            A correctness value of True means that the student's answer meets all of the criteria.
            A correctness value of False means that the student's answer does not meet all of the criteria.

            Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

            Avoid simply stating the correct answer at the outset.
            Always respond in valid JSON format.
        """

    llm=getLLM()
    structured_llm=llm.with_structured_output(CorrectnessGrade)
    result=structured_llm.invoke([
        ("system",SYSTEM_PROMPT),
        ("user",f"""
            QUESTION: {input_test}
            GROUND TRUTH ANSWER: {reference}
            STUDENT ANSWER: {response}
            """)
    ])
    
    return {
        "key": "correctness",
        "score": int(result.correct),
        "comment": result.explanation
    }

    
    
#  Relevance: Response vs input
class RelevanceGrade(BaseModel):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    relevant: Annotated[bool, ..., "Provide the score on whether the answer addresses the question"]

def relevance(inputs: dict, outputs: dict) -> dict:
    """A simple evaluator for RAG answer helpfulness."""

    input_test=inputs["query"]
    response=outputs["answer"]
    
    SYSTEM_PROMPT="""You are a teacher grading a quiz. 

            You will be given a QUESTION and a STUDENT ANSWER. 

            Here is the grade criteria to follow:
            (1) Ensure the STUDENT ANSWER is concise and relevant to the QUESTION
            (2) Ensure the STUDENT ANSWER helps to answer the QUESTION

            Relevance:
            A relevance value of True means that the student's answer meets all of the criteria.
            A relevance value of False means that the student's answer does not meet all of the criteria.

            Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

            Avoid simply stating the correct answer at the outset.
            Always respond in valid JSON format.
        """
    
    llm=getLLM()
    structured_llm=llm.with_structured_output(RelevanceGrade)
    result=structured_llm.invoke([
        ("system",SYSTEM_PROMPT),
        ("user",f"""
            QUESTION: {input_test}
            STUDENT ANSWER: {response}
            """)
    ])
    
    return {
        "key": "relevance",
        "score": int(result.relevant),
        "comment": result.explanation
    }



# Groundedness: Response vs retrieved docs
class GroundedGrade(BaseModel):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    grounded: Annotated[bool, ..., "Provide the score on if the answer hallucinates from the documents"]

def groundedness(inputs: dict, outputs: dict) -> dict:
    """A simple evaluator for RAG answer groundedness."""
    SYSTEM_PROMPT="""You are a teacher grading a quiz. 

        You will be given FACTS and a STUDENT ANSWER. 
        
        Here is the grade criteria to follow:
        (1) Ensure the STUDENT ANSWER is grounded in the FACTS. 
        (2) Ensure the STUDENT ANSWER does not contain "hallucinated" information outside the scope of the FACTS.

        Grounded:
        A grounded value of True means that the student's answer meets all of the criteria.
        A grounded value of False means that the student's answer does not meet all of the criteria.

        Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

        Avoid simply stating the correct answer at the outset.
        Always respond in valid JSON format.
    """
    
    docs_list=[]
    for k,v in outputs["docs"].items():
        docs_list.extend(v)
    
    docs_string="\n\n".join(docs_list)

    llm=getLLM()
    structured_llm=llm.with_structured_output(GroundedGrade)
    result=structured_llm.invoke([
        ("system",SYSTEM_PROMPT),
        ("user",f"""
            FACTS: {docs_string}
            STUDENT ANSWER: {outputs['answer']}
            """
        )
    ])
    
    return {
        "key": "groundedness",
        "score": int(result.grounded),
        "comment": result.explanation
    }



# Retrieval Relevance: Retrieved docs vs input
class RetrievalRelevanceGrade(BaseModel):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    relevant: Annotated[bool, ..., "True if the retrieved documents are relevant to the question, False otherwise"]

def retrieval_relevance(inputs: dict, outputs: dict) -> dict:
    """An evaluator for document relevance"""
    SYSTEM_PROMPT="""You are a teacher grading a quiz. 

            You will be given a QUESTION and a set of FACTS provided by the student. 

            Here is the grade criteria to follow:
            (1) You goal is to identify FACTS that are completely unrelated to the QUESTION
            (2) If the facts contain ANY keywords or semantic meaning related to the question, consider them relevant
            (3) It is OK if the facts have SOME information that is unrelated to the question as long as (2) is met

            Relevance:
            A relevance value of True means that the FACTS contain ANY keywords or semantic meaning related to the QUESTION and are therefore relevant.
            A relevance value of False means that the FACTS are completely unrelated to the QUESTION.

            Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

            Avoid simply stating the correct answer at the outset.
            Always respond in valid JSON format.
        """

    docs_list=[]
    for k,v in outputs["docs"].items():
        docs_list.extend(v)
    
    doc_string="\n\n".join(docs_list)
    answer = f"FACTS: {doc_string}\nQUESTION: {inputs['query']}"
    llm=getLLM()
    structured_llm=llm.with_structured_output(RetrievalRelevanceGrade)
    grade = structured_llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": answer}
    ])
    return {
        "key": "relevance",
        "score": int(grade.relevant),
        "comment": grade.explanation
    }



def evaluation():
    print("creating database.......")
    createDataset()

    print("start Evaluation..........")
    results=client.evaluate(
        run_agent,
        data=DATASET_NAME,
        evaluators=[correctness, groundedness, relevance, retrieval_relevance],
        experiment_prefix="rag-doc-relevance",
        metadata={"version": " constitution-Rag-langgraph-llamarunner-1"},
    )

    return     