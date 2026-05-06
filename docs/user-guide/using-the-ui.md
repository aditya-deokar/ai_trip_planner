# Using the UI (Streamlit)

The Streamlit app is the quickest way to interact with the agent.

## Start the UI

Follow [`../getting-started/running-locally.md`](../getting-started/running-locally.md) to run:

- Backend: `uvicorn main:app ...` on `http://localhost:8000`
- UI: `streamlit run streamlit_app.py` on `http://localhost:8501`

## UI behavior

The UI sends your input to the backend endpoint:

- `POST http://localhost:8000/query`

The backend returns a JSON payload like:

```json
{ "answer": "<markdown travel plan>" }
```

The UI then renders the answer as Markdown in the Streamlit page.

## Tips for better answers

- Specify **days**, **month/season**, **traveler count**, and **budget**.
- Ask for constraints (e.g. “vegetarian food”, “no long drives”, “kid friendly”).
- If you want the plan to include costs in your currency, mention it explicitly (the agent can call `convert_currency`).

## Example prompts

See [`example-queries.md`](example-queries.md).

