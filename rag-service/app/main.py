from app.loader import load_documents
from app.chunker import chunk_documents
from app.embedder import create_embeddings
from app.vectorstore import create_faiss_index
from app.rag_pipeline import query_rag

# Load docs
docs = load_documents("../data")

print("Loaded docs:", len(docs))

# Chunk
chunks = chunk_documents(docs)
print("Chunks:", len(chunks))

# Embeddings
embeddings = create_embeddings(chunks)

# Vector DB
index = create_faiss_index(embeddings)

print("RAG Ready 🚀")

# CLI loop
while True:
    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    answer, sources = query_rag(query, index, chunks)

    print("\nAnswer:\n", answer)