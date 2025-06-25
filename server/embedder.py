from mcp.server.fastmcp import FastMCP
from typing import List
from langchain_openai import OpenAIEmbeddings
import json
import os
from pathlib import Path

mcp = FastMCP("embedder")

def get_api_key():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.strip().split('=')[1]
    return None

@mcp.tool()
def embed_chunks(text_chunks: List[str]) -> List[str]:
    """
    Generates vector embeddings for a list of text chunks using OpenAI embeddings.
    Args:
        text_chunks: List of text chunks.
    Returns:
        List of embedding vectors as JSON strings (one per chunk).
    """
    try:
        api_key = get_api_key()
        if not api_key:
            raise ValueError("Could not find OPENAI_API_KEY in .env file")
        embedder = OpenAIEmbeddings(api_key=api_key)
        vectors = embedder.embed_documents(text_chunks)
        return [json.dumps(vec) for vec in vectors]
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    mcp.run(transport="stdio") 