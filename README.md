# Knowledgeverse

Local-first typed knowledge graph primitives for connecting notes, concepts,
and source-backed information.

## Current status

The repository includes deterministic in-memory nodes, typed relationships,
full-text term search, bounded neighborhood traversal, and portable JSON graph
export. AI query providers, persistence, decentralized replication, and
authentication are not implemented yet.

## Development

```sh
python -m venv .venv
.venv/bin/pip install pytest
PYTHONPATH=src .venv/bin/pytest
```

The graph API supports `add_node`, `connect`, `search`, `neighbors`,
`connected`, `export_json`, and `from_json`. JSON exports can be imported to
restore nodes and typed relationships. `connected` traverses relationships in
both directions by default so discovery does not depend on edge orientation.

## Browser showcase

The `web/` directory contains a dependency-free interactive graph explorer
with typed relationships, search, concept selection, and a visual neighborhood
view. Preview it with:

```sh
python -m http.server 8000 --directory web
```
