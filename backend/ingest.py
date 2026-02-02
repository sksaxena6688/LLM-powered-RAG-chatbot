# backend/ingest.py

import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = "../data"
VECTOR_DB_PATH = "vectorstore"

def ingest_documents():
    pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader, silent_errors=True)
    txt_loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader, silent_errors=True)
    
    pdf_docs = pdf_loader.load()
    txt_docs = txt_loader.load()
    documents = pdf_docs + txt_docs
    
    if not documents:
        raise ValueError("No documents found in data directory. Please add PDF or TXT files.")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    embeddings = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)
    
    print(f"Ingested {len(chunks)} chunks from {len(documents)} documents")

if __name__ == "__main__":
    ingest_documents()
