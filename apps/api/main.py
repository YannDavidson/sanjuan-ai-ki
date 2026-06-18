"""SanJuan AI MVP API.

Run locally from the repository root:

    uvicorn apps.api.main:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from packages.ingestion.load_sources import SourceRegistryError, load_sources
from packages.shared.source_schema import Source

app = FastAPI(
    title="SanJuan AI API",
    description="MVP backend for Puerto Rico's AI-native public knowledge infrastructure.",
    version="0.1.0",
)


class AskRequest(BaseModel):
    """Placeholder ask request until retrieval is connected."""

    question: str = Field(..., min_length=2, description="User question for SanJuan AI.")
    language: str | None = Field(default=None, description="Optional preferred response language, such as 'en' or 'es'.")


class AskResponse(BaseModel):
    """Placeholder ask response."""

    answer: str
    sources: list[dict[str, Any]] = Field(default_factory=list)


def _load_sources_or_500() -> list[Source]:
    try:
        return load_sources()
    except SourceRegistryError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint for deployment and monitoring."""
    return {"status": "ok", "service": "sanjuan-ai-api"}


@app.get("/sources")
def get_sources(
    category: str | None = None,
    trust_level: str | None = None,
    geography: str | None = None,
    language: str | None = None,
) -> dict[str, Any]:
    """Return registered Puerto Rico sources, with optional filters."""
    sources = _load_sources_or_500()

    if category:
        sources = [source for source in sources if source.category == category]
    if trust_level:
        sources = [source for source in sources if source.trust_level == trust_level]
    if geography:
        sources = [source for source in sources if source.geography == geography]
    if language:
        sources = [source for source in sources if source.language == language]

    return {
        "count": len(sources),
        "sources": [source.model_dump(mode="json") for source in sources],
    }


@app.get("/sources/{source_id}")
def get_source(source_id: str) -> dict[str, Any]:
    """Return one registered source by id."""
    sources = _load_sources_or_500()
    source = next((item for item in sources if item.id == source_id), None)

    if source is None:
        raise HTTPException(status_code=404, detail=f"Source not found: {source_id}")

    return source.model_dump(mode="json")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Placeholder assistant endpoint.

    Retrieval will be connected after the ingestion and citation strategy are implemented.
    """
    _ = request
    return AskResponse(
        answer="SanJuan AI is not connected to retrieval yet. The source registry is live, and citation-based answers are the next step.",
        sources=[],
    )
