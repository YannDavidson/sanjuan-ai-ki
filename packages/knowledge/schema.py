"""Schemas for SanJuan Knowledge Graph Markdown nodes."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

NodeType = Literal["agency", "service", "topic", "location", "index"]
ReviewStatus = Literal["machine_compiled", "human_reviewed", "stale", "draft"]
TrustLevel = Literal["official", "institutional", "community", "experimental"]
LanguageCode = Literal["en", "es", "en-es", "multi"]


class KnowledgeSource(BaseModel):
    """Evidence reference retained by a graph node."""

    model_config = ConfigDict(str_strip_whitespace=True)

    source_id: str = Field(..., min_length=2)
    url: HttpUrl
    title: str | None = None
    fetched_at: str | None = None
    content_hash: str | None = None


class KnowledgeRelation(BaseModel):
    """Directed relationship between two graph nodes."""

    model_config = ConfigDict(str_strip_whitespace=True)

    relation: str = Field(..., min_length=2)
    target: str = Field(..., min_length=2)


class KnowledgeNode(BaseModel):
    """Validated frontmatter and body for one knowledge graph node."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(..., min_length=2)
    title: str = Field(..., min_length=2)
    node_type: NodeType
    language: LanguageCode = "en-es"
    geography: str = "puerto_rico"
    trust_level: TrustLevel
    review_status: ReviewStatus = "draft"
    related_agencies: list[str] = Field(default_factory=list)
    related_services: list[str] = Field(default_factory=list)
    related_topics: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    sources: list[KnowledgeSource] = Field(default_factory=list)
    relations: list[KnowledgeRelation] = Field(default_factory=list)
    last_verified: str | None = None
    reviewed_by: str | None = None
    reviewed_at: str | None = None
    body: str = ""
    file_path: str | None = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not value.replace("_", "").replace("-", "").isalnum():
            raise ValueError("id may only contain letters, numbers, underscores, and hyphens")
        return value

    @field_validator("sources")
    @classmethod
    def require_sources_for_evidence_nodes(cls, values: list[KnowledgeSource]) -> list[KnowledgeSource]:
        return values

    def citation_ready(self) -> bool:
        """Return whether this node has at least one traceable evidence URL."""
        return bool(self.sources)
