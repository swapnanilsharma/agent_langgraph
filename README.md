# AWS LangGraph Agentic Tool App

This application uses LangGraph to create an agentic tool that can:
1. Convert natural language to Cypher queries for AWS Neptune graph database
2. Query AWS DocumentDB using natural language

## Prerequisites

- Python 3.9+
- AWS Account with access to:
  - Amazon Neptune
  - Amazon DocumentDB
  - Amazon Bedrock (for Claude 3.5 Sonnet)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
NEPTUNE_ENDPOINT=your_neptune_endpoint
DOCDB_ENDPOINT=your_docdb_endpoint
```

3. Run the application:
```bash
python main.py
```

## Usage

The application provides two main functionalities:

1. Natural Language to Cypher Query:
   - Input: Natural language question about graph data
   - Output: Results from Neptune database

2. DocumentDB Query:
   - Input: Natural language question about documents
   - Output: Relevant information from DocumentDB

## Architecture

The application uses:
- LangGraph for workflow orchestration
- AWS Bedrock (Claude 3.5 Sonnet) for LLM capabilities
- AWS Neptune for graph database operations
- AWS DocumentDB for document storage and retrieval 