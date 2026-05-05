<div align="center">

# 🌍 AI Trip Planner

### *Your Intelligent Travel Companion — Powered by Agentic AI*

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6%2B-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Plan smarter. Travel better. Experience the world — with AI as your co-pilot.**

[Features](#-features) · [Architecture](#-architecture) · [Getting Started](#-getting-started) · [API Reference](#-api-reference) · [Contributing](#-contributing)

---

</div>

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [API Reference](#-api-reference)
- [Agentic Tools](#-agentic-tools)
- [LLM Configuration](#-llm-configuration)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌐 Overview

**AI Trip Planner** is a production-grade, agentic AI application that acts as your personal travel assistant. Powered by a **ReAct (Reasoning + Acting) agent** built with **LangGraph**, it autonomously gathers real-time data from multiple APIs and synthesizes a comprehensive, personalized travel itinerary — all in one conversational interaction.

Whether you're dreaming of the Taj Mahal's grandeur or a hidden beach in Goa, the agent fetches live weather, discovers local attractions, calculates expenses in your home currency, and delivers **two complete travel plans** — one for classic tourist routes and one for off-beat hidden gems.

> *"Don't just search for your next trip. Let AI plan it for you."*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Agentic AI Workflow** | ReAct agent with LangGraph orchestrates multi-step reasoning and tool use autonomously |
| 🗓️ **Day-by-Day Itinerary** | Fully detailed daily plans covering morning, afternoon, and evening activities |
| 🏨 **Hotel Recommendations** | Curated boarding options with approximate per-night pricing |
| 🍽️ **Restaurant Discovery** | Top restaurants with cuisine types and price ranges |
| 🗺️ **Attractions & Activities** | Tourist highlights and adventure activities with full details |
| 🚌 **Transportation Guide** | Available transport modes, routes, and estimated costs |
| 💱 **Live Currency Conversion** | Real-time exchange rates for accurate budget planning in your currency |
| 🌤️ **Weather Intelligence** | Current conditions and multi-day forecast for your destination |
| 💰 **Expense Breakdown** | Detailed cost analysis with daily budget estimates |
| 🗺️ **Dual Itinerary Mode** | One plan for mainstream tourism, one for off-beat exploration |
| 🔀 **Multi-LLM Support** | Switch between Groq (DeepSeek-R1) and Google Gemini 2.5 Pro |
| 🔄 **Fallback Search** | Tavily web search as intelligent fallback when Google Places API fails |

---

## 🏗️ Architecture

The application follows a **microservices-inspired** design with a decoupled backend (FastAPI) and frontend (Streamlit), connected via a REST API.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI (Port 8501)                 │
│                    User enters travel query                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │  HTTP POST /query
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend (Port 8000)                  │
│                    Receives & validates request                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph ReAct Agent                         │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │  START   │───▶│  AGENT   │───▶│  TOOLS   │                  │
│  └──────────┘    │  (LLM)   │◀───│  NODE    │                  │
│                  └────┬─────┘    └──────────┘                  │
│                       │                                         │
│                  ┌────▼─────┐                                   │
│                  │   END    │                                   │
│                  └──────────┘                                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │  Tool Calls
          ┌───────────────┼───────────────┐──────────────────┐
          ▼               ▼               ▼                  ▼
  ┌──────────────┐ ┌───────────┐ ┌──────────────┐ ┌───────────────┐
  │ Google Places│ │OpenWeather│ │ Exchange Rate │ │    Tavily     │
  │     API      │ │    API    │ │     API      │ │  Search API   │
  └──────────────┘ └───────────┘ └──────────────┘ └───────────────┘
```

### Agent Decision Flow

The **LangGraph StateGraph** implements a cyclical ReAct loop:

1. **Agent Node** — The LLM receives the user query + system prompt and decides which tools to call
2. **Tools Node** — Selected tools execute in parallel, fetching real-time data
3. **Conditional Edge** — If more tool calls are needed, loops back to the Agent; otherwise routes to END
4. **Final Response** — Comprehensive Markdown-formatted travel plan returned to the user

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance async REST API |
| **Frontend** | [Streamlit](https://streamlit.io/) | Rapid AI/ML application UI |
| **AI Orchestration** | [LangGraph](https://langchain-ai.github.io/langgraph/) | Stateful agentic workflow |
| **LLM Framework** | [LangChain](https://python.langchain.com/) | LLM abstractions and tool integrations |
| **Primary LLM** | [Groq — DeepSeek-R1-Distill-LLaMA-70B](https://groq.com/) | Ultra-fast inference |
| **Secondary LLM** | [Google Gemini 2.5 Pro](https://ai.google.dev/) | Advanced multimodal reasoning |
| **Place Search** | [Google Places API](https://developers.google.com/maps/documentation/places/web-service) | Attractions, restaurants, transport |
| **Fallback Search** | [Tavily Search API](https://tavily.com/) | Web search fallback for places |
| **Weather** | [OpenWeatherMap API](https://openweathermap.org/api) | Current & forecast weather data |
| **Currency** | [Exchange Rate API](https://www.exchangerate-api.com/) | Real-time currency conversion |
| **Package Manager** | [uv](https://docs.astral.sh/uv/) | Fast Python dependency management |
| **Server** | [Uvicorn](https://www.uvicorn.org/) | ASGI server for FastAPI |

---

## 📁 Project Structure

```
ai_trip_planner/
│
├── 📂 agent/
│   ├── __init__.py
│   └── agentic_workflow.py      # LangGraph ReAct agent & GraphBuilder
│
├── 📂 config/
│   └── config.yaml              # LLM provider & model configuration
│
├── 📂 exception/
│   └── exceptions.py            # Custom exception classes
│
├── 📂 logger/
│   └── logger.py                # Centralized logging setup
│
├── 📂 notebook/                 # Jupyter notebooks for experimentation
│
├── 📂 prompt_library/
│   ├── __init__.py
│   └── prompt.py                # System prompt for the travel agent
│
├── 📂 tools/
│   ├── __init__.py
│   ├── currency_conversion_tool.py   # Currency conversion via Exchange Rate API
│   ├── expense_calculator_tool.py    # Trip cost calculator
│   ├── place_search_tool.py          # Google Places + Tavily search
│   └── weather_info_tool.py          # OpenWeatherMap current & forecast
│
├── 📂 utils/
│   ├── __init__.py
│   ├── calculator.py            # Arithmetic helper for cost calculations
│   ├── config_loader.py         # YAML config loader utility
│   ├── currency_convertor.py    # Currency conversion API wrapper
│   ├── model_loader.py          # LLM factory (Groq / Google Gemini)
│   ├── place_info_search.py     # Google Places & Tavily API wrappers
│   ├── save_to_document.py      # Export travel plan to document
│   └── weather_info.py          # OpenWeatherMap API wrapper
│
├── main.py                      # FastAPI application entry point
├── streamlit_app.py             # Streamlit frontend application
├── pyproject.toml               # Project metadata & dependencies (uv)
├── requirements.txt             # pip-compatible dependency list
├── my_graph.png                 # LangGraph agent visualization (auto-generated)
└── .env                         # Environment variables (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.12+** — [Download](https://www.python.org/downloads/)
- **uv** (recommended) — [Install uv](https://docs.astral.sh/uv/getting-started/installation/) or use `pip`
- API keys (see [Environment Variables](#environment-variables))

### Installation

#### Option 1: Using `uv` (Recommended)

```bash
# Clone the repository
git clone https://github.com/aditya-deokar/ai_trip_planner.git
cd ai_trip_planner

# Create virtual environment and install dependencies
uv sync
```

#### Option 2: Using `pip`

```bash
# Clone the repository
git clone https://github.com/aditya-deokar/ai_trip_planner.git
cd ai_trip_planner

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# ─── LLM Providers ────────────────────────────────────────
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# ─── Place & Search APIs ──────────────────────────────────
GPLACES_API_KEY=your_google_places_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# ─── Weather API ──────────────────────────────────────────
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here

# ─── Currency API ─────────────────────────────────────────
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key_here
```

> **Where to get the keys:**
>
> | Key | Provider | Link |
> |---|---|---|
> | `GROQ_API_KEY` | Groq Cloud | [console.groq.com](https://console.groq.com) |
> | `GOOGLE_API_KEY` | Google AI Studio | [aistudio.google.com](https://aistudio.google.com) |
> | `GPLACES_API_KEY` | Google Cloud Console | [console.cloud.google.com](https://console.cloud.google.com) |
> | `TAVILY_API_KEY` | Tavily | [tavily.com](https://tavily.com) |
> | `OPENWEATHERMAP_API_KEY` | OpenWeatherMap | [openweathermap.org](https://openweathermap.org/api) |
> | `EXCHANGE_RATE_API_KEY` | ExchangeRate-API | [exchangerate-api.com](https://www.exchangerate-api.com) |

### Running the Application

The app has two components that must both be running:

#### Step 1 — Start the FastAPI Backend

```bash
# Using uv
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Using pip/venv
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be live at: **`http://localhost:8000`**

Interactive API docs: **`http://localhost:8000/docs`**

#### Step 2 — Launch the Streamlit Frontend

Open a **new terminal** and run:

```bash
# Using uv
uv run streamlit run streamlit_app.py

# Using pip/venv
streamlit run streamlit_app.py
```

The frontend will open automatically in your browser at: **`http://localhost:8501`**

#### Example Queries to Try

```
Plan a 5-day trip to Goa for a couple in April
I want to visit Tokyo for 7 days with a budget of $2000
Suggest a weekend getaway from Mumbai
Plan a solo backpacking trip to Rajasthan for 10 days
```

---

## 📡 API Reference

### `POST /query`

Execute a travel planning query through the AI agent.

**Request Body**

```json
{
  "question": "Plan a 5-day trip to Goa for 2 people in December"
}
```

**Success Response** `200 OK`

```json
{
  "answer": "# 🌍 Complete 5-Day Goa Travel Plan\n\n## Day 1: Arrival & North Goa Beaches\n..."
}
```

**Error Response** `500 Internal Server Error`

```json
{
  "error": "Description of what went wrong"
}
```

**cURL Example**

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Plan a 3-day trip to Manali in winter"}'
```

**Python Example**

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": "Plan a 7-day trip to Europe covering Paris and Rome"}
)
print(response.json()["answer"])
```

---

## 🔧 Agentic Tools

The LangGraph agent has access to **9 specialized tools** that it autonomously selects and calls:

### 🌤️ Weather Tools
| Tool | Description |
|---|---|
| `get_current_weather` | Fetches real-time temperature and weather description for any city |
| `get_weather_forecast` | Retrieves multi-day forecast with daily temperature and conditions |

### 🗺️ Place Search Tools
| Tool | Description |
|---|---|
| `search_attractions` | Discovers tourist attractions via Google Places (Tavily fallback) |
| `search_restaurants` | Finds top restaurants with details via Google Places (Tavily fallback) |
| `search_activities` | Lists activities and experiences available in and around a location |
| `search_transportation` | Identifies transport modes available at the destination |

### 💰 Expense Tools
| Tool | Description |
|---|---|
| `estimate_total_hotel_cost` | Calculates total accommodation cost (price/night × days) |
| `calculate_total_expense` | Sums all individual trip expenses |
| `calculate_daily_expense_budget` | Computes daily budget from total cost and trip duration |

### 💱 Currency Tool
| Tool | Description |
|---|---|
| `convert_currency` | Converts amounts between any two currencies using live exchange rates |

---

## ⚙️ LLM Configuration

Model configuration is managed in `config/config.yaml`. Switch providers to change the underlying LLM:

```yaml
llm:
  groq:
    provider: "groq"
    model_name: "deepseek-r1-distill-llama-70b"   # Ultra-fast inference

  google:
    provider: "google"
    model_name: "gemini-2.5-pro"                  # Advanced reasoning
```

To change the active provider, update the `model_provider` parameter in `main.py`:

```python
# main.py
graph = GraphBuilder(model_provider="groq")    # Use Groq (default)
graph = GraphBuilder(model_provider="google")  # Use Google Gemini
```

---

## 📸 Screenshots

### Streamlit Chat Interface
The conversational interface makes trip planning feel natural and intuitive.

```
┌─────────────────────────────────────────────────┐
│  🌍 Travel Planner Agentic Application          │
│─────────────────────────────────────────────────│
│  How can I help you in planning a trip?         │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ e.g. Plan a trip to Goa for 5 days  🔍 │   │
│  └─────────────────────────────────────────┘   │
│                          [ Send ]              │
│                                                 │
│  ✈️  AI is thinking...                          │
│                                                 │
│  # 🌍 AI Travel Plan                           │
│  **Day 1**: Arrival at Dabolim Airport...       │
└─────────────────────────────────────────────────┘
```

### Agent Graph Visualization
The LangGraph agent topology is auto-saved as `my_graph.png` on each run, showing the full decision flow of the ReAct agent.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes with a clear message
   ```bash
   git commit -m "feat: add hotel booking tool integration"
   ```
4. **Push** your branch
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open** a Pull Request with a clear description of your changes

### Ideas for Contribution

- 🏨 Hotel booking API integration (Booking.com, Expedia)
- ✈️ Flight search tool (Skyscanner, Google Flights)
- 🗺️ Interactive map generation with plotted itinerary
- 💬 Chat history / multi-turn conversation support
- 🌐 Multi-language output support
- 📄 PDF export of travel plans
- 🔒 User authentication & saved trips
- 🐳 Docker containerization

---

## 📋 Environment Setup Reference

### Quick `.env` Template

Copy this template and fill in your API keys:

```bash
cp .env.example .env   # (if .env.example exists)
# or manually create .env with the keys listed above
```

### Python Version

This project requires **Python 3.12+**. The `.python-version` file pins the exact version for `pyenv` and `uv` users.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Aditya Deokar**

- GitHub: [@aditya-deokar](https://github.com/aditya-deokar)

---

<div align="center">

**⭐ If this project helped you plan an amazing trip, give it a star!**

*Built with ❤️ using LangGraph, FastAPI & Streamlit*

</div>
