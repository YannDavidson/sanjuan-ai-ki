"""Local development smoke tests for the SanJuan AI MVP.

These tests intentionally avoid network access and do not require generated corpus
artifacts. They protect imports, source validation, retrieval fallbacks, and the
FastAPI response contract.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.config import DEFAULT_DEV_CORS_ORIGINS, load_api_settings, parse_bool_env, parse_csv_env, parse_int_env
from apps.api.main import app
from apps.api.rate_limit import InMemoryRateLimiter
from packages.ingestion.agency_loaders import build_priority_urls, get_agency_loader_profile, list_agency_loader_profiles
from packages.ingestion.corpus_status import build_corpus_status
from packages.ingestion.load_sources import load_sources
from packages.ingestion.refresh_corpus import refresh_corpus
from packages.ingestion.safe_crawler import document_id_for_url, is_url_allowed, normalize_url
from packages.retrieval.hybrid_search import search_hybrid
from packages.retrieval.keyword_search import search_chunks
from packages.shared.answer_schema import AskAnswer
from packages.shared.source_schema import CrawlRules


def test_source_registry_loads_registered_sources() -> None:
    sources = load_sources()

    assert len(sources) >= 10
    assert any(source.id == "pr_gov_main" for source in sources)
    assert all(source.id for source in sources)
    assert all(source.url for source in sources)


def test_source_registry_loads_crawl_rules() -> None:
    sources = load_sources()
    pr_gov = next(source for source in sources if source.id == "pr_gov_main")

    assert pr_gov.crawl is not None
    assert pr_gov.crawl.enabled is True
    assert pr_gov.crawl.max_pages_per_source == 10
    assert "/servicios" in pr_gov.crawl.allowed_paths
    assert "/login" in pr_gov.crawl.blocked_paths


def test_agency_loader_profiles_cover_high_value_sources() -> None:
    expected_source_ids = {
        "pr_gov_main",
        "pr_hacienda",
        "pr_dtop",
        "pr_salud",
        "pr_estado",
        "pr_ddec",
        "san_juan_municipio",
        "nws_san_juan",
    }
    profiles = list_agency_loader_profiles()

    assert {profile.source_id for profile in profiles} == expected_source_ids
    assert get_agency_loader_profile("pr_hacienda") is not None
    assert get_agency_loader_profile("census_api") is None
    assert all(profile.priority_paths for profile in profiles)


def test_agency_loader_priority_urls_are_same_domain_and_curated() -> None:
    sources = load_sources()
    pr_gov = next(source for source in sources if source.id == "pr_gov_main")
    profile = get_agency_loader_profile("pr_gov_main")

    assert profile is not None
    urls = build_priority_urls(pr_gov, profile)

    assert "https://www.pr.gov/servicios" in urls
    assert "https://www.pr.gov/agencias" in urls
    assert all(url.startswith("https://www.pr.gov") for url in urls)


def test_safe_crawler_url_normalization_and_rules() -> None:
    base_url = "https://www.pr.gov/"
    rules = CrawlRules(
        enabled=True,
        max_pages_per_source=10,
        allowed_paths=["/servicios", "tramites"],
        blocked_paths=["/login", "/admin"],
    )

    normalized = normalize_url(base_url, "/servicios/licencias?utm_source=test#section")

    assert normalized == "https://www.pr.gov/servicios/licencias"
    assert is_url_allowed(normalized, base_url, rules) is True
    assert is_url_allowed("https://www.pr.gov/tramites", base_url, rules) is True
    assert is_url_allowed("https://www.pr.gov/login", base_url, rules) is False
    assert is_url_allowed("https://www.pr.gov/search", base_url, rules) is False
    assert is_url_allowed("https://www.pr.gov/noticias", base_url, rules) is False
    assert is_url_allowed("https://example.com/servicios", base_url, rules) is False
    assert normalize_url(base_url, "mailto:info@example.com") is None
    assert document_id_for_url("pr_gov_main", "https://www.pr.gov/servicios/licencias").startswith(
        "pr_gov_main__servicios-licencias-"
    )


def test_api_settings_parse_cors_origins(monkeypatch) -> None:
    monkeypatch.setenv("SANJUAN_ENV", "production")
    monkeypatch.setenv("SANJUAN_CORS_ORIGINS", "https://sanjuan-ai.example.com, https://www.sanjuan-ai.example.com")
    settings = load_api_settings()

    assert settings.is_production is True
    assert settings.cors_origins == ("https://sanjuan-ai.example.com", "https://www.sanjuan-ai.example.com")
    assert parse_csv_env("a, b,,c") == ("a", "b", "c")


def test_api_settings_default_dev_cors(monkeypatch) -> None:
    monkeypatch.delenv("SANJUAN_ENV", raising=False)
    monkeypatch.delenv("SANJUAN_CORS_ORIGINS", raising=False)
    settings = load_api_settings()

    assert settings.environment == "development"
    assert settings.cors_origins == DEFAULT_DEV_CORS_ORIGINS


def test_api_settings_parse_rate_limit_env(monkeypatch) -> None:
    monkeypatch.setenv("SANJUAN_RATE_LIMIT_ENABLED", "false")
    monkeypatch.setenv("SANJUAN_ASK_RATE_LIMIT_PER_MINUTE", "5")
    settings = load_api_settings()

    assert settings.rate_limit_enabled is False
    assert settings.ask_rate_limit_per_minute == 5
    assert parse_bool_env("yes") is True
    assert parse_bool_env("off", default=True) is False
    assert parse_int_env("bad", default=7, minimum=1) == 7
    assert parse_int_env("0", default=7, minimum=1) == 1


def test_in_memory_rate_limiter_blocks_after_limit() -> None:
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)

    first = limiter.check("client-a", now=100.0)
    second = limiter.check("client-a", now=101.0)
    third = limiter.check("client-a", now=102.0)
    later = limiter.check("client-a", now=161.1)

    assert first.allowed is True
    assert second.allowed is True
    assert third.allowed is False
    assert third.retry_after_seconds > 0
    assert later.allowed is True


def test_corpus_status_handles_missing_directories(tmp_path: Path) -> None:
    status = build_corpus_status(
        raw_dir=tmp_path / "missing-raw",
        chunks_dir=tmp_path / "missing-chunks",
        vectors_dir=tmp_path / "missing-vectors",
    )

    assert status.ready_for_keyword_retrieval is False
    assert status.ready_for_vector_retrieval is False
    assert status.raw_documents_count == 0
    assert status.chunks_count == 0
    assert status.vectors_count == 0
    assert status.warnings


def test_keyword_search_returns_safe_empty_results_for_missing_chunks(tmp_path: Path) -> None:
    results = search_chunks(query="business registration Puerto Rico", chunks_dir=tmp_path / "chunks")

    assert results == []


def test_hybrid_search_returns_safe_empty_results_for_missing_artifacts(tmp_path: Path) -> None:
    results = search_hybrid(
        query="business registration Puerto Rico",
        chunks_dir=tmp_path / "chunks",
        vectors_dir=tmp_path / "vectors",
    )

    assert results == []


def test_refresh_corpus_dry_run_avoids_network_and_writes(tmp_path: Path) -> None:
    summary = refresh_corpus(
        raw_dir=tmp_path / "raw",
        chunks_dir=tmp_path / "chunks",
        vectors_dir=tmp_path / "vectors",
        status_path=tmp_path / "status" / "source_status.json",
        refresh_log_path=tmp_path / "status" / "last_refresh.json",
        dry_run=True,
    )

    assert summary["mode"] == "dry_run"
    assert summary["network_required"] is False
    assert summary["writes_artifacts"] is False
    assert summary["would_require_network"] is True
    assert summary["would_write_artifacts"] is True
    assert not (tmp_path / "raw").exists()
    assert not (tmp_path / "status" / "last_refresh.json").exists()


def test_fastapi_health_endpoint_includes_corpus_status_and_security_headers() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "sanjuan-ai-api"
    assert "environment" in payload
    assert "cors_configured" in payload
    assert "rate_limit_enabled" in payload
    assert "ask_rate_limit_per_minute" in payload
    assert "corpus" in payload
    assert "ready_for_keyword_retrieval" in payload["corpus"]


def test_fastapi_sources_endpoint_returns_registry() -> None:
    client = TestClient(app)
    response = client.get("/sources")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 10
    assert any(source["id"] == "pr_gov_main" for source in payload["sources"])


def test_fastapi_ask_endpoint_matches_answer_contract_and_rate_limit_headers() -> None:
    client = TestClient(app)
    response = client.post("/ask", json={"question": "business registration Puerto Rico", "language": "en"})

    assert response.status_code == 200
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    answer = AskAnswer(**response.json())
    assert answer.answer
    assert answer.language == "en"
    assert answer.confidence in {"high", "medium", "low", "placeholder"}
    assert answer.ingestion_status is not None
