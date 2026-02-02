# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_chain import query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    result = query(request.question)
    return QueryResponse(answer=result["answer"], sources=result["sources"])

@app.get("/health")
def health():
    return {"status": "ok"}
