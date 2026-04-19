from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import numpy as np
import ollama

from app.vectorstore import load_vectorstore
from app.embedder import model
from app.memory import save_chat, get_chat

app = FastAPI()

index, docs = load_vectorstore()

class Query(BaseModel):
    question: str
    session_id: str


@app.post("/ask-stream")
def ask_stream(query: Query):

    def generate():
        query_embedding = model.encode([query.question])
        query_embedding = np.array(query_embedding).astype("float32")

        D, I = index.search(query_embedding, k=2)

        context = "\n".join([docs[i]["content"] for i in I[0] if i != -1])

        prompt = f"""
Answer briefly.

Context:
{context}

Q: {query.question}
A:
"""

        stream = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        full_answer = ""

        for chunk in stream:
            content = chunk["message"]["content"]
            full_answer += content
            yield content

        save_chat(query.session_id, query.question, full_answer)

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/history/{session_id}")
def history(session_id: str):
    return get_chat(session_id)