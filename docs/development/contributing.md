# Contributing

Thanks for contributing to AI Trip Planner.

## Project philosophy

- Keep the app **simple to run locally**.
- Keep tools **small and composable**.
- Prefer **clear interfaces** (inputs/outputs) over cleverness.

## Development workflow

- Create a feature branch.
- Make changes with focused commits.
- Update docs when behavior changes (docs are part of the deliverable).

## Adding a new tool (checklist)

1. **Implement tool** in `tools/` using `@tool` from `langchain.tools`.
2. If the tool needs API calls, add a wrapper under `utils/`.
3. Add required env vars to env var docs: [`../reference/environment-variables.md`](../reference/environment-variables.md).
4. Register the tool in `GraphBuilder` (`agent/agentic_workflow.py`) by adding it to `self.tools`.
5. Document the tool in [`../architecture/tools-and-integrations.md`](../architecture/tools-and-integrations.md).
6. Smoke test using `POST /query`.

## Changing the agent behavior

- Update the system prompt in [`prompt_library/prompt.py`](../../prompt_library/prompt.py).
- If you change the output structure, update [`../user-guide/output-format.md`](../user-guide/output-format.md).

## Reporting issues

When filing a bug report, include:

- OS and Python version
- install method (`uv` or `pip`)
- the exact prompt you used
- backend logs / error message
- whether the failure is specific to one provider (Groq vs Google)

