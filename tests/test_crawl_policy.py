"""Network-free tests for robots.txt and polite crawl configuration."""

from __future__ import annotations

from urllib.robotparser import RobotFileParser

from packages.ingestion.crawl_policy import RobotsPolicy, robots_url_for
from packages.shared.source_schema import CrawlRules


def test_crawl_rules_default_to_polite_behavior() -> None:
    rules = CrawlRules(enabled=True)

    assert rules.respect_robots_txt is True
    assert rules.request_delay_seconds == 1.0


def test_robots_url_uses_source_origin() -> None:
    assert robots_url_for("https://www.pr.gov/servicios/example") == "https://www.pr.gov/robots.txt"


def test_robots_policy_blocks_disallowed_paths_without_network() -> None:
    parser = RobotFileParser()
    parser.parse([
        "User-agent: *",
        "Disallow: /private",
        "Allow: /servicios",
    ])
    policy = RobotsPolicy(
        robots_url="https://example.test/robots.txt",
        parser=parser,
        available=True,
    )

    assert policy.allows("https://example.test/servicios") is True
    assert policy.allows("https://example.test/private/records") is False
