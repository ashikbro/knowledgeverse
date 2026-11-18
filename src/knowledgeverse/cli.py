"""Minimal CLI for the knowledge graph."""

import argparse
import json
import sys
from pathlib import Path

from knowledgeverse.graph import KnowledgeGraph


def main() -> None:
    parser = argparse.ArgumentParser(description="Local-first knowledge graph CLI")
    parser.add_argument("command", choices=["demo", "export"])
    parser.add_argument("--output", type=Path, help="Output file for export")
    args = parser.parse_args()

    graph = KnowledgeGraph()
    graph.add_node("python", "Python", "A programming language")
    graph.add_node("ml", "Machine Learning", "Models learn from data")
    graph.add_node("graphs", "Knowledge Graphs", "Typed relationships between concepts")
    graph.connect("python", "supports", "ml")
    graph.connect("ml", "uses", "graphs")

    if args.command == "demo":
        print("Demo graph created.")
        print("Search 'learn':", [n.label for n in graph.search("learn")])
        print("Neighbors of python:", [n.label for n in graph.neighbors("python")])
    elif args.command == "export":
        data = graph.export_json()
        if args.output:
            args.output.write_text(data)
            print(f"Exported to {args.output}")
        else:
            print(data)


if __name__ == "__main__":
    main()
