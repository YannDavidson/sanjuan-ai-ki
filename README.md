# SanJuan AI KI

![Beta](https://img.shields.io/badge/status-public%20beta%20prep-61e4c5)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)
![Next.js](https://img.shields.io/badge/frontend-Next.js-black)
![Retrieval](https://img.shields.io/badge/retrieval-hybrid%20keyword%20%2B%20vector-purple)
![Bilingual](https://img.shields.io/badge/language-English%20%2B%20Spanish-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**SanJuan AI KI** is a bilingual, citation-first civic intelligence platform for Puerto Rico, starting with San Juan and expanding island-wide.

> Modern Caribbean Intelligence — built for Puerto Rico first.

SanJuan AI helps residents, founders, visitors, researchers, civic technologists, and public-sector partners ask questions about Puerto Rico and receive answers grounded in trusted public sources.

---

## What problem does this solve?

Puerto Rico public information is important but fragmented across many websites: government portals, agency pages, municipal services, permits, business resources, tax guidance, health information, weather alerts, tourism resources, and public safety notices.

SanJuan AI turns that fragmented ecosystem into a searchable, explainable, bilingual knowledge layer.

The project is designed around one principle:

> **No source, no answer.**

For sensitive topics such as permits, taxes, health, legal/court information, immigration, public benefits, police, and emergency guidance, SanJuan AI should cite official sources and avoid guessing.

---

## Current MVP capabilities

- Curated Puerto Rico source registry
- Static page ingestion
- Bounded same-domain crawling
- Agency-specific loader profiles
- Source freshness/status dashboard
- Document chunking
- Local keyword retrieval
- Local deterministic vector-search scaffold
- Hybrid keyword + vector retrieval
- Spanish-first bilingual query expansion
- FastAPI backend
- Next.js web app
- Citation-first `/ask` response contract
- Structured answers with direct answer, steps, requirements, citations, confidence, related agencies, and warnings
- Local smoke tests and retrieval fixture tests
- GitHub Actions CI
- Deployment configuration for backend and web

---

## Screenshots and demo media

Public beta visual assets are being prepared.

| Asset | Status |
| --- | --- |
| Project logo | Placeholder ready |
| Architecture diagram | Placeholder ready |
| Web app screenshot | To be captured before beta invite |
| `/ask` demo GIF | To be captured before beta invite |
| Source status dashboard screenshot | To be captured before beta invite |

Suggested paths:

```txt
assets/logo/sanjuan-ai-logo.svg
assets/diagrams/architecture.md
assets/screenshots/README.md
assets/demo/README.md
```

---

## Architecture

```txt
Source Registry
      ↓
Ingestion Pipeline
      ↓
Raw Documents
      ↓
Chunking
      ↓
Keyword Search + Local Vector Search
      ↓
Hybrid Retrieval
      ↓
Structured /ask Answer
      ↓
Next.js Web App
```

Read the architecture placeholder: [`docs/ARCHITECTURE_OVERVIEW.md`](docs/ARCHITECTURE_OVERVIEW.md)

---

## How SanJuan AI works

1. **Register trusted sources** in `data/sources/pr_sources.yml`.
2. **Ingest public content** using homepage ingestion, bounded crawling, or agency-specific loaders.
3. **Normalize and store documents** under `data/documents/raw/`.
4. **Chunk documents** into retrieval-ready evidence blocks.
5. **Build local vectors** using deterministic bilingual-expanded hashed vectors.
6. **Search with hybrid retrieval** using keyword and vector results.
7. **Answer with citations** through the FastAPI `/ask` endpoint.
8. **Display structured answers** in the Next.js web app.

---

## Quick Start

### 1. Clone and install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run tests

```bash
pytest -q
```

### 3. Start the API

```bash
uvicorn apps.api.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

### 4. Start the web app

```bash
cd apps/web
npm install
npm run dev
```

Open:

```txt
http://localhost:3000
```

---

## Build local retrieval artifacts

Homepage-only ingestion:

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

Agency-specific loader mode:

```bash
python -m packages.ingestion.batch_ingest_sources --agency-loaders --max-pages 3 --pretty
```

Chunk documents:

```bash
python -m packages.retrieval.chunk_documents --pretty
```

Build local vectors:

```bash
python -m packages.retrieval.local_vector_search build --pretty
```

Test hybrid retrieval:

```bash
python -m packages.retrieval.hybrid_search "business registration Puerto Rico" --pretty
python -m packages.retrieval.hybrid_search "registro de negocio Puerto Rico" --pretty
```

---

## Example questions

Try questions like:

```txt
How do I register a business in Puerto Rico?
Where can I find San Juan municipal services?
What official sources should I check for hurricane alerts?
How do I renew a driver's license in Puerto Rico?
What agency handles Puerto Rico taxes?
¿Qué necesito para registrar un negocio en Puerto Rico?
¿Dónde encuentro servicios municipales de San Juan?
¿Qué fuentes oficiales debo revisar durante una emergencia?
```

---

## Supported source categories

Current source registry coverage includes:

- Puerto Rico government portal
- Alerts and emergency information
- Transportation and DTOP
- Health
- Economic development
- Taxes and Hacienda
- Business registration and Departamento de Estado
- San Juan municipal services
- Tourism
- Census/demographic data
- Weather
- Earthquakes

---

## Documentation

Core docs:

- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
- [`docs/ASK_ANSWER_FORMAT.md`](docs/ASK_ANSWER_FORMAT.md)
- [`docs/BILINGUAL_RETRIEVAL.md`](docs/BILINGUAL_RETRIEVAL.md)
- [`docs/AGENCY_LOADERS.md`](docs/AGENCY_LOADERS.md)
- [`docs/CRAWLING_RULES.md`](docs/CRAWLING_RULES.md)
- [`docs/SOURCE_STATUS_DASHBOARD.md`](docs/SOURCE_STATUS_DASHBOARD.md)
- [`docs/API_ABUSE_PROTECTION.md`](docs/API_ABUSE_PROTECTION.md)
- [`docs/PUBLIC_BETA_CHECKLIST.md`](docs/PUBLIC_BETA_CHECKLIST.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md)
- [`CHANGELOG.md`](CHANGELOG.md)

Community docs:

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`SECURITY.md`](SECURITY.md)
- [`SUPPORTED_VERSIONS.md`](SUPPORTED_VERSIONS.md)

---

## FAQ

### Is this an official government project?

No. SanJuan AI is an independent civic technology project. It is designed to cite official public sources whenever possible, but it is not an official government service.

### Can I rely on it for legal, tax, medical, immigration, emergency, or permit decisions?

No. Use SanJuan AI as a research and navigation tool. Always verify sensitive topics directly with the cited official agency.

### Does it use paid AI APIs?

The current MVP retrieval layer runs locally with keyword search and deterministic hashed vector search. Future versions may add provider-based embeddings or LLM summarization, but the project is designed to remain citation-first.

### Is it bilingual?

Yes. The MVP includes English and Spanish query expansion, accent normalization, and mixed-language retrieval support.

### Can I add a new Puerto Rico source?

Yes. Open an issue using the new source template or submit a pull request updating `data/sources/pr_sources.yml`.

---

## Contributing

Contributions are welcome during beta preparation. Start with:

```bash
pytest -q
cd apps/web
npm install
npm run build
```

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

Good first contribution areas:

- Add or verify Puerto Rico sources
- Improve Spanish/English glossary terms
- Improve documentation
- Add source-specific loaders
- Improve tests
- Capture screenshots and demo GIFs
- Validate deployment docs

---

## Public beta status

SanJuan AI is preparing for public beta.

Before inviting external testers, track the checklist in:

[`docs/PUBLIC_BETA_CHECKLIST.md`](docs/PUBLIC_BETA_CHECKLIST.md)

---

## Roadmap

Near-term roadmap:

1. Public beta repository polish
2. Citation-aware answer synthesis
3. Agency-specific reasoning
4. Conversation memory
5. Multi-source evidence fusion
6. Source quality scoring
7. PDF and form ingestion
8. Government service workflow guidance

Read the full roadmap: [`ROADMAP.md`](ROADMAP.md)

---

## Security

Please do not report security issues through public GitHub issues.

Read [`SECURITY.md`](SECURITY.md).

---

## License

MIT License. See [`LICENSE`](LICENSE).
