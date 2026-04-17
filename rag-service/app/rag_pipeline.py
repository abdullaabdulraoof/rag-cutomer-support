import numpy as np
import ollama

from app.embedder import model

def query_rag(query, index, chunks):
    
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, k=3)

    retrieved_chunks = []
    for i in I[0]:
        if i != -1:
            retrieved_chunks.append(chunks[i])

    context = "\n".join([c.page_content for c in retrieved_chunks])

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {query}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"], retrieved_chunks