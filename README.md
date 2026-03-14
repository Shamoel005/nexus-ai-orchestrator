# Nexus — Multimodal Distributed AI Orchestrator

A distributed system to process multimodal inputs (Images/PDFs) with 
asynchronous task queuing, ML classification, and vector search.

## Tech Stack
- **FastAPI** — REST API server
- **Redis** — Async task queue
- **Scikit-learn** — Document classification
- **Pinecone** — Vector search database
- **Matplotlib** — Real-time dashboard
- **PyMuPDF + Pillow** — PDF & Image processing

## Features
- Upload PDF or Image documents via API
- Automatic ML-based categorization (technology, medical, legal, finance)
- Vector embeddings stored in Pinecone for similarity search
- Live performance dashboard with real-time graphs
- Fully async pipeline — never blocks on processing

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Setup .env file
PINECONE_API_KEY=your_key_here
PINECONE_INDEX=nexus-index

### 3. Start Redis
brew services start redis

### 4. Start API Server
uvicorn main:app --reload

### 5. Start Worker
python worker.py

### 6. Start Dashboard
python dashboard.py

## API Endpoints
- GET / — Health check
- POST /upload — Upload a document
- GET /results — View all processed results
- GET /status — Check queue status

## Project Structure
main.py — FastAPI server
worker.py — Document processor
classifier.py — ML classifier
vector_store.py — Pinecone integration
dashboard.py — Matplotlib dashboard