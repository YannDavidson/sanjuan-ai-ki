# SanJuan AI Deployment

This document describes the first deployment-ready setup for the SanJuan AI MVP.

The project currently has two deployable services:

1. **API service** — FastAPI backend in `apps/api`
2. **Web service** — Next.js frontend in `apps/web`

The backend and frontend can be deployed separately. The web app talks to the API through the `NEXT_PUBLIC_SANJUAN_API_URL` environment variable.

## Backend deployment

### Production start command

From the repository root:

```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Required files

- `requirements.txt`
- `apps/api/main.py`
- `render.yaml` for Render-style deployment
- `Dockerfile.api` for container deployment

### Render-style setup

The included `render.yaml` defines a web service named `sanjuan-ai-api`.

Default values:

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

### Backend environment variables

No secrets are required for the current MVP backend.

Future likely variables:

```bash
SANJUAN_ENV=production
SANJUAN_CORS_ORIGINS=https://your-web-domain.com
SANJUAN_RETRIEVAL_MODE=hybrid
```

## Web deployment

### Production build

From `apps/web`:

```bash
npm install
npm run build
npm run start
```

### Required environment variable

```bash
NEXT_PUBLIC_SANJUAN_API_URL=https://your-api-domain.com
```

For local development, this defaults to:

```bash
http://127.0.0.1:8000
```

### Vercel-style setup

The included `apps/web/vercel.json` configures the Next.js app as the web project root.

On Vercel, use:

- Framework preset: Next.js
- Root directory: `apps/web`
- Build command: `npm run build`
- Output: Next.js default

Set:

```bash
NEXT_PUBLIC_SANJUAN_API_URL=https://your-api-domain.com
```

## Container deployment

Build the API container from the repository root:

```bash
docker build -f Dockerfile.api -t sanjuan-ai-api .
docker run -p 8000:8000 sanjuan-ai-api
```

Then open:

```txt
http://127.0.0.1:8000/health
```

## Deployment checklist

Before deploying:

```bash
pip install -r requirements.txt
pytest -q
cd apps/web
npm install
npm run build
```

After deploying:

1. Open `/health` on the API.
2. Confirm the response includes `status: ok`.
3. Set `NEXT_PUBLIC_SANJUAN_API_URL` in the web app.
4. Open `/ask` and submit a test question.
5. Open `/sources` and `/status`.

## Current MVP limitation

The production API currently reads local file-based corpus artifacts from the repository filesystem. For a real hosted deployment, run ingestion/chunking/vector generation before deployment or mount/persist generated artifacts.

Recommended future upgrade:

- Move documents/chunks/vectors into Postgres + pgvector or object storage.
- Add a scheduled ingestion job.
- Add an admin-only source refresh command.
