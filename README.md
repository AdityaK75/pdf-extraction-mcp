# MCP PDF Assistant 📄🤖

A modular, microservice-based PDF Assistant leveraging **Machine Control Protocol (MCP)** microservices for robust PDF **extraction, chunking, embedding, vector storage**, **QnA**, and **summarization**.

Built with **modularity**, **observability**, and **extensibility** in mind. Offers both **CLI** and **Streamlit UI**. Powered by **OpenTelemetry** and **Arize Phoenix** for advanced monitoring and debugging.

---

## 📚 Table of Contents

- [Features](#features)
- [Architecture & Components](#architecture--components)
- [Workflow](#workflow)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
  - [Starting MCP Servers](#starting-mcp-servers)
  - [Streamlit UI](#streamlit-ui)
  - [Command-line Interface (CLI)](#command-line-interface-cli)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Extensibility & Observability](#extensibility--observability)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🚀 Features

- ✅ **Modular MCP microservices** for extraction, chunking, embedding, and vector storage.
- 💬 **QnA & Summarization** powered by Retrieval-Augmented Generation (RAG) + fallback LLMs.
- 🖥️ **Streamlit UI** for no-code operation.
- 🛠️ **CLI** for scripting and automation workflows.
- 📈 **Observability** via OpenTelemetry and Arize Phoenix.
- 🧱 **Highly modular pipeline** for easy extension and debugging.

---

## 🧩 Architecture & Components

| Component         | Responsibility                                          |
|------------------|----------------------------------------------------------|
| `extractor`      | PDF text & metadata extraction                          |
| `chunker`        | Splits content into semantic chunks                     |
| `embedder`       | Embeds chunks into vectors using LLM embeddings         |
| `vector store`   | Stores and retrieves embeddings using similarity search |
| `rag+llm`        | Handles QnA and summarization via RAG and LLM fallback  |
| `app_streamlit.py` | Streamlit-based UI                                     |
| `cli.py`         | CLI interface                                           |
| `modules/`       | Core orchestration logic                                |
| `server/`        | Hosts all microservices                                 |
| `start_mcp_servers.sh` | Script to launch all services                     |

---

## 🔁 Workflow

1. **Upload PDF** → Upload document via UI or CLI.
2. **Extraction** → Extract text & metadata using `extractor`.
3. **Chunking** → Segment text into meaningful units via `chunker`.
4. **Embedding** → Convert chunks to vector embeddings using `embedder`.
5. **Vector Storage** → Save vectors into a similarity-based vector store.
6. **QnA / Summarization** → Retrieve and answer using RAG + fallback LLM.
7. **Observability** → Monitor the entire pipeline using OpenTelemetry + Phoenix.

---

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/AdityaK75/pdf-extraction-mcp.git
cd pdf-extraction-mcp/mcp-pdf-ectractor

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
