from mcp.server.fastmcp import FastMCP
from typing import List, Union
from langchain_openai import ChatOpenAI

mcp = FastMCP("summarizer")

@mcp.tool()
def summarize_text(text: Union[str, List[str]]) -> str:
    """
    Generates a summary for the input text or list of text chunks using an LLM (OpenAI).
    Args:
        text: A string or list of text chunks to summarize.
    Returns:
        A summary string.
    """
    llm = ChatOpenAI(model="gpt-4-turbo-preview")
    if isinstance(text, list):
        text = "\n".join(text)
    prompt = f"Summarize the following document or text chunks as concisely as possible:\n\n{text}"
    return llm.invoke(prompt)

if __name__ == "__main__":
    mcp.run(transport="stdio") 