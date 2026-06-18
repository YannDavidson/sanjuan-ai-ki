"""Chunk ingested SanJuan AI documents for retrieval.

Run from the repository root after batch ingestion:

    python -m packages.retrieval.chunk_documents --pretty
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "data" / "documents" / "raw"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "documents" / "chunks"
DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200


def normalize_text(text: str) -> str:
    """Normalize whitespace for stable chunking."""
    return re.sub(r"\s+", " ", text).strip()


def stable_chunk_id(document_id: str, chunk_index: int, chunk_text: str) -> str:
    """Build a stable ID for a document chunk."""
    digest = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()[:16]
    return f"{document_id}:chunk:{chunk_index:04d}:{digest}"


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into overlapping character chunks.

    Character-based chunking is intentionally simple for the MVP. A later step can
    replace this with token-aware chunking when an embedding provider is selected.
    """
    normalized = normalize_text(text)
    if not normalized:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    text_length = len(normalized)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_length:
            break
        start = max(0, end - chunk_overlap)

    return chunks


def load_json_documents(input_dir: Path) -> list[dict[str, Any]]:
    """Load raw JSON document files from a directory."""
    if not input_dir.exists():
        return []

    documents: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as file:
            document = json.load(file)
        document["_input_path"] = str(path)
        documents.append(document)

    return documents


def build_chunks_for_document(
    document: dict[str, Any],
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict[str, Any]]:
    """Create retrieval chunks from one raw document."""
    document_id = str(document.get("document_id") or "unknown-document")
    source = document.get("source") or {}
    text = document.get("text") or ""
    chunks = split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    output: list[dict[str, Any]] = []
    for index, chunk_text in enumerate(chunks):
        output.append(
            {
                "chunk_id": stable_chunk_id(document_id, index, chunk_text),
                "document_id": document_id,
                "chunk_index": index,
                "text": chunk_text,
                "character_count": len(chunk_text),
                "source_id": source.get("id") or document_id,
                "source_name": source.get("name"),
                "source_url": document.get("url") or source.get("url"),
                "title": document.get("title"),
                "trust_level": source.get("trust_level"),
                "category": source.get("category"),
                "geography": source.get("geography"),
                "language": source.get("language"),
                "source_type": source.get("source_type"),
                "fetched_at": document.get("fetched_at"),
                "content_hash": document.get("content_hash"),
                "citation": {
                    "title": document.get("title") or source.get("name"),
                    "url": document.get("url") or source.get("url"),
                    "source_id": source.get("id") or document_id,
                    "source_name": source.get("name"),
                },
            }
        )

    return output


def write_chunks(chunks: list[dict[str, Any]], output_dir: Path, pretty: bool = False) -> Path | None:
    """Write all chunks for one document to a JSON file."""
    if not chunks:
        return None

    output_dir.mkdir(parents=True, exist_ok=True)
    document_id = chunks[0]["document_id"]
    output_path = output_dir / f"{document_id}.chunks.json"
    indent = 2 if pretty else None

    with output_path.open("w", encoding="utf-8") as file:
        json.dump({"document_id": document_id, "chunks": chunks}, file, ensure_ascii=False, indent=indent)
        file.write("\n")

    return output_path


def chunk_documents(
    input_dir: Path,
    output_dir: Path,
    chunk_size: int,
    chunk_overlap: int,
    pretty: bool = False,
) -> dict[str, Any]:
    """Chunk all raw documents in an input directory and return a summary."""
    documents = load_json_documents(input_dir)
    results: list[dict[str, Any]] = []
    total_chunks = 0

    for document in documents:
        document_id = str(document.get("document_id") or "unknown-document")
        chunks = build_chunks_for_document(
            document,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        output_path = write_chunks(chunks, output_dir=output_dir, pretty=pretty)
        total_chunks += len(chunks)

        results.append(
            {
                "document_id": document_id,
                "source_id": (document.get("source") or {}).get("id"),
                "status": "chunked" if chunks else "skipped",
                "chunk_count": len(chunks),
                "output_path": str(output_path.relative_to(REPO_ROOT)) if output_path else None,
                "reason": None if chunks else "No usable text found.",
            }
        )

    return {
        "input_dir": str(input_dir.relative_to(REPO_ROOT)) if input_dir.is_relative_to(REPO_ROOT) else str(input_dir),
        "output_dir": str(output_dir.relative_to(REPO_ROOT)) if output_dir.is_relative_to(REPO_ROOT) else str(output_dir),
        "documents_seen": len(documents),
        "documents_chunked": len([result for result in results if result["status"] == "chunked"]),
        "documents_skipped": len([result for result in results if result["status"] == "skipped"]),
        "total_chunks": total_chunks,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chunk SanJuan AI raw documents for retrieval.")
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory containing raw JSON documents.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where chunk JSON files should be written.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Chunk size in characters. Default: {DEFAULT_CHUNK_SIZE}",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=DEFAULT_CHUNK_OVERLAP,
        help=f"Chunk overlap in characters. Default: {DEFAULT_CHUNK_OVERLAP}",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print output JSON files and summary.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        summary = chunk_documents(
            input_dir=Path(args.input_dir),
            output_dir=Path(args.output_dir),
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            pretty=args.pretty,
        )
    except ValueError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    indent = 2 if args.pretty else None
    print(json.dumps(summary, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
