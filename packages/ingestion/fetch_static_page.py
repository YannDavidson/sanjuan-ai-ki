"""Fetch and normalize a public static HTML page.

Run from the repository root:

    python -m packages.ingestion.fetch_static_page https://www.pr.gov/
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from typing import Any

import requests
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT_SECONDS = 20
USER_AGENT = "SanJuanAI-MVP/0.1 (+https://github.com/YannDavidson/sanjuan-ai)"


class StaticPageFetchError(RuntimeError):
    """Raised when a static page cannot be fetched or parsed."""


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace and trim the result."""
    return re.sub(r"\s+", " ", text).strip()


def extract_visible_text(html: str) -> tuple[str | None, str]:
    """Extract the page title and visible text from an HTML document."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "canvas", "iframe"]):
        tag.decompose()

    title = normalize_whitespace(soup.title.get_text(" ")) if soup.title else None

    # Remove high-noise structural elements where practical while preserving page content.
    for tag in soup.find_all(["nav", "footer", "aside"]):
        tag.decompose()

    text = normalize_whitespace(soup.get_text(" "))
    return title, text


def fetch_static_page(url: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Fetch a URL and return normalized JSON-ready page content."""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout_seconds,
        )
    except requests.RequestException as exc:
        raise StaticPageFetchError(f"Could not fetch {url}: {exc}") from exc

    content_type = response.headers.get("content-type", "")
    if "html" not in content_type.lower():
        raise StaticPageFetchError(
            f"Expected HTML content from {url}, got content-type: {content_type or 'unknown'}"
        )

    if response.status_code >= 400:
        raise StaticPageFetchError(f"Request failed for {url} with status code {response.status_code}")

    title, text = extract_visible_text(response.text)
    fetched_at = datetime.now(UTC).isoformat()
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return {
        "url": url,
        "title": title,
        "text": text,
        "fetched_at": fetched_at,
        "content_hash": content_hash,
        "status_code": response.status_code,
        "content_length": len(text),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and normalize a public static HTML page.")
    parser.add_argument("url", help="Public page URL to fetch.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Request timeout in seconds. Default: {DEFAULT_TIMEOUT_SECONDS}",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = fetch_static_page(args.url, timeout_seconds=args.timeout)
    except StaticPageFetchError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
