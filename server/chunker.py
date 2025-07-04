from mcp.server.fastmcp import FastMCP
from typing import List

mcp = FastMCP("chunker")

@mcp.tool()
def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 0) -> List[str]:
    """
    Splits the input text into chunks of approximately chunk_size characters, with optional overlap.
    Args:
        text: The input text to chunk.
        chunk_size: The maximum size of each chunk (default: 500).
        chunk_overlap: The number of characters to overlap between chunks (default: 0).
    Returns:
        List of text chunks (as strings).
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size")
    step = chunk_size - chunk_overlap if chunk_overlap > 0 else chunk_size
    return [str(text[i:i+chunk_size]) for i in range(0, len(text), step)]

if __name__ == "__main__":
    mcp.run(transport="stdio") 