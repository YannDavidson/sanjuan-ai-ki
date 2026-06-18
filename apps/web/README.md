# SanJuan AI Web

Next.js MVP web app for SanJuan AI.

## What is included

- `/` — landing page for the SanJuan AI vision
- `/ask` — citation-first assistant UI placeholder
- `/sources` — filterable source registry directory

The source directory currently reads from:

```txt
data/sources/pr_sources.yml
```

## Run locally

From the repo root:

```bash
cd apps/web
npm install
npm run dev
```

Then open:

```txt
http://localhost:3000
```

## Design principles

- Modern Caribbean intelligence
- Clean civic-tech feel
- Dark mode first
- Bilingual-ready copy
- Citation-first answer UX
- Official source trust is visible in the interface

## Next steps

1. Connect `/ask` to the FastAPI backend.
2. Replace the placeholder answer with a live API response.
3. Show real citations once retrieval is implemented.
4. Add Spanish UI copy and language toggle.
5. Add deployment configuration.
