from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama

from app.vectorstore import load_vectorstore
from app.memory import get_memory, update_memory
from app.embedder import model
import numpy as np

app = FastAPI()

index, docs = load_vectorstore()

class Query(BaseModel):
    question: str
    session_id: str


@app.post("/ask-stream")
def ask_stream(query: Query):

    def generate():
        # 🔹 Step 1: Get memory
        history = get_memory(query.session_id)

        history_text = ""
        for chat in history:
            history_text += f"Q: {chat['question']}\nA: {chat['answer']}\n"

        # 🔹 Step 2: RAG retrieval
        query_embedding = model.encode([query.question])
        query_embedding = np.array(query_embedding).astype("float32")

        D, I = index.search(query_embedding, k=3)

        retrieved_chunks = []
        for i in I[0]:
            if i != -1:
                retrieved_chunks.append(docs[i]["text"])

        context = "\n".join(retrieved_chunks)

        # 🔥 FINAL PROMPT (IMPORTANT)
        prompt = f"""
You are an AI customer support assistant.

Use conversation history if relevant.
Use context if relevant.
Otherwise answer normally.

Conversation History:
{history_text}

Context:
{context}

Question:
{query.question}

Answer clearly.
"""

        # 🔥 STREAM RESPONSE
        stream = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        full_answer = ""

        for chunk in stream:
            content = chunk["message"]["content"]
            full_answer += content
            yield content  # 🔥 send live

        # 🔹 Step 3: Save memory AFTER response
        update_memory(query.session_id, query.question, full_answer)

    return StreamingResponse(generate(), media_type="text/plain")