# AI Trip Planner docs

AI Trip Planner is an **agentic travel planning app** built with **Streamlit** (UI), **FastAPI** (backend), and a **LangGraph ReAct agent** (reasoning + tool use). It generates a complete trip plan in one response by fetching live data (weather, places, currency rates) and calculating budgets.

## Quick links

- **Install**: [`getting-started/installation.md`](getting-started/installation.md)
- **Configure keys**: [`getting-started/configuration.md`](getting-started/configuration.md)
- **Run locally**: [`getting-started/running-locally.md`](getting-started/running-locally.md)
- **Use API**: [`user-guide/using-the-api.md`](user-guide/using-the-api.md)
- **How it works**: [`architecture/system-overview.md`](architecture/system-overview.md)
- **Contribute**: [`development/contributing.md`](development/contributing.md)

## What this project does

- Creates a **day-by-day itinerary** (morning/afternoon/evening).
- Provides **two plans**: classic tourist route + off-beat/hidden gems (as instructed by the system prompt).
- Recommends **hotels**, **restaurants**, **attractions**, **activities**, and **transport options**.
- Adds **weather details**, **currency conversion**, and a **cost breakdown** with **daily budget** estimates.

## When to use it

- You want a travel plan that combines **real-time signals** (APIs/search) and **structured reasoning** (agent workflow).
- You want a reference implementation of **LangGraph tools + loop** wired into a small app (FastAPI + Streamlit).

## Where to go next

- New to the repo? Start with [`getting-started/overview.md`](getting-started/overview.md).
- Want the technical deep dive? Read [`architecture/agentic-workflow.md`](architecture/agentic-workflow.md).

