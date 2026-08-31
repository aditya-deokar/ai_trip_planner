# AI Trip Planner MCP Server: Complete Technical Reference

**Specification:** Model Context Protocol (MCP) 2025/2026 Standard  
**SDK:** Python `mcp` >= 2.1.1 (`MCPServer`)  
**Repository Module:** `mcp_server/`  
**Supported Transports:** `stdio` (Desktop AI IDEs) & `SSE` (Network / Remote Clients)  

---

## 1. Architecture Overview

The **AI Trip Planner MCP Server** provides native integration between the AI Trip Planner's agentic workflow and external AI clients such as **Claude Desktop**, **Cursor IDE**, **Antigravity IDE**, **VS Code Copilot**, and distributed multi-agent systems.

Rather than only providing an isolated chatbot UI, this server turns the application into an **open, callable travel capability layer**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MCP Client Applications                          │
│         Claude Desktop  │  Cursor IDE  │  Antigravity  │  Agent Swarms      │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │ stdio transport               │ SSE / HTTP transport
                       ▼                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                  AI Trip Planner MCP Server (mcp_server/)                   │
│                                                                             │
│  ┌─────────────────────────────────┐   ┌─────────────────────────────────┐  │
│  │   Autonomous Meta-Tools         │   │   Atomic Domain Tools           │  │
│  │   - plan_trip                   │   │   - get_weather                 │  │
│  │   - refine_trip                 │   │   - search_attractions          │  │
│  │                                 │   │   - search_restaurants          │  │
│  ├─────────────────────────────────┤   │   - search_activities           │  │
│  │   Dynamic Resources             │   │   - search_transportation       │  │
│  │   - trip://system/status        │   │   - convert_currency            │  │
│  │   - trip://itinerary/{id}       │   │   - calculate_budget            │  │
│  ├─────────────────────────────────┤   └─────────────────────────────────┘  │
│  │   Prompt Templates              │                                        │
│  │   - plan_vacation               │                                        │
│  │   - trip_budget                 │                                        │
│  └─────────────────────────────────┘                                        │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────────┐
│   LangGraph 1.2 Multi-Turn Engine     │ │   External Domain APIs            │
│   (agentic_workflow.py + MemorySaver) │ │   - OpenWeatherMap API            │
│   - Gemini 2.5 Flash / Pro            │ │   - Google Places (New) API       │
│   - Llama 3.3 / DeepSeek-R1 (Groq)    │ │   - ExchangeRate-API              │
│   - Session persistence via thread_id │ │   - Tavily Search (Fallback)      │
└───────────────────────────────────────┘ └───────────────────────────────────┘
```

---

## 2. Capability Reference

### 2.1 Autonomous Meta-Tools (Full Agent Execution)

These tools execute the complete cyclical ReAct agent workflow using LangGraph 1.2. The agent independently decides which tools to call, fetches real-time data, and synthesizes a complete travel plan.

#### 1. `plan_trip`
Generates a comprehensive, day-by-day travel plan from scratch.
- **Parameters:**
  - `destination` (*string, required*): Target city or region (e.g. `"Tokyo"`, `"Paris"`, `"Goa"`).
  - `days` (*integer, required*): Total duration of the trip (e.g. `3`, `5`, `7`).
  - `budget` (*string, optional*): Budget style or limit (e.g. `"moderate"`, `"budget under $1500"`, `"luxury"`).
  - `preferences` (*string, optional*): Interests, food restrictions, or traveler style (e.g. `"foodie, historical sites, walking"`, `"family with kids"`).
  - `model_provider` (*string, default: `"google"`*): LLM backend (`"google"` or `"groq"`).
  - `model_name` (*string, optional*): Model override (e.g. `"gemini-2.5-flash"`, `"gemini-3.6-flash"`, `"llama-3.3-70b-versatile"`).
  - `session_id` (*string, optional*): Custom session thread ID. If omitted, a unique `mcp-trip-xxxxxxxx` ID is generated.
- **Returns:** Full markdown itinerary (morning/afternoon/evening), classic vs off-beat routes, hotel options, weather forecast, and itemized budget. Returns the active `Session ID`.

#### 2. `refine_trip`
Conversationally adjusts or asks questions about an existing itinerary.
- **Parameters:**
  - `session_id` (*string, required*): The `Session ID` returned from a prior `plan_trip` call.
  - `modification_request` (*string, required*): Follow-up instruction (e.g. `"Make Day 2 kid-friendly"`, `"Suggest vegetarian restaurants for dinner on Day 3"`, `"Switch hotels to budget hostels"`).
  - `model_provider` (*string, default: `"google"`*): Provider to use.
  - `model_name` (*string, optional*): Model override.
- **Returns:** Updated travel recommendations retaining complete historical context via LangGraph's `MemorySaver`.

---

### 2.2 Atomic Travel Domain Tools

Clients can invoke these tools individually for specific, targeted travel queries without running the full itinerary agent:

| Tool | Parameters | Output | Description |
| :--- | :--- | :--- | :--- |
| **`get_weather`** | `city` (*str*), `forecast` (*bool, default: True*) | Text string | Returns current weather and 5-day forecast with daily temperatures and sky conditions. |
| **`search_attractions`** | `place` (*str*) | Text string | Discovers top sights and attractions using Google Places API (with Tavily fallback). |
| **`search_restaurants`** | `place` (*str*) | Text string | Discovers top-rated restaurants, cafes, and local cuisine spots. |
| **`search_activities`** | `place` (*str*) | Text string | Searches popular sightseeing, adventure, cultural, and outdoor activities. |
| **`search_transportation`** | `place` (*str*) | Text string | Discovers public transit, metro networks, and taxi options for a city. |
| **`convert_currency`** | `amount` (*float*), `from_currency` (*str*), `to_currency` (*str*) | Text string | Converts travel currency using live exchange rates (e.g. `100 USD = 8350.00 INR`). |
| **`calculate_budget`** | `price_per_night` (*float*), `total_days` (*int*), `estimated_daily_food_and_activities` (*float*), `transit_cost` (*float*) | Text string | Formats an itemized expense sheet with accommodation total, daily allowances, transit, grand total, and average daily cost. |

---

### 2.3 Dynamic MCP Resources

Resources allow LLM clients to directly read structured state and metadata using custom `trip://` URIs:

#### 1. `trip://system/status`
- **Description:** Exposes active server health, loaded providers, default models, and capability flags.
- **Response Format:** JSON document.
- **Example Data:**
  ```json
  {
    "server_name": "AI Trip Planner MCP Server",
    "version": "1.0.0",
    "protocol": "Model Context Protocol (MCP) 2.x",
    "status": "online",
    "active_configuration": {
      "google_provider": {
        "default_model": "gemini-2.5-flash",
        "available_models": ["gemini-2.5-flash", "gemini-3.6-flash", "gemini-2.5-pro"]
      },
      "groq_provider": {
        "default_model": "llama-3.3-70b-versatile",
        "available_models": ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b"]
      }
    }
  }
  ```

#### 2. `trip://itinerary/{session_id}`
- **Description:** Reads back the raw conversation messages and generated itinerary for any active session from memory.
- **Response Format:** Markdown text containing each turn's role and content.

---

### 2.4 Guided MCP Prompt Templates

Pre-configured prompt templates help users or client applications formulate high-quality travel queries:

1. **`plan_vacation`**:
   - **Arguments:** `destination`, `days`, `budget_level`, `traveler_type`, `interests`.
   - **Behavior:** Constructs a comprehensive instruction instructing the LLM to inspect destination weather, search attractions, estimate accommodation, and generate morning/afternoon/evening daily schedules.
2. **`trip_budget`**:
   - **Arguments:** `destination`, `days`, `home_currency`, `local_currency`.
   - **Behavior:** Guides the LLM to calculate accommodation, daily living costs, currency conversion, and recommended contingency buffers.

---

## 3. Transports & Deployment Modes

### Mode 1: Local Desktop IDEs (`stdio` Transport)

Desktop AI applications communicate with the MCP server over standard input/output streams.

**Command to launch:**
```powershell
.venv\Scripts\python -m mcp_server
```

#### Configuration for Claude Desktop
File path: `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):
```json
{
  "mcpServers": {
    "ai-trip-planner": {
      "command": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_server"],
      "cwd": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner"
    }
  }
}
```

#### Configuration for Cursor IDE
In `.cursor/mcp.json` or through **Cursor Settings** ➔ **Features** ➔ **MCP**:
```json
{
  "mcpServers": {
    "ai-trip-planner": {
      "command": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_server"],
      "cwd": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner"
    }
  }
}
```

---

### Mode 2: Network / Remote Clients (`SSE` Transport)

The MCP server is mounted directly into the FastAPI application under the `/mcp` route.

**Command to launch:**
```powershell
.venv\Scripts\uvicorn main:app --port 8000 --reload
```

- **SSE Stream Endpoint:** `http://localhost:8000/mcp/sse`
- **Messages Endpoint:** `http://localhost:8000/mcp/messages`

#### Remote Client Configuration:
```json
{
  "mcpServers": {
    "ai-trip-planner": {
      "url": "http://localhost:8000/mcp/sse"
    }
  }
}
```

---

## 4. Testing & Verification

### Programmatic Python Verification
```powershell
.venv\Scripts\python -c "
import asyncio
from mcp_server.server import mcp

async def test():
    tools = await mcp.list_tools()
    print('Tools:', [t.name for t in tools])
    resources = await mcp.list_resources()
    print('Resources:', [r.uri for r in resources])
    prompts = await mcp.list_prompts()
    print('Prompts:', [p.name for p in prompts])

asyncio.run(test())
"
```

### Testing with the Official MCP Inspector
Anthropic provides a visual browser-based testing tool:
```powershell
npx @modelcontextprotocol/inspector c:\Users\adity\Documents\langgraph\ai_trip_planner\.venv\Scripts\python.exe -m mcp_server
```
Navigate to `http://localhost:5173` to test tool calls, inspect payloads, and view live JSON-RPC exchanges.
