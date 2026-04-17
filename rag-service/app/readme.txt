Build CLI RAG system
We separate:

loader → load PDFs
chunker → split text
embedder → embeddings
vectorstore → FAISS
rag_pipeline → logic
main → run program

run project:
cd rag-service
python app/main.py