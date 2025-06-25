from mcp.server.fastmcp import FastMCP
from typing import List, Union
from langchain_openai import ChatOpenAI
from pathlib import Path

mcp = FastMCP("summarizer")

def get_api_key():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.strip().split('=')[1]
    return None

@mcp.tool()
def summarize_text(text: Union[str, List[str]]) -> str:
    """
    Generates a summary for the input text or list of text chunks using an LLM (OpenAI).
    Args:
        text: A string or list of text chunks to summarize.
    Returns:
        A summary string.
    """
    # Defensive: handle dict input
    if isinstance(text, dict) and 'text' in text:
        text = text['text']
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Could not find OPENAI_API_KEY in .env file")
    llm = ChatOpenAI(model="gpt-4-turbo-preview", api_key=api_key)
    if isinstance(text, list):
        text = "\n".join(text)
    prompt = f"Summarize the following document or text chunks as concisely as possible:\n\n{text}"
    return llm.invoke(prompt)

if __name__ == "__main__":
    mcp.run(transport="stdio") 