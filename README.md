# Knowledgeverse

Local-first typed knowledge graph primitives for connecting notes, concepts,
and source-backed information.

## Current status

The repository includes deterministic in-memory nodes, typed relationships,
full-text term search, and neighborhood traversal. AI query providers,
persistence, decentralized replication, and authentication are not implemented
yet.

## Development

```sh
python -m venv .venv
.venv/bin/pip install pytest
PYTHONPATH=src .venv/bin/pytest
```
