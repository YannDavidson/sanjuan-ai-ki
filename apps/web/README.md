# SanJuan AI Web

Next.js MVP web app for SanJuan AI.

## What is included

- `/` — landing page for the SanJuan AI vision
- `/ask` — citation-first assistant UI connected to the FastAPI backend
- `/sources` — filterable source registry directory

The source directory currently reads from:

```txt
data/sources/pr_sources.yml
```

## Run locally

First, start the backend from the repo root:

```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload
```

Then start the web app:

```bash
cd apps/web
npm install
npm run dev
```

Then open:

```txt
http://localhost:3000
```

## API configuration

The `/ask` page calls the FastAPI backend using this environment variable:

```bash
NEXT_PUBLIC_SANJUAN_API_URL=http://127.0.0.1:8000
```

If the variable is not set, the app defaults to:

```txt
http://127.0.0.1:8000
```

## Design principles

- Modern Caribbean intelligence
- Clean civic-tech feel
- Dark mode first
- Bilingual-ready copy
- Citation-first answer UX
- Official source trust is visible in the interface

## Next steps

1. Replace the `/ask` placeholder backend answer with retrieval results.
2. Show real citations once source chunking and search are implemented.
3. Add Spanish UI copy and language toggle.
4. Add deployment configuration.
