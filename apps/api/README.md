# SanJuan AI API

FastAPI backend for SanJuan AI's Puerto Rico source registry, local ingestion pipeline, retrieval layer, and citation-first `/ask` endpoint.

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

Citation-first assistant endpoint. The MVP uses local keyword retrieval over chunked documents and returns extractive answers from the top evidence block. It does not call an external LLM yet.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I register a business in Puerto Rico?","language":"en"}'
```

The response includes:

- `answer`
- `language`
- `confidence`
- `citations`
- `sources`
- `safety_note`

If no chunks are available or no evidence is found, `/ask` returns a clear fallback instead of guessing.

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

## Batch ingest registered sources

Create one raw JSON document per registered source:

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

By default, output is written to:

```txt
data/documents/raw/
```

Each document includes source metadata, fetch status, page title, normalized text, fetch timestamp, content hash, status code, content length, and structured error details when a source cannot be fetched.

Useful options:

```bash
python -m packages.ingestion.batch_ingest_sources \
  --registry data/sources/pr_sources.yml \
  --output-dir data/documents/raw \
  --timeout 20 \
  --pretty
```

## Chunk documents for retrieval

After batch ingestion, split raw documents into citation-ready chunks:

```bash
python -m packages.retrieval.chunk_documents --pretty
```

By default, chunks are read from and written to:

```txt
Input:  data/documents/raw/
Output: data/documents/chunks/
```

Each chunk preserves citation-critical metadata:

- stable `chunk_id`
- `document_id`
- `chunk_index`
- chunk text
- character count
- source ID and name
- source URL
- page title
- trust level
- category
- geography
- language
- fetched timestamp
- content hash
- citation object

Useful options:

```bash
python -m packages.retrieval.chunk_documents \
  --input-dir data/documents/raw \
  --output-dir data/documents/chunks \
  --chunk-size 1200 \
  --chunk-overlap 200 \
  --pretty
```

## Search local chunks

Run local keyword retrieval over chunked documents:

```bash
python -m packages.retrieval.keyword_search "business registration Puerto Rico" --pretty
```

Useful filters:

```bash
python -m packages.retrieval.keyword_search "permit" \
  --trust-level official \
  --language es \
  --limit 5 \
  --pretty
```

The search layer ranks chunks using exact phrase matches, token overlap, metadata matches, and source trust boosts. It is intentionally simple and transparent for the MVP.

## End-to-end local data flow

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
python -m packages.retrieval.chunk_documents --pretty
python -m packages.retrieval.keyword_search "business registration Puerto Rico" --pretty
uvicorn apps.api.main:app --reload
```

Then test `/ask`:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"business registration Puerto Rico","language":"en"}'
```
