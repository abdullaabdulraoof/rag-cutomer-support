from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama

from app.vectorstore import load_vectorstore
from app.rag_pipeline import get_answer

app = FastAPI()

index, docs = load_vectorstore()

class Query(BaseModel):
    question: str


@app.post("/ask-stream")
def ask_stream(query: Query):

    def generate():

        prompt = f"""
Answer the question clearly.

Question:
{query.question}
"""

        # 🔥 STREAM from Ollama
        stream = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            yield content

    return StreamingResponse(generate(), media_type="text/plain")