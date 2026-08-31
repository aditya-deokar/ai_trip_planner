# AI Trip Planner MCP Server Guide

This document describes how to use and integrate the **AI Trip Planner Model Context Protocol (MCP) Server**.

---

## 1. Overview

The AI Trip Planner application exposes its complete travel planning capabilities as an official **MCP Server** built on Python `mcp` 2.x (`MCPServer`).

Any MCP-compatible client (such as **Claude Desktop**, **Cursor**, **Antigravity IDE**, **VS Code Copilot**, or external agent swarms) can connect to this server and use both:
1. **Autonomous LangGraph Meta-Tools** (`plan_trip`, `refine_trip`)
2. **Atomic Travel Tools** (`get_weather`, `search_attractions`, `search_restaurants`, `search_activities`, `search_transportation`, `convert_currency`, `calculate_budget`)

---

## 2. Available Tools Reference

### 🚀 Autonomous Meta-Tools (Phase 3)

| Tool Name | Arguments | Description |
| :--- | :--- | :--- |
| **`plan_trip`** | `destination` (str)<br>`days` (int)<br>`budget` (str, opt)<br>`preferences` (str, opt)<br>`model_provider` (str, default: "google")<br>`model_name` (str, opt)<br>`session_id` (str, opt) | Autonomously executes the full LangGraph ReAct agent loop. Researches live weather, places, food, and exchange rates, outputting a complete day-by-day itinerary (morning/afternoon/evening), classic & off-beat routes, hotel estimates, and budget breakdown. Returns a `Session ID` for follow-ups. |
| **`refine_trip`** | `session_id` (str)<br>`modification_request` (str)<br>`model_provider` (str, opt)<br>`model_name` (str, opt) | Modifies or asks follow-up questions about an existing itinerary using LangGraph 1.2's `MemorySaver` checkpointer. Retains all previous conversation context. |

### 🛠️ Atomic Travel Domain Tools (Phase 2)

| Tool Name | Arguments | Description |
| :--- | :--- | :--- |
| **`get_weather`** | `city` (str)<br>`forecast` (bool, default: True) | Fetches current conditions and 5-day weather forecast for any destination. |
| **`search_attractions`** | `place` (str) | Searches top landmarks and tourist attractions (Google Places with Tavily fallback). |
| **`search_restaurants`** | `place` (str) | Searches top-rated dining spots, cafes, and eateries. |
| **`search_activities`** | `place` (str) | Finds outdoor, cultural, and adventure activities. |
| **`search_transportation`** | `place` (str) | Finds public transit, metro, and taxi options. |
| **`convert_currency`** | `amount` (float)<br>`from_currency` (str)<br>`to_currency` (str) | Converts travel expenses using live exchange rates. |
| **`calculate_budget`** | `price_per_night` (float)<br>`total_days` (int)<br>`estimated_daily_food_and_activities` (float)<br>`transit_cost` (float) | Calculates total accommodation, daily spending, transit, and grand total trip budget. |

---

## 3. Client Configuration

### Connecting from Claude Desktop
Open or create `%APPDATA%\Claude\claude_desktop_config.json` (on Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (on macOS) and add:

```json
{
  "mcpServers": {
    "ai-trip-planner": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner",
        "python",
        "-m",
        "mcp_server"
      ]
    }
  }
}
```

### Connecting from Cursor / Antigravity IDE
Add the following to your IDE MCP configuration (`mcp.json` or Custom MCP Server Settings):

```json
{
  "mcpServers": {
    "ai-trip-planner": {
      "command": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner\\.venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "mcp_server"
      ],
      "cwd": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner"
    }
  }
}
```

---

## 4. Running & Verifying Locally

You can test the MCP server directly via CLI:
```powershell
.venv\Scripts\python -m mcp_server
```

Or inspect tools programmatically:
```powershell
.venv\Scripts\python -c "import asyncio; from mcp_server.server import mcp; print(asyncio.run(mcp.list_tools()))"
```
