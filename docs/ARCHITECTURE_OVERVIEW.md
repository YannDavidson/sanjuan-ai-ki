# Architecture Overview

SanJuan AI is organized as a citation-first civic intelligence pipeline.

## System diagram

```txt
┌──────────────────────┐
│ Source Registry       │
│ pr_sources.yml        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Ingestion             │
│ homepage / crawl /    │
│ agency loaders        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Raw Documents         │
│ data/documents/raw    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Chunking              │
│ citation metadata     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Retrieval             │
│ keyword + vectors     │
│ bilingual expansion   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ FastAPI /ask          │
│ structured answer     │
│ citations + warnings  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Next.js Web App       │
│ /ask /sources /status │
└──────────────────────┘
```

## Main components

### Source registry

`data/sources/pr_sources.yml` defines trusted Puerto Rico sources with metadata such as category, geography, language, trust level, source type, and optional crawl rules.

### Ingestion

The ingestion layer can fetch homepages, run bounded same-domain crawling, or use agency-specific loader profiles.

### Raw documents

Fetched pages are normalized and stored as JSON documents under `data/documents/raw/`.

### Chunking

Raw documents are split into retrieval chunks with source and citation metadata preserved.

### Retrieval

SanJuan AI combines:

- keyword retrieval
- local deterministic vector search
- Spanish-first bilingual query expansion
- hybrid ranking

### API

The FastAPI backend exposes `/health`, `/sources`, `/sources/{source_id}`, and `/ask`.

### Web app

The Next.js app exposes `/`, `/ask`, `/sources`, and `/status`.

## Future architecture

Future production versions may move documents, chunks, and vectors into Postgres + pgvector or object storage, add background queues, and use stronger embedding models while keeping citation-first behavior.
