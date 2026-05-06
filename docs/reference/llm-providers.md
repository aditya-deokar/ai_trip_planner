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
- Model name source: `config/config.yaml` → `llm.google.model_name`

## Where the provider is chosen today

In [`main.py`](../../main.py), the backend instantiates:

- `GraphBuilder(model_provider="groq")`

To switch providers, change the `model_provider` argument.

## Operational considerations

- Different providers have different rate limits and error modes. Expect transient failures and add retries/timeouts if you productionize.
- Keep provider keys separate per environment (local `.env`, CI secrets, cloud secret store).

