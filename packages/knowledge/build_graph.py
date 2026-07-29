"""Compile Markdown knowledge nodes into a machine-readable graph index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from packages.knowledge.markdown import iter_markdown_nodes, parse_markdown_node

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KNOWLEDGE_ROOT = REPO_ROOT / "knowledge"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data" / "knowledge" / "graph.json"


def build_graph(root: Path = DEFAULT_KNOWLEDGE_ROOT) -> dict:
    nodes = [parse_markdown_node(path) for path in iter_markdown_nodes(root)]
    node_ids = {node.id for node in nodes}
    edges: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []

    for node in nodes:
        for relation in node.relations:
            edge = {"source": node.id, "relation": relation.relation, "target": relation.target}
            edges.append(edge)
            if relation.target not in node_ids:
                unresolved.append(edge)

    return {
        "schema_version": "0.1.0",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": [node.model_dump(mode="json") for node in nodes],
        "edges": edges,
        "unresolved_relations": unresolved,
    }


def write_graph(output_path: Path = DEFAULT_OUTPUT_PATH, root: Path = DEFAULT_KNOWLEDGE_ROOT) -> dict:
    graph = build_graph(root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    return graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the SanJuan Knowledge Graph index.")
    parser.add_argument("--root", type=Path, default=DEFAULT_KNOWLEDGE_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    graph = write_graph(args.output, args.root)
    print(json.dumps(graph, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
