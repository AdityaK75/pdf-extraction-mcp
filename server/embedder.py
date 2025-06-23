from mcp.server.fastmcp import FastMCP
from typing import List
from langchain_openai import OpenAIEmbeddings
import json

mcp = FastMCP("embedder")

@mcp.tool()
def embed_chunks(chunks: List[str]) -> List[str]:
    """
    Generates vector embeddings for a list of text chunks using OpenAI embeddings.
    Args:
        chunks: List of text chunks.
    Returns:
        List of embedding vectors as JSON strings (one per chunk).
    """
    embedder = OpenAIEmbeddings()
    vectors = embedder.embed_documents(chunks)
    return [json.dumps(vec) for vec in vectors]

if __name__ == "__main__":
    mcp.run(transport="stdio") 