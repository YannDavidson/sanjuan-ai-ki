# Bounded Source Crawling Rules

SanJuan AI supports safe, opt-in crawling for selected internal pages on registered sources.

Bounded crawling only runs when:

1. The source has `crawl.enabled: true`.
2. Batch ingestion is run with `--crawl`, or an agency-specific loader is selected.

## Example source rule

```yaml
crawl:
  enabled: true
  max_pages_per_source: 10
  respect_robots_txt: true
  request_delay_seconds: 1.0
  allowed_paths:
    - /servicios
    - /tramites
    - /agencias
  blocked_paths:
    - /login
    - /admin
    - /search
    - /calendar
```

## Safety and politeness behavior

The crawler:

- checks `/robots.txt` before crawling when enabled
- skips URLs disallowed by robots.txt
- waits between page requests using `request_delay_seconds`
- only follows same-domain links
- removes fragments and query strings
- blocks common noisy/authentication paths
- respects page caps
- follows configured allow-lists
- skips common binary/static extensions
- avoids duplicate URLs
- preserves citation-ready source metadata

Robots fetch failures are recorded in crawl summaries. The crawler currently fails open when robots.txt is unavailable because a temporary error should not be interpreted as a permanent prohibition; deployments that require fail-closed behavior can change that policy later.

## Commands

Homepage only:

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

Bounded crawl:

```bash
python -m packages.ingestion.batch_ingest_sources --crawl --max-pages 3 --pretty
```

Agency loaders:

```bash
python -m packages.ingestion.batch_ingest_sources --agency-loaders --max-pages 3 --pretty
```

One source:

```bash
python -m packages.ingestion.safe_crawler pr_gov_main --max-pages 3 --pretty
```

## Recommended production rules

- Keep page caps between 5 and 10 during beta.
- Keep `respect_robots_txt: true`.
- Use at least a one-second delay unless a source explicitly supports faster access.
- Prefer public-service path allow-lists.
- Do not crawl login, admin, search, calendar, or private paths.

## Remaining limitations

The crawler does not yet parse sitemaps, canonical tags, crawl-delay directives from robots.txt, or JavaScript-rendered pages. PDF and structured-document loaders are also future work.
