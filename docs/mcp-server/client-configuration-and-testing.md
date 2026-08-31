# MCP Client Configuration & Testing Guide (Phase 6)

This document provides production-ready configuration snippets and verification instructions for connecting AI clients (**Claude Desktop**, **Cursor IDE**, **Antigravity IDE**, and **VS Code Copilot**) to the **AI Trip Planner MCP Server**.

---

## 1. Supported Connection Transports

The AI Trip Planner MCP Server supports two transports:

| Transport | Connection Type | Best For | Endpoint / Command |
| :--- | :--- | :--- | :--- |
| **`stdio`** | Local Process (Standard Input/Output) | Claude Desktop, Cursor, Antigravity, local CLI | `.venv\Scripts\python.exe -m mcp_server` |
| **`SSE`** | Network HTTP / Server-Sent Events | Web clients, multi-agent swarms, remote servers | `http://localhost:8000/mcp/sse` |

---

## 2. Client Configurations

### 2.1 Claude Desktop

1. Locate your Claude Desktop configuration file:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the following entry under `mcpServers`:

```json
{
  "mcpServers": {
    "ai-trip-planner": {
      "command": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner\\.venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "mcp_server"
      ],
      "cwd": "c:\\Users\\adity\\Documents\\langgraph\\ai_trip_planner",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

3. Restart Claude Desktop. You will see a hammer icon 🔨 indicating that the **9 tools**, **resources**, and **prompts** are active.

---

### 2.2 Cursor IDE

1. Open **Settings** ➔ **Features** ➔ **MCP**.
2. Click **+ Add New MCP Server**.
3. Choose transport **`stdio`**:
   - **Name:** `ai-trip-planner`
   - **Command:** `c:\Users\adity\Documents\langgraph\ai_trip_planner\.venv\Scripts\python.exe -m mcp_server`
4. Or configure it directly in your project root `.cursor/mcp.json`:

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

### 2.3 Antigravity IDE

Add the server to your Antigravity IDE configuration at `~/.gemini/antigravity-ide/mcp_config.json`:

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

### 2.4 Remote / Network SSE Connection (FastAPI Mount)

When running the FastAPI server:
```powershell
.venv\Scripts\uvicorn main:app --port 8000 --reload
```

Remote clients can connect directly over HTTP SSE:
- **SSE URL:** `http://localhost:8000/mcp/sse`
- **Messages URL:** `http://localhost:8000/mcp/messages`

Client configuration using SSE:
```json
{
  "mcpServers": {
    "ai-trip-planner-remote": {
      "url": "http://localhost:8000/mcp/sse"
    }
  }
}
```

---

## 3. Available MCP Capabilities Summary

### 🛠️ Tools (9 Tools)
1. `plan_trip`: Autonomously designs full morning/afternoon/evening travel plans.
2. `refine_trip`: Multi-turn conversational modification retaining context.
3. `get_weather`: Live conditions + 5-day forecast.
4. `search_attractions`: Tourist landmarks & highlights.
5. `search_restaurants`: Curated dining spots.
6. `search_activities`: Outdoor and cultural tours.
7. `search_transportation`: Local transit options.
8. `convert_currency`: Foreign exchange conversions.
9. `calculate_budget`: Itemized hotel and daily budgets.

### 📦 Resources (2 URIs)
1. `trip://system/status`: Server metadata and active model configurations.
2. `trip://itinerary/{session_id}`: Retrieves stored plan history for an active session.

### 📝 Prompts (2 Templates)
1. `plan_vacation`: Guided vacation planning workflow template.
2. `trip_budget`: Financial analysis & currency conversion template.

---

## 4. End-to-End Verification with MCP Inspector

You can visually test and inspect all tools using Anthropic's official MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector c:\Users\adity\Documents\langgraph\ai_trip_planner\.venv\Scripts\python.exe -m mcp_server
```

This opens a browser testing UI at `http://localhost:5173` where you can execute any tool, inspect JSON-RPC payloads, and read resources interactively.
