# Installation

This project supports both `uv` (recommended) and `pip`.

## Prerequisites

- Python **3.12+**

## Option A: Install with `uv` (recommended)

From the repo root:

```bash
uv sync
```

Then run commands via `uv run ...` (see [`running-locally.md`](running-locally.md)).

## Option B: Install with `pip` (venv)

From the repo root (PowerShell friendly):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Sanity check

Verify imports work:

```bash
python -c "import fastapi, streamlit, langgraph; print('ok')"
```

