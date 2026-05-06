# Runbook

This runbook covers common operational tasks and incident triage.

## Basic health checks

### Backend

- Is the backend process running?
- Is the API reachable? `GET http://localhost:8000/docs` should load when running locally.
### Frontend

- Is Streamlit running?
- Can Streamlit reach the backend at `BASE_URL` (see `streamlit_app.py`)?

## Common incidents

### `POST /query` returns `500`

1. Check backend logs for missing keys or provider errors.
2. Verify `.env` is present and loaded.
3. Validate external API keys and quotas.
See [`../troubleshooting/common-issues.md`](../troubleshooting/common-issues.md).

### Streamlit shows connection error

- Ensure backend is running on the expected port.
- Confirm `BASE_URL` in `streamlit_app.py` matches your backend.

## Key rotation

- Replace keys in your secret manager or `.env`.
- Restart backend and UI processes.
- Validate with a known query.

