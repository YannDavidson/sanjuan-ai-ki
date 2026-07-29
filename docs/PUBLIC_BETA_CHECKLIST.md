# Public Beta Readiness Checklist

Use this checklist before inviting external testers to SanJuan AI.

## Repository readiness

- [x] Polished README with quick start
- [x] Project badges
- [x] Current architecture clearly separated from future architecture
- [x] Roadmap
- [x] Known limitations
- [x] Changelog
- [x] Contributing guide
- [x] Code of conduct
- [x] Security policy
- [x] Supported versions policy
- [x] License
- [x] Comprehensive `.gitignore`
- [ ] Screenshots captured and committed
- [ ] Demo GIF captured and committed
- [x] Logo asset finalized and committed
- [x] Favicon/icon asset committed

## Engineering readiness

- [ ] Latest CI run is green
- [ ] `pytest -q` passes locally
- [ ] `npm run build` passes in `apps/web`
- [ ] `/health` returns `status: ok`
- [ ] `/ask` returns structured answers
- [ ] `/sources` loads the source registry in the deployed web build
- [ ] `/status` loads source health data or a helpful fallback
- [x] Production CORS variable declared in `render.yaml`
- [x] Vercel/standalone source registry tracing configured
- [x] Source loader fails safely if the registry is unavailable
- [ ] Deployment docs verified on a clean environment

## Crawler readiness

- [x] Same-domain restriction
- [x] Allowed and blocked path controls
- [x] Per-source page caps
- [x] robots.txt checks
- [x] Polite request delay
- [x] Network-free crawl policy tests
- [ ] Low-page-cap live crawl reviewed before public scheduling

## Data readiness

- [ ] Source registry reviewed
- [ ] High-value official Puerto Rico sources verified
- [ ] Agency-specific loaders tested with low page caps
- [ ] Source status generated
- [ ] Raw documents generated
- [ ] Chunks generated
- [ ] Vectors generated
- [ ] Bilingual retrieval tested in English and Spanish

## Beta tester experience

- [x] Example questions listed in README
- [x] Feedback instructions visible through GitHub issue templates
- [x] Bug-report issue template added
- [x] New-source issue template added
- [x] Contribution instructions clear
- [x] Known limitations visible
- [x] Sensitive-topic disclaimer visible
- [x] Extractive MVP and future LLM direction documented

## Suggested beta invitation wording

> SanJuan AI is an early public beta of a bilingual, citation-first civic intelligence assistant for Puerto Rico. It is not an official government service. Please test it, verify citations, report bad answers, and suggest trusted Puerto Rico sources.

## Do not launch public beta until

- CI is green.
- README quick start has been tested on a fresh clone.
- At least one screenshot or demo GIF is available.
- The first real corpus has been built and reviewed.
- Known limitations and sensitive-topic disclaimers remain visible.
