from typing import Dict, List, Any
from langchain_core.tools import tool
from langchain_core.tools import bind_tools
from db_clients import NeptuneClient
from llm_config import CYPHER_PROMPT, get_llm

class NeptuneTool:
    def __init__(self):
        self.client = NeptuneClient()
        self.llm = get_llm()
        self.tools = self._create_tools()

    def _create_tools(self):
        """Create and bind tools for Neptune operations."""
        @tool
        async def query_neptune(question: str) -> List[Dict[str, Any]]:
            """Convert natural language to Cypher query and execute it on Neptune."""
            # Generate Cypher query using LLM
            chain = CYPHER_PROMPT | self.llm
            cypher_query = chain.invoke({"question": question})
            
            # Execute query on Neptune
            results = await self.client.execute_query(cypher_query)
            return results

        @tool
        def get_neptune_schema() -> Dict[str, Any]:
            """Get the Neptune graph schema."""
            return self.client.get_schema()

        return bind_tools(
            [query_neptune, get_neptune_schema],
            self.llm,
            "You are an expert in working with AWS Neptune graph database. Use these tools to query and understand the graph structure."
        )

    async def process_query(self, query: str) -> List[Dict[str, Any]]:
        """Process a query using the bound tools."""
        response = await self.tools.ainvoke(query)
        return response 