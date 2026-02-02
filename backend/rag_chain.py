# backend/rag_chain.py

import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = "vectorstore"

def query(question: str):
    embeddings = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
    vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # Retrieve relevant documents
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    
    # Build context from retrieved documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create prompt with context
    system_message = """You are a helpful assistant. Use only the following context to answer the question.
If you cannot find the answer in the context, respond with "I don't know"."""
    
    user_message = f"""Context: {context}

Question: {question}

Answer:"""
    
    # Get response from LLM
    llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", temperature=0)
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]
    response = llm.invoke(messages)
    
    return {
        "answer": response.content,
        "sources": [doc.page_content for doc in docs]
    }
