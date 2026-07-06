# Public Beta Readiness Checklist

Use this checklist before inviting external testers to SanJuan AI.

## Repository readiness

- [x] Polished README with quick start
- [x] Project badges
- [x] Architecture overview placeholder
- [x] Roadmap
- [x] Known limitations
- [x] Changelog
- [x] Contributing guide
- [x] Code of conduct
- [x] Security policy
- [x] Supported versions policy
- [x] License
- [ ] Screenshots captured and committed
- [ ] Demo GIF captured and committed
- [ ] Logo asset finalized and committed

## Engineering readiness

- [ ] Latest CI run is green
- [ ] `pytest -q` passes locally
- [ ] `npm run build` passes in `apps/web`
- [ ] `/health` returns `status: ok`
- [ ] `/ask` returns structured answers
- [ ] `/sources` loads the source registry
- [ ] `/status` loads source health data or a helpful fallback
- [ ] Deployment docs verified on a clean environment

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

- [ ] Example questions listed in README
- [ ] Feedback instructions visible
- [ ] Bug-report issue template added
- [ ] New-source issue template added
- [ ] Contribution instructions clear
- [ ] Known limitations visible
- [ ] Sensitive-topic disclaimer visible

## Suggested beta invitation wording

> SanJuan AI is an early public beta of a bilingual, citation-first civic intelligence assistant for Puerto Rico. It is not an official government service. Please test it, verify citations, report bad answers, and suggest trusted Puerto Rico sources.

## Do not launch public beta until

- CI is green.
- README quick start has been tested on a fresh clone.
- At least one screenshot or demo GIF is available.
- Known limitations are visible.
- Sensitive-topic disclaimers are visible.
