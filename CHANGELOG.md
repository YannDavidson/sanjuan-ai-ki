# Changelog

All notable changes to SanJuan AI will be documented here.

## Unreleased

### Added

- Public beta readiness checklist
- Professional README
- Community and contribution policies
- Roadmap and known limitations
- Architecture overview
- Logo and favicon assets
- Comprehensive `.gitignore`
- robots.txt policy helper
- configurable polite crawl delay
- network-free crawl policy tests
- production CORS declaration in `render.yaml`
- Vercel/standalone source registry tracing
- safe source-registry fallback in the web app

### Changed

- `docs/ARCHITECTURE.md` now distinguishes the current JSON-based MVP from the future Postgres/pgvector architecture.
- Retrieval documentation now reflects implemented hybrid and bilingual retrieval.
- Web documentation now reflects the working `/ask`, `/sources`, and `/status` pages.
- Deployment documentation now explains production CORS and source registry tracing.
- The roadmap now clarifies that extractive no-LLM answers are an intentional MVP stage before citation-aware LLM synthesis.
- Removed the unused `SANJUAN_RETRIEVAL_MODE` example setting.

### Existing MVP foundation

- FastAPI backend
- Next.js frontend
- Source registry
- Static page ingestion
- Bounded crawling
- Agency-specific loader profiles
- Source status dashboard
- Document chunking
- Keyword retrieval
- Local vector-search scaffold
- Hybrid retrieval
- Spanish-first bilingual retrieval
- Structured `/ask` answer contract
- Smoke and retrieval fixture tests
- GitHub Actions CI
- Deployment docs

## Planned v1.0.0-beta

- Final beta screenshots
- Demo GIF
- Fresh-clone validation
- Build and review the first real corpus
- Green CI on release commit
- Beta release notes
