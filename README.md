# LLM-Powered RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot that answers questions based on your PDF documents using OpenAI and FAISS.

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Streamlit  │─────▶│   FastAPI    │─────▶│  RAG Chain  │
│  Frontend   │      │   Backend    │      │  (LangChain)│
└─────────────┘      └──────────────┘      └─────────────┘
                                                    │
                                                    ▼
                                            ┌─────────────┐
                                            │    FAISS    │
                                            │ Vector Store│
                                            └─────────────┘
                                                    │
                                                    ▼
                                            ┌─────────────┐
                                            │   OpenAI    │
                                            │ Embeddings  │
                                            └─────────────┘
```

## How RAG Works

1. **Document Ingestion**: PDFs are loaded and split into chunks
2. **Embedding Generation**: Each chunk is converted to vector embeddings using OpenAI
3. **Vector Storage**: Embeddings are stored in FAISS for fast retrieval
4. **Query Processing**: User questions are embedded and matched against stored vectors
5. **Context Retrieval**: Top-k most relevant chunks are retrieved
6. **Answer Generation**: LLM generates answer using only retrieved context
7. **Source Grounding**: Original source chunks are returned with the answer

## Use Case
This project demonstrates a Retrieval-Augmented Generation (RAG) chatbot designed for querying private or domain-specific documents such as PDFs, reports, or internal knowledge bases. Instead of relying on generic LLM knowledge, the system retrieves relevant document chunks using vector similarity search and generates answers strictly grounded in the retrieved context.

This approach is ideal for enterprise knowledge assistants, document Q&A systems, customer support bots, and internal tools where accuracy, hallucination control, and data privacy are critical. The architecture is modular, production-ready, and easily deployable, making it suitable for real-world applications beyond demos or prototypes.

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd rag-chatbot
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-...
```

### 3. Add Documents

Place your PDF files in the `data/` directory.

### 4. Ingest Documents

```bash
python ingest.py
```

This creates a FAISS vector database in `backend/vectorstore/`.

### 5. Start Backend

```bash
uvicorn app:app --reload
```

Backend runs at `http://localhost:8000`

### 6. Start Frontend

```bash
cd ../frontend
pip install streamlit requests
streamlit run streamlit_app.py
```

Frontend runs at `http://localhost:8501`

## Deployment

### Railway/Render

1. Create `Procfile` in backend/:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

2. Set environment variable `OPENAI_API_KEY`

3. Run ingestion once before deploying or as a one-time job

4. Deploy frontend separately with `BACKEND_URL` pointing to backend service

## API Endpoints

### POST /chat
```json
Request:
{
  "question": "What is RAG?"
}

Response:
{
  "answer": "RAG stands for...",
  "sources": ["chunk1...", "chunk2...", "chunk3..."]
}
```

### GET /health
```json
Response:
{
  "status": "ok"
}
```

## Tech Stack

- **Language**: Python 3.10+
- **Backend**: FastAPI
- **RAG Framework**: LangChain
- **LLM**: OpenAI GPT-3.5-turbo
- **Vector Store**: FAISS (local)
- **Embeddings**: OpenAI text-embedding-ada-002
- **Frontend**: Streamlit

## License

MIT
