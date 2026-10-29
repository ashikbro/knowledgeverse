import pytest

from knowledgeverse import KnowledgeGraph


def test_graph_search_and_typed_neighbors():
    graph = KnowledgeGraph()
    graph.add_node("python", "Python", "A programming language")
    graph.add_node("ml", "Machine Learning", "Models learn from data")
    graph.add_node("web", "Web", "Application development")
    graph.connect("python", "supports", "ml")
    graph.connect("python", "used-in", "web")
    assert [node.id for node in graph.search("learn data")] == ["ml"]
    assert [node.id for node in graph.neighbors("python", "supports")] == ["ml"]


def test_edges_require_existing_nodes():
    with pytest.raises(KeyError):
        KnowledgeGraph().connect("missing", "rel", "other")
