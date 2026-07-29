# SanJuan AI Deployment

SanJuan AI currently has two deployable services:

1. FastAPI backend in `apps/api`
2. Next.js frontend in `apps/web`

The frontend calls the backend through `NEXT_PUBLIC_SANJUAN_API_URL`.

## Backend deployment

Start command:

```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Render setup

`render.yaml` defines the API service and now declares the production CORS variable as a required dashboard value.

Set:

```bash
SANJUAN_ENV=production
SANJUAN_API_VERSION=0.6.0
SANJUAN_CORS_ORIGINS=https://your-web-domain.com
SANJUAN_CORS_ALLOW_CREDENTIALS=false
SANJUAN_RATE_LIMIT_ENABLED=true
SANJUAN_ASK_RATE_LIMIT_PER_MINUTE=30
```

`SANJUAN_CORS_ORIGINS` is required for browser access from the deployed frontend. Use a comma-separated list if more than one origin is needed. Do not use `*` when credentials are enabled.

After deployment, `/health` should report:

```txt
status: ok
cors_configured: true
```

The API also adds security headers and an MVP in-memory `/ask` rate limiter. Public traffic should eventually use edge, API-gateway, or Redis-backed protection.

## Web deployment

From `apps/web`:

```bash
npm install
npm run build
npm run start
```

Set:

```bash
NEXT_PUBLIC_SANJUAN_API_URL=https://your-api-domain.com
```

### Vercel / standalone source registry

The web app reads `data/sources/pr_sources.yml`. `apps/web/next.config.ts` now configures output-file tracing so the registry is included in standalone deployments.

`apps/web/lib/sources.ts` also checks multiple runtime paths and returns a safe empty list instead of crashing if the registry is unavailable.

After deployment, open `/sources` and verify that the registry appears. If it is empty, inspect the build output and root-directory settings.

Recommended Vercel settings:

- Framework: Next.js
- Root directory: `apps/web`
- Build command: `npm run build`
- Environment: `NEXT_PUBLIC_SANJUAN_API_URL`

## Corpus refresh

Run the local refresh pipeline:

```bash
python -m packages.ingestion.refresh_corpus --pretty
```

Dry-run validation:

```bash
python -m packages.ingestion.refresh_corpus --dry-run --pretty
```

The current hosted API reads file-based corpus artifacts. Run ingestion/chunking/vector generation before deployment or provide persistent storage.

## Deployment checklist

Before deployment:

```bash
pip install -r requirements.txt
pytest -q
cd apps/web
npm install
npm run build
```

After deployment:

1. Confirm API `/health` returns `status: ok`.
2. Confirm `cors_configured: true`.
3. Confirm the web app can call `/ask`.
4. Confirm `/sources` renders without a server error.
5. Confirm `/status` renders a dashboard or safe fallback.
6. Verify citations open the intended official pages.

## Future production upgrade

- Postgres + pgvector or managed vector storage
- object storage for raw documents
- scheduled ingestion workers
- distributed rate limiting
- stronger multilingual embeddings
- citation-aware LLM synthesis
