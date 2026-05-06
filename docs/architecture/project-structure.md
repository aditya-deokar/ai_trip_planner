# Project structure

This is a curated guide to “where to change what”.

## Top-level

- `main.py`: FastAPI backend (API surface)
- `streamlit_app.py`: Streamlit frontend (UI)
- `config/config.yaml`: non-secret configuration (model names)
- `.env` (local only): API keys and secrets

## Agent

- `agent/agentic_workflow.py`: LangGraph graph builder and ReAct loop
- `prompt_library/prompt.py`: `SYSTEM_PROMPT` that defines expected output sections and behavior

## Tools and integrations

- `tools/`: LangChain tool definitions exposed to the agent
  - `place_search_tool.py`: Google Places + Tavily fallback
  - `weather_info_tool.py`: OpenWeatherMap tools
  - `currency_conversion_tool.py`: ExchangeRate-API tool
  - `expense_calculator_tool.py`: expense calculators
- `utils/`: wrappers/helpers used by tools
  - `place_info_search.py`, `weather_info.py`, `currency_convertor.py`, `calculator.py`
  - `model_loader.py`: LLM provider selection and instantiation
  - `config_loader.py`: loads `config/config.yaml`

## Where to extend

- Add a new tool: implement a module in `tools/` and add it to `GraphBuilder.tools` in `agent/agentic_workflow.py`.
- Change output behavior: update `SYSTEM_PROMPT` in `prompt_library/prompt.py`.
- Add a new model/provider: extend `utils/model_loader.py` and update `config/config.yaml` + docs.

