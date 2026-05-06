# Assets

This folder is for documentation assets (images/diagrams) referenced from Markdown docs.

## Conventions

- Use lowercase filenames with hyphens: `agent-graph.png`, `system-overview.svg`
- Keep assets stable (avoid auto-generated timestamps)
- Prefer `.png` for screenshots, `.svg` for diagrams when possible

## Referencing assets

Use relative Markdown links from docs, e.g.:

```md
![Agent graph](../assets/agent-graph.png)
```

## Notes

The backend currently generates `my_graph.png` in the repo root on requests. If you want a stable documentation image, copy a representative graph into this folder with a stable name and reference it from docs.

