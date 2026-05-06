# Deployment

This project is currently optimized for local development. This document outlines a production-friendly deployment shape.

## Recommended deployment topology

Deploy as two services:

- **Backend service**: FastAPI (`uvicorn main:app`)
- **Frontend service**: Streamlit (`streamlit run streamlit_app.py`)

You can also deploy them on the same VM/container host as separate processes.

## Configuration and secrets

- Store API keys in a secret manager (not in repo): see [`../reference/environment-variables.md`](../reference/environment-variables.md).
- Keep non-secret configuration in `config/config.yaml`: see [`../reference/configuration-reference.md`](../reference/configuration-reference.md).

## CORS

`main.py` currently sets:

- `allow_origins=["*"]`

For production, restrict this to your Streamlit domain/origin.

## Artifacts

The backend currently writes `my_graph.png` on each request (see [`../architecture/data-flow.md`](../architecture/data-flow.md)). For production, consider disabling this or writing to a structured log/artifact path.

