"""Batch ingest registered SanJuan AI sources into local raw documents.

Run from the repository root:

    python -m packages.ingestion.batch_ingest_sources --pretty

To enable bounded crawling for sources with crawl.enabled=true:

    python -m packages.ingestion.batch_ingest_sources --crawl --pretty
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from packages.ingestion.fetch_static_page import StaticPageFetchError, fetch_static_page
from packages.ingestion.load_sources import DEFAULT_SOURCE_REGISTRY_PATH, SourceRegistryError, load_sources_from_path
from packages.ingestion.safe_crawler import CrawlError, crawl_source
from packages.shared.source_schema import Source

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "documents" / "raw"


def slugify(value: str) -> str:
    """Return a filesystem-safe slug."""
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "document"


def build_document_payload(source: Source, timeout_seconds: int) -> dict[str, Any]:
    """Fetch one source homepage and return a normalized document payload.

    The payload is intentionally JSON-friendly and includes both successful fetches
    and structured failures so downstream steps can reason about coverage.
    """
    source_payload = source.model_dump(mode="json")

    try:
        fetched = fetch_static_page(str(source.url), timeout_seconds=timeout_seconds)
    except StaticPageFetchError as exc:
        return {
            "document_id": source.id,
            "source": source_payload,
            "url": str(source.url),
            "title": None,
            "text": "",
            "fetched_at": None,
            "content_hash": None,
            "status": "failed",
            "error": str(exc),
        }

    return {
        "document_id": source.id,
        "source": source_payload,
        "url": fetched["url"],
        "title": fetched.get("title"),
        "text": fetched.get("text", ""),
        "fetched_at": fetched.get("fetched_at"),
        "content_hash": fetched.get("content_hash"),
        "status_code": fetched.get("status_code"),
        "content_length": fetched.get("content_length"),
        "crawl_depth": 0,
        "status": "success",
        "error": None,
    }


def write_document(document: dict[str, Any], output_dir: Path, pretty: bool = False) -> Path:
    """Write one document payload to disk and return the output path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    document_id = slugify(str(document["document_id"]))
    output_path = output_dir / f"{document_id}.json"
    indent = 2 if pretty else None

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(document, file, ensure_ascii=False, indent=indent)
        file.write("\n")

    return output_path


def _relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _result_for_document(source: Source, document: dict[str, Any], output_path: Path) -> dict[str, Any]:
    return {
        "source_id": source.id,
        "document_id": document.get("document_id"),
        "name": source.name,
        "url": document.get("url"),
        "status": document["status"],
        "output_path": _relative_path(output_path),
        "error": document.get("error"),
        "content_length": document.get("content_length", 0),
        "crawl_depth": document.get("crawl_depth", 0),
    }


def ingest_source_homepage(source: Source, output_dir: Path, timeout_seconds: int, pretty: bool) -> list[dict[str, Any]]:
    """Ingest one source homepage."""
    document = build_document_payload(source, timeout_seconds=timeout_seconds)
    output_path = write_document(document, output_dir=output_dir, pretty=pretty)
    return [_result_for_document(source, document, output_path)]


def ingest_source_with_crawl(
    source: Source,
    output_dir: Path,
    timeout_seconds: int,
    pretty: bool,
    max_pages_override: int | None = None,
) -> list[dict[str, Any]]:
    """Ingest one source using bounded crawling when enabled."""
    if not source.crawl or not source.crawl.enabled:
        return ingest_source_homepage(source, output_dir=output_dir, timeout_seconds=timeout_seconds, pretty=pretty)

    try:
        crawl_result = crawl_source(source, timeout_seconds=timeout_seconds, max_pages_override=max_pages_override)
    except CrawlError as exc:
        document = {
            "document_id": source.id,
            "source": source.model_dump(mode="json"),
            "url": str(source.url),
            "title": None,
            "text": "",
            "fetched_at": None,
            "content_hash": None,
            "crawl_depth": 0,
            "status": "failed",
            "error": str(exc),
        }
        output_path = write_document(document, output_dir=output_dir, pretty=pretty)
        return [_result_for_document(source, document, output_path)]

    results: list[dict[str, Any]] = []
    for document in crawl_result["documents"]:
        output_path = write_document(document, output_dir=output_dir, pretty=pretty)
        results.append(_result_for_document(source, document, output_path))

    for error in crawl_result.get("errors", []):
        results.append(
            {
                "source_id": source.id,
                "document_id": None,
                "name": source.name,
                "url": error.get("url"),
                "status": "failed",
                "output_path": None,
                "error": error.get("error"),
                "content_length": 0,
                "crawl_depth": error.get("depth", 0),
            }
        )

    if not results:
        document = {
            "document_id": source.id,
            "source": source.model_dump(mode="json"),
            "url": str(source.url),
            "title": None,
            "text": "",
            "fetched_at": None,
            "content_hash": None,
            "crawl_depth": 0,
            "status": "failed",
            "error": "Crawl completed without any documents.",
        }
        output_path = write_document(document, output_dir=output_dir, pretty=pretty)
        return [_result_for_document(source, document, output_path)]

    return results


def ingest_sources(
    registry_path: Path,
    output_dir: Path,
    timeout_seconds: int,
    pretty: bool = False,
    crawl: bool = False,
    max_pages_override: int | None = None,
) -> dict[str, Any]:
    """Batch ingest all registered sources and return a summary."""
    sources = load_sources_from_path(registry_path)
    results: list[dict[str, Any]] = []

    for source in sources:
        if crawl:
            results.extend(
                ingest_source_with_crawl(
                    source,
                    output_dir=output_dir,
                    timeout_seconds=timeout_seconds,
                    pretty=pretty,
                    max_pages_override=max_pages_override,
                )
            )
        else:
            results.extend(
                ingest_source_homepage(source, output_dir=output_dir, timeout_seconds=timeout_seconds, pretty=pretty)
            )

    successful = [result for result in results if result["status"] == "success"]
    failed = [result for result in results if result["status"] == "failed"]
    crawled_sources = [source for source in sources if source.crawl and source.crawl.enabled]

    return {
        "mode": "bounded_crawl" if crawl else "homepage_only",
        "total_sources": len(sources),
        "crawl_enabled_sources": len(crawled_sources),
        "total_documents_or_attempts": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "output_dir": _relative_path(output_dir),
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch ingest SanJuan AI registered sources.")
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_SOURCE_REGISTRY_PATH),
        help="Path to the source registry YAML file.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where raw JSON documents should be written.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Request timeout in seconds for each source. Default: 20",
    )
    parser.add_argument(
        "--crawl",
        action="store_true",
        help="Enable bounded crawling for sources with crawl.enabled=true. Default is homepage-only ingestion.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional maximum page override for each crawl-enabled source.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print output JSON documents and summary.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        summary = ingest_sources(
            registry_path=Path(args.registry),
            output_dir=Path(args.output_dir),
            timeout_seconds=args.timeout,
            pretty=args.pretty,
            crawl=args.crawl,
            max_pages_override=args.max_pages,
        )
    except SourceRegistryError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    indent = 2 if args.pretty else None
    print(json.dumps(summary, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
