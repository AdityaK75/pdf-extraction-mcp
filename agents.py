from typing import List, Any, Optional
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

class DocumentAgents:
    """
    Holds LLM and agent configuration. Each method returns a LangChain Tool for a document understanding step.
    """
    def __init__(self, llm=None):
        self.llm = llm or ChatOpenAI(model="gpt-4-turbo-preview")

    def pdf_extractor_tool(self) -> Tool:
        """LangChain Tool for PDF extraction via MCP stdio tool."""
        def extract(pdf_path: str) -> str:
            async def extract_async():
                server_params = StdioServerParameters(
                    command="python",
                    args=["server/pdfserver.py"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool(
                            "extract_pdf_contents",
                            arguments={"pdf_path": pdf_path}
                        )
                        return result.content[0].text
            return asyncio.run(extract_async())
        return Tool(
            name="PDF Extractor",
            description="Extracts text from a PDF file using the MCP pdfextractor tool.",
            func=extract
        )

    def chunker_tool(self) -> Tool:
        """LangChain Tool for chunking via MCP stdio tool."""
        def chunk(text: str, chunk_size: int = 500) -> List[str]:
            async def chunk_async():
                server_params = StdioServerParameters(
                    command="python",
                    args=["server/chunker.py"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool(
                            "chunk_text",
                            arguments={"text": text, "chunk_size": chunk_size}
                        )
                        return [c.text for c in result.content]
            return asyncio.run(chunk_async())
        return Tool(
            name="Chunker",
            description="Splits text into chunks using the MCP chunker tool.",
            func=chunk
        )

    def embedder_tool(self) -> Tool:
        """LangChain Tool for embedding via MCP stdio tool."""
        def embed(chunks: List[str]) -> List[List[float]]:
            async def embed_async():
                server_params = StdioServerParameters(
                    command="python",
                    args=["server/embedder.py"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool(
                            "embed_chunks",
                            arguments={"chunks": chunks}
                        )
                        return [json.loads(c.text) for c in result.content]
            return asyncio.run(embed_async())
        return Tool(
            name="Embedder",
            description="Embeds text chunks using the MCP embedder tool.",
            func=embed
        )

    def summarizer_tool(self) -> Tool:
        """LangChain Tool for summarization via MCP stdio tool."""
        def summarize(text_or_chunks: Any) -> str:
            async def summarize_async():
                server_params = StdioServerParameters(
                    command="python",
                    args=["server/summarizer.py"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool(
                            "summarize_text",
                            arguments={"text": text_or_chunks}
                        )
                        return result.content[0].text
            return asyncio.run(summarize_async())
        return Tool(
            name="Summarizer",
            description="Summarizes text or chunks using the MCP summarizer tool.",
            func=summarize
        )

    def qna_tool(self) -> Tool:
        """LangChain Tool for QnA via MCP stdio tool."""
        def qna(question: str, doc_id: str, top_k: int = 5) -> str:
            async def qna_async():
                server_params = StdioServerParameters(
                    command="python",
                    args=["server/qna.py"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool(
                            "answer_question",
                            arguments={"question": question, "doc_id": doc_id, "top_k": top_k}
                        )
                        return result.content[0].text
            return asyncio.run(qna_async())
        return Tool(
            name="QnA",
            description="Answers questions using the MCP QnA tool.",
            func=qna
        )

class DocumentProcessingPipeline:
    """
    Orchestrates the document processing workflow using LangChain tools.
    Provides methods to get a summary and answer questions about the document.
    """
    def __init__(self, pdf_path: str, chunk_size: int = 500):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.text: Optional[str] = None
        self.chunks: Optional[List[str]] = None
        self.embeddings: Optional[List[List[float]]] = None
        self.doc_id: Optional[str] = None
        self.agents = DocumentAgents()
        self._process_document()

    def _process_document(self):
        """Runs the pipeline: extract -> chunk -> embed."""
        self.text = self.agents.pdf_extractor_tool().run(self.pdf_path)
        self.chunks = self.agents.chunker_tool().run(self.text, self.chunk_size)
        self.embeddings = self.agents.embedder_tool().run({"chunks": self.chunks})
        self.doc_id = self.pdf_path

    def get_summary(self) -> str:
        """Returns a summary of the document."""
        return self.agents.summarizer_tool().run(self.text)

    def ask_question(self, question: str, top_k: int = 5) -> str:
        """Answers a question based on the document content."""
        return self.agents.qna_tool().run(question, self.doc_id, top_k=top_k)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Agentic Document Processing Pipeline (LangChain-style)")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("--question", type=str, help="Ask a question about the document")
    parser.add_argument("--summary", action="store_true", help="Get a summary of the document")
    args = parser.parse_args()

    pipeline = DocumentProcessingPipeline(args.pdf_path)
    if args.summary:
        print("\nSummary:\n" + pipeline.get_summary())
    if args.question:
        print(f"\nQ: {args.question}\nA: {pipeline.ask_question(args.question)}")

    