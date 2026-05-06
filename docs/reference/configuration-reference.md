# Configuration reference

Non-secret configuration lives in `config/config.yaml` and is loaded by [`utils/config_loader.py`](../../utils/config_loader.py).

## File: `config/config.yaml`

Current shape:

```yaml
llm:
  groq:
    provider: "groq"
    model_name: "deepseek-r1-distill-llama-70b"

  google:
    provider: "google"
    model_name: "gemini-2.5-pro"
```

## How it is used

- `utils/model_loader.py` loads this config and reads:
  - `llm.groq.model_name`
  - `llm.google.model_name`

## Change management guidelines

- Treat `config/config.yaml` as **public, non-secret** config.
- Keep secrets in env vars (see [`environment-variables.md`](environment-variables.md)).
- If you add a new provider:
  - update `config/config.yaml`
  - update `utils/model_loader.py`
  - update [`llm-providers.md`](llm-providers.md)

