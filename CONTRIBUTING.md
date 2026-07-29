# Contributing to SanJuan AI KI

Thank you for helping build **SanJuan Knowledge Infrastructure**, an open, bilingual, citation-first civic knowledge project for Puerto Rico.

Contributors do not need to understand graph databases, embeddings, or AI systems. You can contribute by finding official sources, documenting public services, reviewing local context, correcting stale information, or maintaining a subject-specific Knowledge Base.

## Ways to contribute

- **Contribute a Source** — propose an official page, form, PDF, dataset, feed, or recognized institutional resource.
- **Create a Knowledge Page** — add or improve an agency, service, topic, or location page with citations.
- **Join a Knowledge Base** — help maintain business, transportation, health, emergency, municipal, tourism, or another approved subject area.
- **Review Outdated Knowledge** — report broken links, renamed agencies, changed procedures, or stale citations.
- Improve English/Spanish terminology, documentation, tests, loaders, UI, screenshots, and deployment guidance.

Use the GitHub issue forms when you are not ready to open a pull request.

## SanJuan KI terminology

- **SanJuan KI** is the complete Knowledge Infrastructure: sources, ingestion, Knowledge Bases, Knowledge Graph, retrieval, API, and public assistant.
- A **Knowledge Base** is a contributor-facing subject collection with defined scope, sources, maintainers, and review rules.
- The **SanJuan Knowledge Graph** is the technical relationship layer connecting agencies, services, topics, locations, and citations.

## Contributor roles

- **Source Contributor:** finds and documents public sources.
- **Knowledge Editor:** creates or improves cited knowledge pages.
- **Regional Reviewer:** verifies Puerto Rico-specific language and local context.
- **Domain Reviewer:** reviews a field such as health, taxes, transportation, or emergency information.
- **Maintainer:** approves publication and keeps a Knowledge Base current.

Roles describe responsibility, not hierarchy. New contributors may begin with a single source or correction.

## Submission-to-publication workflow

1. Submit an issue or focused pull request.
2. Automated checks validate metadata, IDs, citations, and relationships.
3. A reviewer confirms provenance and assigns the correct trust level.
4. Sensitive claims are checked against official evidence.
5. The contribution remains `proposed` or `submitted` until approved.
6. A maintainer merges the contribution and marks it active or published.
7. The Knowledge Graph compiler makes approved content available to retrieval systems.
8. Git history and source URLs preserve the evidence trail.

Never mark your own contribution as human-reviewed or published unless you are an authorized maintainer performing that review.

## Knowledge Base contributions

Knowledge Base definitions live under:

```txt
knowledge/bases/<knowledge-base>/knowledge-base.yml
```

Start from:

```txt
knowledge/bases/_template/knowledge-base.yml
```

Every Knowledge Base must declare:

- stable ID beginning with `kb-`
- title and description
- geography and languages
- covered topics
- maintainers
- review status
- whether it includes sensitive topics
- source policy
- labeled sources

Validate all Knowledge Bases with:

```bash
python -m packages.knowledge.knowledge_base --pretty
```

## Source contributions

When adding a source, include:

- source name and public URL
- owning agency or institution
- related Knowledge Base
- geography and language
- trust level: `official`, `institutional`, `community`, or `unverified`
- source type and update frequency, when known
- what the source contains
- when and how provenance was verified
- whether it supports sensitive claims

Prefer official Puerto Rico government or public-authority sources. Institutional and community sources must remain clearly labeled.

## Knowledge-page contributions

Use:

```txt
knowledge/_templates/knowledge-page-contribution.md
```

Every factual or procedural claim must be traceable to a listed source. Missing requirements, fees, deadlines, forms, eligibility rules, and procedures should be placed under **What is not yet verified** rather than guessed.

## Review and trust states

Knowledge Base states:

- `proposed`
- `active`
- `needs_review`
- `archived`

Knowledge Graph pages may additionally use submission and publication review states defined by the graph schema.

Trust level describes the source, while review status describes the contribution. They are not interchangeable.

## Safety rules

Do not add unsupported:

- legal or immigration guidance
- tax requirements
- medical advice
- permit or licensing requirements
- emergency instructions
- public-benefit eligibility
- fees, deadlines, office hours, forms, or procedures

For sensitive topics, SanJuan KI must cite current official sources and admit uncertainty when evidence is missing.

Do not commit private data, credentials, personal case information, paywalled material, or content you do not have permission to redistribute.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Web app:

```bash
cd apps/web
npm install
npm run dev
```

Build check:

```bash
cd apps/web
npm run build
```

## Development workflow

1. Create or comment on an issue before major changes.
2. Keep changes focused.
3. Add or update tests when behavior changes.
4. Update documentation when commands, schemas, or workflows change.
5. Run tests and validators before opening a pull request.

## Pull request checklist

- [ ] `pytest -q` passes
- [ ] `python -m packages.knowledge.knowledge_base --pretty` passes when Knowledge Bases change
- [ ] `python -m packages.knowledge.validate_graph --pretty` passes when graph pages change
- [ ] `npm run build` passes in `apps/web` when frontend code changes
- [ ] Every factual claim is traceable to a public source
- [ ] Source trust levels are accurate
- [ ] Sensitive-topic claims use official evidence
- [ ] Review status does not overstate approval
- [ ] Docs are updated when needed
- [ ] No secrets, private data, or generated corpus artifacts are committed

## Code style

Keep Python, TypeScript, YAML, and Markdown simple, explicit, and easy for another contributor to review.

## Questions

Open a GitHub issue with the `question` label or start a discussion when GitHub Discussions are enabled.
