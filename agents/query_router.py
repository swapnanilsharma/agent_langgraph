from typing import Dict, Any
from langgraph.graph import StateGraph
from tools.neptune_tool import NeptuneTool
from tools.docdb_tool import DocumentDBTool

class QueryRouter:
    def __init__(self):
        self.neptune_tool = NeptuneTool()
        self.docdb_tool = DocumentDBTool()
        self.workflow = self._create_workflow()

    def _route_by_tool(self, state: Dict[str, Any]) -> str:
        """Route to appropriate tool based on the query."""
        messages = state["messages"]
        last_message = messages[-1]["content"].lower()
        
        if "graph" in last_message or "neptune" in last_message:
            return "neptune"
        elif "document" in last_message or "doc" in last_message:
            return "docdb"
        else:
            return "end"

    def _process_results(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process and format results from the tools."""
        results = state["results"]
        state["messages"].append({
            "role": "assistant",
            "content": f"Here are the results: {results}"
        })
        return state

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("neptune", self.neptune_tool.query_neptune)
        workflow.add_node("docdb", self.docdb_tool.query_docdb)
        workflow.add_node("process", self._process_results)

        # Add edges
        workflow.add_edge("neptune", "process")
        workflow.add_edge("docdb", "process")
        workflow.add_conditional_edges(
            "route",
            self._route_by_tool,
            {
                "neptune": "neptune",
                "docdb": "docdb",
                "end": "end"
            }
        )

        # Set entry point
        workflow.set_entry_point("route")

        return workflow.compile()

    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query."""
        initial_state = {
            "messages": [
                {"role": "user", "content": query}
            ],
            "current_tool": "",
            "query": query,
            "results": []
        }
        
        return await self.workflow.ainvoke(initial_state) 