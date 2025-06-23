from mcp.server.fastmcp import FastMCP
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

mcp = FastMCP("qna")

@mcp.tool()
def answer_question(question: str, doc_id: str, top_k: int = 5) -> str:
    """
    Answers a user question using Retrieval-Augmented Generation (RAG):
    1. Embeds the question
    2. Retrieves relevant chunks from the vector store (via MCP tool)
    3. Uses an LLM to answer based on the retrieved context
    Args:
        question: The user's question
        doc_id: The document ID to search within
        top_k: Number of relevant chunks to retrieve
    Returns:
        The answer string
    """
    # 1. Embed the question
    embedder = OpenAIEmbeddings()
    question_embedding = embedder.embed_query(question)

    # 2. Retrieve relevant chunks from the vector store (assume MCP tool 'search_embeddings')
    async def retrieve_chunks():
        vector_server_params = StdioServerParameters(
            command="python",
            args=["server/vector_store.py"],  # Adjust path to your vector store MCP server
        )
        async with stdio_client(vector_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(
                    "search_embeddings",
                    arguments={"query_embedding": question_embedding, "doc_id": doc_id, "top_k": top_k}
                )
                return [c.text for c in result.content]

    chunks = asyncio.run(retrieve_chunks())
    context = "\n".join(chunks)

    # 3. Use LLM to answer based on context
    llm = ChatOpenAI(model="gpt-4-turbo-preview")
    prompt = f"Answer the following question based on the provided context.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    return llm.invoke(prompt)

if __name__ == "__main__":
    mcp.run(transport="stdio") 