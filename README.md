<p align="center">
  <a href="https://postimg.cc/w7GyBPCx">
    <img src="https://i.postimg.cc/w7GyBPCx/SJAI-logo.png" alt="SanJuan KI logo" width="640" />
  </a>
</p>

<h1 align="center">SanJuan KI</h1>

<p align="center"><strong>Open Civic Knowledge Infrastructure for Puerto Rico</strong></p>

<p align="center">
  Building a trusted, bilingual knowledge layer for Puerto Rico through public evidence, open collaboration, explainable relationships, and citation-first AI.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#knowledge-bases">Knowledge Bases</a> ·
  <a href="#contributing">Contribute</a> ·
  <a href="docs/ARCHITECTURE_OVERVIEW.md">Architecture</a> ·
  <a href="ROADMAP.md">Roadmap</a>
</p>

<p align="center">
  <img alt="Open civic knowledge infrastructure" src="https://img.shields.io/badge/infrastructure-open%20civic%20knowledge-0f766e" />
  <img alt="Public beta preparation" src="https://img.shields.io/badge/status-public%20beta%20prep-61e4c5" />
  <img alt="Citation first" src="https://img.shields.io/badge/principle-citation--first-2563eb" />
  <img alt="Official sources prioritized" src="https://img.shields.io/badge/sources-official%20prioritized-7c3aed" />
  <img alt="English and Spanish" src="https://img.shields.io/badge/language-English%20%2B%20Spanish-f97316" />
  <img alt="Python 3.11 or newer" src="https://img.shields.io/badge/python-3.11%2B-3776ab" />
  <img alt="FastAPI" src="https://img.shields.io/badge/backend-FastAPI-009688" />
  <img alt="Next.js" src="https://img.shields.io/badge/frontend-Next.js-black" />
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-green" />
</p>

> **No source, no answer.**

SanJuan KI is an independent, open-source civic technology initiative for organizing, connecting, verifying, and serving Puerto Rico's public knowledge. It begins with San Juan and is designed to expand across the island.

It is not merely a chatbot. The public assistant is one interface built on top of a larger knowledge infrastructure composed of trusted sources, curated Knowledge Bases, a relationship-aware Knowledge Graph, retrieval and citation systems, and public APIs.

---

## Table of contents

- [Vision](#vision)
- [The SanJuan KI Manifesto](#the-sanjuan-ki-manifesto)
- [Why SanJuan KI exists](#why-sanjuan-ki-exists)
- [What is SanJuan KI?](#what-is-sanjuan-ki)
- [Architecture](#architecture)
- [Understanding the terminology](#understanding-the-terminology)
- [The knowledge lifecycle](#the-knowledge-lifecycle)
- [Source Registry](#source-registry)
- [Knowledge Bases](#knowledge-bases)
- [SanJuan Knowledge Graph](#sanjuan-knowledge-graph)
- [Retrieval and Citation Engine](#retrieval-and-citation-engine)
- [Public Assistant and API](#public-assistant-and-api)
- [What contributors can add](#what-contributors-can-add)
- [Trust and review model](#trust-and-review-model)
- [Contributor roles](#contributor-roles)
- [Contribution workflow](#contribution-workflow)
- [Automated validation](#automated-validation)
- [Repository structure](#repository-structure)
- [Current capabilities](#current-capabilities)
- [Quick Start](#quick-start)
- [Build local retrieval artifacts](#build-local-retrieval-artifacts)
- [Example questions](#example-questions)
- [Documentation](#documentation)
- [Why SanJuan KI is different](#why-sanjuan-ki-is-different)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Security](#security)
- [License](#license)

---

## Vision

**SanJuan KI is building the knowledge layer for Puerto Rico.**

Important public information already exists, but it is fragmented across agency portals, municipal websites, PDFs, forms, datasets, manuals, regulations, alerts, and institutional resources. The problem is not always the absence of information. The problem is that the information is difficult to discover, connect, verify, understand, and keep current.

SanJuan KI turns that fragmented ecosystem into an open, bilingual, evidence-backed knowledge infrastructure that people and software can use.

The long-term vision is a shared civic knowledge layer that can support:

- residents navigating public services;
- founders and businesses understanding procedures;
- visitors finding trustworthy local information;
- researchers studying Puerto Rico;
- civic technologists building public-interest tools;
- universities and nonprofits maintaining domain knowledge;
- agencies improving public information access;
- AI systems that must explain where their answers come from.

---

## The SanJuan KI Manifesto

We believe public knowledge should be accessible.

We believe official information should be connected instead of fragmented.

We believe people should be able to verify where an answer comes from.

We believe AI should say when reliable evidence is missing.

We believe bilingual access is essential infrastructure, not an optional feature.

We believe communities should be able to improve public knowledge together.

We believe local context, institutions, language, geography, and culture matter.

We believe Puerto Rico deserves digital infrastructure designed around its own realities.

---

## Why SanJuan KI exists

Puerto Rico's public-information environment spans many independent systems:

- central government portals;
- agency websites;
- municipal pages;
- permits and licensing systems;
- tax and business guidance;
- health resources;
- emergency bulletins;
- transportation information;
- public datasets;
- regulations, manuals, forms, and PDFs;
- institutional and community resources.

A resident may know what they need but not which agency handles it. A business owner may find several versions of a procedure without knowing which is current. A researcher may identify a useful document but not its relationship to an agency, service, or location. A generic AI assistant may produce a confident answer without reliable Puerto Rico-specific evidence.

SanJuan KI addresses this by treating civic information as maintainable infrastructure rather than disposable search results.

---

## What is SanJuan KI?

SanJuan KI is the complete infrastructure.

```text
SanJuan KI
│
├── Source Registry
│
├── Knowledge Bases
│   ├── Business & Commerce
│   ├── Transportation
│   ├── Public Health
│   ├── Emergency Information
│   ├── Municipal Services
│   └── Tourism
│
├── SanJuan Knowledge Graph
│   ├── Agencies
│   ├── Services
│   ├── Topics
│   ├── Locations
│   └── Relationships
│
├── Retrieval & Citation Engine
│
└── Public Assistant & API
```

The project separates human contribution, technical relationships, evidence retrieval, and user-facing answers so that each layer can be reviewed, tested, and improved independently.

---

## Architecture

```text
                         SANJUAN KI
          Open Civic Knowledge Infrastructure
────────────────────────────────────────────────────────

Official and verified public evidence
                       │
                       ▼
                Source Registry
                       │
                       ▼
          Knowledge Bases — human curated
                       │
                       ▼
       SanJuan Knowledge Graph — connected
                       │
                       ▼
          Retrieval & Citation Engine
                       │
                       ▼
         Public Assistant • API • Future SDK
```

A more detailed implementation view:

```text
Source Registry
      │
      ├── homepage ingestion
      ├── bounded same-domain crawling
      └── agency-specific loaders
      │
      ▼
Normalized Documents
      │
      ├── metadata
      ├── freshness status
      └── source provenance
      │
      ▼
Knowledge Bases + Knowledge Graph
      │
      ├── agencies
      ├── services
      ├── topics
      ├── locations
      └── relationships
      │
      ▼
Chunking + Local Vector Index
      │
      ▼
Hybrid Retrieval
      │
      ▼
Citation-first `/ask` response
      │
      ▼
Next.js Public Assistant
```

Read the detailed architecture overview: [`docs/ARCHITECTURE_OVERVIEW.md`](docs/ARCHITECTURE_OVERVIEW.md).

---

## Understanding the terminology

| Layer | Meaning | Primary audience |
| --- | --- | --- |
| **SanJuan KI** | The complete open civic knowledge infrastructure | Everyone |
| **Source Registry** | The catalog of public evidence, provenance, metadata, and source status | Contributors, reviewers, ingestion systems |
| **Knowledge Base** | A contributor-facing, curated subject collection | Contributors and domain communities |
| **SanJuan Knowledge Graph** | The technical relationship layer connecting agencies, services, topics, locations, and evidence | Developers, maintainers, retrieval systems |
| **Retrieval & Citation Engine** | The system that finds supporting evidence and prepares citation-backed context | Backend and AI systems |
| **Public Assistant & API** | User-facing ways to ask questions and access structured knowledge | Residents, developers, partners |

### The essential distinction

- **Knowledge Base:** a contributor-facing subject collection.
- **Knowledge Graph:** the technical relationship layer connecting everything.
- **SanJuan KI:** the full infrastructure containing both of them and the systems around them.

Contributors should not need to think in terms of graph nodes. They should be able to contribute a source, create a knowledge page, join a Knowledge Base, review information, or report outdated knowledge. Internally, approved content can be compiled into graph entities and relationships.

---

## The knowledge lifecycle

SanJuan KI is designed as a living knowledge system rather than a static repository.

```text
Official Evidence
        │
        ▼
Source Registry
        │
        ▼
Knowledge Base
        │
        ▼
Knowledge Graph
        │
        ▼
Retrieval & Citation
        │
        ▼
Public Assistant and API
        │
        ▼
Community Feedback
        │
        └──────────────────┐
                           ▼
                  Updated Knowledge
```

Every broken link reported, procedure corrected, relationship reviewed, and source refreshed improves the infrastructure underneath future answers.

---

## Source Registry

The Source Registry records where knowledge comes from and how it should be treated.

Sources may include:

- Puerto Rico government pages;
- agency portals;
- municipal pages;
- official forms;
- public datasets;
- regulations and public manuals;
- emergency bulletins;
- official PDFs;
- verified institutional resources.

The current registry is maintained in:

```text
data/sources/pr_sources.yml
```

The registry supports source discovery, ingestion, provenance, trust decisions, freshness monitoring, and citation generation.

For sensitive topics—such as taxes, permits, health, legal or court information, immigration, public benefits, police, and emergencies—official sources should be prioritized and unsupported claims should not be presented as authoritative.

---

## Knowledge Bases

Knowledge Bases are the primary collaboration surface for people contributing civic knowledge.

They organize sources, structured pages, maintainers, services, and topics around a recognizable domain. A Knowledge Base is not an AI model and does not require machine-learning expertise.

Initial Knowledge Bases:

| Knowledge Base | Scope |
| --- | --- |
| **Business & Commerce** | Business registration, merchant processes, permits, economic development, taxes, and commercial services |
| **Transportation** | Driver licensing, roads, mobility, transit, vehicles, and transportation agencies |
| **Public Health** | Public-health agencies, services, guidance, and verified health resources |
| **Emergency Information** | Hurricanes, earthquakes, alerts, preparedness, public safety, and emergency resources |
| **Municipal Services** | San Juan and municipal services, offices, procedures, locations, and contacts |
| **Tourism** | Official tourism information, visitor services, destinations, and institutional resources |

The Knowledge Base workspace lives under:

```text
knowledge/bases/
```

A mature Knowledge Base can contain:

```text
knowledge/bases/<knowledge-base>/
├── README.md
├── sources.yml
├── maintainers.yml
├── services/
└── topics/
```

Example Knowledge Base metadata:

```yaml
id: kb-transportation
title: Puerto Rico Transportation Knowledge Base
description: Official transportation, licensing, road, and mobility information.
geography: puerto_rico
languages:
  - es
  - en
maintainers:
  - github_username
review_status: active
```

See [`knowledge/bases/README.md`](knowledge/bases/README.md) and [`docs/COMMUNITY_KNOWLEDGE_BASES.md`](docs/COMMUNITY_KNOWLEDGE_BASES.md) for the community model.

---

## SanJuan Knowledge Graph

The SanJuan Knowledge Graph is the internal relationship layer that connects the project's knowledge.

It represents entities such as:

- agencies;
- services;
- topics;
- locations;
- forms;
- programs;
- source documents;
- relationships between them.

Examples:

```text
Departamento de Estado
        administers
Business Registration
```

```text
DTOP
        administers
Driver Licensing
```

```text
Hacienda
        related_to
Merchant Registration
```

The Knowledge Graph allows SanJuan KI to answer more than “Which document contains these words?” It can also help resolve questions such as:

- Which agency administers this service?
- Which procedure applies to this location?
- Which form belongs to this program?
- Which sources support this relationship?
- Which services are related to this topic?

Approved Knowledge Base content can be compiled into graph entities and relationships after validation and review.

---

## Retrieval and Citation Engine

The Retrieval and Citation Engine finds evidence relevant to a user's question.

The current MVP includes:

- local keyword retrieval;
- deterministic local vector-search scaffolding;
- hybrid keyword and vector retrieval;
- Spanish-first bilingual query expansion;
- accent normalization;
- structured citation-first answer contracts;
- source and confidence metadata.

The retrieval system is designed to prefer evidence over fluency. When trustworthy supporting material is unavailable, the expected behavior is to say so rather than fabricate an answer.

---

## Public Assistant and API

The Public Assistant is the user-facing experience built on top of the infrastructure.

It is intended to help residents, founders, visitors, researchers, civic technologists, and public-sector partners ask questions about Puerto Rico and receive structured, evidence-backed answers.

The FastAPI `/ask` contract can return:

- a direct answer;
- steps;
- requirements;
- citations;
- confidence information;
- related agencies;
- warnings and limitations.

The Next.js application presents those results through a bilingual web experience.

The assistant is not an official government service and should be used as a research and navigation tool. Sensitive decisions must be verified directly with the cited responsible agency.

---

## What contributors can add

### Contribute a Source

Add an official link, public document, dataset, form, manual, bulletin, regulation, or verified institutional resource with appropriate metadata.

### Create a Knowledge Page

Create or improve a structured Markdown page explaining a public process or service, for example:

- How to register a corporation;
- How to obtain a birth certificate;
- How to renew a driver's license;
- Where to find municipal services;
- Which agency handles a given procedure.

### Add or improve relationships

Document real-world connections between agencies, services, topics, locations, forms, and programs. Contributors may describe these relationships in human-readable pages or structured metadata; maintainers can compile approved content into the Knowledge Graph.

### Report outdated knowledge

Freshness contributions are essential. Examples include:

- broken link;
- outdated procedure;
- agency renamed;
- new form;
- changed URL;
- stale citation;
- new official publication;
- changed agency responsibility.

### Join or review a Knowledge Base

Contributors with Puerto Rico-specific, regional, institutional, or domain expertise can help maintain an entire subject area.

Public contribution language:

- **Contribute a Source**
- **Create a Knowledge Page**
- **Join a Knowledge Base**
- **Review a Knowledge Base**
- **Report Outdated Knowledge**

---

## Trust and review model

Not every contribution immediately becomes trusted production knowledge.

### Review status

```yaml
review_status:
  - submitted
  - source_verified
  - content_reviewed
  - published
```

| Status | Meaning |
| --- | --- |
| `submitted` | Contribution received but not yet verified |
| `source_verified` | Source identity, accessibility, and provenance checked |
| `content_reviewed` | Claims, structure, citations, and relationships reviewed |
| `published` | Approved for trusted graph and production retrieval use |

### Trust level

```yaml
trust_level:
  - official
  - institutional
  - community
  - unverified
```

| Trust level | Meaning |
| --- | --- |
| `official` | Government or legally authoritative public source |
| `institutional` | Verified university, nonprofit, public-interest, or recognized institutional source |
| `community` | Useful community-maintained knowledge with transparent provenance |
| `unverified` | Submitted material that has not completed review |

Review status and trust level are separate. A source can be official but still awaiting review, while a well-reviewed community resource remains a community source.

Sensitive answers should continue to prioritize official evidence even when institutional or community materials are available.

---

## Contributor roles

SanJuan KI uses lightweight roles that give contributors a path to grow within the project.

### Source Contributor

Adds official links, documents, datasets, and source metadata.

### Knowledge Editor

Creates and improves structured Markdown knowledge pages.

### Regional Reviewer

Verifies Puerto Rico-specific language, agency responsibilities, geography, and local context.

### Domain Reviewer

Reviews specialized areas such as taxes, health, transportation, business, municipal services, or emergency information.

### Maintainer

Approves publication into the trusted graph and production retrieval index, maintains project standards, and resolves review conflicts.

Roles describe contribution responsibilities; they do not imply employment, government authority, or legal certification.

---

## Contribution workflow

The public GitHub workflow is intentionally simple:

```text
Contributor
     │
     ▼
Issue template or Markdown edit
     │
     ▼
Pull request
     │
     ▼
Automated validation
     │
     ▼
Source and evidence review
     │
     ▼
Relationship and domain review
     │
     ▼
Maintainer approval
     │
     ▼
Knowledge Graph compilation
     │
     ▼
Published in SanJuan KI
```

Contributors can begin with a GitHub issue when they are unsure where a contribution belongs. Maintainers can then guide the contribution into the appropriate Knowledge Base, source registry, structured page, or relationship model.

---

## Automated validation

Automated checks should confirm, where applicable:

- valid frontmatter;
- valid and reachable URL structure;
- at least one citation for substantive knowledge pages;
- recognized Knowledge Base category;
- no duplicate node or page identifier;
- relationships point to valid entities;
- sensitive claims include official evidence;
- required metadata is present;
- review status is not falsely marked as approved or published;
- YAML and Markdown structures parse successfully;
- tests continue to pass.

Automation supports review; it does not replace local, regional, domain, or editorial judgment.

---

## Repository structure

```text
sanjuan-ai-ki/
├── apps/
│   ├── api/                    # FastAPI application
│   └── web/                    # Next.js public assistant
│
├── assets/                     # Logos, screenshots, and demo assets
│
├── data/
│   ├── sources/                # Puerto Rico Source Registry
│   └── documents/              # Ingested and normalized documents
│
├── docs/                       # Architecture, operations, and contributor documentation
│
├── knowledge/
│   ├── bases/
│   │   ├── business-and-commerce/
│   │   ├── transportation/
│   │   ├── public-health/
│   │   ├── emergency-information/
│   │   ├── municipal-services/
│   │   ├── tourism/
│   │   └── _template/
│   ├── agencies/
│   ├── services/
│   ├── topics/
│   ├── locations/
│   ├── _templates/
│   └── _indexes/
│
├── packages/
│   ├── ingestion/              # Crawling, loaders, and normalization
│   ├── knowledge/              # Knowledge validation and graph tooling
│   └── retrieval/              # Chunking, vectors, and hybrid search
│
├── tests/                       # Behavioral and validation tests
├── CONTRIBUTING.md
├── ROADMAP.md
└── README.md
```

Some directories represent the target organizational model and may be introduced incrementally as the infrastructure grows.

---

## Current capabilities

- Curated Puerto Rico Source Registry
- Static page ingestion
- Bounded same-domain crawling
- `robots.txt`-aware crawler controls
- Agency-specific loader profiles
- Source freshness and status dashboard
- Document normalization and chunking
- Local keyword retrieval
- Local deterministic vector-search scaffold
- Hybrid keyword and vector retrieval
- Spanish-first bilingual query expansion
- FastAPI backend
- Next.js web application
- Citation-first `/ask` response contract
- Structured answers with direct answer, steps, requirements, citations, confidence, related agencies, and warnings
- Knowledge Base contribution model
- Knowledge Graph foundation and validation tooling
- Local smoke tests and retrieval fixture tests
- GitHub Actions CI
- Deployment configuration for backend and web

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YannDavidson/sanjuan-ai-ki.git
cd sanjuan-ai-ki
```

### 2. Create a Python environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Run the test suite

```bash
pytest -q
```

### 4. Start the API

```bash
uvicorn apps.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

### 5. Start the web application

```bash
cd apps/web
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

---

## Build local retrieval artifacts

### Ingest registered source homepages

```bash
python -m packages.ingestion.batch_ingest_sources --pretty
```

### Run agency-specific loaders

```bash
python -m packages.ingestion.batch_ingest_sources --agency-loaders --max-pages 3 --pretty
```

### Chunk normalized documents

```bash
python -m packages.retrieval.chunk_documents --pretty
```

### Build local vectors

```bash
python -m packages.retrieval.local_vector_search build --pretty
```

### Test hybrid retrieval

```bash
python -m packages.retrieval.hybrid_search "business registration Puerto Rico" --pretty
python -m packages.retrieval.hybrid_search "registro de negocio Puerto Rico" --pretty
```

---

## Example questions

```text
How do I register a business in Puerto Rico?
Where can I find San Juan municipal services?
What official sources should I check for hurricane alerts?
How do I renew a driver's license in Puerto Rico?
Which agency handles Puerto Rico taxes?
¿Qué necesito para registrar un negocio en Puerto Rico?
¿Dónde encuentro servicios municipales de San Juan?
¿Qué fuentes oficiales debo revisar durante una emergencia?
```

---

## Documentation

### Architecture and development

- [`docs/ARCHITECTURE_OVERVIEW.md`](docs/ARCHITECTURE_OVERVIEW.md)
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
- [`docs/ASK_ANSWER_FORMAT.md`](docs/ASK_ANSWER_FORMAT.md)
- [`docs/BILINGUAL_RETRIEVAL.md`](docs/BILINGUAL_RETRIEVAL.md)
- [`docs/AGENCY_LOADERS.md`](docs/AGENCY_LOADERS.md)
- [`docs/CRAWLING_RULES.md`](docs/CRAWLING_RULES.md)
- [`docs/SOURCE_STATUS_DASHBOARD.md`](docs/SOURCE_STATUS_DASHBOARD.md)
- [`docs/API_ABUSE_PROTECTION.md`](docs/API_ABUSE_PROTECTION.md)

### Knowledge infrastructure and community

- [`knowledge/bases/README.md`](knowledge/bases/README.md)
- [`docs/COMMUNITY_KNOWLEDGE_BASES.md`](docs/COMMUNITY_KNOWLEDGE_BASES.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`SECURITY.md`](SECURITY.md)
- [`SUPPORTED_VERSIONS.md`](SUPPORTED_VERSIONS.md)

### Project status

- [`docs/PUBLIC_BETA_CHECKLIST.md`](docs/PUBLIC_BETA_CHECKLIST.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md)
- [`CHANGELOG.md`](CHANGELOG.md)

---

## Why SanJuan KI is different

| Generic AI assistant | SanJuan KI |
| --- | --- |
| Searches or summarizes broad internet content | Organizes Puerto Rico-specific civic knowledge |
| May provide uncited answers | Citation-first by design |
| Treats pages as isolated documents | Connects agencies, services, topics, locations, and evidence |
| Knowledge is opaque to contributors | Knowledge Bases are public and contributor-facing |
| Often optimized primarily for fluent output | Optimized for evidence, provenance, and transparent limitations |
| Generic geographic context | Puerto Rico-specific language, institutions, and local context |
| Closed or anonymous knowledge process | Open contribution and review workflow |
| May guess when evidence is weak | **No source, no answer** |

SanJuan KI is not built from anonymous AI answers. It is built from traceable public evidence, curated Knowledge Bases, connected through the SanJuan Knowledge Graph, and maintained by people who understand Puerto Rico.

---

## Contributing

**Help build Puerto Rico's open civic knowledge infrastructure.**

You do not need to be an AI engineer to contribute. Useful contributions include finding an official source, correcting an outdated procedure, improving a bilingual explanation, documenting a service, reviewing agency responsibility, adding tests, or improving the developer experience.

Start here:

1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md).
2. Review the Knowledge Base model in [`knowledge/bases/README.md`](knowledge/bases/README.md).
3. Choose a public contribution path:
   - Contribute a Source;
   - Create a Knowledge Page;
   - Join a Knowledge Base;
   - Review a Knowledge Base;
   - Report Outdated Knowledge.
4. Open an issue or pull request.
5. Respond to automated validation and reviewer feedback.

Before opening a pull request, run:

```bash
pytest -q
cd apps/web
npm install
npm run build
```

Every official source added, every outdated procedure corrected, every relationship documented, and every Knowledge Base improved makes Puerto Rico's public knowledge more accessible.

---

## Public beta status

SanJuan KI is preparing for public beta. The infrastructure, contribution model, and retrieval behavior are still evolving.

Track readiness in [`docs/PUBLIC_BETA_CHECKLIST.md`](docs/PUBLIC_BETA_CHECKLIST.md).

---

## Roadmap

Near-term priorities include:

1. Expand and review the initial Knowledge Bases.
2. Strengthen Knowledge Graph compilation and validation.
3. Improve citation-aware answer synthesis.
4. Add multi-source evidence fusion.
5. Improve source quality and freshness scoring.
6. Expand PDF, form, and dataset ingestion.
7. Add agency- and service-aware reasoning.
8. Improve bilingual and Puerto Rico-specific retrieval.
9. Develop government-service workflow guidance.
10. Prepare the Public Assistant and API for beta participation.

Read the full roadmap: [`ROADMAP.md`](ROADMAP.md).

---

## FAQ

### Is SanJuan KI an official government project?

No. SanJuan KI is an independent civic technology project. It is designed to cite official public sources whenever possible, but it is not an official government service.

### Can I rely on it for legal, tax, medical, immigration, emergency, or permit decisions?

No. Use SanJuan KI as a research and navigation tool. Always verify sensitive topics directly with the cited official agency or a qualified professional.

### What is the difference between a Knowledge Base and the Knowledge Graph?

A Knowledge Base is a human-facing subject collection that contributors can understand and maintain. The Knowledge Graph is the technical relationship layer connecting approved agencies, services, topics, locations, documents, and other entities.

### Do contributors edit the AI model?

No. Most contributors improve the knowledge infrastructure underneath the assistant by adding sources, pages, corrections, metadata, reviews, and relationships.

### Does SanJuan KI use paid AI APIs?

The current MVP retrieval layer runs locally with keyword search and deterministic hashed vector search. Future versions may add provider-based embeddings or language-model synthesis, but the project is designed to remain citation-first and provider-flexible.

### Is it bilingual?

Yes. The MVP includes English and Spanish query expansion, accent normalization, and mixed-language retrieval support. Full bilingual parity remains an ongoing community and engineering effort.

### Can I add a new Puerto Rico source?

Yes. Use the source contribution issue template or submit a pull request with the required metadata and evidence.

### Can institutions maintain a Knowledge Base?

The contribution model is designed to support collaboration with universities, nonprofits, civic organizations, researchers, and public institutions. Publication into trusted production knowledge remains subject to the project's review and governance process.

---

## Open-source philosophy

SanJuan KI treats civic knowledge as shared infrastructure.

The project aims to remain:

- open to public inspection;
- traceable to evidence;
- explicit about uncertainty;
- bilingual by design;
- respectful of Puerto Rico's local context;
- welcoming to nontechnical contributors;
- modular for developers and institutions;
- cautious around sensitive public information.

> **Help build Puerto Rico's open civic knowledge infrastructure.**
>
> Contribute official sources, verify public information, document government services, and help keep SanJuan KI accurate, bilingual, and useful.

---

## Security

Do not report security vulnerabilities through public GitHub issues.

Read [`SECURITY.md`](SECURITY.md) for the responsible disclosure process.

---

## License

SanJuan KI is licensed under the MIT License. See [`LICENSE`](LICENSE).
