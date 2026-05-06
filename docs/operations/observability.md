# Observability

This project currently uses print-style logging in a few places. For production-grade operation, treat observability as part of the interface.

## What to log

### Backend (FastAPI)

- Request start/end for `POST /query`
- Provider selected (`groq` vs `google`)
- Tool call outcomes (success/failure)
- External API error messages (sanitized)
- Latency per request and per tool category

### Frontend (Streamlit)

- Backend connectivity failures (status code + message)

## Metrics to monitor

- **API**: request rate, p95 latency, error rate (`5xx`)
- **Providers**: Groq/Gemini error rate, latency
- **External APIs**: Places, OpenWeather, ExchangeRate-API, Tavily error rate and latency

## Tracing (future)

If you extend this into production, add correlation IDs:

- assign a request ID at the FastAPI boundary
- include it in tool logs and external call logs

