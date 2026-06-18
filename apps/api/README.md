# SanJuan AI API

FastAPI backend for SanJuan AI's Puerto Rico source registry and future retrieval layer.

## Run locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn apps.api.main:app --reload
```

Then open:

- API docs: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>
- Sources: <http://127.0.0.1:8000/sources>

## Endpoints

### `GET /health`

Returns service health.

```json
{
  "status": "ok",
  "service": "sanjuan-ai-api"
}
```

### `GET /sources`

Returns the validated Puerto Rico source registry.

Optional query filters:

- `category`
- `trust_level`
- `geography`
- `language`

Example:

```bash
curl "http://127.0.0.1:8000/sources?trust_level=official&language=es"
```

### `GET /sources/{source_id}`

Returns a single source by ID.

Example:

```bash
curl "http://127.0.0.1:8000/sources/pr_gov_main"
```

### `POST /ask`

Placeholder assistant endpoint until retrieval is connected. It already returns the citation-first answer contract used by the web UI.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I register a business in Puerto Rico?","language":"en"}'
```

## Validate source registry

From the repository root:

```bash
python -m packages.ingestion.load_sources
python -m packages.ingestion.load_sources --json
```

## Fetch a static page

Use the first static page ingestion script to fetch and normalize public HTML content:

```bash
python -m packages.ingestion.fetch_static_page https://www.pr.gov/ --pretty
```

The command returns JSON with:

- `url`
- `title`
- `text`
- `fetched_at`
- `content_hash`
- `status_code`
- `content_length`
