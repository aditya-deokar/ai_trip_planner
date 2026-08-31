"""
MCP Resources and Guided Prompt Templates for AI Trip Planner.
Phase 4 of the MCP Server integration.
"""
import json
from typing import Optional
from utils.config_loader import load_config
from mcp_server.tools_agent import _mcp_checkpointer

def get_system_status_resource() -> str:
    """
    Returns live metadata about the AI Trip Planner server, active models, and available tools.
    URI: trip://system/status
    """
    config = load_config()
    status_info = {
        "server_name": "AI Trip Planner MCP Server",
        "version": "1.0.0",
        "protocol": "Model Context Protocol (MCP) 2.x",
        "status": "online",
        "active_configuration": {
            "google_provider": {
                "default_model": config["llm"]["google"]["model_name"],
                "available_models": config["llm"]["google"].get("available_models", [])
            },
            "groq_provider": {
                "default_model": config["llm"]["groq"]["model_name"],
                "available_models": config["llm"]["groq"].get("available_models", [])
            }
        },
        "supported_capabilities": [
            "autonomous_trip_planning",
            "multi_turn_conversational_refinement",
            "weather_forecasts",
            "google_places_attractions_search",
            "restaurant_discovery",
            "live_currency_conversion",
            "travel_budget_calculation"
        ]
    }
    return json.dumps(status_info, indent=2)


def get_trip_itinerary_resource(session_id: str) -> str:
    """
    Retrieves stored trip plan messages and itinerary history for an active session thread.
    URI: trip://itinerary/{session_id}
    """
    try:
        config = {"configurable": {"thread_id": session_id}}
        checkpoint = _mcp_checkpointer.get(config)
        if not checkpoint:
            return f"No trip history found for session ID: '{session_id}'."
        
        channel_values = checkpoint.get("channel_values", {})
        messages = channel_values.get("messages", [])
        
        if not messages:
            return f"Session '{session_id}' exists but contains no messages."

        rendered = [f"# Stored Trip Itinerary for Session: {session_id}\n"]
        for i, msg in enumerate(messages):
            role = getattr(msg, "type", "message")
            content = getattr(msg, "content", str(msg))
            if content:
                rendered.append(f"### Turn {i + 1} ({role.title()}):\n{content}\n")
                
        return "\n".join(rendered)
    except Exception as e:
        return f"Error retrieving itinerary for session '{session_id}': {str(e)}"


# -------------------------------------------------------------
# Guided Prompt Templates
# -------------------------------------------------------------
def prompt_plan_vacation(
    destination: str,
    days: int,
    budget_level: str = "moderate",
    traveler_type: str = "couple or solo",
    interests: str = "food, culture, sightseeing"
) -> str:
    """
    Prompt template to initiate a structured travel planning session.
    """
    return (
        f"You are an expert AI Travel Concierge. Please plan a comprehensive {days}-day vacation to {destination}.\n\n"
        f"Key Traveler Context:\n"
        f"- Target Destination: {destination}\n"
        f"- Duration: {days} days\n"
        f"- Budget Style: {budget_level}\n"
        f"- Traveling Party: {traveler_type}\n"
        f"- Top Interests: {interests}\n\n"
        f"Requirements:\n"
        f"1. Use the `get_weather` tool to check destination climate and pack appropriately.\n"
        f"2. Use `search_attractions` and `search_restaurants` to uncover both major highlights and hidden gems.\n"
        f"3. Use `calculate_budget` and `convert_currency` to compute realistic hotel and daily spending.\n"
        f"4. Provide a day-by-day morning, afternoon, and evening itinerary.\n"
    )


def prompt_budget_breakdown(
    destination: str,
    days: int,
    home_currency: str = "USD",
    local_currency: str = "EUR"
) -> str:
    """
    Prompt template to calculate and analyze estimated travel costs with currency conversion.
    """
    return (
        f"Please analyze estimated travel costs for a {days}-day trip to {destination}.\n\n"
        f"Financial Requirements:\n"
        f"1. Estimate realistic lodging cost per night and total hotel costs for {days - 1} nights.\n"
        f"2. Estimate daily food, sightseeing, and local transportation expenses in {local_currency}.\n"
        f"3. Use the `convert_currency` tool to convert costs between {home_currency} and {local_currency}.\n"
        f"4. Provide a contingency/buffer recommendation of 10-15%.\n"
    )
