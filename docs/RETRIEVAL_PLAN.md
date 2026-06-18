# SanJuan AI Retrieval and Citation Plan

SanJuan AI must behave like a trusted Puerto Rico public knowledge layer, not a generic chatbot. The retrieval system should make it easy to answer local questions while showing exactly where the answer came from.

## Goals

1. Retrieve the most relevant Puerto Rico-specific sources.
2. Prefer official sources for government, legal, health, safety, tax, permit, public benefit, court, police, and emergency questions.
3. Support English and Spanish queries.
4. Return citations in every answer that uses external facts.
5. Say when the system does not know instead of inventing answers.
6. Keep source metadata visible to users.

## MVP retrieval flow

```txt
User question
  ↓
Language detection and topic classification
  ↓
High-risk topic check
  ↓
Candidate source filtering
  ↓
Keyword + semantic retrieval
  ↓
Trust, geography, recency, and language ranking
  ↓
Answer generation with citations
  ↓
Fallback if evidence is weak or missing
```

## Source ranking strategy

Each candidate source should receive a score using these dimensions:

| Signal | Purpose | MVP Weight |
| --- | --- | --- |
| Text relevance | Match between query and source content | High |
| Trust level | Prefer official and institutional sources | High |
| Geography | Prefer San Juan or Puerto Rico sources depending on question | Medium |
| Recency | Prefer newer content when dates exist | Medium |
| Language | Prefer user's language when available | Medium |
| Category | Match topic category such as health, transport, taxes, tourism | Medium |

Suggested trust boost:

```txt
official: +0.35
institutional: +0.20
community: +0.05
experimental: +0.00
```

For high-risk questions, only `official` and selected `institutional` sources should be allowed unless a human admin explicitly approves an exception.

## High-risk topic policy

High-risk topics include:

- Emergency instructions
- Health and medical guidance
- Legal procedures
- Taxes
- Permits and licensing
- Public benefits
- Immigration
- Courts and police matters
- Disaster response
- Public safety alerts

For these topics, SanJuan AI should:

1. Use official sources first.
2. Include source citations in the answer.
3. Avoid giving definitive advice when the source is unclear or outdated.
4. Recommend contacting the relevant agency for case-specific decisions.
5. Avoid claiming fees, deadlines, office hours, eligibility rules, or procedures unless they appear in retrieved evidence.

## Chunking strategy

For web pages, PDFs, and long documents:

- Extract page title, URL, source ID, fetched timestamp, language, and category.
- Split text into chunks of roughly 500–900 tokens.
- Use 100–150 token overlap for continuity.
- Preserve section headings where possible.
- Store source metadata with every chunk.

Chunk metadata should include:

```json
{
  "source_id": "pr_gov_main",
  "source_name": "PR.gov",
  "url": "https://www.pr.gov/",
  "title": "Page title",
  "category": "government_portal",
  "geography": "puerto_rico",
  "language": "es",
  "trust_level": "official",
  "fetched_at": "2026-06-18T00:00:00Z",
  "published_at": null,
  "chunk_index": 0
}
```

## Metadata strategy

Every source and chunk should carry enough metadata to support filtering and transparent answers.

Required source metadata:

- `id`
- `name`
- `url`
- `category`
- `geography`
- `language`
- `trust_level`
- `source_type`
- `update_frequency`
- `notes`

Recommended document metadata:

- `document_id`
- `source_id`
- `url`
- `title`
- `language`
- `content_hash`
- `fetched_at`
- `published_at`
- `updated_at`

Recommended chunk metadata:

- `chunk_id`
- `document_id`
- `source_id`
- `chunk_index`
- `heading`
- `category`
- `geography`
- `language`
- `trust_level`

## Citation strategy

Every generated answer should include a `citations` array.

MVP citation object:

```json
{
  "source_id": "pr_dtop",
  "source_name": "Departamento de Transportación y Obras Públicas",
  "title": "DTOP page title",
  "url": "https://www.dtop.pr.gov/",
  "trust_level": "official",
  "snippet": "Short evidence excerpt or summary",
  "fetched_at": "2026-06-18T00:00:00Z"
}
```

Rules:

1. Every factual paragraph should be traceable to at least one citation.
2. Do not cite sources that were not actually used.
3. Prefer direct source URLs over homepages when page-level URLs are available.
4. For high-risk topics, answers without citations should be refused or downgraded to a source-navigation response.
5. Citations should appear both in the API response and in the UI.

## Bilingual retrieval strategy

MVP:

- Accept a user-provided `language` value of `en` or `es`.
- If language is omitted, infer from the question later.
- Search sources in both English and Spanish when possible.
- Prefer answer language matching the user's question.
- Keep official agency names in their original language.

Future:

- Translate query terms for cross-lingual retrieval.
- Store multilingual aliases for common topics:
  - permits / permisos
  - taxes / contribuciones / hacienda
  - health / salud
  - transportation / transportación
  - business registration / registro de comerciante / registro corporativo
- Use bilingual embeddings or multilingual retrieval models.

## Fallback behavior

When no trusted answer is found, SanJuan AI should say:

> I do not have enough trusted source evidence to answer that confidently yet.

Then provide:

- Related official sources from the registry
- Suggested next search terms
- A note that the source registry is still growing

For high-risk questions, the fallback should be stricter:

> I cannot answer that confidently without an official source. Here are the most relevant official Puerto Rico sources to check.

## API answer contract

The `/ask` endpoint should use this response shape:

```json
{
  "answer": "Human-readable answer.",
  "language": "en",
  "confidence": "placeholder",
  "citations": [],
  "sources": [],
  "safety_note": null
}
```

Field definitions:

- `answer`: final user-facing answer
- `language`: response language
- `confidence`: `high`, `medium`, `low`, or `placeholder`
- `citations`: specific evidence used in the answer
- `sources`: broader relevant sources
- `safety_note`: optional warning for high-risk topics

## Frontend UX requirements

The web app should make source trust visible.

On the ask page:

- Show that retrieval is not yet connected.
- Show the planned citation-first answer structure.
- Display example citations as cards.
- Make it clear that official sources are prioritized.

On the sources page:

- Show source name, category, geography, language, trust level, and URL.
- Add filters for category, trust level, geography, and language.
- Use badges for trust levels.

## MVP implementation phases

### Phase A: Current source registry

- YAML source registry is the source of truth.
- `/sources` exposes source registry.
- `/ask` returns placeholder answer contract.

### Phase B: Static page ingestion

- Fetch allowed public pages.
- Extract title and text.
- Store normalized documents and chunks.
- Add content hash to avoid duplicates.

### Phase C: Retrieval MVP

- Add keyword search first.
- Add vector search with pgvector.
- Rank by relevance, trust, geography, language, and recency.
- Return citations from matched chunks.

### Phase D: Production RAG

- Add hybrid retrieval.
- Add user language detection.
- Add source freshness warnings.
- Add admin source review workflow.
- Add municipal expansion.

## Definition of done for Issue #4

- `docs/RETRIEVAL_PLAN.md` exists.
- It explains ranking, chunking, metadata, citations, bilingual retrieval, fallback behavior, and high-risk safety.
- The `/ask` response contract supports citation-first UX.
- The web app can be built around citations from the beginning.
