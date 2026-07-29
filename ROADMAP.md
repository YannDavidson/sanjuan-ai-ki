# SanJuan AI Roadmap

This roadmap describes the path from MVP to public beta and beyond.

## Current status

SanJuan AI has a working technical foundation:

- FastAPI backend
- Next.js frontend
- Source registry
- Ingestion pipeline
- Bounded crawler with robots.txt support and polite request delays
- Agency-specific loader profiles
- Chunking
- Keyword retrieval
- Local vector-search scaffold
- Hybrid retrieval
- Spanish-first bilingual retrieval
- Structured `/ask` answers
- Source status dashboard
- SanJuan Knowledge Graph foundation
- Smoke tests and CI

## v1.0.0-beta preparation

Goal: make the repository easy to understand, run, test, and contribute to.

- [x] Public beta checklist
- [x] Professional README
- [x] Contributing guide
- [x] Security policy
- [x] Code of conduct
- [x] Known limitations
- [x] Changelog
- [x] Supported versions policy
- [x] Final logo asset
- [x] Launch-hardening review fixes
- [x] SanJuan Knowledge Graph foundation
- [ ] Screenshots
- [ ] Demo GIF
- [ ] Fresh clone test
- [ ] CI green on latest commit

## SanJuan Knowledge Graph direction

The graph is a Git-backed, Obsidian-compatible evidence layer containing connected agency, service, topic, and location nodes.

Near-term graph work:

1. Compile graph nodes from ingested official evidence.
2. Add graph-aware retrieval alongside raw chunk retrieval.
3. Add stale-evidence detection and review queues.
4. Add bilingual node aliases and paired content.
5. Add human review fingerprints and approval history.

The graph must remain citation-linked to raw official evidence and must never become an unsupported source of truth.

## LLM direction

The current extractive, deterministic answer path is intentional for the MVP. It provides a testable safety baseline while the source registry, crawling, retrieval, citations, bilingual behavior, and knowledge graph mature.

The planned direction is citation-aware LLM synthesis that:

- receives only retrieved evidence and graph context
- preserves source URLs and evidence boundaries
- refuses unsupported sensitive claims
- does not invent fees, requirements, dates, forms, or eligibility rules
- can be disabled in favor of deterministic extraction

## Phase 2 — Intelligence

1. Citation-aware answer synthesis
2. Agency-specific reasoning
3. Conversation memory
4. Multi-source evidence fusion
5. Source quality scoring
6. Temporal reasoning for stale/current information
7. PDF and form ingestion
8. Government service workflow guidance
9. Knowledge Graph retrieval integration

## Phase 3 — Public usefulness

- Better Spanish-first UX
- Source request workflow
- Admin dashboard
- Public feedback loop
- Deployment hardening
- Scheduled ingestion refresh
- Better source freshness alerts
- Knowledge Graph review dashboard

## Phase 4 — Puerto Rico expansion

- Broader municipality coverage
- More official agencies
- Public benefits navigation
- Business and startup resource navigation
- Emergency preparedness guidance
- Transportation and license workflows
- Health source navigation

## Long-term vision

SanJuan AI can become the first deployment of a broader Puerto Rico/Caribbean civic intelligence network:

- SanJuan AI — city/metro assistant
- Puerto Rico AI — island-wide assistant
- Caribbean AI — regional knowledge platform
- Local AI Framework — reusable civic intelligence infrastructure
