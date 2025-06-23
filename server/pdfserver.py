from mcp.server.fastmcp import FastMCP
from pdf_extractor import PDFExtractor

extractor = PDFExtractor()
mcp = FastMCP(
    name="pdf_extractor",
    host="0.0.0.0",
    port=8002
)

@mcp.tool()
def extract_pdf_contents(pdf_path: str, pages: str = None) -> str:
    """
    Extracts text from a PDF file.
    Args:
        pdf_path: Path to the PDF file.
        pages: Comma-separated page numbers (optional).
    Returns:
        Extracted text as a string.
    """
    return extractor.extract_content(pdf_path, pages)

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"

if __name__ == "__main__":
    mcp.run(transport="stdio")