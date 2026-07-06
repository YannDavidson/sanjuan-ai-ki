"""Agency-specific loader profiles for high-value Puerto Rico sources.

These loaders focus ingestion on predictable public-service sections of official
Puerto Rico sources while preserving the same raw document format used by the
rest of SanJuan AI.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin

from packages.ingestion.fetch_static_page import StaticPageFetchError
from packages.ingestion.safe_crawler import build_document_payload, fetch_page_with_links, is_url_allowed, normalize_url
from packages.shared.source_schema import CrawlRules, Source


@dataclass(frozen=True)
class AgencyLoaderProfile:
    """Configuration for one agency-specific loader."""

    source_id: str
    agency_name: str
    priority_paths: tuple[str, ...]
    blocked_paths: tuple[str, ...] = ("/login", "/admin", "/search", "/calendar")
    max_pages: int = 10
    extraction_hints: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""


AGENCY_LOADER_PROFILES: dict[str, AgencyLoaderProfile] = {
    "pr_gov_main": AgencyLoaderProfile("pr_gov_main", "PR.gov", ("/servicios", "/agencias", "/directorio", "/tramites"), extraction_hints=("services", "agency directory", "government procedures"), notes="Central government portal."),
    "pr_hacienda": AgencyLoaderProfile("pr_hacienda", "Departamento de Hacienda", ("/servicios", "/comerciantes", "/contribuyentes", "/publicaciones"), extraction_hints=("merchant registration", "taxpayer services", "publications"), notes="Tax and treasury source."),
    "pr_dtop": AgencyLoaderProfile("pr_dtop", "Departamento de Transportación y Obras Públicas", ("/servicios", "/tramites", "/licencias", "/avisos"), extraction_hints=("licenses", "transportation services", "public notices"), notes="Transportation source."),
    "pr_salud": AgencyLoaderProfile("pr_salud", "Departamento de Salud", ("/servicios", "/programas", "/avisos", "/informacion"), extraction_hints=("health services", "programs", "public health notices"), notes="Health source. High-risk topic; official-only."),
    "pr_estado": AgencyLoaderProfile("pr_estado", "Departamento de Estado", ("/servicios", "/corporaciones", "/tramites", "/registros"), extraction_hints=("corporations", "registries", "certificates", "business filings"), notes="Business registration and corporate registry source."),
    "pr_ddec": AgencyLoaderProfile("pr_ddec", "Departamento de Desarrollo Económico y Comercio", ("/servicios", "/programas", "/incentivos", "/emprendimiento"), extraction_hints=("economic incentives", "entrepreneurship", "business support programs"), notes="Economic development source."),
    "san_juan_municipio": AgencyLoaderProfile("san_juan_municipio", "Municipio de San Juan", ("/servicios", "/permisos", "/municipio", "/avisos"), extraction_hints=("municipal services", "permits", "announcements"), notes="Municipal source."),
    "nws_san_juan": AgencyLoaderProfile("nws_san_juan", "National Weather Service San Juan", ("/sju", "/safety", "/wrn"), blocked_paths=("/login", "/admin", "/search", "/calendar", "/source"), max_pages=8, extraction_hints=("forecast office", "weather safety", "warnings"), notes="Weather and hazard source."),
}


def get_agency_loader_profile(source_id: str) -> AgencyLoaderProfile | None:
    """Return an agency loader profile for a source, if one exists."""
    return AGENCY_LOADER_PROFILES.get(source_id)


def list_agency_loader_profiles() -> list[AgencyLoaderProfile]:
    """Return all agency loader profiles sorted by source id."""
    return [AGENCY_LOADER_PROFILES[key] for key in sorted(AGENCY_LOADER_PROFILES)]


def crawl_rules_for_profile(profile: AgencyLoaderProfile, max_pages_override: int | None = None) -> CrawlRules:
    """Convert a profile into crawl rules understood by the safe crawler."""
    return CrawlRules(
        enabled=True,
        max_pages_per_source=max_pages_override or profile.max_pages,
        allowed_paths=list(profile.priority_paths),
        blocked_paths=list(profile.blocked_paths),
    )


def build_priority_urls(source: Source, profile: AgencyLoaderProfile) -> list[str]:
    """Build normalized homepage + profile-priority URLs for an agency source."""
    base_url = normalize_url(str(source.url), str(source.url)) or str(source.url)
    rules = crawl_rules_for_profile(profile)
    urls: list[str] = []
    seen: set[str] = set()

    for href in ("/", *profile.priority_paths):
        candidate = normalize_url(base_url, urljoin(base_url, href))
        if not candidate or not is_url_allowed(candidate, base_url, rules) or candidate in seen:
            continue
        seen.add(candidate)
        urls.append(candidate)

    return urls


def load_agency_source(source: Source, timeout_seconds: int = 20, max_pages_override: int | None = None) -> dict[str, Any]:
    """Load a source using its agency-specific profile."""
    profile = get_agency_loader_profile(source.id)
    if profile is None:
        raise ValueError(f"No agency loader profile exists for source {source.id}")

    rules = crawl_rules_for_profile(profile, max_pages_override=max_pages_override)
    max_pages = rules.max_pages_per_source
    base_url = normalize_url(str(source.url), str(source.url)) or str(source.url)
    queue: deque[tuple[str, int]] = deque((url, 0) for url in build_priority_urls(source, profile))
    seen: set[str] = set()
    documents: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    while queue and len(documents) < max_pages:
        url, depth = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        if not is_url_allowed(url, base_url, rules):
            continue

        try:
            page = fetch_page_with_links(url, rules=rules, timeout_seconds=timeout_seconds)
        except StaticPageFetchError as exc:
            errors.append({"url": url, "error": str(exc), "depth": depth})
            continue

        document = build_document_payload(source, page, crawl_depth=depth)
        document["loader"] = {
            "type": "agency_specific",
            "agency_name": profile.agency_name,
            "profile_source_id": profile.source_id,
            "extraction_hints": list(profile.extraction_hints),
            "notes": profile.notes,
        }
        documents.append(document)

        for link in page.get("links", []):
            if link not in seen and len(seen) + len(queue) < max_pages * 4:
                queue.append((link, depth + 1))

    return {
        "source_id": source.id,
        "agency_name": profile.agency_name,
        "max_pages": max_pages,
        "documents": documents,
        "errors": errors,
        "visited_count": len(seen),
        "profile": {
            "priority_paths": list(profile.priority_paths),
            "blocked_paths": list(profile.blocked_paths),
            "extraction_hints": list(profile.extraction_hints),
            "notes": profile.notes,
        },
    }
