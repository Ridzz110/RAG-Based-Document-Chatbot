---
title: Local RAG Document Q&A Chatbot
emoji: 📄
colorFrom: green
colorTo: teal
sdk: gradio
sdk_version: "6.2.0"
app_file: src/app.py
pinned: false
---
# Local RAG-Based Document Q&A Chatbot

A local, retrieval-augmented generation (RAG) chatbot for querying your own documents. This project allows you to upload documents (PDF, DOCX, TXT), prepare them, and interact with them via a lightweight, locally running language model. It is designed to be computationally efficient, suitable for standard laptops.

## Features

+ Works entirely locally — no cloud required.

+ Supports multiple document formats: PDF, DOCX, TXT.

+ Documents are chunked and stored in a vector store (FAISS).

+ Uses all-MiniLM-L6-v2 embeddings for document chunks.

+ Retrieves relevant chunks based on queries via similarity search.

+ Uses SLM Ollama Phi for generating answers with context from your documents (Ollama Phi
).
+ App metrics and monitoring logs to keep track of performance.

## How It Works

### Document Preparation

+ Upload your documents in DOCX, PDF, or TXT format.

+ Documents are chunked along with source information and IDs.

### Embedding Creation

+ Each chunk is converted into vector embeddings using the all-MiniLM-L6-v2 model.

+ Embeddings are stored in a FAISS vector store for efficient retrieval.

### Query Retrieval

+ When a query is entered, a similarity search retrieves the most relevant chunks from the vector store.

### Answer Generation

+ Retrieved chunks are passed as context to a prompt.

+ The prompt is sent to the Ollama Phi SLM model, which generates the final answer.

## Requirements

All Python dependencies are listed in requirements.txt.

### Key packages include:

+ gradio for the UI

+ faiss for vector store

+ sentence-transformers for embeddings

+ ollama for SLM integration

## Setup Instructions

Clone the repository:
```
git clone https://github.com/Ridzz110/Local-RAG-Based-Document-Q-A-Chatbot.git
cd Local-RAG-Based-Document-Q-A-Chatbot
```
Set up Python virtual environment:
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
Install Python dependencies:
```
pip install -r requirements.txt
```
Set up Ollama Phi model:

Install Ollama from https://ollama.com
 if not installed.
```
Pull the Phi model:

ollama pull phi
```
Run the Gradio interface:
```
python src/app.py
```

This will start the local RAG chatbot UI.

## Notes

* Docker was intentionally not used due to system constraints.
* The performance can be slow and computationally heavy on CPU only systems.

## Future Improvements.
+ Implement docker.
+ User Sessions persistance.

## Author

**Rida Batool**
AI Undergraduate | Aspiring ML Engineer

GitHub: [https://github.com/Ridzz110](https://github.com/Ridzz110)
LinkedIn: [https://www.linkedin.com/in/ridabatool110](https://www.linkedin.com/in/ridabatool110)
