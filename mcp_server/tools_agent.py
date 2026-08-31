"""
Autonomous LangGraph Meta-Tools for MCP Server.
Exposes full itinerary generation and multi-turn trip refinement with persistent checkpointer.
"""
from typing import Optional, Dict
import uuid
from agent.agentic_workflow import GraphBuilder
from langgraph.checkpoint.memory import MemorySaver

# Persistent checkpointer for MCP server sessions
_mcp_checkpointer = MemorySaver()
_graph_cache: Dict[str, any] = {}

def _get_mcp_graph(model_provider: str = "google", model_name: Optional[str] = None):
    cache_key = f"{model_provider}:{model_name or 'default'}"
    if cache_key not in _graph_cache:
        builder = GraphBuilder(
            model_provider=model_provider,
            model_name=model_name,
            checkpointer=_mcp_checkpointer
        )
        _graph_cache[cache_key] = builder.build_graph()
    return _graph_cache[cache_key]


def plan_complete_trip(
    destination: str,
    days: int,
    budget: Optional[str] = None,
    preferences: Optional[str] = None,
    model_provider: str = "google",
    model_name: Optional[str] = None,
    session_id: Optional[str] = None
) -> str:
    """
    Generate a complete, comprehensive travel plan using the autonomous LangGraph ReAct agent.

    The agent autonomously researches live weather, attractions, restaurants, and foreign exchange,
    producing:
      1. Day-by-day morning/afternoon/evening schedule
      2. Dual itinerary (classic highlights + off-beat hidden gems)
      3. Hotel & dining suggestions with pricing
      4. Complete currency-converted budget breakdown

    Args:
        destination: Destination city or region (e.g. "Tokyo", "Barcelona", "Goa").
        days: Number of days for the trip (e.g. 3, 5, 7).
        budget: Optional budget guideline (e.g. "luxury", "budget under $1500", "₹50,000 total").
        preferences: Optional traveler interests or constraints (e.g. "foodie, anime, walking", "family with toddlers").
        model_provider: LLM provider ("google" or "groq"). Defaults to "google".
        model_name: Specific model (e.g. "gemini-2.5-flash", "gemini-3.6-flash", "llama-3.3-70b-versatile").
        session_id: Optional session identifier. If omitted, a new session ID is generated and returned.

    Returns:
        A detailed Markdown travel itinerary followed by the Session ID for follow-up refinements.
    """
    thread_id = session_id or f"mcp-trip-{uuid.uuid4().hex[:8]}"

    # Construct the user prompt
    prompt_parts = [f"Plan a detailed {days}-day trip to {destination}."]
    if budget:
        prompt_parts.append(f"Budget: {budget}.")
    if preferences:
        prompt_parts.append(f"Traveler preferences/style: {preferences}.")
    prompt_parts.append(
        "Please provide a complete day-by-day schedule (morning, afternoon, evening), "
        "both classic and off-beat recommendations, hotel/food estimates, weather details, and total budget."
    )
    user_prompt = " ".join(prompt_parts)

    try:
        graph = _get_mcp_graph(model_provider=model_provider, model_name=model_name)
        config = {"configurable": {"thread_id": thread_id}}
        
        output = graph.invoke({"messages": [user_prompt]}, config=config)

        if isinstance(output, dict) and "messages" in output:
            final_answer = output["messages"][-1].content
        else:
            final_answer = str(output)

        return (
            f"{final_answer}\n\n"
            f"---\n"
            f"**Session ID:** `{thread_id}`  \n"
            f"*Tip: Use `refine_trip_plan(session_id='{thread_id}', modification_request='...')` to adjust this plan.*"
        )
    except Exception as e:
        return f"Error executing autonomous trip planner agent: {str(e)}"


def refine_trip_plan(
    session_id: str,
    modification_request: str,
    model_provider: str = "google",
    model_name: Optional[str] = None
) -> str:
    """
    Modify, adjust, or ask follow-up questions about an existing trip itinerary using multi-turn conversational memory.

    Args:
        session_id: The session ID returned from a prior `plan_complete_trip` call (e.g. "mcp-trip-a1b2c3d4").
        modification_request: Specific change or follow-up question (e.g. "Make Day 2 kid-friendly", "Switch hotel to budget hostel", "What is the best afternoon museum on Day 3?").
        model_provider: LLM provider ("google" or "groq"). Defaults to "google".
        model_name: Specific model to use.

    Returns:
        The updated itinerary adjustments or answers from the agent retaining full prior context.
    """
    try:
        graph = _get_mcp_graph(model_provider=model_provider, model_name=model_name)
        config = {"configurable": {"thread_id": session_id}}

        output = graph.invoke({"messages": [modification_request]}, config=config)

        if isinstance(output, dict) and "messages" in output:
            final_answer = output["messages"][-1].content
        else:
            final_answer = str(output)

        return (
            f"{final_answer}\n\n"
            f"---\n"
            f"**Session ID:** `{session_id}`"
        )
    except Exception as e:
        return f"Error refining trip plan for session '{session_id}': {str(e)}"
