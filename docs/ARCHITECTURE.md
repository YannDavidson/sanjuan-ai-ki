# SanJuan AI Architecture

SanJuan AI is a Puerto Rico-first, bilingual, citation-first civic intelligence layer.

This document separates the **current MVP architecture** from the **future production architecture** so contributors can tell what exists today and what remains on the roadmap.

## Current MVP architecture

```txt
Public Source Registry (YAML)
          ↓
Homepage Ingestion / Bounded Crawler / Agency Loaders
          ↓
Raw JSON Documents
          ↓
JSON Chunk Files
          ↓
Keyword Search + Local Hashed Vector Search
          ↓
Hybrid Retrieval with Trust Weighting
          ↓
Deterministic Structured Answer Builder
          ↓
FastAPI API + Next.js Web App
```

### Current storage

The MVP uses repository-local JSON files:

```txt
data/sources/pr_sources.yml
data/documents/raw/
data/documents/chunks/
data/documents/vectors/
data/status/
```

Generated corpus files are intentionally ignored by Git. The committed test fixtures under `tests/fixtures/` provide deterministic CI coverage.

### Current retrieval

The current retrieval layer includes:

- keyword search
- deterministic local hashed vectors
- hybrid ranking
- source trust weighting
- geography/category/language filters
- Spanish-first English/Spanish query expansion

### Current answer generation

The MVP answer builder is deterministic and extractive. It returns:

- direct answer
- steps
- requirements
- citations
- confidence
- related agencies
- official-source warnings

No external LLM is required for the current MVP.

## Safety principles

- No source, no answer.
- Never invent official requirements, fees, deadlines, eligibility, or procedures.
- Prefer official sources for permits, taxes, health, emergencies, legal/court topics, immigration, police, and public benefits.
- Clearly state when evidence is missing.
- Preserve citation URLs and source metadata.

## Future production architecture

Postgres + pgvector remains a planned production direction, not the current implementation.

```txt
Public Sources
      ↓
Scheduled Ingestion Workers
      ↓
Object Storage + Postgres Document Metadata
      ↓
Postgres Full-Text Search + pgvector
      ↓
Quality/Recency/Trust Ranking
      ↓
Citation-Aware LLM Synthesis
      ↓
API, Web App, Widgets, Partner Integrations
```

Potential future components:

- Postgres + pgvector
- object storage for raw documents
- Redis or managed job queues
- stronger multilingual embedding models
- citation-aware LLM synthesis
- temporal reasoning
- PDF/form/table parsing
- multi-source evidence fusion
- admin and municipal dashboards

## Repository components

- `apps/web`: Next.js frontend
- `apps/api`: FastAPI backend
- `packages/ingestion`: loaders, crawler, refresh/status pipeline
- `packages/retrieval`: keyword, vector, bilingual, and hybrid retrieval
- `packages/shared`: schemas and shared models
- `data/sources`: committed source registry
- `data/documents`: generated local corpus artifacts
- `tests/fixtures`: committed deterministic test corpus

## Product direction

SanJuan AI should grow beyond a chatbot into reusable public knowledge infrastructure supporting:

- civic service navigation
- Puerto Rico business resources
- municipal information
- emergency and weather source navigation
- tourism and local discovery
- public data and research
- future embeddable and white-label deployments
