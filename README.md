# MCP PDF Assistant

A modular, microservice-based PDF assistant using MCP (Machine Control Protocol) microservices for PDF extraction, chunking, embedding, vector storage, QnA, and summarization. Supports both CLI and Streamlit UI, with robust OpenTelemetry tracing (Arize Phoenix) and a LangChain-style pipeline abstraction.

## Features
- **PDF Extraction, Chunking, Embedding, Vector Storage** via MCP microservices
- **QnA and Summarization** with RAG and fallback to LLM
- **Streamlit UI** and **CLI** interface
- **OpenTelemetry Tracing** with Arize Phoenix
- **Modular, observable, and extensible pipeline**

## Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/AdityaK75/pdf-extraction-mcp.git
   cd pdf-extraction-mcp/mcp-pdf-ectractor
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables:**
   - `PHOENIX_ENDPOINT` (Arize Phoenix collector endpoint)
   - `PHOENIX_API_KEY` (if required)
   - `OPENAI_API_KEY` (for LLM and embedding)

## Running the App
### Start MCP Servers
```bash
./start_mcp_servers.sh
```

### Run Streamlit UI
```bash
streamlit run app_streamlit.py
```

### Run CLI
```bash
python cli.py
```

## Deployment
- **Streamlit Community Cloud:** Push to GitHub, connect, and set env vars in the UI.
- **Docker/Cloud:** Use a Dockerfile and set env vars as needed.

## Project Structure
- `app_streamlit.py` — Streamlit UI
- `cli.py` — Command-line interface
- `modules/` — Pipeline and orchestration logic
- `server/` — MCP microservices (extractor, chunker, embedder, vector store, etc.)
- `start_mcp_servers.sh` — Script to launch all MCP servers

## License
MIT
