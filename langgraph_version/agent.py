"""
LangGraph Agent implementation for the Ecommerce Assistant
"""
from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langsmith import traceable
from .tools import ALL_TOOLS
from .config import DEFAULT_MODEL


class AgentState(TypedDict):
    """State definition for the agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class EcommerceAgent:
    """LangGraph-based ecommerce customer service agent"""
    
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model = ChatGroq(model=model_name).bind_tools(ALL_TOOLS)
        self.agent = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        graph = StateGraph(AgentState)
        tool_node = ToolNode(tools=ALL_TOOLS)
        
        graph.add_node("agent", self._model_call)
        graph.add_node("tools", tool_node)
        graph.set_entry_point("agent")
        
        graph.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "tools": "tools",
                "end": END,
            },
        )
        graph.add_edge("tools", "agent")
        
        return graph.compile()
    
    @traceable(name="model_call")
    def _model_call(self, state: AgentState):
        """Main model call with system prompt"""
        system_prompt = SystemMessage(
            content="""You are a helpful ecommerce customer service assistant. 
            You can help customers check their order status and track shipments.
            
            When a customer asks about their order:
            1. Ask for their order ID if they haven't provided it
            2. Use the lookup_order_status tool to get order information
            3. If they need tracking information, use the lookup_transit_status tool with the tracking ID
            
            Be friendly, helpful, and provide clear information about their orders and shipments."""
        )
        response = self.model.invoke([system_prompt] + state['messages'])
        return {"messages": [response]}
    
    @traceable(name="should_continue")
    def _should_continue(self, state: AgentState):
        """Determine whether to continue to tools or end"""
        messages = state['messages']
        last_message = messages[-1]
        if not last_message.tool_calls:
            return "end"
        else:
            return "tools"
    
    async def ainvoke(self, input_data: dict):
        """Async invoke method for the agent"""
        return await self.agent.ainvoke(input_data)
