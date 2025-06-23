# Document Understanding System

This project is a scalable, modular, and intelligent document understanding system. Users can upload documents (currently supporting PDFs), generate summaries, and ask questions based on the document's content.

## Architecture

The system is built with a modular architecture, separating the API, document processing, and vector database services.

- **API (`api/`)**: A FastAPI application that exposes endpoints for document upload, summarization, and Q&A.
- **Document Processor (`core/`)**: Handles PDF extraction, text chunking, and generating embeddings using LangChain.
- **Qdrant Service (`services/`)**: Manages all interactions with the Qdrant vector database, including storage and retrieval of document vectors.

## Features

- **Document Upload**: Upload PDF files via a REST API.
- **Summarization**: Generate a concise summary of the entire document.
- **Question Answering**: Ask questions about the document's content using a Retrieval-Augmented Generation (RAG) pipeline.

## Setup

1. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
2. **Set up environment variables**:
   Create a `.env` file and add your `OPENAI_API_KEY`.
3. **Run the application**:
   ```sh
   uvicorn api.main:app --reload
   ```

## Usage

- **Upload a document**: `POST /upload`
- **Summarize a document**: `GET /summarize/{document_id}`
- **Ask a question**: `POST /ask`
