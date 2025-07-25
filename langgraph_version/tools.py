"""
Tools for the LangGraph Ecommerce Assistant
"""
import requests
from langchain_core.tools import tool
from .config import ORDER_API_BASE_URL, REQUEST_TIMEOUT


@tool
def lookup_order_status(order_id: str) -> str:
    """
    Retrieves the current status of an order using its unique ID.
    
    This tool requires a valid order ID. If a user requests an order status
    without providing an ID, you must ask them for it. Do not attempt to guess IDs.
    
    Args:
        order_id: The unique identifier for the order (e.g., "10", "25").
        
    Returns:
        A string describing the order status or a detailed error message.
    """
    try:
        url = f"{ORDER_API_BASE_URL}/api/order-status/{order_id}"
        headers = {"Accept": "application/json"}
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 404:
            return (
                f"❌ No order found with ID '{order_id}'. "
                "Please double-check the ID, as this one does not exist in our system."
            )
            
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        tracking_id = data.get("tracking_id")
        
        if status:
            result = f"✅ The status for order ID '{order_id}' is: '{status}'."
            if tracking_id:
                result += f" Tracking ID: {tracking_id}"
            return result
        else:
            return f"ℹ️ Order ID '{order_id}' was found, but its status is currently unavailable."
            
    except requests.exceptions.RequestException as e:
        return f"⚠️ A network error occurred while checking order '{order_id}': {e}"
    except Exception as e:
        return f"⚠️ An unexpected error occurred for order ID '{order_id}': {e}"


@tool
def lookup_transit_status(tracking_id: str) -> str:
    """
    Retrieves the current transit status and location of a shipment using its tracking ID.
    
    Args:
        tracking_id: The unique tracking identifier for the shipment.
        
    Returns:
        A string describing the transit status and location or an error message.
    """
    try:
        url = f"{ORDER_API_BASE_URL}/api/transit-status/{tracking_id}"
        headers = {"Accept": "application/json"}
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 404:
            return (
                f"❌ No transit information found for tracking ID '{tracking_id}'. "
                "Please verify the tracking ID is correct."
            )
            
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        location = data.get("location")
        
        if status and location:
            return f"🚚 Transit status for tracking ID '{tracking_id}': {status} at {location}."
        else:
            return f"ℹ️ Tracking ID '{tracking_id}' was found, but transit details are currently unavailable."
            
    except requests.exceptions.RequestException as e:
        return f"⚠️ A network error occurred while checking tracking '{tracking_id}': {e}"
    except Exception as e:
        return f"⚠️ An unexpected error occurred for tracking ID '{tracking_id}': {e}"


# Export all tools
ALL_TOOLS = [lookup_order_status, lookup_transit_status]
