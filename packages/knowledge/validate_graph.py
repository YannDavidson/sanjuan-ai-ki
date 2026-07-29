"""Validate SanJuan Knowledge Graph Markdown nodes and relationships."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from packages.knowledge.markdown import iter_markdown_nodes, parse_markdown_node
from packages.knowledge.build_graph import DEFAULT_KNOWLEDGE_ROOT


def validate_graph(root: Path = DEFAULT_KNOWLEDGE_ROOT) -> dict:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    nodes = []

    for path in iter_markdown_nodes(root):
        try:
            node = parse_markdown_node(path)
        except (ValueError, ValidationError) as exc:
            errors.append({"file": str(path), "message": str(exc)})
            continue

        nodes.append(node)
        if node.node_type != "index" and not node.sources:
            errors.append({"file": str(path), "message": "Evidence node must include at least one source citation."})
        if node.review_status == "human_reviewed" and not node.reviewed_by:
            errors.append({"file": str(path), "message": "Human-reviewed node must include reviewed_by."})
        if not node.relations:
            warnings.append({"file": str(path), "message": "Node has no graph relationships."})

    node_ids = {node.id for node in nodes}
    for node in nodes:
        for relation in node.relations:
            if relation.target not in node_ids:
                warnings.append(
                    {
                        "file": node.file_path or node.id,
                        "message": f"Unresolved relation target: {relation.target}",
                    }
                )

    return {
        "valid": not errors,
        "node_count": len(nodes),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the SanJuan Knowledge Graph vault.")
    parser.add_argument("--root", type=Path, default=DEFAULT_KNOWLEDGE_ROOT)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = validate_graph(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
