from app.db import faq_collection
from app.embedder import model
from app.vectorstore import create_faiss_index, save_vectorstore

import numpy as np

def run_ingestion():
    docs = []

    for item in faq_collection.find():
        text = f"Q: {item['question']}\nA: {item['answer']}"

        docs.append({
            "content": text,
            "source": item["category"]
        })

    print("Loaded docs:", len(docs))

    # Convert to embeddings
    texts = [d["content"] for d in docs]

    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    # Create index
    index = create_faiss_index(embeddings)

    # Save
    save_vectorstore(index, docs)

    print("✅ Ingestion complete")
    

if __name__ == "__main__":
    run_ingestion()