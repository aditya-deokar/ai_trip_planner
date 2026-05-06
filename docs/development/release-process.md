# Release process

This repo does not currently define an automated release pipeline. This document describes a lightweight, production-style process you can adopt.

## Versioning

- Keep the project version in `pyproject.toml` (`[project].version`).
- Treat versions as SemVer (`MAJOR.MINOR.PATCH`):
  - bump **PATCH** for fixes
  - bump **MINOR** for backward-compatible features
  - bump **MAJOR** for breaking changes

## Release checklist

### Code

- Ensure the app runs end-to-end locally (backend + UI).
- Ensure config and provider selection still work.
### Documentation

- Update docs if behavior changed:
  - API changes: [`../reference/api.md`](../reference/api.md)
  - env var changes: [`../reference/environment-variables.md`](../reference/environment-variables.md)
  - tool changes: [`../architecture/tools-and-integrations.md`](../architecture/tools-and-integrations.md)

### Packaging

- Confirm `pyproject.toml` version is bumped.
- Confirm dependencies are correct (`pyproject.toml` and/or `requirements.txt`).

## Suggested future improvements

- Add CI with lint + tests + basic smoke run.
- Add an automated changelog.
- Publish docs as a site (MkDocs Material) when you want search/nav.

