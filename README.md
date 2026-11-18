# Knowledgeverse

**Local-first typed knowledge graph** for connecting notes, concepts, and source-backed information.

Search, traverse neighborhoods, and export portable JSON — all without sending your data anywhere.

## What it does

- Deterministic in-memory nodes and typed relationships
- Full-text term search
- Bounded neighborhood traversal
- Portable JSON graph export

AI query providers, persistence, decentralized replication, and authentication are not implemented yet.

## Quick start

```sh
python -m venv .venv
.venv/bin/pip install pytest
PYTHONPATH=src .venv/bin/pytest
```

Core API: `add_node`, `connect`, `search`, `neighbors`, `connected`, `export_json`.

## Browser demo

Interactive graph explorer in `web/` (no dependencies):

```sh
python -m http.server 8000 --directory web
```

## Keywords

knowledge graph · local-first · python · search · notes · knowledge management
