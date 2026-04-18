from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import get_answer
from app.vectorstore import load_vectorstore
from app.embedder import model

app = FastAPI()

# Load FAISS once
index, docs = load_vectorstore()

class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):
    answer, sources = get_answer(query.question, index, docs)

    return {
        "question": query.question,
        "answer": answer,
        "sources": sources
    }