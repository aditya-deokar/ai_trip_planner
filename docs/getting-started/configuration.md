# Configuration

Configuration is split into:

- **Secrets** in `.env` (API keys)
- **Non-secret config** in [`config/config.yaml`](../reference/configuration-reference.md)

## 1) Create `.env`

Create a `.env` file in the repo root (same level as `main.py`).

Minimal set to run the default stack (Groq + Places + Weather + Currency + Tavily fallback):

```env
GROQ_API_KEY=...
GPLACES_API_KEY=...
OPENWEATHERMAP_API_KEY=...
EXCHANGE_RATE_API_KEY=...
TAVILY_API_KEY=...
```

If you want to use Google Gemini as the LLM provider:

```env
GOOGLE_API_KEY=...
```

For the canonical list, see [`../reference/environment-variables.md`](../reference/environment-variables.md).

## 2) Choose LLM provider

The backend currently selects the provider in code:

- `main.py` constructs `GraphBuilder(model_provider="groq")` by default.
- Supported values in `utils/model_loader.py`: `groq` and `google`.

See [`../reference/llm-providers.md`](../reference/llm-providers.md) for details.

## 3) Configure model names

Model names live in `config/config.yaml`:

- `llm.groq.model_name`
- `llm.google.model_name`

See [`../reference/configuration-reference.md`](../reference/configuration-reference.md).

