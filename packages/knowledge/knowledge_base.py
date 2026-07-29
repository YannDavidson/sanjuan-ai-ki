"""Schemas and validation helpers for contributor-maintained Knowledge Bases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASES_PATH = REPO_ROOT / "knowledge" / "bases"

KnowledgeBaseStatus = Literal["proposed", "active", "needs_review", "archived"]
SourceTrust = Literal["official", "institutional", "community", "unverified"]
ContributorRole = Literal[
    "source_contributor",
    "knowledge_editor",
    "regional_reviewer",
    "domain_reviewer",
    "maintainer",
]


class KnowledgeBaseSource(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(..., min_length=2)
    name: str = Field(..., min_length=2)
    url: HttpUrl
    trust_level: SourceTrust
    source_type: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    notes: str | None = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not value.replace("-", "").replace("_", "").isalnum():
            raise ValueError(
                "source id may only contain letters, numbers, hyphens, and underscores"
            )
        return value


class KnowledgeBaseDefinition(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(..., min_length=3)
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    geography: list[str] = Field(min_length=1)
    languages: list[str] = Field(min_length=1)
    topics: list[str] = Field(min_length=1)
    maintainers: list[str] = Field(default_factory=list)
    review_status: KnowledgeBaseStatus = "proposed"
    sensitive_topics: bool = False
    source_policy: str = Field(..., min_length=10)
    sources: list[KnowledgeBaseSource] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not value.startswith("kb-"):
            raise ValueError("Knowledge Base id must start with 'kb-'")
        if not value.replace("-", "").isalnum():
            raise ValueError(
                "Knowledge Base id may only contain letters, numbers, and hyphens"
            )
        return value


def load_knowledge_base(path: Path) -> KnowledgeBaseDefinition:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return KnowledgeBaseDefinition.model_validate(data)


def iter_knowledge_base_files(root: Path) -> list[Path]:
    """Return publishable Knowledge Base definitions, excluding templates.

    Directories whose names begin with an underscore are repository scaffolding
    and must never be counted or compiled as real Knowledge Bases.
    """

    return sorted(
        path
        for path in root.glob("*/knowledge-base.yml")
        if not path.parent.name.startswith("_")
    )


def validate_knowledge_bases(root: Path = DEFAULT_BASES_PATH) -> dict[str, object]:
    errors: list[str] = []
    bases: list[KnowledgeBaseDefinition] = []
    seen_base_ids: set[str] = set()
    seen_source_ids: set[str] = set()

    for path in iter_knowledge_base_files(root):
        try:
            base = load_knowledge_base(path)
        except Exception as exc:  # validation command should report all failures
            errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
            continue

        if base.id in seen_base_ids:
            errors.append(f"duplicate Knowledge Base id: {base.id}")
        seen_base_ids.add(base.id)

        if base.review_status == "active" and not base.maintainers:
            errors.append(
                f"{base.id}: active Knowledge Bases require at least one maintainer"
            )

        if base.sensitive_topics and not any(
            source.trust_level == "official" for source in base.sources
        ):
            errors.append(
                f"{base.id}: sensitive Knowledge Bases require at least one official source"
            )

        for source in base.sources:
            scoped_id = f"{base.id}:{source.id}"
            if scoped_id in seen_source_ids:
                errors.append(f"duplicate source id in {base.id}: {source.id}")
            seen_source_ids.add(scoped_id)

        bases.append(base)

    return {
        "valid": not errors,
        "knowledge_base_count": len(bases),
        "source_count": sum(len(base.sources) for base in bases),
        "errors": errors,
        "knowledge_bases": [base.model_dump(mode="json") for base in bases],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate SanJuan KI community Knowledge Bases."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_BASES_PATH)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = validate_knowledge_bases(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
