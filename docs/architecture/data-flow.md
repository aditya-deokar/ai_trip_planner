# Data flow

This document traces one request end-to-end.

## Request sequence

```mermaid
sequenceDiagram
  participant U as User
  participant S as Streamlit_UI
  participant F as FastAPI_Backend
  participant G as LangGraph_Agent
  participant T as Tools

  U->>S: Enter travel question
  S->>F: POST /query {question}
  F->>G: build_graph + invoke(MessagesState)
  loop ReAct_until_done
    G->>T: tool_calls (weather/places/currency/expense)
    T-->>G: tool_results
  end
  G-->>F: final_markdown_answer
  F-->>S: {answer: markdown}
  S-->>U: render Markdown
```

## Backend specifics

In [`main.py`](../../main.py):

- The endpoint instantiates `GraphBuilder(model_provider="groq")`.
- It compiles and invokes the graph with `{"messages": [query.question]}`.
- It writes a diagram image to disk:
  - `my_graph.png` is generated from `react_app.get_graph().draw_mermaid_png()`.

Operational note:

- Writing `my_graph.png` on every request is convenient for debugging, but can be noisy in production environments. If you deploy this, consider gating it behind a config flag.

