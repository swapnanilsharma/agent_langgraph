from typing import Dict, List, Any
from langchain_core.tools import tool
from db_clients import NeptuneClient
from llm_config import CYPHER_PROMPT, get_llm

class NeptuneTool:
    def __init__(self):
        self.client = NeptuneClient()
        self.llm = get_llm()

    @tool
    async def query_neptune(self, question: str) -> List[Dict[str, Any]]:
        """Convert natural language to Cypher query and execute it on Neptune."""
        # Generate Cypher query using LLM
        chain = CYPHER_PROMPT | self.llm
        cypher_query = chain.invoke({"question": question})
        
        # Execute query on Neptune
        results = await self.client.execute_query(cypher_query)
        return results

    def get_schema(self) -> Dict[str, Any]:
        """Return the Neptune graph schema."""
        return self.client.get_schema() 