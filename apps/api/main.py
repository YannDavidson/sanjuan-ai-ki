"""SanJuan AI MVP API.

Run locally from the repository root:

    uvicorn apps.api.main:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from packages.ingestion.load_sources import SourceRegistryError, load_sources
from packages.retrieval.keyword_search import search_chunks
from packages.shared.answer_schema import AnswerSource, AskAnswer, Citation
from packages.shared.source_schema import Source

app = FastAPI(
    title="SanJuan AI API",
    description="MVP backend for Puerto Rico's AI-native public knowledge infrastructure.",
    version="0.3.0",
)

HIGH_RISK_KEYWORDS = {
    "benefits",
    "court",
    "courts",
    "crime",
    "criminal",
    "emergency",
    "health",
    "hospital",
    "immigration",
    "legal",
    "license",
    "medical",
    "permit",
    "permits",
    "police",
    "public benefit",
    "tax",
    "taxes",
    "visa",
    "asilo",
    "beneficios",
    "corte",
    "emergencia",
    "impuestos",
    "inmigración",
    "licencia",
    "médico",
    "permiso",
    "permisos",
    "policía",
    "salud",
}


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


def _retrieval_result_to_answer_source(result: dict[str, Any]) -> AnswerSource | None:
    url = result.get("source_url") or (result.get("citation") or {}).get("url")
    if not url:
        return None

    return AnswerSource(
        source_id=str(result.get("source_id") or "unknown-source"),
        source_name=str(result.get("source_name") or "Unknown source"),
        url=url,
        category=str(result.get("category") or "unknown"),
        geography=str(result.get("geography") or "unknown"),
        language=str(result.get("language") or "unknown"),
        trust_level=str(result.get("trust_level") or "unknown"),
    )


def _retrieval_result_to_citation(result: dict[str, Any]) -> Citation | None:
    citation = result.get("citation") or {}
    url = citation.get("url") or result.get("source_url")
    if not url:
        return None

    return Citation(
        source_id=str(citation.get("source_id") or result.get("source_id") or "unknown-source"),
        source_name=str(citation.get("source_name") or result.get("source_name") or "Unknown source"),
        title=citation.get("title") or result.get("title"),
        url=url,
        trust_level=str(result.get("trust_level") or "unknown"),
        snippet=_truncate_text(str(result.get("text") or ""), max_length=420),
        fetched_at=result.get("fetched_at"),
    )


def _dedupe_sources(sources: list[AnswerSource]) -> list[AnswerSource]:
    seen: set[str] = set()
    output: list[AnswerSource] = []
    for source in sources:
        if source.source_id in seen:
            continue
        seen.add(source.source_id)
        output.append(source)
    return output


def _truncate_text(text: str, max_length: int = 900) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_length:
        return normalized
    return f"{normalized[: max_length - 1].rstrip()}…"


def _detect_language(question: str, preferred_language: str | None) -> str:
    if preferred_language in {"en", "es"}:
        return preferred_language

    spanish_markers = {"cómo", "dónde", "qué", "cuál", "permiso", "salud", "impuestos"}
    normalized = question.lower()
    if any(marker in normalized for marker in spanish_markers):
        return "es"
    return "en"


def _is_high_risk_question(question: str) -> bool:
    normalized = question.lower()
    return any(keyword in normalized for keyword in HIGH_RISK_KEYWORDS)


def _build_extractive_answer(question: str, language: str, results: list[dict[str, Any]]) -> str:
    top_result = results[0]
    source_name = top_result.get("source_name") or "a Puerto Rico source"
    excerpt = _truncate_text(str(top_result.get("text") or ""), max_length=900)

    if language == "es":
        return (
            f"Encontré información relevante en {source_name}. "
            "Como esta versión MVP todavía no usa generación con IA, aquí está el fragmento más relevante encontrado:\n\n"
            f"{excerpt}"
        )

    return (
        f"I found relevant Puerto Rico source material from {source_name}. "
        "Because this MVP is not using AI generation yet, here is the most relevant excerpt found:\n\n"
        f"{excerpt}"
    )


def _build_fallback_answer(language: str, high_risk: bool) -> str:
    if language == "es":
        if high_risk:
            return (
                "Todavía no encontré evidencia suficiente en las fuentes oficiales ingeridas para responder esta pregunta con seguridad. "
                "Para temas de permisos, impuestos, salud, emergencias, beneficios públicos, policía, tribunales o inmigración, SanJuan AI no debe adivinar."
            )
        return (
            "Todavía no encontré evidencia suficiente en los documentos ingeridos para responder con citas. "
            "Prueba ejecutar la ingestión y el chunking, o agrega más fuentes relevantes al registro."
        )

    if high_risk:
        return (
            "I did not find enough evidence in the ingested official sources to answer this safely. "
            "For permits, taxes, health, emergency, public benefits, police, court, legal, or immigration topics, SanJuan AI should not guess."
        )
    return (
        "I did not find enough evidence in the ingested documents to answer with citations yet. "
        "Try running ingestion and chunking, or add more relevant sources to the registry."
    )


def _build_safety_note(language: str, high_risk: bool, has_results: bool) -> str | None:
    if not high_risk:
        return None

    if language == "es":
        if has_results:
            return (
                "Tema sensible: verifica siempre la página oficial citada antes de tomar decisiones sobre permisos, impuestos, salud, emergencias, beneficios, policía, tribunales o inmigración."
            )
        return (
            "Tema sensible: se requieren fuentes oficiales antes de dar una respuesta directa. SanJuan AI no debe inventar requisitos, costos, fechas ni instrucciones."
        )

    if has_results:
        return (
            "Sensitive topic: always verify the cited official page before making decisions about permits, taxes, health, emergencies, benefits, police, courts, or immigration."
        )
    return (
        "Sensitive topic: official sources are required before giving a direct answer. SanJuan AI should not invent requirements, fees, dates, or instructions."
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
    """Return a citation-first answer using local retrieval over chunks."""
    language = _detect_language(request.question, request.language)
    high_risk = _is_high_risk_question(request.question)
    results = search_chunks(
        query=request.question,
        limit=5,
    )

    citations = [citation for result in results if (citation := _retrieval_result_to_citation(result)) is not None]
    sources = [source for result in results if (source := _retrieval_result_to_answer_source(result)) is not None]
    sources = _dedupe_sources(sources)

    if not results:
        fallback_sources = []
        if high_risk:
            official_sources = [source for source in _load_sources_or_500() if source.trust_level == "official"][:5]
            fallback_sources = [_source_to_answer_source(source) for source in official_sources]

        return AskAnswer(
            answer=_build_fallback_answer(language=language, high_risk=high_risk),
            language=language,
            confidence="low",
            citations=[],
            sources=fallback_sources,
            safety_note=_build_safety_note(language=language, high_risk=high_risk, has_results=False),
        )

    top_score = float(results[0].get("score") or 0)
    confidence = "high" if top_score >= 18 else "medium" if top_score >= 10 else "low"

    return AskAnswer(
        answer=_build_extractive_answer(question=request.question, language=language, results=results),
        language=language,
        confidence=confidence,
        citations=citations[:3],
        sources=sources[:5],
        safety_note=_build_safety_note(language=language, high_risk=high_risk, has_results=True),
    )
