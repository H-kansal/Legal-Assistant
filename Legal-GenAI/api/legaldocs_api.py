from fastapi import APIRouter, HTTPException,UploadFile,File
from pydantic import BaseModel
from typing import Optional, List
from helper.graph_runner import docs_graph_runner
import shutil
import traceback
import os
router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@router.post("/")
def legal_docs(file: UploadFile = File(...)):
    try:
        allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")
        
        file_path=os.path.join(BASE_DIR,"docs",file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result=docs_graph_runner(file.filename)
        
        return result
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    


    