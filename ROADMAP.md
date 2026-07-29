# SanJuan AI Roadmap

This roadmap describes the path from the current MVP to public beta and production-grade civic intelligence.

## Current foundation

- FastAPI backend
- Next.js frontend
- Source registry
- Homepage ingestion, bounded crawling, and agency loaders
- robots.txt checks and polite crawl delays
- JSON document/chunk/vector storage
- Keyword and local vector retrieval
- Hybrid retrieval
- Spanish-first bilingual expansion
- Structured extractive `/ask` answers
- Source status dashboard
- Smoke tests and CI
- Deployment configuration

## v1.0.0-beta preparation

- [x] Public beta checklist
- [x] Professional README
- [x] Community, security, and contribution policies
- [x] Known limitations and changelog
- [x] Architecture documentation aligned with current code
- [x] `.gitignore`
- [x] robots.txt and crawl-delay support
- [x] Production CORS configuration path
- [x] Vercel `/sources` hardening
- [x] Documentation drift cleanup
- [x] Logo and favicon assets
- [ ] Screenshots
- [ ] Demo GIF
- [ ] Fresh-clone test
- [ ] CI green on latest release candidate
- [ ] Build and evaluate the first real corpus

## Answer-generation strategy

The current extractive, no-LLM answer builder is an intentional first stage, not the final destination.

It provides a deterministic safety baseline while the corpus, citations, freshness signals, and evaluation suite mature.

The next intelligence milestone is **citation-aware LLM synthesis**. Any future model must:

- answer only from retrieved evidence
- preserve direct citations
- avoid unsupported requirements, fees, deadlines, and procedures
- fall back safely when evidence is insufficient
- apply stricter controls to high-risk topics

## Phase 2 — Intelligence

1. Citation-aware answer synthesis
2. Multi-source evidence fusion
3. Agency-specific reasoning
4. Source quality scoring
5. Temporal reasoning for current vs. outdated guidance
6. Conversation memory with cited context
7. PDF, form, and table ingestion
8. Government service workflow guidance

## Phase 3 — Public usefulness

- Better Spanish-first UX
- Answer feedback and correction workflow
- Source request workflow
- Admin dashboard
- Scheduled ingestion refresh
- Source freshness alerts
- Production storage and distributed rate limiting

## Phase 4 — Puerto Rico expansion

- Broader municipality coverage
- More official agencies
- Public benefits navigation
- Business and startup resource navigation
- Emergency preparedness guidance
- Transportation and license workflows
- Health source navigation

## Long-term vision

- SanJuan AI — city and metro assistant
- Puerto Rico AI — island-wide assistant
- Caribbean AI — regional knowledge platform
- Local AI Framework — reusable civic intelligence infrastructure
