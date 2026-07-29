"""Robots.txt and polite-delay helpers for SanJuan AI crawlers."""

from __future__ import annotations

import time
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

from packages.ingestion.fetch_static_page import USER_AGENT


@dataclass(frozen=True)
class RobotsPolicy:
    """Resolved robots policy for one source origin."""

    robots_url: str
    parser: RobotFileParser | None
    available: bool
    error: str | None = None

    def allows(self, url: str, user_agent: str = USER_AGENT) -> bool:
        if self.parser is None:
            return True
        return self.parser.can_fetch(user_agent, url)


def robots_url_for(source_url: str) -> str:
    parsed = urlparse(source_url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def load_robots_policy(source_url: str, timeout_seconds: int = 10) -> RobotsPolicy:
    """Fetch and parse robots.txt; fail open when unavailable.

    Failing open is intentional for temporary network errors, but the returned
    policy records the error so crawl summaries remain transparent.
    """
    robots_url = robots_url_for(source_url)
    try:
        response = requests.get(robots_url, headers={"User-Agent": USER_AGENT}, timeout=timeout_seconds)
        if response.status_code >= 400:
            return RobotsPolicy(robots_url=robots_url, parser=None, available=False, error=f"status {response.status_code}")
        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(response.text.splitlines())
        return RobotsPolicy(robots_url=robots_url, parser=parser, available=True)
    except requests.RequestException as exc:
        return RobotsPolicy(robots_url=robots_url, parser=None, available=False, error=str(exc))


def polite_delay(seconds: float) -> None:
    """Sleep between requests when a positive delay is configured."""
    if seconds > 0:
        time.sleep(seconds)
