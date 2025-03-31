from typing import Dict, List, Any, TypedDict, Annotated
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from config import settings
from db_clients import NeptuneClient, DocumentDBClient
from llm_config import get_llm, CYPHER_PROMPT, DOCDB_PROMPT

# Define state type
class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    current_tool: str
    query: str
    results: List[Dict[str, Any]]

# Initialize clients
neptune_client = NeptuneClient()
docdb_client = DocumentDBClient()
llm = get_llm()

@tool
async def query_neptune(question: str) -> List[Dict[str, Any]]:
    """Convert natural language to Cypher query and execute it on Neptune."""
    # Generate Cypher query using LLM
    chain = CYPHER_PROMPT | llm
    cypher_query = chain.invoke({"question": question})
    
    # Execute query on Neptune
    results = await neptune_client.execute_query(cypher_query)
    return results

@tool
async def query_docdb(question: str) -> List[Dict[str, Any]]:
    """Convert natural language to DocumentDB query and execute it."""
    # Generate DocumentDB query using LLM
    chain = DOCDB_PROMPT | llm
    docdb_query = chain.invoke({"question": question})
    
    # Execute query on DocumentDB
    results = await docdb_client.query_documents(docdb_query)
    return results

def route_by_tool(state: AgentState) -> str:
    """Route to appropriate tool based on the query."""
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()
    
    if "graph" in last_message or "neptune" in last_message:
        return "neptune"
    elif "document" in last_message or "doc" in last_message:
        return "docdb"
    else:
        return "end"

def process_results(state: AgentState) -> AgentState:
    """Process and format results from the tools."""
    results = state["results"]
    state["messages"].append({
        "role": "assistant",
        "content": f"Here are the results: {results}"
    })
    return state

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("neptune", query_neptune)
workflow.add_node("docdb", query_docdb)
workflow.add_node("process", process_results)

# Add edges
workflow.add_edge("neptune", "process")
workflow.add_edge("docdb", "process")
workflow.add_conditional_edges(
    "route",
    route_by_tool,
    {
        "neptune": "neptune",
        "docdb": "docdb",
        "end": "end"
    }
)

# Set entry point
workflow.set_entry_point("route")

# Compile the graph
app = workflow.compile()

import asyncio
from agents.query_router import QueryRouter

async def main():
    # Initialize the query router
    router = QueryRouter()
    
    # Example queries
    queries = [
        "Show me all nodes in the graph database",
        "Find all articles written by Jane Smith",
        "What companies are located in San Francisco?"
    ]
    
    # Process each query
    for query in queries:
        print(f"\nProcessing query: {query}")
        result = await router.process_query(query)
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 