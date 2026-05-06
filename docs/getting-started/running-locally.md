# Running locally

You must run **two processes**:

- FastAPI backend (serves `POST /query`)
- Streamlit frontend (UI)

## Start the backend (FastAPI)

From the repo root:

### If you installed with `uv`

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### If you installed with `pip`

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend URLs:

- API base: `http://localhost:8000`
- Interactive docs (FastAPI Swagger): `http://localhost:8000/docs`

## Start the frontend (Streamlit)

Open a **new terminal** from the repo root:

### If you installed with `uv`

```bash
uv run streamlit run streamlit_app.py
```

### If you installed with `pip`

```bash
streamlit run streamlit_app.py
```

Frontend URL:

- `http://localhost:8501`

## Verify it works

1. Open Streamlit and submit a query like:

   - `Plan a 3-day trip to Manali in winter`

2. If you prefer verifying the backend directly:

```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\": \"Plan a 2-day trip to Pune\"}"
```

If you get `500`, jump to [`../troubleshooting/common-issues.md`](../troubleshooting/common-issues.md).

