# Security

## Secrets handling

- Keep API keys in environment variables (local `.env`, production secret manager).
- Never commit `.env`.
- Treat logs as sensitive: avoid logging full prompts if they contain personal travel details.

See [`../reference/environment-variables.md`](../reference/environment-variables.md).

## Input handling

- The API accepts user-provided text. Assume it may contain unexpected content.
- Validate request schema at the API boundary (FastAPI + Pydantic already does basic schema validation).

## External API usage

- Rate limits and quotas apply. Handle provider errors gracefully.
- Avoid returning raw stack traces to end users in production.

## Dependency hygiene

- Keep dependencies updated (FastAPI, LangChain/LangGraph, Streamlit).
- For production deployments, pin versions and run vulnerability scanning as part of CI.

