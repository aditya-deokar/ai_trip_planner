import streamlit as st
import requests
import json
import uuid
import re

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="🌍 AI Travel Planner Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for rich modern aesthetic
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# 1. State Management
if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"trip-session-{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sidebar Controls
with st.sidebar:
    st.title("⚙️ Travel Agent Settings")
    
    provider_choice = st.selectbox(
        "AI Provider",
        options=["google", "groq"],
        index=0,
        help="Select the AI platform to power your travel planner."
    )

    if provider_choice == "google":
        model_options = ["gemini-2.5-flash", "gemini-3.6-flash", "gemini-2.5-pro"]
        selected_model = st.selectbox(
            "Model Name",
            options=model_options,
            index=0,
            help="gemini-2.5-flash and gemini-3.6-flash deliver ultra-low latency."
        )
    else:
        model_options = ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b"]
        selected_model = st.selectbox(
            "Model Name",
            options=model_options,
            index=0,
            help="High-speed open models hosted on Groq LPU."
        )

    st.markdown("---")
    st.markdown(f"**Session ID:** `{st.session_state.thread_id}`")
    
    if st.button("🔄 Start New Trip / Reset Memory", use_container_width=True):
        st.session_state.thread_id = f"trip-session-{uuid.uuid4().hex[:8]}"
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Quick Prompt Ideas")
    prompts = [
        "Plan a 4-day trip to Tokyo for foodies and anime lovers with a medium budget.",
        "5-day relaxing romantic getaway to Bali with beach villas and cafe spots.",
        "Weekend road trip to Goa for 4 friends under ₹30,000 total budget.",
    ]
    for p in prompts:
        if st.button(p, key=f"quick_{p[:12]}"):
            st.session_state.queued_prompt = p
            st.rerun()

# 3. Main Header
st.title("🌍 AI Travel Planner Agent")
st.caption(f"Powered by **{provider_choice.title()} ({selected_model})** with real-time LangGraph multi-tool reasoning.")

# 4. Render Conversation History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Extract <think> reasoning tags if present
        content = msg["content"]
        think_match = re.search(r"<think>(.*?)</think>", content, flags=re.DOTALL)
        if think_match:
            think_text = think_match.group(1).strip()
            visible_text = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
            with st.expander("🧠 View Agent Reasoning & Route Analysis", expanded=False):
                st.markdown(think_text)
            st.markdown(visible_text)
        else:
            st.markdown(content)

# 5. Handle Incoming Prompt (from chat_input or quick prompt button)
user_prompt = st.chat_input("Ask for an itinerary or say 'Make Day 2 kid-friendly'...")

if not user_prompt and "queued_prompt" in st.session_state:
    user_prompt = st.session_state.pop("queued_prompt")

if user_prompt:
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Process assistant response
    with st.chat_message("assistant"):
        status_box = st.status("Agent researching your travel destination...", expanded=True)
        response_placeholder = st.empty()
        
        full_response_text = ""
        payload = {
            "question": user_prompt,
            "thread_id": st.session_state.thread_id,
            "model_provider": provider_choice,
            "model_name": selected_model
        }

        try:
            # Stream response via SSE endpoint
            res = requests.post(f"{BASE_URL}/stream_query", json=payload, stream=True, timeout=90)
            
            if res.status_code == 200:
                for line in res.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8")
                        if decoded_line.startswith("data: "):
                            data_str = decoded_line[6:]
                            try:
                                data = json.loads(data_str)
                                event_type = data.get("type")

                                if event_type == "token":
                                    token = data.get("content", "")
                                    full_response_text += token
                                    # Dynamically update the markdown stream
                                    response_placeholder.markdown(full_response_text + "▌")

                                elif event_type == "tool_start":
                                    t_name = data.get("name", "tool")
                                    t_input = data.get("input", "")
                                    status_box.write(f"🔍 Running **{t_name}** (`{t_input}`)...")

                                elif event_type == "tool_end":
                                    t_name = data.get("name", "tool")
                                    status_box.write(f"✅ **{t_name}** completed.")

                                elif event_type == "done":
                                    status_box.update(label="✈️ Itinerary & Travel Plan Ready!", state="complete", expanded=False)

                                elif event_type == "error":
                                    st.error(f"Error during agent execution: {data.get('error')}")

                            except json.JSONDecodeError:
                                pass
                
                # Final clean render
                response_placeholder.markdown(full_response_text)
                st.session_state.messages.append({"role": "assistant", "content": full_response_text})
            
            else:
                # Fallback to sync endpoint if stream fails
                status_box.write("Stream unavailable, falling back to standard query...")
                fallback_res = requests.post(f"{BASE_URL}/query", json=payload, timeout=60)
                if fallback_res.status_code == 200:
                    ans = fallback_res.json().get("answer", "")
                    status_box.update(label="✈️ Travel Plan Generated", state="complete", expanded=False)
                    response_placeholder.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    status_box.update(label="Generation Failed", state="error")
                    st.error(f"API Error ({fallback_res.status_code}): {fallback_res.text}")

        except Exception as e:
            status_box.update(label="Connection Error", state="error")
            st.error(f"Failed to connect to backend: {e}. Ensure FastAPI is running on port 8000 (`uvicorn main:app --port 8000`).")