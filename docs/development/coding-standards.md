# Coding standards

## General

- Prefer clear, descriptive names over abbreviations.
- Keep modules small and focused (one primary responsibility).
- Fail with actionable errors (include context, avoid silent `pass`).

## Tools

- Tool functions should have stable, descriptive names (these become part of the “agent API”).
- Keep tool I/O simple (strings / numbers) and document required env vars.
- For network calls, use timeouts and propagate useful failure info.

## Configuration

- Secrets belong in env vars, not in `config/config.yaml`.
- `config/config.yaml` is non-secret and should remain safe to commit.

## Documentation

- If you change behavior or configuration, update the canonical docs in `docs/reference/`.
- Keep cross-links relative so GitHub rendering works.

