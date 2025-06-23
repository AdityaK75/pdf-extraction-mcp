from mcp.server.fastmcp import FastMCP
from typing import List

mcp = FastMCP("chunker")

@mcp.tool()
def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Splits the input text into chunks of approximately chunk_size characters.
    Args:
        text: The input text to chunk.
        chunk_size: The maximum size of each chunk (default: 500).
    Returns:
        List of text chunks.
    """
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

if __name__ == "__main__":
    mcp.run(transport="stdio") 