"""Batch ingest registered SanJuan AI sources into local raw documents.

Run from the repository root:

    python -m packages.ingestion.batch_ingest_sources --pretty
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from packages.ingestion.fetch_static_page import StaticPageFetchError, fetch_static_page
from packages.ingestion.load_sources import DEFAULT_SOURCE_REGISTRY_PATH, SourceRegistryError, load_sources_from_path
from packages.shared.source_schema import Source

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "documents" / "raw"


def slugify(value: str) -> str:
    """Return a filesystem-safe slug."""
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "document"


def build_document_payload(source: Source, timeout_seconds: int) -> dict[str, Any]:
    """Fetch one source and return a normalized document payload.

    The payload is intentionally JSON-friendly and includes both successful fetches
    and structured failures so downstream steps can reason about coverage.
    """
    source_payload = source.model_dump(mode="json")

    try:
        fetched = fetch_static_page(source.url, timeout_seconds=timeout_seconds)
    except StaticPageFetchError as exc:
        return {
            "document_id": source.id,
            "source": source_payload,
            "url": source.url,
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


def ingest_sources(
    registry_path: Path,
    output_dir: Path,
    timeout_seconds: int,
    pretty: bool = False,
) -> dict[str, Any]:
    """Batch ingest all registered sources and return a summary."""
    sources = load_sources_from_path(registry_path)
    results: list[dict[str, Any]] = []

    for source in sources:
        document = build_document_payload(source, timeout_seconds=timeout_seconds)
        output_path = write_document(document, output_dir=output_dir, pretty=pretty)
        results.append(
            {
                "source_id": source.id,
                "name": source.name,
                "status": document["status"],
                "output_path": str(output_path.relative_to(REPO_ROOT)),
                "error": document.get("error"),
                "content_length": document.get("content_length", 0),
            }
        )

    successful = [result for result in results if result["status"] == "success"]
    failed = [result for result in results if result["status"] == "failed"]

    return {
        "total_sources": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "output_dir": str(output_dir.relative_to(REPO_ROOT)) if output_dir.is_relative_to(REPO_ROOT) else str(output_dir),
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
        )
    except SourceRegistryError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    indent = 2 if args.pretty else None
    print(json.dumps(summary, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
