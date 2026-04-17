from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)
    return chunks