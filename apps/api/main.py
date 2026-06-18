"""SanJuan AI MVP API.

Run locally from the repository root:

    uvicorn apps.api.main:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from packages.ingestion.load_sources import SourceRegistryError, load_sources
from packages.shared.answer_schema import AnswerSource, AskAnswer
from packages.shared.source_schema import Source

app = FastAPI(
    title="SanJuan AI API",
    description="MVP backend for Puerto Rico's AI-native public knowledge infrastructure.",
    version="0.2.0",
)


class AskRequest(BaseModel):
    """Ask request for the citation-first SanJuan AI assistant."""

    question: str = Field(..., min_length=2, description="User question for SanJuan AI.")
    language: str | None = Field(default=None, description="Optional preferred response language, such as 'en' or 'es'.")


def _load_sources_or_500() -> list[Source]:
    try:
        return load_sources()
    except SourceRegistryError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _source_to_answer_source(source: Source) -> AnswerSource:
    return AnswerSource(
        source_id=source.id,
        source_name=source.name,
        url=source.url,
        category=source.category,
        geography=source.geography,
        language=source.language,
        trust_level=source.trust_level,
    )


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


@app.post("/ask", response_model=AskAnswer)
def ask(request: AskRequest) -> AskAnswer:
    """Citation-first placeholder assistant endpoint.

    Retrieval is not connected yet. Until then, return the final response shape
    the frontend should design around: answer, language, confidence, citations,
    broader sources, and an optional safety note.
    """
    sources = _load_sources_or_500()
    official_sources = [source for source in sources if source.trust_level == "official"][:5]
    language = request.language or "en"

    return AskAnswer(
        answer=(
            "SanJuan AI is not connected to retrieval yet. The source registry is live, "
            "and the next implementation step is citation-based retrieval over trusted Puerto Rico sources."
        ),
        language=language,
        confidence="placeholder",
        citations=[],
        sources=[_source_to_answer_source(source) for source in official_sources],
        safety_note=(
            "For permits, taxes, health, legal, emergency, public benefits, police, courts, or immigration questions, "
            "SanJuan AI will require trusted official sources before giving a direct answer."
        ),
    )
