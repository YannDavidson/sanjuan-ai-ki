"""Shared embedding schema for SanJuan AI retrieval.

The MVP uses local deterministic hash vectors so development can continue without
external embedding APIs. The schema is designed to remain compatible with future
provider-backed embeddings and pgvector storage.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

EmbeddingProvider = Literal["local_hash", "openai", "cohere", "voyage", "sentence_transformers"]


class Citation(BaseModel):
    """Citation metadata carried from source chunks to vector records."""

    title: str | None = None
    url: HttpUrl | str | None = None
    source_id: str | None = None
    source_name: str | None = None


class EmbeddingRecord(BaseModel):
    """Embedding/vector metadata for one retrieval chunk."""

    embedding_id: str = Field(..., min_length=1)
    chunk_id: str = Field(..., min_length=1)
    document_id: str = Field(..., min_length=1)
    source_id: str = Field(..., min_length=1)
    source_name: str | None = None
    source_url: HttpUrl | str | None = None
    title: str | None = None
    category: str | None = None
    geography: str | None = None
    language: str | None = None
    trust_level: str | None = None
    provider: EmbeddingProvider = "local_hash"
    model: str = Field(..., min_length=1)
    dimensions: int = Field(..., gt=0)
    vector: list[float]
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    content_hash: str | None = None
    citation: Citation = Field(default_factory=Citation)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("vector")
    @classmethod
    def vector_must_not_be_empty(cls, value: list[float]) -> list[float]:
        if not value:
            raise ValueError("vector must not be empty")
        return value

    @field_validator("vector")
    @classmethod
    def vector_values_must_be_finite(cls, value: list[float]) -> list[float]:
        for item in value:
            if not isinstance(item, int | float):
                raise ValueError("vector values must be numeric")
            if item != item or item in (float("inf"), float("-inf")):
                raise ValueError("vector values must be finite")
        return [float(item) for item in value]

    @field_validator("dimensions")
    @classmethod
    def dimensions_must_match_vector(cls, value: int, info: Any) -> int:
        vector = info.data.get("vector") if hasattr(info, "data") else None
        if vector is not None and len(vector) != value:
            raise ValueError("dimensions must match vector length")
        return value
