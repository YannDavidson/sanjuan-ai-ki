# SanJuan AI Web

Next.js web app for the SanJuan AI public beta.

## Routes

- `/` — landing page
- `/ask` — structured citation-first assistant UI
- `/sources` — filterable source registry
- `/status` — source/corpus status dashboard

## Current capabilities

The web app currently supports:

- English and Spanish question selection
- Hybrid retrieval responses from the FastAPI backend
- Direct answers, steps, requirements, confidence, and warnings
- Citation cards
- Related agency cards
- Corpus readiness indicators
- Source registry filters
- Source status visibility

## Source registry

The `/sources` page reads:

```txt
data/sources/pr_sources.yml
```

`next.config.ts` includes the registry in standalone output tracing. The loader also checks multiple runtime paths and returns an empty state instead of crashing if the file is unavailable.

## Run locally

Start the backend from the repository root:

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

Open:

```txt
http://localhost:3000
```

## API configuration

```bash
NEXT_PUBLIC_SANJUAN_API_URL=http://127.0.0.1:8000
```

For production, set this to the deployed API URL and configure the API's `SANJUAN_CORS_ORIGINS` to include the deployed web origin.

## Build validation

```bash
npm run build
```

After deployment, verify `/ask`, `/sources`, and `/status`.

## Next improvements

- Capture public beta screenshots and demo GIFs
- Improve Spanish-first UI copy
- Add a clearer empty state when the source registry is unavailable
- Add feedback controls for incorrect answers
- Add conversation history after the citation-aware synthesis layer is ready
