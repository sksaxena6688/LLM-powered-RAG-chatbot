# frontend/streamlit_app.py

import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")
st.write("Ask questions about your documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "sources" in message:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.text_area(f"Source {i}", source, height=100, disabled=True, key=f"hist_{id(message)}_{i}")

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"question": prompt}
                )
                response.raise_for_status()
                data = response.json()
                
                st.write(data["answer"])
                
                if data["sources"]:
                    with st.expander("View Sources"):
                        for i, source in enumerate(data["sources"], 1):
                            st.text_area(f"Source {i}", source, height=100, disabled=True, key=f"src_{len(st.session_state.messages)}_{i}")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data["sources"]
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")
