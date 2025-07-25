"""
Configuration settings for the LangGraph Ecommerce Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ORDER_API_BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 10

# Server Configuration
HOST = "127.0.0.1"
PORT = 8080

# LangChain/LangSmith Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_TRACING_V2 = "true"
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "langgraph-ecommerce")

# Model Configuration
DEFAULT_MODEL = "qwen/qwen3-32b"
CONVERSATION_HISTORY_LIMIT = 4  # 2 user + 2 assistant messages

# Environment setup
def setup_environment():
    """Set up environment variables for LangChain and LangSmith"""
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY or ""
    os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
    os.environ["LANGCHAIN_ENDPOINT"] = LANGSMITH_ENDPOINT
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY or ""
    os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
