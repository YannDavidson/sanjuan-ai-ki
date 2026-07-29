# SanJuan KI Knowledge Bases

Knowledge Bases are contributor-facing collections of trusted sources and structured knowledge for one Puerto Rico subject area. They organize contributions without requiring contributors to understand graph databases, embeddings, or retrieval internals.

Approved Knowledge Base content can be compiled into the SanJuan Knowledge Graph, but the original source links and Git history remain the evidence trail.

## Initial Knowledge Bases

- Business and Commerce
- Transportation
- Public Health
- Emergency Information
- Municipal Services
- Tourism

## Ways to contribute

1. **Contribute a Source** — propose an official page, form, dataset, PDF, feed, or recognized institutional resource.
2. **Create a Knowledge Page** — document an agency, public service, topic, or location using cited evidence.
3. **Join a Knowledge Base** — help maintain a subject area over time.
4. **Review Outdated Knowledge** — report broken links, changed requirements, renamed agencies, or stale citations.

## Review states

- `proposed`: newly submitted and not production-ready
- `active`: reviewed and currently maintained
- `needs_review`: incomplete, stale, or awaiting specialist review
- `archived`: retained for history but not used for current answers

## Trust levels

- `official`: government, public authority, official dataset, regulation, or agency publication
- `institutional`: university, recognized nonprofit, chamber, or public-interest institution
- `community`: locally useful but not authoritative for sensitive claims
- `unverified`: submitted but not yet verified

## Contributor roles

- Source Contributor
- Knowledge Editor
- Regional Reviewer
- Domain Reviewer
- Maintainer

## Validation

Run:

```bash
python -m packages.knowledge.knowledge_base --pretty
```

Sensitive Knowledge Bases must include at least one official source. Active Knowledge Bases must name at least one maintainer.
