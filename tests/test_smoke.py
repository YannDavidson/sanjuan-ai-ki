"""Local development smoke tests for the SanJuan AI MVP.

These tests intentionally avoid network access and do not require generated corpus
artifacts. They protect imports, source validation, retrieval fallbacks, and the
FastAPI response contract.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.ingestion.corpus_status import build_corpus_status
from packages.ingestion.load_sources import load_sources
from packages.retrieval.hybrid_search import search_hybrid
from packages.retrieval.keyword_search import search_chunks
from packages.shared.answer_schema import AskAnswer


def test_source_registry_loads_registered_sources() -> None:
    sources = load_sources()

    assert len(sources) >= 10
    assert any(source.id == "pr_gov_main" for source in sources)
    assert all(source.id for source in sources)
    assert all(source.url for source in sources)


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


def test_fastapi_health_endpoint_includes_corpus_status() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "sanjuan-ai-api"
    assert "corpus" in payload
    assert "ready_for_keyword_retrieval" in payload["corpus"]


def test_fastapi_sources_endpoint_returns_registry() -> None:
    client = TestClient(app)
    response = client.get("/sources")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 10
    assert any(source["id"] == "pr_gov_main" for source in payload["sources"])


def test_fastapi_ask_endpoint_matches_answer_contract() -> None:
    client = TestClient(app)
    response = client.post("/ask", json={"question": "business registration Puerto Rico", "language": "en"})

    assert response.status_code == 200
    answer = AskAnswer(**response.json())
    assert answer.answer
    assert answer.language == "en"
    assert answer.confidence in {"high", "medium", "low", "placeholder"}
    assert answer.ingestion_status is not None
