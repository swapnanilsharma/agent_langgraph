import boto3
from typing import Dict, List, Any
from langchain_aws.graphs import NeptuneAnalyticsGraph
from config import settings
from schemas import NeptuneNode, NeptuneRelationship, Document, EXAMPLE_NEPTUNE_SCHEMA, EXAMPLE_DOCDB_SCHEMA

class NeptuneClient:
    def __init__(self):
        self.graph = NeptuneAnalyticsGraph(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            endpoint=settings.NEPTUNE_ENDPOINT
        )
        self.schema = EXAMPLE_NEPTUNE_SCHEMA

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a Cypher query on Neptune database."""
        try:
            results = await self.graph.query(query)
            return results
        except Exception as e:
            print(f"Error executing Neptune query: {str(e)}")
            return []

    def get_schema(self) -> Dict[str, Any]:
        """Return the Neptune graph schema."""
        return self.schema

class DocumentDBClient:
    def __init__(self):
        self.client = boto3.client(
            'docdb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.endpoint = settings.DOCDB_ENDPOINT
        self.schema = EXAMPLE_DOCDB_SCHEMA

    async def query_documents(self, query: str) -> List[Dict[str, Any]]:
        """Query documents from DocumentDB based on natural language query."""
        try:
            # This is a placeholder. You'll need to implement the actual query logic
            # based on your DocumentDB schema and requirements
            response = self.client.query(
                endpoint=self.endpoint,
                query=query
            )
            return response.get('results', [])
        except Exception as e:
            print(f"Error querying DocumentDB: {str(e)}")
            return []

    def get_schema(self) -> Dict[str, Any]:
        """Return the DocumentDB schema."""
        return self.schema 