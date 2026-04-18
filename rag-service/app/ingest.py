from app.db import collection
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Fetch data
docs = []
for item in collection.find():
    text = f"Q: {item['question']}\nA: {item['answer']}"
    docs.append({
        "text": text,
        "source": item["category"]
    })

print("Loaded docs:", len(docs))

# Convert to embeddings
texts = [d["text"] for d in docs]
embeddings = model.encode(texts)
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS
os.makedirs("vectorstore", exist_ok=True)
faiss.write_index(index, "vectorstore/faiss_index.bin")

# Save metadata
with open("vectorstore/metadata.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ Ingestion complete. FAISS index saved.")