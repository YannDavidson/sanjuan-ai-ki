"""Retrieval tests that use committed demo corpus fixtures.

These tests verify real retrieval behavior without fetching live websites.
"""

from __future__ import annotations

from pathlib import Path

from packages.retrieval.bilingual import expand_query_text, normalize_for_bilingual
from packages.retrieval.hybrid_search import search_hybrid
from packages.retrieval.keyword_search import RetrievalFilters, search_chunks
from packages.retrieval.local_vector_search import build_vector_store, search_vectors

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "corpus"
CHUNKS_DIR = FIXTURES_DIR / "chunks"


def test_bilingual_query_expansion_adds_spanish_terms() -> None:
    expanded = expand_query_text("business registration Puerto Rico")

    assert "business" in expanded
    assert "registro" in expanded
    assert "negocio" in expanded
    assert "corporaciones" in expanded
    assert normalize_for_bilingual("trámites") == "tramites"


def test_bilingual_query_expansion_adds_english_terms() -> None:
    expanded = expand_query_text("permisos San Juan")

    assert "permisos" in expanded
    assert "permits" in expanded
    assert "permit" in expanded


def test_keyword_retrieval_finds_demo_business_registration_fixture() -> None:
    results = search_chunks(
        query="business registration Puerto Rico Department of State",
        chunks_dir=CHUNKS_DIR,
        limit=3,
    )

    assert results
    top = results[0]
    assert top["source_id"] == "demo_pr_business"
    assert top["trust_level"] == "official"
    assert "business registration" in top["text"].lower()
    assert top["citation"]["url"] == "https://example.test/puerto-rico-business-registration"


def test_keyword_retrieval_supports_spanish_query_against_english_fixture() -> None:
    results = search_chunks(
        query="registro de negocio comerciante corporaciones Puerto Rico",
        chunks_dir=CHUNKS_DIR,
        limit=3,
    )

    assert results
    assert results[0]["source_id"] == "demo_pr_business"
    assert "query_expansion" in results[0]


def test_keyword_retrieval_respects_fixture_filters() -> None:
    results = search_chunks(
        query="business registration Puerto Rico",
        chunks_dir=CHUNKS_DIR,
        filters=RetrievalFilters(category="business_registration", trust_level="official", geography="puerto_rico", language="en"),
        limit=3,
    )

    assert results
    assert all(result["category"] == "business_registration" for result in results)
    assert all(result["trust_level"] == "official" for result in results)


def test_local_vector_retrieval_can_be_built_from_fixture(tmp_path: Path) -> None:
    vectors_dir = tmp_path / "vectors"
    summary = build_vector_store(chunks_dir=CHUNKS_DIR, vectors_dir=vectors_dir, dimensions=64, pretty=True)

    assert summary["documents_seen"] == 1
    assert summary["documents_vectorized"] == 1
    assert summary["total_vectors"] == 2
    assert summary["bilingual_expansion"] is True

    results = search_vectors(query="Puerto Rico permits and merchant requirements", vectors_dir=vectors_dir, limit=3)

    assert results
    assert any(result["source_id"] == "demo_pr_business" for result in results)


def test_local_vector_retrieval_supports_spanish_query_against_english_fixture(tmp_path: Path) -> None:
    vectors_dir = tmp_path / "vectors"
    build_vector_store(chunks_dir=CHUNKS_DIR, vectors_dir=vectors_dir, dimensions=64)

    results = search_vectors(query="requisitos comerciante registro negocio", vectors_dir=vectors_dir, limit=3)

    assert results
    assert any(result["source_id"] == "demo_pr_business" for result in results)
    assert "query_expansion" in results[0]


def test_hybrid_retrieval_combines_fixture_keyword_and_vector_results(tmp_path: Path) -> None:
    vectors_dir = tmp_path / "vectors"
    build_vector_store(chunks_dir=CHUNKS_DIR, vectors_dir=vectors_dir, dimensions=64)

    results = search_hybrid(
        query="Puerto Rico business registration permits",
        chunks_dir=CHUNKS_DIR,
        vectors_dir=vectors_dir,
        limit=5,
    )

    assert results
    assert results[0]["source_id"] == "demo_pr_business"
    assert "score_components" in results[0]
    assert results[0]["retrieval_methods"]
    assert results[0]["citation"]["source_id"] == "demo_pr_business"
