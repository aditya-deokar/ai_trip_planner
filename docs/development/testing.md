# Testing

The repo currently does not include a dedicated test suite. This page defines a pragmatic, production-style testing approach you can add incrementally.

## Recommended test layers

### 1) Unit tests (fast)

Target:

- `utils/*` wrappers (currency, weather, places wrappers, calculator)
- deterministic helpers (`Calculator`)

Guidelines:

- mock network calls (`requests.get`) so tests are stable
- validate error handling (bad status codes, missing keys)

### 2) API contract tests (medium)

Target:

- `POST /query` shape and status codes

Approach:

- start `uvicorn main:app` in a test environment
- run a request and assert response schema `{answer: str}` or `{error: str}`

### 3) Golden output tests (slow / optional)

Because LLM outputs vary, avoid strict equality. Prefer:

- minimal structural checks (must include headings or sections)
- tool-call “smoke checks” (ensure the agent can call at least one tool with keys present)

## Manual smoke test checklist

- Backend runs without errors.
- UI connects to backend.
- A query returns a Markdown answer.
- `my_graph.png` is generated when a request is made.

