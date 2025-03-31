from typing import Dict, List, Any
from langchain_core.tools import tool
from db_clients import DocumentDBClient
from llm_config import DOCDB_PROMPT, get_llm

class DocumentDBTool:
    def __init__(self):
        self.client = DocumentDBClient()
        self.llm = get_llm()

    @tool
    async def query_docdb(self, question: str) -> List[Dict[str, Any]]:
        """Convert natural language to DocumentDB query and execute it."""
        # Generate DocumentDB query using LLM
        chain = DOCDB_PROMPT | self.llm
        docdb_query = chain.invoke({"question": question})
        
        # Execute query on DocumentDB
        results = await self.client.query_documents(docdb_query)
        return results

    def get_schema(self) -> Dict[str, Any]:
        """Return the DocumentDB schema."""
        return self.client.get_schema() 