import numpy as np
import ollama
from app.embedder import model


def get_answer(query, index, docs):

    # 🔹 Convert query to embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # 🔹 Search FAISS
    D, I = index.search(query_embedding, k=2)

    retrieved_texts = []
    sources = []

    for i in I[0]:
        if i != -1:
            retrieved_texts.append(docs[i]["text"])
            sources.append(docs[i]["source"])

    # 🔹 Build context
    context = "\n".join(retrieved_texts)

    # 🔹 Prompt
    prompt = f"""
Use the context to answer briefly.

Context:
{context}

Question:
{query}
"""

    # 🔹 LLM call
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]

    return answer, list(set(sources))