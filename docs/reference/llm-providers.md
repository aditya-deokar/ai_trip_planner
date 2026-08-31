# LLM providers

Provider selection is implemented in [`utils/model_loader.py`](../../utils/model_loader.py).

## Supported providers

### Groq (`model_provider="groq"`)

- Class used: `langchain_groq.ChatGroq`
- Env var: `GROQ_API_KEY`
- Model name source: `config/config.yaml` → `llm.groq.model_name`

### Google Gemini (`model_provider="google"`)

- Class used: `langchain_google_genai.ChatGoogleGenerativeAI`
- Env var: `GOOGLE_API_KEY`
- Default model: `gemini-2.5-flash` (also supports `gemini-3.6-flash` and `gemini-2.5-pro`)
- Config source: `config/config.yaml` → `llm.google`

### Groq (`model_provider="groq"`)

- Class used: `langchain_groq.ChatGroq`
- Env var: `GROQ_API_KEY`
- Default model: `llama-3.3-70b-versatile` (also supports `deepseek-r1-distill-llama-70b`)
- Config source: `config/config.yaml` → `llm.groq`

## Where the provider is chosen today

Providers and specific models can be configured dynamically in the Streamlit UI sidebar or by sending `model_provider` and `model_name` parameters in API requests to `/query` or `/stream_query`.

## Operational considerations

- Different providers have different rate limits and error modes. Expect transient failures and add retries/timeouts if you productionize.
- Keep provider keys separate per environment (local `.env`, CI secrets, cloud secret store).

