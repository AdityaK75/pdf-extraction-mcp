from mcp.server.fastmcp import FastMCP
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
from pathlib import Path
import nest_asyncio

mcp = FastMCP("qna")

def get_api_key():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.strip().split('=')[1]
    return None

def run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        nest_asyncio.apply()
        return loop.run_until_complete(coro)
    else:
        return asyncio.run(coro)

@mcp.tool()
def answer_question(question: str, doc_id: str = None, context: str = None, top_k: int = 5) -> str:
    """
    Answers a user question using Retrieval-Augmented Generation (RAG):
    If context is provided, uses it directly. Otherwise, retrieves relevant chunks from the vector store.
    Args:
        question: The user's question
        doc_id: The document ID to search within (optional if context is provided)
        context: The context string to use for answering (optional)
        top_k: Number of relevant chunks to retrieve if context is not provided
    Returns:
        The answer string
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Could not find OPENAI_API_KEY in .env file")

    if context is None:
        # 1. Embed the question
        embedder = OpenAIEmbeddings(api_key=api_key)
        question_embedding = embedder.embed_query(question)

        # 2. Retrieve relevant chunks from the vector store (assume MCP tool 'search_embeddings')
        async def retrieve_chunks():
            vector_server_params = StdioServerParameters(
                command="python",
                args=["server/vector_store.py"],
            )
            async with stdio_client(vector_server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(
                        "search_embeddings",
                        arguments={"query_embedding": question_embedding, "doc_id": doc_id, "top_k": top_k}
                    )
                    return [c.text for c in result.content]

        chunks = run_async(retrieve_chunks())
        # Defensive: flatten to string if needed
        if isinstance(chunks, list):
            chunks = [c.text if hasattr(c, 'text') else str(c) for c in chunks]
        context = "\n".join(chunks)

    # 3. Use LLM to answer based on context
    llm = ChatOpenAI(model="gpt-4-turbo-preview", api_key=api_key)
    prompt = (
        "Based only on the following context from the PDF, answer the question. "
        "If the answer is not in the context, say 'Not found in document.'\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    result = llm.invoke(prompt)
    if hasattr(result, 'content'):
        result = result.content
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio") 