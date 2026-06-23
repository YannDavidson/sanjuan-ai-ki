"""Hybrid retrieval for SanJuan AI.

This module combines transparent keyword retrieval with the local vector-search
scaffold. It is intentionally file-based and inspectable for the MVP.

Run after ingestion, chunking, and optional vector building:

    python -m packages.retrieval.hybrid_search "business registration Puerto Rico" --pretty

Hybrid search still works when vector files are missing. In that case it falls
back to keyword-only results and marks the retrieval mode accordingly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from packages.retrieval.keyword_search import DEFAULT_CHUNKS_DIR, DEFAULT_LIMIT, RetrievalFilters, load_chunks, search_chunks
from packages.retrieval.local_vector_search import DEFAULT_VECTORS_DIR, search_vectors

KEYWORD_WEIGHT = 0.65
VECTOR_WEIGHT = 0.35


def _safe_float(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _normalize_score(score: float, max_score: float) -> float:
    if max_score <= 0:
        return 0.0
    return max(min(score / max_score, 1.0), 0.0)


def _chunk_index(chunks_dir: Path = DEFAULT_CHUNKS_DIR) -> dict[str, dict[str, Any]]:
    """Return chunks keyed by chunk ID for vector-result enrichment."""
    indexed: dict[str, dict[str, Any]] = {}
    for chunk in load_chunks(chunks_dir):
        chunk_id = chunk.get("chunk_id")
        if chunk_id:
            indexed[str(chunk_id)] = chunk
    return indexed


def _enrich_vector_result(result: dict[str, Any], chunks_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Add chunk text/fetched metadata to vector-only results when available."""
    chunk_id = str(result.get("chunk_id") or "")
    chunk = chunks_by_id.get(chunk_id, {})
    citation = result.get("citation") or chunk.get("citation") or {}

    enriched = {
        **result,
        "text": chunk.get("text") or result.get("text") or "",
        "fetched_at": chunk.get("fetched_at") or result.get("fetched_at"),
        "content_hash": chunk.get("content_hash") or result.get("content_hash"),
        "source_type": chunk.get("source_type") or result.get("source_type"),
        "citation": {
            "title": citation.get("title") or result.get("title") or chunk.get("title"),
            "url": citation.get("url") or result.get("source_url") or chunk.get("source_url"),
            "source_id": citation.get("source_id") or result.get("source_id") or chunk.get("source_id"),
            "source_name": citation.get("source_name") or result.get("source_name") or chunk.get("source_name"),
        },
    }
    return enriched


def _merge_results(keyword_results: list[dict[str, Any]], vector_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate and combine retrieval scores by chunk ID."""
    max_keyword_score = max((_safe_float(result.get("score")) for result in keyword_results), default=0.0)
    max_vector_score = max((_safe_float(result.get("score")) for result in vector_results), default=0.0)
    merged: dict[str, dict[str, Any]] = {}

    for result in keyword_results:
        chunk_id = str(result.get("chunk_id") or result.get("document_id") or len(merged))
        keyword_score = _safe_float(result.get("score"))
        merged[chunk_id] = {
            **result,
            "chunk_id": chunk_id,
            "keyword_score": keyword_score,
            "vector_score": 0.0,
            "retrieval_methods": ["keyword"],
        }

    for result in vector_results:
        chunk_id = str(result.get("chunk_id") or result.get("document_id") or f"vector-{len(merged)}")
        vector_score = _safe_float(result.get("score"))
        if chunk_id in merged:
            merged[chunk_id]["vector_score"] = max(_safe_float(merged[chunk_id].get("vector_score")), vector_score)
            methods = set(merged[chunk_id].get("retrieval_methods") or [])
            methods.add("vector")
            merged[chunk_id]["retrieval_methods"] = sorted(methods)
        else:
            merged[chunk_id] = {
                **result,
                "chunk_id": chunk_id,
                "keyword_score": 0.0,
                "vector_score": vector_score,
                "retrieval_methods": ["vector"],
            }

    output: list[dict[str, Any]] = []
    for item in merged.values():
        keyword_norm = _normalize_score(_safe_float(item.get("keyword_score")), max_keyword_score)
        vector_norm = _normalize_score(_safe_float(item.get("vector_score")), max_vector_score)
        hybrid_score = (keyword_norm * KEYWORD_WEIGHT) + (vector_norm * VECTOR_WEIGHT)

        # A tiny bonus rewards agreement across both methods without overpowering relevance.
        if {"keyword", "vector"}.issubset(set(item.get("retrieval_methods") or [])):
            hybrid_score += 0.05

        item["score"] = round(hybrid_score, 6)
        item["score_components"] = {
            "keyword_score": round(_safe_float(item.get("keyword_score")), 6),
            "keyword_normalized": round(keyword_norm, 6),
            "vector_score": round(_safe_float(item.get("vector_score")), 6),
            "vector_normalized": round(vector_norm, 6),
            "keyword_weight": KEYWORD_WEIGHT,
            "vector_weight": VECTOR_WEIGHT,
        }
        output.append(item)

    output.sort(key=lambda result: result["score"], reverse=True)
    return output


def search_hybrid(
    query: str,
    chunks_dir: Path = DEFAULT_CHUNKS_DIR,
    vectors_dir: Path = DEFAULT_VECTORS_DIR,
    filters: RetrievalFilters | None = None,
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    """Search chunks with keyword + vector retrieval and return merged evidence."""
    query = query.strip()
    if not query:
        return []

    keyword_limit = max(limit * 2, limit, 1)
    vector_limit = max(limit * 2, limit, 1)

    keyword_results = search_chunks(query=query, chunks_dir=chunks_dir, filters=filters, limit=keyword_limit)
    chunks_by_id = _chunk_index(chunks_dir)
    vector_results = [
        _enrich_vector_result(result, chunks_by_id)
        for result in search_vectors(query=query, vectors_dir=vectors_dir, filters=filters, limit=vector_limit)
    ]

    merged = _merge_results(keyword_results=keyword_results, vector_results=vector_results)
    return merged[: max(limit, 0)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run SanJuan AI hybrid retrieval over local chunks and vectors.")
    parser.add_argument("query", help="Search query.")
    parser.add_argument("--chunks-dir", default=str(DEFAULT_CHUNKS_DIR), help="Directory containing chunk JSON files.")
    parser.add_argument("--vectors-dir", default=str(DEFAULT_VECTORS_DIR), help="Directory containing vector JSON files.")
    parser.add_argument("--category", default=None, help="Optional category filter.")
    parser.add_argument("--trust-level", default=None, help="Optional trust level filter.")
    parser.add_argument("--geography", default=None, help="Optional geography filter.")
    parser.add_argument("--language", default=None, help="Optional language filter.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Maximum results. Default: {DEFAULT_LIMIT}")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    filters = RetrievalFilters(
        category=args.category,
        trust_level=args.trust_level,
        geography=args.geography,
        language=args.language,
    )
    results = search_hybrid(
        query=args.query,
        chunks_dir=Path(args.chunks_dir),
        vectors_dir=Path(args.vectors_dir),
        filters=filters,
        limit=args.limit,
    )

    payload = {
        "query": args.query,
        "chunks_dir": args.chunks_dir,
        "vectors_dir": args.vectors_dir,
        "mode": "hybrid",
        "count": len(results),
        "results": results,
    }
    indent = 2 if args.pretty else None
    print(json.dumps(payload, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
