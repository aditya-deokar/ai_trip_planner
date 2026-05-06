# ADR 0001: FastAPI + Streamlit + LangGraph architecture

## Status

Accepted

## Context

The project needs:

- a simple UI for interactive travel planning
- an API layer suitable for integration and future deployment
- an agent orchestration layer that can reliably loop between reasoning and tool calls

## Decision

We use:

- **Streamlit** for the UI (`streamlit_app.py`)
- **FastAPI** for the backend API (`main.py`)
- **LangGraph** to orchestrate a ReAct-style loop with tool usage (`agent/agentic_workflow.py`)

Tool integrations live behind LangChain `@tool` wrappers in `tools/*`, with API wrappers in `utils/*`.

## Consequences

### Positive

- Easy local development (two processes, simple ports)
- Clear separation: UI ↔ API ↔ agent workflow
- Tools are modular and extensible

### Negative / trade-offs

- Two-process deployment adds operational overhead
- LLM output variability makes strict testing harder
- External APIs introduce quota/rate-limit failure modes

### Follow-ups

- Add retries/timeouts for external API calls and LLM calls if productionizing
- Add structured logging + request IDs for better observability

