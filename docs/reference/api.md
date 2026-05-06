# API reference

The FastAPI app is defined in [`main.py`](../../main.py).

## Base URL (local)

- `http://localhost:8000`

## `POST /query`

Runs the agent against a user question.

### Request

Content-Type: `application/json`

Body schema (see `QueryRequest` in `main.py`):

```json
{
  "question": "string"
}
```

### Responses

#### `200 OK`

```json
{
  "answer": "string (markdown)"
}
```

#### `500 Internal Server Error`

```json
{
  "error": "string"
}
```

### Notes

- The backend builds a new graph per request (`GraphBuilder(...)`).
- The backend generates `my_graph.png` on each request.

## Interactive Swagger

When running locally, FastAPI serves Swagger UI at:

- `http://localhost:8000/docs`

