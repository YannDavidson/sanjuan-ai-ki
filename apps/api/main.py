"""SanJuan AI MVP API.

Run locally from the repository root:

    uvicorn apps.api.main:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from apps.api.config import load_api_settings
from apps.api.rate_limit import InMemoryRateLimiter, RateLimitDecision
from packages.ingestion.corpus_status import build_corpus_status_dict
from packages.ingestion.load_sources import SourceRegistryError, load_sources
from packages.retrieval.hybrid_search import search_hybrid
from packages.shared.answer_schema import AnswerSource, AskAnswer, Citation, IngestionStatus, RelatedAgency, StructuredAnswer
from packages.shared.source_schema import Source

settings = load_api_settings()
ask_rate_limiter = InMemoryRateLimiter(max_requests=settings.ask_rate_limit_per_minute)

app = FastAPI(
    title="SanJuan AI API",
    description="MVP backend for Puerto Rico's AI-native public knowledge infrastructure.",
    version=settings.api_version,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=settings.allow_credentials,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        max_age=600,
    )


@app.middleware("http")
async def add_security_headers(request: Request, call_next: Any) -> Response:
    """Add conservative security headers for API responses."""
    response: Response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("X-SanJuan-AI-Env", settings.environment)
    return response


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

STEP_HINTS = {
    "apply",
    "application",
    "complete",
    "create",
    "fill",
    "file",
    "go to",
    "register",
    "renew",
    "request",
    "submit",
    "visit",
    "aplicar",
    "completar",
    "llenar",
    "radicar",
    "registrar",
    "renovar",
    "solicitar",
    "someter",
    "visitar",
}

REQUIREMENT_HINTS = {
    "certificate",
    "certification",
    "document",
    "fee",
    "form",
    "id",
    "license",
    "payment",
    "required",
    "requirement",
    "tax id",
    "certificado",
    "documento",
    "formulario",
    "identificación",
    "licencia",
    "pago",
    "requisito",
    "requerido",
}


class AskRequest(BaseModel):
    """Ask request for the citation-first SanJuan AI assistant."""

    question: str = Field(..., min_length=2, description="User question for SanJuan AI.")
    language: str | None = Field(default=None, description="Optional preferred response language, such as 'en' or 'es'.")


def _client_identifier(request: Request) -> str:
    """Return the best available client identifier for MVP rate limiting."""
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip() or "unknown-forwarded-client"

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown-client"


def _apply_ask_rate_limit(request: Request) -> RateLimitDecision | None:
    """Apply the configured in-memory limiter to /ask requests."""
    if not settings.rate_limit_enabled:
        return None

    decision = ask_rate_limiter.check(_client_identifier(request))
    if not decision.allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded for /ask. Please slow down and try again shortly.",
            headers={
                "Retry-After": str(decision.retry_after_seconds),
                "X-RateLimit-Limit": str(decision.limit),
                "X-RateLimit-Remaining": str(decision.remaining),
            },
        )
    return decision


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


def _dedupe_citations(citations: list[Citation]) -> list[Citation]:
    seen: set[str] = set()
    output: list[Citation] = []
    for citation in citations:
        key = f"{citation.source_id}:{citation.url}"
        if key in seen:
            continue
        seen.add(key)
        output.append(citation)
    return output


def _truncate_text(text: str, max_length: int = 900) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_length:
        return normalized
    return f"{normalized[: max_length - 1].rstrip()}…"


def _split_sentences(text: str) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []
    raw_sentences = []
    for part in normalized.replace("\n", " ").split(". "):
        sentence = part.strip(" .")
        if len(sentence) >= 45:
            raw_sentences.append(f"{sentence}.")
    return raw_sentences


def _sentences_matching(results: list[dict[str, Any]], hints: set[str], limit: int) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for result in results:
        for sentence in _split_sentences(str(result.get("text") or "")):
            lowered = sentence.lower()
            if any(hint in lowered for hint in hints):
                cleaned = _truncate_text(sentence, max_length=220)
                if cleaned not in seen:
                    seen.add(cleaned)
                    output.append(cleaned)
            if len(output) >= limit:
                return output
    return output


def _latest_fetched_at(citations: list[Citation]) -> str | None:
    fetched_values = sorted([citation.fetched_at for citation in citations if citation.fetched_at], reverse=True)
    return fetched_values[0] if fetched_values else None


def _related_agencies_from_sources(sources: list[AnswerSource]) -> list[RelatedAgency]:
    agencies: list[RelatedAgency] = []
    for source in sources:
        agencies.append(
            RelatedAgency(
                source_id=source.source_id,
                name=source.source_name,
                category=source.category,
                url=source.url,
                trust_level=source.trust_level,
            )
        )
    return agencies[:5]


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


def _build_official_source_warning(language: str, high_risk: bool, citations: list[Citation]) -> str | None:
    if not high_risk:
        return None
    has_official = any(citation.trust_level == "official" for citation in citations)
    if language == "es":
        if has_official:
            return "Tema sensible: usa solamente las fuentes oficiales citadas para confirmar requisitos, fechas, costos o instrucciones antes de actuar."
        return "Tema sensible: no hay suficientes citas oficiales en el corpus para dar una respuesta completa. No se deben inventar requisitos, fechas, costos ni instrucciones."
    if has_official:
        return "Sensitive topic: use the cited official sources to verify requirements, dates, fees, or instructions before acting."
    return "Sensitive topic: there are not enough official citations in the corpus to give a complete answer. Do not infer requirements, dates, fees, or instructions."


def _build_direct_answer(language: str, source_name: str, excerpt: str) -> str:
    if language == "es":
        return (
            f"Encontré evidencia relevante en {source_name}. "
            "La respuesta todavía es extractiva y debe verificarse con las citas oficiales antes de actuar. "
            f"Fragmento principal: {_truncate_text(excerpt, max_length=360)}"
        )
    return (
        f"I found relevant evidence from {source_name}. "
        "This is still an extractive MVP answer and should be verified against the cited official sources before acting. "
        f"Key excerpt: {_truncate_text(excerpt, max_length=360)}"
    )


def _build_structured_answer(
    question: str,
    language: str,
    results: list[dict[str, Any]],
    citations: list[Citation],
    sources: list[AnswerSource],
    confidence: str,
    high_risk: bool,
    ingestion_status: dict[str, Any],
) -> StructuredAnswer:
    if not results:
        direct_answer = _build_fallback_answer(language=language, high_risk=high_risk, ingestion_status=ingestion_status)
        return StructuredAnswer(
            direct_answer=direct_answer,
            steps_to_follow=[],
            requirements=[],
            official_citations=[],
            last_updated=None,
            confidence=confidence,
            related_agencies=_related_agencies_from_sources(sources),
            official_source_warning=_build_official_source_warning(language, high_risk, []),
        )

    top_result = results[0]
    source_name = str(top_result.get("source_name") or "a Puerto Rico source")
    excerpt = str(top_result.get("text") or "")
    official_citations = [citation for citation in citations if citation.trust_level == "official"] or citations
    steps = _sentences_matching(results, STEP_HINTS, limit=5)
    requirements = _sentences_matching(results, REQUIREMENT_HINTS, limit=5)

    if not steps:
        steps = [
            "Open the cited official source.",
            "Review the page for current requirements and instructions.",
            "Contact the related agency if the page does not clearly answer your situation.",
        ]
        if language == "es":
            steps = [
                "Abre la fuente oficial citada.",
                "Revisa la página para confirmar requisitos e instrucciones vigentes.",
                "Contacta la agencia relacionada si la página no responde claramente tu situación.",
            ]

    if not requirements:
        requirements = [
            "No specific requirements were safely extracted from the current evidence. Verify the cited official page before acting."
        ]
        if language == "es":
            requirements = [
                "No se extrajeron requisitos específicos con suficiente seguridad. Verifica la página oficial citada antes de actuar."
            ]

    return StructuredAnswer(
        direct_answer=_build_direct_answer(language, source_name, excerpt),
        steps_to_follow=steps,
        requirements=requirements,
        official_citations=official_citations[:3],
        last_updated=_latest_fetched_at(citations),
        confidence=confidence,
        related_agencies=_related_agencies_from_sources(sources),
        official_source_warning=_build_official_source_warning(language, high_risk, citations),
    )


def _build_answer_text(structured_answer: StructuredAnswer, language: str) -> str:
    if language == "es":
        parts = [f"Respuesta directa: {structured_answer.direct_answer}"]
        if structured_answer.steps_to_follow:
            parts.append("Pasos a seguir: " + " | ".join(structured_answer.steps_to_follow[:3]))
        if structured_answer.requirements:
            parts.append("Requisitos: " + " | ".join(structured_answer.requirements[:3]))
        if structured_answer.official_source_warning:
            parts.append(f"Nota: {structured_answer.official_source_warning}")
        return "\n\n".join(parts)

    parts = [f"Direct answer: {structured_answer.direct_answer}"]
    if structured_answer.steps_to_follow:
        parts.append("Steps to follow: " + " | ".join(structured_answer.steps_to_follow[:3]))
    if structured_answer.requirements:
        parts.append("Requirements: " + " | ".join(structured_answer.requirements[:3]))
    if structured_answer.official_source_warning:
        parts.append(f"Note: {structured_answer.official_source_warning}")
    return "\n\n".join(parts)


def _build_fallback_answer(language: str, high_risk: bool, ingestion_status: dict[str, Any]) -> str:
    warnings = ingestion_status.get("warnings") or []
    readiness_note = f" Current corpus warnings: {' '.join(warnings)}" if warnings else ""

    if language == "es":
        if high_risk:
            return (
                "Todavía no encontré evidencia suficiente en las fuentes oficiales ingeridas para responder esta pregunta con seguridad. "
                "Para temas de permisos, impuestos, salud, emergencias, beneficios públicos, policía, tribunales o inmigración, SanJuan AI no debe adivinar."
                f"{readiness_note}"
            )
        return (
            "Todavía no encontré evidencia suficiente en los documentos ingeridos para responder con citas. "
            "Prueba ejecutar la ingestión, el chunking y el vector build, o agrega más fuentes relevantes al registro."
            f"{readiness_note}"
        )

    if high_risk:
        return (
            "I did not find enough evidence in the ingested official sources to answer this safely. "
            "For permits, taxes, health, emergency, public benefits, police, court, legal, or immigration topics, SanJuan AI should not guess."
            f"{readiness_note}"
        )
    return (
        "I did not find enough evidence in the ingested documents to answer with citations yet. "
        "Try running ingestion, chunking, and vector build, or add more relevant sources to the registry."
        f"{readiness_note}"
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
def health() -> dict[str, Any]:
    """Health check endpoint for deployment and monitoring."""
    return {
        "status": "ok",
        "service": "sanjuan-ai-api",
        "environment": settings.environment,
        "cors_configured": bool(settings.cors_origins),
        "rate_limit_enabled": settings.rate_limit_enabled,
        "ask_rate_limit_per_minute": settings.ask_rate_limit_per_minute,
        "corpus": build_corpus_status_dict(),
    }


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
def ask(request: AskRequest, http_request: Request, response: Response) -> AskAnswer:
    """Return a structured, citation-first answer using hybrid local retrieval."""
    rate_limit_decision = _apply_ask_rate_limit(http_request)
    if rate_limit_decision is not None:
        response.headers["X-RateLimit-Limit"] = str(rate_limit_decision.limit)
        response.headers["X-RateLimit-Remaining"] = str(rate_limit_decision.remaining)

    language = _detect_language(request.question, request.language)
    high_risk = _is_high_risk_question(request.question)
    ingestion_status_payload = build_corpus_status_dict()
    ingestion_status = IngestionStatus(**ingestion_status_payload)
    results = search_hybrid(
        query=request.question,
        limit=5,
    )

    citations = [citation for result in results if (citation := _retrieval_result_to_citation(result)) is not None]
    citations = _dedupe_citations(citations)
    sources = [source for result in results if (source := _retrieval_result_to_answer_source(result)) is not None]
    sources = _dedupe_sources(sources)

    if not results:
        fallback_sources = []
        if high_risk:
            official_sources = [source for source in _load_sources_or_500() if source.trust_level == "official"][:5]
            fallback_sources = [_source_to_answer_source(source) for source in official_sources]

        structured_answer = _build_structured_answer(
            question=request.question,
            language=language,
            results=[],
            citations=[],
            sources=fallback_sources,
            confidence="low",
            high_risk=high_risk,
            ingestion_status=ingestion_status_payload,
        )
        return AskAnswer(
            answer=_build_answer_text(structured_answer, language),
            language=language,
            confidence="low",
            citations=[],
            sources=fallback_sources,
            safety_note=_build_safety_note(language=language, high_risk=high_risk, has_results=False),
            ingestion_status=ingestion_status,
            structured_answer=structured_answer,
        )

    top_score = float(results[0].get("score") or 0)
    confidence = "high" if top_score >= 0.8 else "medium" if top_score >= 0.45 else "low"
    structured_answer = _build_structured_answer(
        question=request.question,
        language=language,
        results=results,
        citations=citations,
        sources=sources,
        confidence=confidence,
        high_risk=high_risk,
        ingestion_status=ingestion_status_payload,
    )

    return AskAnswer(
        answer=_build_answer_text(structured_answer, language),
        language=language,
        confidence=confidence,
        citations=citations[:3],
        sources=sources[:5],
        safety_note=_build_safety_note(language=language, high_risk=high_risk, has_results=True),
        ingestion_status=ingestion_status,
        structured_answer=structured_answer,
    )
