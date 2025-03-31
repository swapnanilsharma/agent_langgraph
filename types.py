from typing import Dict, List, Any, TypedDict

class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    current_tool: str
    query: str
    results: List[Dict[str, Any]] 