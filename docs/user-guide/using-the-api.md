# Using the API

The backend exposes a single main endpoint in [`main.py`](../../main.py):

- `POST /query`

## Endpoint: `POST /query`

### Request body

```json
{
  "question": "Plan a 5-day trip to Goa for 2 people in April with a mid-range budget"
}
```

### Success response (`200`)

```json
{
  "answer": "# ...markdown travel plan..."
}
```

### Error response (`500`)

```json
{
  "error": "Description of what went wrong"
}
```

## cURL example

```bash
curl -X POST "http://localhost:8000/query" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"Plan a 3-day trip to Jaipur\"}"
```

## Python example

```python
import requests

resp = requests.post(
    "http://localhost:8000/query",
    json={"question": "Plan a 4-day trip to Singapore for a solo traveler"},
    timeout=120,
)
resp.raise_for_status()
print(resp.json()["answer"])
```

## Notes

- The response is **Markdown** intended to render in the UI, but you can store it as-is.
- The backend currently writes `my_graph.png` to the current working directory for each request (see [`../architecture/data-flow.md`](../architecture/data-flow.md)).

