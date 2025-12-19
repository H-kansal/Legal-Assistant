from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from helper.graph_runner import run_legal_graph
from structureClass import FinalAnswerOutput
import traceback

router = APIRouter()

# -------------------------
# Request Schema
# -------------------------
class QARequest(BaseModel):
    question: str


# -------------------------
# Response Schema (YOUR structure)
# -------------------------

# -------------------------
# API Endpoint
# -------------------------
@router.post("/")
def legal_qa(req: QARequest):
    try:
        result =run_legal_graph(req.question)
        print(result)
        return result

    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
