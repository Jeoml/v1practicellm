"""
FastAPI web server for the LangGraph Ecommerce Assistant
"""
from fastapi import FastAPI, Request
from langchain_core.messages import HumanMessage, AIMessage
from collections import defaultdict, deque
from .agent import EcommerceAgent
from .config import CONVERSATION_HISTORY_LIMIT


app = FastAPI(title="LangGraph Ecommerce Assistant", version="1.0.0")
agent = EcommerceAgent()
conversation_histories = defaultdict(lambda: deque(maxlen=CONVERSATION_HISTORY_LIMIT))


@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    session_id = data.get("session_id", "default")
    
    if not user_message.strip():
        return {"response": "Please provide a message to get assistance."}
    
    conversation_histories[session_id].append(HumanMessage(content=user_message))
    context = list(conversation_histories[session_id])
    
    try:
        response = await agent.ainvoke({"messages": context})
        assistant_reply = response['messages'][-1].content
        conversation_histories[session_id].append(AIMessage(content=assistant_reply))
        return {"response": assistant_reply}
    except Exception as e:
        error_message = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        conversation_histories[session_id].append(AIMessage(content=error_message))
        return {"response": error_message}


@app.get("/")
async def root():
    return {"message": "LangGraph Ecommerce Assistant API", "endpoints": {"chat": "/ask", "docs": "/docs"}}


@app.get("/health")
async def health():
    return {"status": "healthy", "active_sessions": len(conversation_histories)}
