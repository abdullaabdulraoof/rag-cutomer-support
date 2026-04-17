import numpy as np
import ollama

from app.embedder import model

def get_answer(query, index, chunks):
    
    import numpy as np
    import ollama
    from app.embedder import model

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, k=2)

    retrieved_chunks = []

    for i in I[0]:
        if i != -1:
            retrieved_chunks.append(chunks[i])

    context = "\n".join([c.page_content for c in retrieved_chunks])

    sources = [c.metadata["source"] for c in retrieved_chunks]

    prompt = f"""
Use the context to answer briefly.

Context:
{context}

Question:
{query}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"], list(set(sources))
    
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, k=2)

    retrieved_chunks = []
    for i in I[0]:
        if i != -1:
            retrieved_chunks.append(chunks[i])

    context = "\n".join([c.page_content for c in retrieved_chunks])

    prompt = f"""
Use the context to answer briefly.

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