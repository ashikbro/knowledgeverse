"""A deterministic in-memory knowledge graph."""

from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    content: str


class KnowledgeGraph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.edges: dict[tuple[str, str], set[str]] = {}

    def add_node(self, node_id: str, label: str, content: str) -> Node:
        if not node_id.strip() or not label.strip():
            raise ValueError("node_id and label are required")
        node = Node(node_id, label.strip(), content)
        self.nodes[node_id] = node
        return node

    def connect(self, source_id: str, relation: str, target_id: str) -> None:
        if source_id not in self.nodes or target_id not in self.nodes:
            raise KeyError("both nodes must exist before connecting them")
        if not relation.strip():
            raise ValueError("relation is required")
        self.edges.setdefault((source_id, relation.strip()), set()).add(target_id)

    def search(self, query: str) -> list[Node]:
        terms = query.casefold().split()
        return [
            node for node in sorted(self.nodes.values(), key=lambda item: item.id)
            if all(term in f"{node.label} {node.content}".casefold() for term in terms)
        ]

    def neighbors(self, node_id: str, relation: str | None = None) -> list[Node]:
        if node_id not in self.nodes:
            raise KeyError("node does not exist")
        target_ids = {
            target
            for (source, edge_relation), targets in self.edges.items()
            if source == node_id and (relation is None or edge_relation == relation)
            for target in targets
        }
        return [self.nodes[target] for target in sorted(target_ids)]

    def connected(self, node_id: str, depth: int = 1, undirected: bool = True) -> list[Node]:
        if node_id not in self.nodes:
            raise KeyError("node does not exist")
        if depth < 1:
            raise ValueError("depth must be at least 1")
        seen = {node_id}
        frontier = {node_id}
        for _ in range(depth):
            next_frontier: set[str] = set()
            for source, target in self.edge_pairs():
                if source in frontier:
                    next_frontier.add(target)
                if undirected and target in frontier:
                    next_frontier.add(source)
            next_frontier -= seen
            seen |= next_frontier
            frontier = next_frontier
        return [self.nodes[item] for item in sorted(seen - {node_id})]

    def edge_pairs(self) -> list[tuple[str, str]]:
        return sorted(
            (source, target)
            for (source, _relation), targets in self.edges.items()
            for target in targets
        )

    def export_json(self) -> str:
        edges = [
            {"source": source, "relation": relation, "target": target}
            for (source, relation), targets in sorted(self.edges.items())
            for target in sorted(targets)
        ]
        return json.dumps(
            {"nodes": [node.__dict__ for node in sorted(self.nodes.values(), key=lambda item: item.id)], "edges": edges},
            indent=2,
            sort_keys=True,
        )
