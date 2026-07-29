"""Network-free tests for the SanJuan Knowledge Graph foundation."""

from pathlib import Path

from packages.knowledge.build_graph import build_graph
from packages.knowledge.markdown import parse_markdown_node, render_markdown_node
from packages.knowledge.validate_graph import validate_graph

REPO_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_ROOT = REPO_ROOT / "knowledge"


def test_sample_agency_node_is_citation_ready() -> None:
    node = parse_markdown_node(
        KNOWLEDGE_ROOT / "agencies" / "departamento-de-transportacion-y-obras-publicas.md"
    )

    assert node.id == "agency-pr-dtop"
    assert node.node_type == "agency"
    assert node.trust_level == "official"
    assert node.citation_ready() is True
    assert node.sources[0].source_id == "pr_dtop"


def test_graph_compiler_builds_nodes_and_edges() -> None:
    graph = build_graph(KNOWLEDGE_ROOT)

    assert graph["node_count"] >= 2
    assert graph["edge_count"] >= 2
    assert graph["unresolved_relations"] == []
    assert {node["id"] for node in graph["nodes"]} >= {
        "agency-pr-dtop",
        "service-renew-driver-license-pr",
    }


def test_graph_validator_accepts_foundation_vault() -> None:
    result = validate_graph(KNOWLEDGE_ROOT)

    assert result["valid"] is True
    assert result["error_count"] == 0


def test_markdown_renderer_round_trip_shape(tmp_path: Path) -> None:
    text = render_markdown_node(
        {
            "id": "topic-test",
            "title": "Test Topic",
            "node_type": "topic",
            "language": "en-es",
            "geography": "puerto_rico",
            "trust_level": "official",
            "review_status": "draft",
            "sources": [{"source_id": "test-source", "url": "https://example.gov/topic"}],
            "relations": [],
        },
        "# Test Topic\n",
    )
    path = tmp_path / "topic.md"
    path.write_text(text, encoding="utf-8")

    node = parse_markdown_node(path)
    assert node.id == "topic-test"
    assert "# Test Topic" in node.body
