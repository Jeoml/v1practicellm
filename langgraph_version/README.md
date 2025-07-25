# LangGraph Ecommerce Assistant

A simple, modular LangGraph-based customer service assistant for order status and shipment tracking.

## Features

- 🤖 **LangGraph Agent**: Natural conversation with tool usage
- 📦 **Order Lookup**: Check order status by order ID
- 🚚 **Transit Tracking**: Track shipments using tracking IDs
- 💬 **Session Management**: Conversation history per user
- 🔍 **LangSmith Tracing**: Built-in observability

## Project Structure

```
langgraph-version/
├── main.py      # Entry point
├── config.py    # Configuration
├── tools.py     # Order/transit tools
├── agent.py     # LangGraph agent
├── api.py       # FastAPI routes
└── README.md
```

## Setup

1. **Install**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment** (create `.env`):
   ```env
   GROQ_API_KEY=your_key
   LANGSMITH_API_KEY=your_key
   ```

3. **Start backend**:
   ```bash
   cd ../ecommerce_apis
   uvicorn main:app --port 8001
   ```

4. **Start assistant**:
   ```bash
   python main.py
   ```

## Usage

**POST** `http://127.0.0.1:8080/ask`
```json
{
    "message": "Where is my order with ID 10?",
    "session_id": "user123"
}
```

Simple and clean! 🎯
