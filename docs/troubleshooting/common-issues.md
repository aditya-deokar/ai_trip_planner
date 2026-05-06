# Troubleshooting (common issues)

## Backend returns `500 Internal Server Error`

### Symptoms

- Streamlit shows an error response
- API call to `POST /query` returns `500` with `{ "error": "..." }`

### Likely causes

- Missing or invalid API keys in `.env`
- External API quota/rate limits (Places, Tavily, OpenWeather, ExchangeRate)
- LLM provider error (Groq/Gemini)

### Fix

1. Confirm `.env` exists in the repo root and contains required keys.
2. Check the canonical list: [`../reference/environment-variables.md`](../reference/environment-variables.md)
3. Verify provider selection: [`../reference/llm-providers.md`](../reference/llm-providers.md)
4. Retry with a simpler prompt (e.g. “Plan a 2-day trip to Pune”).

## Streamlit cannot reach backend

### Symptoms

- UI error like connection refused / failed to fetch

### Likely causes

- backend not running
- wrong port (backend not on 8000)
- `BASE_URL` mismatch in `streamlit_app.py`

### Fix

- Start backend first: [`../getting-started/running-locally.md`](../getting-started/running-locally.md)
- Confirm `BASE_URL = "http://localhost:8000"` in `streamlit_app.py`.

## Places tool fails (Google Places)

### Symptoms

- Tool outputs mention Google failure
- Results look empty / generic

### Likely causes

- `GPLACES_API_KEY` missing/invalid
- Google Places API not enabled on the key/project

### Fix

- Verify `GPLACES_API_KEY` is set.
- Check Google Cloud Console: billing + Places API enablement.
- Note: the tool falls back to Tavily on exception (see [`../architecture/tools-and-integrations.md`](../architecture/tools-and-integrations.md)).

## Tavily fallback fails

### Symptoms

- Places results fail and fallback results also error

### Likely causes

- `TAVILY_API_KEY` missing/invalid
- Tavily rate limit/quota

### Fix

- Verify `TAVILY_API_KEY` is set.
- Retry later or switch to a different query.

## Weather tool fails

### Symptoms

- “Could not fetch weather for <city>”

### Likely causes

- `OPENWEATHERMAP_API_KEY` missing/invalid
- location name mismatch (try adding country)

### Fix

- Verify key is set.
- Retry with a more specific city name (e.g. “Paris, FR”).

## Currency conversion fails

### Symptoms

- Currency tool raises an error or returns unexpected result

### Likely causes

- `EXCHANGE_RATE_API_KEY` missing/invalid
- unsupported currency code

### Fix

- Verify key is set.
- Use ISO currency codes like `USD`, `INR`, `EUR`.

