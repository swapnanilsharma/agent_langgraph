from langchain_community.llms import Bedrock
from langchain_core.prompts import ChatPromptTemplate
from config import settings
from schemas import EXAMPLE_NEPTUNE_SCHEMA, EXAMPLE_DOCDB_SCHEMA

def get_llm():
    """Initialize AWS Bedrock LLM with Claude 3.5 Sonnet."""
    return Bedrock(
        model_id=settings.MODEL_ID,
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        model_kwargs={
            "temperature": 0.7,
            "max_tokens": 1000,
        }
    )

# Cypher query generation prompt with schema
CYPHER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f"""You are an expert in converting natural language to Cypher queries for graph databases.
    Generate valid Cypher queries that can be executed on AWS Neptune database.
    Focus on creating efficient and accurate queries that match the user's intent.
    
    Here is the Neptune graph schema:
    {EXAMPLE_NEPTUNE_SCHEMA}
    
    Use this schema to generate appropriate Cypher queries."""),
    ("user", "{question}")
])

# DocumentDB query prompt with schema
DOCDB_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f"""You are an expert in converting natural language to DocumentDB queries.
    Generate appropriate queries that can be executed on AWS DocumentDB.
    Focus on creating queries that accurately retrieve the requested information.
    
    Here is the DocumentDB schema:
    {EXAMPLE_DOCDB_SCHEMA}
    
    Use this schema to generate appropriate DocumentDB queries."""),
    ("user", "{question}")
]) 