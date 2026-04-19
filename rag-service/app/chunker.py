from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)