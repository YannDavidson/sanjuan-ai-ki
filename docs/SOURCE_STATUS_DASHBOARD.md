# Source Status Dashboard

## Purpose

SanJuan AI needs to know which Puerto Rico sources are healthy enough to use for citation-backed answers. A source can be official and important, but still fail ingestion, return little text, or become stale.

The source status dashboard provides a local MVP health layer for the source registry.

## Status categories

| Status | Meaning |
| --- | --- |
| `healthy` | Source was fetched recently and enough text was extracted. |
| `thin` | Source was fetched, but extracted text is too short to trust strongly. |
| `stale` | Source has text, but the fetch is older than the freshness threshold. |
| `unknown_freshness` | Source has text, but no valid fetch timestamp. |
| `empty` | Source fetched but produced no usable text. |
| `failed` | Source fetch failed. |
| `missing` | Source is in the registry but has not been ingested yet. |

## Priority categories

| Priority | Meaning |
| --- | --- |
| `high` | Official source with a missing, failed, or empty document. Needs attention. |
| `medium` | High-value category with thin, stale, or unknown freshness. |
| `high_value` | Official or important category source currently usable but important to monitor. |
| `normal` | Lower urgency source. |

## CLI usage

Run batch ingestion first:

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

Then generate a source health report:

```bash
python -m packages.ingestion.source_status --pretty
```

Write the JSON artifact used by the web app:

```bash
python -m packages.ingestion.source_status --pretty --write-json
```

The artifact is written to:

```txt
data/status/source_status.json
```

## Web dashboard

Run the web app:

```bash
cd apps/web
npm install
npm run dev
```

Open:

```txt
http://localhost:3000/status
```

If the JSON artifact has not been generated yet, the dashboard falls back to the source registry and marks every source as `missing`.

## Recommended operating flow

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
python -m packages.ingestion.source_status --pretty --write-json
python -m packages.retrieval.chunk_documents --pretty
python -m packages.retrieval.keyword_search "business registration Puerto Rico" --pretty
python -m packages.retrieval.local_vector_search build --pretty
python -m packages.retrieval.local_vector_search search "business registration Puerto Rico" --pretty
```

## Why this matters

The assistant should not blindly trust every registered source. The status layer helps identify:

- broken official sources
- pages that need custom ingestion
- sources that need manual review
- high-value sources worth prioritizing
- stale data that should be refreshed before retrieval
