import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    NEPTUNE_ENDPOINT: str = os.getenv("NEPTUNE_ENDPOINT", "")
    DOCDB_ENDPOINT: str = os.getenv("DOCDB_ENDPOINT", "")
    
    # LLM Configuration
    MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    class Config:
        env_file = ".env"

settings = Settings() 