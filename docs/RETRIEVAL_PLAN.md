# SanJuan AI Retrieval and Citation Plan

SanJuan AI is a trusted Puerto Rico public knowledge layer, not a generic chatbot.

This document describes the retrieval system that exists today and the planned path toward stronger synthesis.

## Current retrieval flow

```txt
User question
  ↓
Language detection + high-risk topic check
  ↓
Spanish-first bilingual query expansion
  ↓
Keyword retrieval + local vector retrieval
  ↓
Hybrid ranking
  ↓
Trust, geography, language, and metadata weighting
  ↓
Deterministic structured answer builder
  ↓
Citations, related agencies, confidence, and safety warning
```

## Current implementation

The MVP currently includes:

- committed YAML source registry
- JSON raw documents, chunks, and vector files
- keyword retrieval
- deterministic local hashed vectors
- hybrid result fusion
- English/Spanish query expansion
- source trust weighting
- category, geography, trust, and language filters
- citation metadata on every retrieval result
- safe fallback behavior when evidence is missing

## Ranking principles

| Signal | Current role |
| --- | --- |
| Text relevance | Primary keyword/vector match |
| Trust level | Official sources receive the strongest boost |
| Geography | Supports Puerto Rico and San Juan relevance |
| Language | Mixed-language retrieval with Spanish-first support |
| Category | Helps match taxes, permits, health, transport, and other topics |
| Recency | Used when fetched timestamps are available; stronger temporal reasoning is planned |

## High-risk topic policy

High-risk topics include:

- emergencies and public safety
- health and medical information
- legal procedures
- taxes
- permits and licensing
- public benefits
- immigration
- courts and police matters

For these topics, SanJuan AI should:

1. Prefer official sources.
2. Cite the evidence used.
3. Avoid inventing fees, deadlines, eligibility, office hours, forms, or procedures.
4. State when the corpus is insufficient.
5. Encourage verification with the responsible agency.

## Chunk and citation metadata

Each retrieval chunk should preserve:

- chunk ID
- document ID
- source ID and name
- direct source URL
- title
- category
- geography
- language
- trust level
- fetched timestamp
- content hash
- citation object

## Current answer contract

`/ask` returns:

- `answer`
- `language`
- `confidence`
- `citations`
- `sources`
- `safety_note`
- `ingestion_status`
- `structured_answer`

The structured answer includes:

- direct answer
- steps to follow
- requirements
- official citations
- last updated date
- confidence
- related agencies
- official-source warning

## Bilingual retrieval

The current MVP uses a deterministic English/Spanish civic glossary and accent normalization.

It supports mappings such as:

```txt
business registration ↔ registro de negocio / corporaciones
permits ↔ permisos
taxes ↔ impuestos / hacienda
services ↔ servicios / trámites
health ↔ salud
weather ↔ clima / pronóstico
```

This is not full translation. Strong multilingual embeddings and trusted query translation remain future improvements.

## LLM direction

The current no-LLM, extractive answer builder is intentional for the MVP because it is deterministic, testable, and less likely to invent official procedures.

It is not necessarily permanent.

The planned direction is **citation-aware LLM synthesis**, introduced only after:

- the corpus is populated and evaluated
- source freshness is visible
- citations are preserved end to end
- unsupported claims can be detected
- sensitive-topic answers can fall back safely

Any future LLM layer must summarize retrieved evidence rather than answer from unsupported model memory.

## Future retrieval improvements

- multilingual embedding provider
- Postgres full-text search and pgvector
- temporal reasoning and stale-source penalties
- multi-source evidence fusion
- citation-aware synthesis
- PDF, form, and table parsing
- source quality scoring
- evaluation datasets for English and Spanish questions
