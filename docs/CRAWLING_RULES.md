# Bounded Source Crawling Rules

SanJuan AI now supports safe, opt-in crawling for selected internal pages on registered sources.

The original ingestion behavior remains the default: one homepage per source. Bounded crawling only runs when:

1. The source has `crawl.enabled: true` in `data/sources/pr_sources.yml`.
2. The batch ingestion command is run with `--crawl`.

## Example source rule

```yaml
crawl:
  enabled: true
  max_pages_per_source: 10
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

## Safety behavior

The crawler is intentionally conservative.

It will:

- only crawl same-domain links
- remove URL fragments
- drop query strings to avoid search/filter/calendar loops
- block common noisy paths like `/login`, `/admin`, `/search`, `/calendar`, `/api`, and `/wp-admin`
- respect each source's `max_pages_per_source`
- follow only `allowed_paths` when an allow-list is set
- skip common binary/static file extensions
- avoid duplicate URLs
- preserve source metadata and citation-ready page URLs on every raw document

## Run homepage-only ingestion

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

This is still the default and safest mode.

## Run bounded crawling

```bash
python -m packages.ingestion.batch_ingest_sources --crawl --pretty
```

Use a smaller page cap while testing:

```bash
python -m packages.ingestion.batch_ingest_sources --crawl --max-pages 3 --pretty
```

## Crawl one source for debugging

```bash
python -m packages.ingestion.safe_crawler pr_gov_main --max-pages 3 --pretty
```

## Recommended rules

For high-value Puerto Rico government sources, keep `max_pages_per_source` between 5 and 10 until the source-specific loaders are more mature.

Prefer allow-lists for useful public-service paths:

```yaml
allowed_paths:
  - /servicios
  - /tramites
  - /agencias
  - /permisos
  - /programas
```

Always block paths likely to create noise, authentication issues, or infinite loops:

```yaml
blocked_paths:
  - /login
  - /admin
  - /search
  - /calendar
```

## Current limitation

This is not yet a full production crawler. It does not parse sitemaps, robots.txt, canonical tags, or JavaScript-rendered pages. The next step is to add agency-specific loaders for high-value sources like PR.gov, DTOP, Hacienda, Salud, Estado, DDEC, and the San Juan municipality.
