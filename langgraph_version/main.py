"""
Main entry point for the LangGraph Ecommerce Assistant
"""
import asyncio
import uvicorn
import langchain
from .config import setup_environment, HOST, PORT
from .api import app


async def main():
    setup_environment()
    
    langchain.debug = True
    langchain.tracing_enabled = True
    
    print("🚀 Starting LangGraph Ecommerce Assistant...")
    print(f"🌐 Server: http://{HOST}:{PORT}")
    print(f"📖 Docs: http://{HOST}:{PORT}/docs")
    
    config = uvicorn.Config(app=app, host=HOST, port=PORT, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
