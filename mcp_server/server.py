"""
Main MCP Server definition for AI Trip Planner.
Registers Phase 2 Atomic Tools and Phase 3 Autonomous Meta-Tools.
"""
from mcp.server.mcpserver import MCPServer
from mcp_server.tools_atomic import (
    get_destination_weather,
    search_destination_attractions,
    search_destination_restaurants,
    search_destination_activities,
    search_destination_transportation,
    convert_travel_currency,
    calculate_trip_budget,
)
from mcp_server.tools_agent import (
    plan_complete_trip,
    refine_trip_plan,
)
from mcp_server.resources import (
    get_system_status_resource,
    get_trip_itinerary_resource,
    prompt_plan_vacation,
    prompt_budget_breakdown,
)

# Initialize MCP Server
mcp = MCPServer("AI Trip Planner Server")

# -------------------------------------------------------------
# Phase 4: MCP Resources
# -------------------------------------------------------------
@mcp.resource("trip://system/status")
def system_status() -> str:
    """Live status, active LLM models, and travel capabilities of the AI Trip Planner."""
    return get_system_status_resource()


@mcp.resource("trip://itinerary/{session_id}")
def trip_itinerary(session_id: str) -> str:
    """Stored conversation messages and generated itinerary for an active trip session."""
    return get_trip_itinerary_resource(session_id=session_id)


# -------------------------------------------------------------
# Phase 4: MCP Prompt Templates
# -------------------------------------------------------------
@mcp.prompt()
def plan_vacation(
    destination: str,
    days: int,
    budget_level: str = "moderate",
    traveler_type: str = "couple or solo",
    interests: str = "food, culture, sightseeing"
) -> str:
    """Pre-configured prompt template to initiate a thorough vacation planning workflow."""
    return prompt_plan_vacation(
        destination=destination,
        days=days,
        budget_level=budget_level,
        traveler_type=traveler_type,
        interests=interests
    )


@mcp.prompt()
def trip_budget(
    destination: str,
    days: int,
    home_currency: str = "USD",
    local_currency: str = "EUR"
) -> str:
    """Pre-configured prompt template for travel cost estimation and currency conversion."""
    return prompt_budget_breakdown(
        destination=destination,
        days=days,
        home_currency=home_currency,
        local_currency=local_currency
    )


# -------------------------------------------------------------
# Phase 3: Autonomous LangGraph Meta-Tools
# -------------------------------------------------------------
@mcp.tool()
def plan_trip(
    destination: str,
    days: int,
    budget: str = "",
    preferences: str = "",
    model_provider: str = "google",
    model_name: str = "",
    session_id: str = ""
) -> str:
    """
    Generate a complete, personalized multi-day travel itinerary using an autonomous AI agent.
    
    Researches weather, sights, restaurants, and foreign exchange in real-time,
    producing morning/afternoon/evening schedules, dual classic & off-beat plans,
    hotel recommendations, and an itemized budget.
    """
    return plan_complete_trip(
        destination=destination,
        days=days,
        budget=budget or None,
        preferences=preferences or None,
        model_provider=model_provider,
        model_name=model_name or None,
        session_id=session_id or None
    )


@mcp.tool()
def refine_trip(
    session_id: str,
    modification_request: str,
    model_provider: str = "google",
    model_name: str = ""
) -> str:
    """
    Conversationally modify or ask follow-ups about an existing trip itinerary without losing prior context.
    
    Requires the session_id returned from a previous plan_trip call.
    """
    return refine_trip_plan(
        session_id=session_id,
        modification_request=modification_request,
        model_provider=model_provider,
        model_name=model_name or None
    )


# -------------------------------------------------------------
# Phase 2: Atomic Domain Tools
# -------------------------------------------------------------
@mcp.tool()
def get_weather(city: str, forecast: bool = True) -> str:
    """Get current weather conditions and 5-day forecast for any travel destination."""
    return get_destination_weather(city=city, forecast=forecast)


@mcp.tool()
def search_attractions(place: str) -> str:
    """Search top tourist attractions and must-visit landmarks for a destination."""
    return search_destination_attractions(place=place)


@mcp.tool()
def search_restaurants(place: str) -> str:
    """Search top-rated restaurants, eateries, cafes, and food spots for a destination."""
    return search_destination_restaurants(place=place)


@mcp.tool()
def search_activities(place: str) -> str:
    """Search popular activities, sightseeing spots, and adventure tours for a destination."""
    return search_destination_activities(place=place)


@mcp.tool()
def search_transportation(place: str) -> str:
    """Search public transit, taxis, metro, and transportation modes for a destination."""
    return search_destination_transportation(place=place)


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert travel expenses from one currency to another using live FX rates."""
    return convert_travel_currency(amount=amount, from_currency=from_currency, to_currency=to_currency)


@mcp.tool()
def calculate_budget(
    price_per_night: float,
    total_days: int,
    estimated_daily_food_and_activities: float = 0.0,
    transit_cost: float = 0.0
) -> str:
    """Calculate total accommodation cost, daily allowances, transit, and grand total travel budget."""
    return calculate_trip_budget(
        price_per_night=price_per_night,
        total_days=total_days,
        estimated_daily_food_and_activities=estimated_daily_food_and_activities,
        transit_cost=transit_cost
    )
