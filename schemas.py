from typing import Dict, List, Any, Optional
from pydantic import BaseModel

# Neptune Graph Schema
class NeptuneNode(BaseModel):
    id: str
    labels: List[str]
    properties: Dict[str, Any]

class NeptuneRelationship(BaseModel):
    id: str
    type: str
    start_node: str
    end_node: str
    properties: Dict[str, Any]

class NeptuneGraphSchema(BaseModel):
    nodes: List[NeptuneNode]
    relationships: List[NeptuneRelationship]

# Example Neptune Schema
EXAMPLE_NEPTUNE_SCHEMA = {
    "nodes": [
        {
            "id": "person1",
            "labels": ["Person"],
            "properties": {
                "name": "John Doe",
                "age": 30,
                "email": "john@example.com"
            }
        },
        {
            "id": "company1",
            "labels": ["Company"],
            "properties": {
                "name": "Tech Corp",
                "industry": "Technology",
                "location": "San Francisco"
            }
        }
    ],
    "relationships": [
        {
            "id": "rel1",
            "type": "WORKS_AT",
            "start_node": "person1",
            "end_node": "company1",
            "properties": {
                "since": "2020",
                "role": "Software Engineer"
            }
        }
    ]
}

# DocumentDB Schema
class Document(BaseModel):
    id: str
    collection: str
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

# Example DocumentDB Schema
EXAMPLE_DOCDB_SCHEMA = {
    "collections": {
        "articles": {
            "fields": {
                "title": "string",
                "content": "string",
                "author": "string",
                "published_date": "date",
                "tags": ["string"],
                "metadata": {
                    "category": "string",
                    "read_time": "number",
                    "status": "string"
                }
            }
        },
        "users": {
            "fields": {
                "username": "string",
                "email": "string",
                "profile": {
                    "name": "string",
                    "bio": "string",
                    "location": "string"
                },
                "preferences": {
                    "theme": "string",
                    "notifications": "boolean"
                }
            }
        }
    }
}

# Example Document
EXAMPLE_DOCUMENT = {
    "id": "doc1",
    "collection": "articles",
    "content": {
        "title": "Getting Started with AWS Neptune",
        "content": "This is a comprehensive guide...",
        "author": "Jane Smith",
        "published_date": "2024-03-15",
        "tags": ["AWS", "Graph Database", "Tutorial"],
        "metadata": {
            "category": "Technology",
            "read_time": 5,
            "status": "published"
        }
    }
} 