"""Bilingual retrieval helpers for SanJuan AI.

Puerto Rico public information is often Spanish-first, while users may ask in
English, Spanish, or a mix of both. This module provides deterministic glossary-
based expansion so retrieval can bridge common civic terms without external
translation APIs.
"""

from __future__ import annotations

import unicodedata


BILINGUAL_GLOSSARY: dict[str, tuple[str, ...]] = {
    "business": ("negocio", "empresa", "comerciante", "comercio"),
    "registration": ("registro", "registrar", "inscripcion", "corporaciones"),
    "register": ("registrar", "registro", "inscripcion"),
    "corporation": ("corporacion", "corporaciones", "entidad"),
    "corporations": ("corporaciones", "corporacion", "entidades"),
    "merchant": ("comerciante", "comerciantes", "comercio"),
    "tax": ("impuesto", "impuestos", "hacienda", "contribucion", "contribuyente"),
    "taxes": ("impuestos", "hacienda", "contribuciones", "contribuyente"),
    "permit": ("permiso", "permisos", "autorizacion"),
    "permits": ("permisos", "permiso", "autorizaciones"),
    "license": ("licencia", "licencias"),
    "licenses": ("licencias", "licencia"),
    "driver": ("conductor", "chofer"),
    "transportation": ("transportacion", "dtop", "carreteras", "transito"),
    "health": ("salud", "medico", "hospital", "servicios de salud"),
    "emergency": ("emergencia", "alerta", "avisos", "seguridad"),
    "hurricane": ("huracan", "tormenta", "ciclon", "emergencia"),
    "weather": ("tiempo", "clima", "pronostico", "avisos"),
    "services": ("servicios", "tramites", "gestiones"),
    "service": ("servicio", "tramite", "gestion"),
    "agency": ("agencia", "departamento", "oficina"),
    "agencies": ("agencias", "departamentos", "oficinas"),
    "requirements": ("requisitos", "requerimientos", "documentos"),
    "requirement": ("requisito", "documento requerido"),
    "form": ("formulario", "solicitud"),
    "forms": ("formularios", "solicitudes"),
    "payment": ("pago", "pagos"),
    "fee": ("cargo", "costo", "pago", "tarifa"),
    "municipal": ("municipal", "municipio", "ayuntamiento"),
    "san": ("san"),
    "juan": ("juan"),
    "puerto": ("puerto"),
    "rico": ("rico"),
    "negocio": ("business", "company", "enterprise", "merchant"),
    "empresa": ("business", "company", "enterprise"),
    "comerciante": ("merchant", "business", "taxpayer"),
    "comerciantes": ("merchants", "businesses", "taxpayers"),
    "registro": ("registration", "registry", "register"),
    "registrar": ("register", "registration", "file"),
    "inscripcion": ("registration", "enrollment"),
    "corporaciones": ("corporations", "corporate registry", "entities"),
    "corporacion": ("corporation", "company", "entity"),
    "impuesto": ("tax", "treasury"),
    "impuestos": ("taxes", "treasury", "hacienda"),
    "hacienda": ("treasury", "tax", "taxes"),
    "contribuyente": ("taxpayer", "tax"),
    "permiso": ("permit", "permission", "authorization"),
    "permisos": ("permits", "permissions", "authorizations"),
    "licencia": ("license", "permit"),
    "licencias": ("licenses", "permits"),
    "salud": ("health", "medical", "hospital"),
    "emergencia": ("emergency", "alert", "safety"),
    "huracan": ("hurricane", "storm", "emergency"),
    "clima": ("weather", "forecast"),
    "tiempo": ("weather", "forecast"),
    "pronostico": ("forecast", "weather"),
    "servicio": ("service", "public service"),
    "servicios": ("services", "public services"),
    "tramite": ("procedure", "service", "filing"),
    "tramites": ("procedures", "services", "filings"),
    "agencia": ("agency", "department", "office"),
    "agencias": ("agencies", "departments", "offices"),
    "requisito": ("requirement", "required document"),
    "requisitos": ("requirements", "required documents"),
    "formulario": ("form", "application"),
    "formularios": ("forms", "applications"),
    "pago": ("payment", "fee"),
    "pagos": ("payments", "fees"),
    "municipio": ("municipality", "municipal", "city"),
}


def strip_accents(value: str) -> str:
    """Remove accents while preserving ASCII-friendly matching."""
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(character for character in normalized if not unicodedata.combining(character))


def normalize_for_bilingual(value: str | None) -> str:
    """Normalize text for bilingual matching and glossary lookup."""
    if not value:
        return ""
    return strip_accents(value).lower().strip()


def expand_terms(tokens: list[str], max_terms: int = 80) -> list[str]:
    """Expand tokens with bilingual glossary equivalents."""
    expanded: list[str] = []
    seen: set[str] = set()

    for token in tokens:
        normalized = normalize_for_bilingual(token)
        candidates = (normalized, *BILINGUAL_GLOSSARY.get(normalized, ()))
        for candidate in candidates:
            for part in normalize_for_bilingual(candidate).split():
                if len(part) <= 1 or part in seen:
                    continue
                seen.add(part)
                expanded.append(part)
                if len(expanded) >= max_terms:
                    return expanded

    return expanded


def expand_query_text(query: str, max_terms: int = 80) -> str:
    """Return the original query plus bilingual expansion terms."""
    from packages.retrieval.keyword_search import tokenize

    tokens = tokenize(query)
    expanded = expand_terms(tokens, max_terms=max_terms)
    return " ".join([query, *expanded]).strip()


def expand_document_text(text: str, metadata_terms: list[str] | None = None, max_terms: int = 120) -> str:
    """Return document text enriched with bilingual terms derived from text and metadata."""
    from packages.retrieval.keyword_search import tokenize

    tokens = tokenize(" ".join([text, *(metadata_terms or [])]))
    expanded = expand_terms(tokens, max_terms=max_terms)
    return " ".join([text, *expanded]).strip()
