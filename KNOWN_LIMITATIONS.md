# Known Limitations

SanJuan AI is in MVP/public-beta preparation. It is useful for testing and civic-technology development, but it is not a production government service.

## Not official government guidance

SanJuan AI is independent. It is not an official Puerto Rico government system.

Always verify sensitive answers directly with the cited official source or agency.

## Retrieval limitations

- Retrieval quality depends on ingested documents.
- If ingestion has not run, `/ask` may return safe fallback answers.
- The local vector search is deterministic and development-friendly, not a full semantic embedding model.
- Bilingual retrieval uses a glossary-based expansion layer, not full machine translation.
- Some official websites may be dynamic, JavaScript-heavy, or difficult to ingest with static fetching.

## Source limitations

- Some sources may be stale, unavailable, thin, or blocked.
- The source registry may not yet cover every Puerto Rico agency or municipality.
- Agency-specific loaders are MVP profile-based loaders, not full custom parsers.
- PDF, form, table, and document parsing are not fully implemented yet.

## Answer limitations

- Structured answers are extractive and deterministic.
- SanJuan AI should not invent fees, deadlines, eligibility, requirements, office hours, or procedures.
- Sensitive topics should cite official sources and include warnings.
- Multi-source evidence synthesis is planned but not fully implemented.

## Deployment limitations

- The MVP in-memory rate limiter is not enough for large public traffic.
- Production deployments should use edge/API-gateway/Redis-backed abuse protection.
- Scheduled ingestion refresh is planned and documented, but production hosting choices may vary.

## Beta tester guidance

When testing, please report:

- Missing citations
- Wrong sources
- Confusing answers
- Broken setup steps
- Broken source links
- Spanish/English retrieval failures
- Unsafe or overconfident answers
