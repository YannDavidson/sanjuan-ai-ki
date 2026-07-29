"""Safe bounded crawler for registered SanJuan AI sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import deque
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from packages.ingestion.crawl_policy import load_robots_policy, polite_delay
from packages.ingestion.fetch_static_page import StaticPageFetchError, USER_AGENT, extract_visible_text
from packages.ingestion.load_sources import DEFAULT_SOURCE_REGISTRY_PATH, load_sources_from_path
from packages.shared.source_schema import CrawlRules, Source

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_BLOCKED_PATHS = (
    "/admin", "/api", "/auth", "/calendar", "/cdn-cgi", "/login", "/logout",
    "/private", "/search", "/signin", "/signup", "/wp-admin",
)

IGNORED_EXTENSIONS = (
    ".7z", ".avi", ".css", ".doc", ".docx", ".gif", ".gz", ".ico", ".jpeg",
    ".jpg", ".js", ".json", ".mp3", ".mp4", ".png", ".ppt", ".pptx", ".rar",
    ".svg", ".webp", ".xls", ".xlsx", ".zip",
)


class CrawlError(RuntimeError):
    """Raised when a crawl cannot be completed."""


def normalize_url(base_url: str, href: str) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None
    absolute_url = urljoin(base_url, href)
    absolute_url, _fragment = urldefrag(absolute_url)
    parsed = urlparse(absolute_url)
    if parsed.scheme not in {"http", "https"}:
        return None
    normalized_path = parsed.path or "/"
    if normalized_path != "/":
        normalized_path = normalized_path.rstrip("/")
    if normalized_path.lower().endswith(IGNORED_EXTENSIONS):
        return None
    return urlunparse((parsed.scheme, parsed.netloc.lower(), normalized_path, "", "", ""))


def _path_matches(path: str, patterns: list[str] | tuple[str, ...]) -> bool:
    normalized_path = path.rstrip("/") or "/"
    for pattern in patterns:
        normalized_pattern = pattern.rstrip("/") or "/"
        if normalized_pattern == "/":
            if normalized_path == "/":
                return True
            continue
        if normalized_path == normalized_pattern or normalized_path.startswith(f"{normalized_pattern}/"):
            return True
    return False


def is_url_allowed(candidate_url: str, source_url: str, rules: CrawlRules | None) -> bool:
    candidate = urlparse(candidate_url)
    source = urlparse(source_url)
    if candidate.scheme not in {"http", "https"}:
        return False
    if candidate.netloc.lower() != source.netloc.lower():
        return False
    path = candidate.path or "/"
    blocked_paths = list(DEFAULT_BLOCKED_PATHS)
    allowed_paths: list[str] = []
    if rules:
        blocked_paths.extend(rules.blocked_paths)
        allowed_paths = rules.allowed_paths
    if _path_matches(path, blocked_paths):
        return False
    source_path = source.path.rstrip("/") or "/"
    candidate_path = path.rstrip("/") or "/"
    if candidate_path == source_path:
        return True
    if allowed_paths and not _path_matches(path, allowed_paths):
        return False
    return True


def extract_links(html: str, base_url: str, rules: CrawlRules | None) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        normalized = normalize_url(base_url, str(anchor.get("href")))
        if not normalized or not is_url_allowed(normalized, base_url, rules) or normalized in seen:
            continue
        seen.add(normalized)
        links.append(normalized)
    return links


def fetch_page_with_links(url: str, rules: CrawlRules | None, timeout_seconds: int) -> dict[str, Any]:
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout_seconds)
    except requests.RequestException as exc:
        raise StaticPageFetchError(f"Could not fetch {url}: {exc}") from exc
    content_type = response.headers.get("content-type", "")
    if response.status_code >= 400:
        raise StaticPageFetchError(f"Request failed for {url} with status code {response.status_code}")
    if "html" not in content_type.lower():
        raise StaticPageFetchError(f"Expected HTML content from {url}, got content-type: {content_type or 'unknown'}")
    final_url = normalize_url(url, response.url) or url
    title, text = extract_visible_text(response.text)
    return {
        "url": final_url,
        "title": title,
        "text": text,
        "links": extract_links(response.text, final_url, rules),
        "fetched_at": datetime.now(UTC).isoformat(),
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "status_code": response.status_code,
        "content_length": len(text),
    }


def document_id_for_url(source_id: str, url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "home"
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", path.lower()).strip("-") or "home"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{source_id}__{slug}-{digest}"


def build_document_payload(source: Source, page: dict[str, Any], crawl_depth: int) -> dict[str, Any]:
    return {
        "document_id": document_id_for_url(source.id, page["url"]),
        "source": source.model_dump(mode="json"),
        "url": page["url"],
        "title": page.get("title"),
        "text": page.get("text", ""),
        "fetched_at": page.get("fetched_at"),
        "content_hash": page.get("content_hash"),
        "status_code": page.get("status_code"),
        "content_length": page.get("content_length"),
        "crawl_depth": crawl_depth,
        "status": "success",
        "error": None,
    }


def crawl_source(source: Source, timeout_seconds: int = 20, max_pages_override: int | None = None) -> dict[str, Any]:
    rules = source.crawl or CrawlRules(enabled=False)
    if not rules.enabled:
        raise CrawlError(f"Crawling is not enabled for source {source.id}")

    max_pages = max_pages_override or rules.max_pages_per_source
    start_url = normalize_url(str(source.url), str(source.url)) or str(source.url)
    queue: deque[tuple[str, int]] = deque([(start_url, 0)])
    seen: set[str] = set()
    documents: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    robots_policy = load_robots_policy(start_url, timeout_seconds=min(timeout_seconds, 10)) if rules.respect_robots_txt else None
    requests_made = 0

    while queue and len(documents) < max_pages:
        url, depth = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        if not is_url_allowed(url, start_url, rules):
            continue
        if robots_policy and not robots_policy.allows(url):
            errors.append({"url": url, "error": "Blocked by robots.txt", "depth": depth})
            continue
        if requests_made:
            polite_delay(rules.request_delay_seconds)
        try:
            page = fetch_page_with_links(url, rules=rules, timeout_seconds=timeout_seconds)
            requests_made += 1
        except StaticPageFetchError as exc:
            requests_made += 1
            errors.append({"url": url, "error": str(exc), "depth": depth})
            continue
        documents.append(build_document_payload(source, page, crawl_depth=depth))
        for link in page.get("links", []):
            if link not in seen and len(seen) + len(queue) < max_pages * 4:
                queue.append((link, depth + 1))

    return {
        "source_id": source.id,
        "max_pages": max_pages,
        "documents": documents,
        "errors": errors,
        "visited_count": len(seen),
        "requests_made": requests_made,
        "robots_txt": {
            "respected": rules.respect_robots_txt,
            "url": robots_policy.robots_url if robots_policy else None,
            "available": robots_policy.available if robots_policy else None,
            "error": robots_policy.error if robots_policy else None,
        },
        "request_delay_seconds": rules.request_delay_seconds,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safely crawl one registered SanJuan AI source.")
    parser.add_argument("source_id")
    parser.add_argument("--registry", default=str(DEFAULT_SOURCE_REGISTRY_PATH))
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    sources = load_sources_from_path(Path(args.registry))
    source = next((item for item in sources if item.id == args.source_id), None)
    if not source:
        parser.exit(status=1, message=f"Error: unknown source id {args.source_id}\n")
    try:
        result = crawl_source(source, timeout_seconds=args.timeout, max_pages_override=args.max_pages)
    except CrawlError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
