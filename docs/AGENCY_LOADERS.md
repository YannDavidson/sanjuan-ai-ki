# Agency-Specific Loaders

SanJuan AI now supports agency-specific loader profiles for high-value Puerto Rico sources.

Generic crawling treats every site as arbitrary HTML. Agency loaders add a source-aware layer by focusing on public sections that are more likely to contain useful official information.

## Supported MVP profiles

- `pr_gov_main` — PR.gov
- `pr_hacienda` — Departamento de Hacienda
- `pr_dtop` — Departamento de Transportación y Obras Públicas
- `pr_salud` — Departamento de Salud
- `pr_estado` — Departamento de Estado
- `pr_ddec` — Departamento de Desarrollo Económico y Comercio
- `san_juan_municipio` — Municipio de San Juan
- `nws_san_juan` — National Weather Service San Juan

## Loader profile fields

Each loader profile defines:

- `source_id`
- `agency_name`
- `priority_paths`
- `blocked_paths`
- `max_pages`
- `extraction_hints`
- `notes`

The MVP implementation still uses static HTML fetching and safe same-domain link following, but the profile gives ingestion a stronger starting map than generic crawling.

## Run homepage-only ingestion

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

## Run bounded crawling

```bash
python -m packages.ingestion.batch_ingest_sources --crawl --max-pages 3 --pretty
```

## Run agency-specific loaders

```bash
python -m packages.ingestion.batch_ingest_sources --agency-loaders --max-pages 3 --pretty
```

Sources with an agency profile use their profile. Sources without a profile fall back to homepage-only ingestion.

## Why this matters

Agency-specific loaders make the corpus more useful because they prioritize pages likely to answer real public questions:

- services
- permits
- licenses
- merchant/taxpayer information
- corporation/registry information
- economic incentives
- municipal services
- weather safety and warnings

## Current limitation

These are MVP profile-based loaders, not fully custom parsers yet. They do not currently parse agency-specific APIs, sitemaps, JavaScript-rendered content, PDFs, or structured tables. The next upgrade should add true per-agency parsers where needed.
