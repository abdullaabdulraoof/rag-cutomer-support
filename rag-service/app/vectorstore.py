import faiss
import pickle
import numpy as np
import os

VECTOR_PATH = "vectorstore/faiss_index.bin"
METADATA_PATH = "vectorstore/metadata.pkl"


# 🔹 Create FAISS index
def create_faiss_index(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index


# 🔥 ADD THIS FUNCTION (IMPORTANT)
def load_vectorstore():
    if not os.path.exists(VECTOR_PATH) or not os.path.exists(METADATA_PATH):
        raise Exception("❌ Vectorstore not found. Run ingestion first.")

    index = faiss.read_index(VECTOR_PATH)

    with open(METADATA_PATH, "rb") as f:
        docs = pickle.load(f)

    return index, docs