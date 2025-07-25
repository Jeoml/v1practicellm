from fastapi import FastAPI
import sys
import os

# Add parent directories to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ecommerce_apis')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../langgraph_version')))

from ecommerce_apis.main import app as ecommerce_app
from langgraph_version.api import app as langgraph_app

app = FastAPI(title="Combined Ecommerce & LangGraph API")

# Mount ecommerce endpoints at /api
app.mount("/api", ecommerce_app)

# Mount langgraph endpoints at /langgraph
app.mount("/langgraph", langgraph_app)

@app.get("/")
async def root():
    return {
        "message": "Combined Ecommerce & LangGraph API",
        "endpoints": {
            "ecommerce": "/api",
            "langgraph": "/langgraph",
            "docs": "/docs"
        }
    }