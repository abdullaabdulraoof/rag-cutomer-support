from fastapi import FastAPI
from pydantic import BaseModel

from app.loader import load_documents
from app.chunker import chunk_documents
from app.embedder import create_embeddings
from app.vectorstore import create_faiss_index
from app.rag_pipeline import get_answer

app = FastAPI()

# -------------------------
# Load everything ONCE
# -------------------------
docs = load_documents("../data")
chunks = chunk_documents(docs)
embeddings = create_embeddings(chunks)
index = create_faiss_index(embeddings)

print("RAG API Ready 🚀")


# -------------------------
# Request Schema
# -------------------------
class QueryRequest(BaseModel):
    question: str


# -------------------------
# API Endpoint
# -------------------------
@app.post("/ask")
def ask_question(request: QueryRequest):
    answer, sources = get_answer(request.question, index, chunks)

    return {
        "answer": answer,
        "sources": sources
    }