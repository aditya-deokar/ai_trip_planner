from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import json
import asyncio
from typing import Optional, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

app = FastAPI(title="AI Travel Planner API", version="1.0.0")
from mcp_server.server import mcp as mcp_server_instance

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP Server SSE Sub-App for remote network clients (Phase 5)
mcp_sse = mcp_server_instance.sse_app()
app.mount("/mcp", mcp_sse)

# Global shared checkpointer for thread persistence across requests
shared_checkpointer = MemorySaver()
graph_instances: Dict[str, any] = {}

def get_or_create_graph(model_provider: str = "google", model_name: Optional[str] = None):
    cache_key = f"{model_provider}:{model_name or 'default'}"
    if cache_key not in graph_instances:
        builder = GraphBuilder(
            model_provider=model_provider,
            model_name=model_name,
            checkpointer=shared_checkpointer
        )
        graph_instances[cache_key] = builder.build_graph()
        
        # Save mermaid diagram
        try:
            png_graph = graph_instances[cache_key].get_graph().draw_mermaid_png()
            with open("my_graph.png", "wb") as f:
                f.write(png_graph)
            print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        except Exception as e:
            print(f"Could not render graph image: {e}")
            
    return graph_instances[cache_key]


class QueryRequest(BaseModel):
    question: str
    thread_id: Optional[str] = "default-session"
    model_provider: Optional[str] = "google"
    model_name: Optional[str] = None


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    """Synchronous query endpoint with multi-turn thread memory."""
    try:
        react_app = get_or_create_graph(
            model_provider=query.model_provider or "google",
            model_name=query.model_name
        )

        config = {"configurable": {"thread_id": query.thread_id or "default-session"}}
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages, config=config)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {
            "answer": final_output,
            "thread_id": query.thread_id
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/stream_query")
async def stream_travel_agent(query: QueryRequest):
    """Real-time streaming endpoint yielding SSE events for token-by-token and tool feedback."""
    try:
        react_app = get_or_create_graph(
            model_provider=query.model_provider or "google",
            model_name=query.model_name
        )

        config = {"configurable": {"thread_id": query.thread_id or "default-session"}}
        messages = {"messages": [query.question]}

        async def sse_event_stream():
            try:
                # Use astream_events (v2) to capture live tool calls and token output
                async for event in react_app.astream_events(messages, config=config, version="v2"):
                    kind = event.get("event")

                    # Model is generating tokens
                    if kind == "on_chat_model_stream":
                        chunk = event.get("data", {}).get("chunk")
                        if chunk and hasattr(chunk, "content"):
                            token_text = chunk.content
                            if token_text:
                                yield f"data: {json.dumps({'type': 'token', 'content': token_text})}\n\n"

                    # Tool start notification
                    elif kind == "on_tool_start":
                        tool_name = event.get("name", "tool")
                        tool_input = event.get("data", {}).get("input", "")
                        yield f"data: {json.dumps({'type': 'tool_start', 'name': tool_name, 'input': str(tool_input)[:120]})}\n\n"

                    # Tool complete notification
                    elif kind == "on_tool_end":
                        tool_name = event.get("name", "tool")
                        yield f"data: {json.dumps({'type': 'tool_end', 'name': tool_name})}\n\n"

                yield f"data: {json.dumps({'type': 'done', 'thread_id': query.thread_id})}\n\n"
            except Exception as stream_err:
                yield f"data: {json.dumps({'type': 'error', 'error': str(stream_err)})}\n\n"

        return StreamingResponse(sse_event_stream(), media_type="text/event-stream")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})