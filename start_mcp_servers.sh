#!/bin/bash

# Start MCP Server 1: QnA + Summarizer
.venv/bin/python -m mcp.server \
  --tool server/qna.py \
  --tool server/summarizer.py \
  --host 127.0.0.1 \
  --port 5001 \
  > logs/mcp_server_qna_summarizer.log 2>&1 &
echo "Started MCP Server 1 (QnA + Summarizer) on port 5001, logging to logs/mcp_server_qna_summarizer.log"

# Start MCP Server 2: Extractor, Embedder, Chunker
.venv/bin/python -m mcp.server \
  --tool server/pdf_extractor.py \
  --tool server/embedder.py \
  --tool server/chunker.py \
  --host 127.0.0.1 \
  --port 5002 \
  > logs/mcp_server_extract_embed_chunk.log 2>&1 &
echo "Started MCP Server 2 (Extractor, Embedder, Chunker) on port 5002, logging to logs/mcp_server_extract_embed_chunk.log" 