from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.legalQA_api import router as qa_router
from api.legaldocs_api import router as docs_router
from uvicorn import run as app_run
from Evaluation.test import evaluation


app = FastAPI(title="AI Legal Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa_router, prefix="/qa", tags=["Legal Q&A"])
app.include_router(docs_router, prefix="/analyze", tags=["Legal Docs"])

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)

    # evaluation()