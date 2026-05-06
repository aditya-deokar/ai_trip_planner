# Developer setup

This guide is for contributors extending tools, prompts, or the backend/UI.

## Setup

Follow [`../getting-started/installation.md`](../getting-started/installation.md) and [`../getting-started/configuration.md`](../getting-started/configuration.md).

## Local workflow (recommended)

- Run backend with reload: `uvicorn main:app --reload`
- Run Streamlit separately: `streamlit run streamlit_app.py`
- Iterate on tools and prompt behavior, then validate via:
  - UI prompt
  - `POST /query` call

## Useful files while developing

- Agent graph: `agent/agentic_workflow.py`
- Prompt: `prompt_library/prompt.py`
- Tools: `tools/*`
- Tool wrappers: `utils/*`
- Config: `config/config.yaml`

