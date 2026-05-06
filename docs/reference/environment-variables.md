# Environment variables

This project uses environment variables for secrets (API keys). Most are loaded via `python-dotenv` (see `load_dotenv()` usage in `main.py` and `tools/*`).

## Required (typical local run)

### LLM provider

- `GROQ_API_KEY`: required when using Groq (`model_provider="groq"`)
- `GOOGLE_API_KEY`: required when using Google Gemini (`model_provider="google"`)

### Places/search

- `GPLACES_API_KEY`: required for Google Places tool usage
- `TAVILY_API_KEY`: required for Tavily fallback search (used by `langchain_tavily`)

### Weather

- `OPENWEATHERMAP_API_KEY`: required to call OpenWeatherMap endpoints

### Currency

- `EXCHANGE_RATE_API_KEY`: required to call ExchangeRate-API

## Recommended `.env` template

```env
# LLM providers
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_ai_key

# Places & search
GPLACES_API_KEY=your_google_places_key
TAVILY_API_KEY=your_tavily_key

# Weather
OPENWEATHERMAP_API_KEY=your_openweather_key

# Currency
EXCHANGE_RATE_API_KEY=your_exchange_rate_key
```

## Notes

- Do **not** commit `.env`.
- If you see runtime failures calling tools, the first thing to check is missing keys or API quota. See [`../troubleshooting/common-issues.md`](../troubleshooting/common-issues.md).

