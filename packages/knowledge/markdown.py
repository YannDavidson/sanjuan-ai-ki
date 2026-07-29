"""Read and write Obsidian-compatible knowledge graph Markdown files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from packages.knowledge.schema import KnowledgeNode

FRONTMATTER_DELIMITER = "---"


def parse_markdown_node(path: Path) -> KnowledgeNode:
    """Parse YAML frontmatter and Markdown body into a validated node."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith(f"{FRONTMATTER_DELIMITER}\n"):
        raise ValueError(f"Missing YAML frontmatter in {path}")

    parts = text.split(FRONTMATTER_DELIMITER, 2)
    if len(parts) != 3:
        raise ValueError(f"Malformed YAML frontmatter in {path}")

    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"Frontmatter must be a mapping in {path}")

    metadata["body"] = parts[2].lstrip("\n")
    metadata["file_path"] = str(path)
    return KnowledgeNode.model_validate(metadata)


def render_markdown_node(metadata: dict[str, Any], body: str) -> str:
    """Render frontmatter and Markdown body using stable YAML formatting."""
    frontmatter = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{frontmatter}\n---\n\n{body.rstrip()}\n"


def iter_markdown_nodes(root: Path) -> list[Path]:
    """Return graph node files, excluding templates and generated indexes."""
    return sorted(
        path
        for path in root.rglob("*.md")
        if "_templates" not in path.parts and "_generated" not in path.parts and path.name != "README.md"
    )
