# Community Knowledge Bases

SanJuan KI invites independent contributors to help build Puerto Rico's open civic knowledge infrastructure by adding public sources, documenting services, connecting related knowledge, and reviewing stale information.

## Public promise

> Help build Puerto Rico's open civic knowledge infrastructure. Contribute official sources, verify public information, document government services, and help keep SanJuan KI accurate, bilingual, and useful.

SanJuan KI is not built from anonymous AI answers. It is built from traceable public evidence maintained by people who understand Puerto Rico.

## How Knowledge Bases fit

```txt
SanJuan Knowledge Infrastructure
├── Source Registry
├── Community Knowledge Bases
├── SanJuan Knowledge Graph
├── Ingestion and Retrieval
├── API
└── Public Assistant
```

Knowledge Bases organize contributions by subject. Approved pages and relationships become nodes and edges in the SanJuan Knowledge Graph. Raw evidence remains available to retrieval and is never replaced by community summaries.

## Contribution paths

### Contribute a Source

Use the GitHub source contribution form or edit a Knowledge Base definition. Include provenance, trust level, public URL, language, and the information it supports.

### Create a Knowledge Page

Use the contributor page template. Cite every factual or procedural claim and list unverified details explicitly.

### Join a Knowledge Base

Contributors may volunteer as source contributors, editors, regional reviewers, domain reviewers, or maintainers. Maintainer status requires demonstrated review quality and project approval.

### Review Outdated Knowledge

Report broken URLs, changed procedures, stale dates, renamed agencies, superseded forms, or conflicting official sources.

## Review policy

A contribution does not enter trusted retrieval merely because it was submitted.

1. Metadata validation
2. Provenance and trust classification
3. Citation review
4. Sensitive-topic official-source review
5. Relationship and duplication checks
6. Maintainer approval
7. Graph compilation and publication

Contributors may not self-approve a submission unless they are already authorized maintainers and are performing a documented review.

## Sensitive topics

Legal, tax, medical, immigration, public-benefit, permit, licensing, emergency, court, police, fee, deadline, eligibility, and required-form claims need current official evidence. Institutional or community sources may provide context but cannot independently establish authoritative requirements.

## Initial Knowledge Bases

- `kb-business-and-commerce`
- `kb-transportation`
- `kb-public-health`
- `kb-emergency-information`
- `kb-municipal-services`
- `kb-tourism`

New bases should be proposed through the GitHub Knowledge Base issue form.

## Commands

```bash
python -m packages.knowledge.knowledge_base --pretty
python -m packages.knowledge.validate_graph --pretty
python -m packages.knowledge.build_graph --pretty
pytest -q
```

## Publication and traceability

Every approved contribution retains:

- its Git author and review history,
- source URLs and access dates,
- trust and review metadata,
- Knowledge Base membership,
- graph relationships,
- and the original raw evidence used by retrieval.
