from typing import Dict, List, Any
from langchain_core.tools import tool
from langchain_core.tools import bind_tools
from db_clients import DocumentDBClient
from llm_config import DOCDB_PROMPT, get_llm

class DocumentDBTool:
    def __init__(self):
        self.client = DocumentDBClient()
        self.llm = get_llm()
        self.tools = self._create_tools()

    def _create_tools(self):
        """Create and bind tools for DocumentDB operations."""
        @tool
        async def query_docdb(question: str) -> List[Dict[str, Any]]:
            """Convert natural language to DocumentDB query and execute it."""
            # Generate DocumentDB query using LLM
            chain = DOCDB_PROMPT | self.llm
            docdb_query = chain.invoke({"question": question})
            
            # Execute query on DocumentDB
            results = await self.client.query_documents(docdb_query)
            return results

        @tool
        def get_docdb_schema() -> Dict[str, Any]:
            """Get the DocumentDB schema."""
            return self.client.get_schema()

        return bind_tools(
            [query_docdb, get_docdb_schema],
            self.llm,
            "You are an expert in working with AWS DocumentDB. Use these tools to query and understand the document structure."
        )

    async def process_query(self, query: str) -> List[Dict[str, Any]]:
        """Process a query using the bound tools."""
        response = await self.tools.ainvoke(query)
        return response 