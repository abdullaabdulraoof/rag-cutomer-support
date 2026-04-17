from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.loader import load_documents
from app.chunker import chunk_documents
from app.embedder import create_embeddings
from app.vectorstore import create_faiss_index
from app.rag_pipeline import get_answer

app = FastAPI(title="RAG Customer Support API")

# -------------------------
# Enable CORS (IMPORTANT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Load RAG once
# -------------------------
try:
    docs = load_documents("../data")
    chunks = chunk_documents(docs)
    embeddings = create_embeddings(chunks)
    index = create_faiss_index(embeddings)

    print("✅ RAG API Ready")

except Exception as e:
    print("❌ Error loading RAG:", e)
    docs, chunks, index = [], [], None


# -------------------------
# Request Schema
# -------------------------
class QueryRequest(BaseModel):
    question: str


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def health():
    return {"status": "RAG API is running 🚀"}


# -------------------------
# Ask Endpoint
# -------------------------
import time

@app.post("/ask")
def ask_question(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if index is None:
        raise HTTPException(status_code=500, detail="RAG not initialized")

    try:
        # ⏱️ Start timer
        start_time = time.time()

        answer, sources = get_answer(request.question, index, chunks)

        # ⏱️ End timer
        end_time = time.time()

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources,
            "response_time": f"{round(end_time - start_time, 2)} sec"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))