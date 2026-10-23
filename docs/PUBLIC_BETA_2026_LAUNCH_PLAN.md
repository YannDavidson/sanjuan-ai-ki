# SanJuan KI — November 30, 2026 Public Beta Plan

**Status:** implementation planning; not yet deployed.  
**Operating budget:** USD $300–$500/month.  
**Planning load:** 100–500 visitors/day (not necessarily 500 AI requests/day).  
**Release:** November 30, 2026, contingent on launch gates.

## Audited baseline (October 23)
- FastAPI in `apps/api`, Next.js 15 in `apps/web`, Python 3.11 and Node 22 in CI.
- Six YAML Knowledge Bases with validation and a contributor template.
- Existing source registry, ingestion, deterministic local retrieval, hybrid search, graph foundation and citation-first `/ask`.
- Existing Render/Vercel deployment instructions rely on file-based corpus artifacts; durable shared storage is not yet documented as deployed.
- No live public contributor form, review queue, or OpenAI-backed civic/general router was established by this audit.
- `apps/web/package.json` uses `next lint`; replace with `eslint .` and add lint to CI.
- No production cloud resources, billing, domain or successful end-to-end deployment were verified in this audit.

## Architecture decision for beta
1. **Web:** Next.js, managed deployment. **API:** FastAPI on Cloud Run or equivalent.
2. **Data:** PostgreSQL with pgvector; approved public records only in search index.
3. **Evidence:** object storage for snapshots, PDFs and upload files, with retention and lifecycle rules.
4. **Ingestion:** scheduled worker and bounded queue, separate from public request path.
5. **AI:** server-side model API, retrieval-grounded civic mode, explicit general mode; citations must reference retrieved evidence.
6. **Authentication:** managed identity provider; server-side reviewer authorization; no self-approval.
7. **CERVEL:** optional async CKO adapter; no public request-time dependency.
8. **Safety:** per-IP/account limits, request budget, no raw untrusted uploads in retrieval, audit logs, tested backup/restore.

## Delivery backlog
| Issue | Work | Priority | Target |
|---|---|---|---|
| [#34](https://github.com/YannDavidson/sanjuan-ai-ki/issues/34) | Staging/production foundation | P0 | Oct 30 |
| [#35](https://github.com/YannDavidson/sanjuan-ai-ki/issues/35) | Durable schema and migrations | P0 | Nov 6 |
| [#36](https://github.com/YannDavidson/sanjuan-ai-ki/issues/36) | pgvector hybrid retrieval | P0 | Nov 10 |
| [#37](https://github.com/YannDavidson/sanjuan-ai-ki/issues/37) | Public bilingual chat | P0 | Nov 13 |
| [#38](https://github.com/YannDavidson/sanjuan-ai-ki/issues/38) | Contributor portal | P0 | Nov 16 |
| [#39](https://github.com/YannDavidson/sanjuan-ai-ki/issues/39) | Review/publish workflow | P0 | Nov 19 |
| [#40](https://github.com/YannDavidson/sanjuan-ai-ki/issues/40) | Ingestion, storage, freshness | P0 | Nov 21 |
| [#41](https://github.com/YannDavidson/sanjuan-ai-ki/issues/41) | Security, monitoring, QA | P0 | Nov 25 |
| [#42](https://github.com/YannDavidson/sanjuan-ai-ki/issues/42) | Optional CERVEL adapter | P1 | Nov 20 |
| [#43](https://github.com/YannDavidson/sanjuan-ai-ki/issues/43) | Hackathon workspace | P1 | Nov 27 |
| [#44](https://github.com/YannDavidson/sanjuan-ai-ki/issues/44) | Beta go/no-go and release | P0 | Nov 30 |

## Critical path
#34 → #35 → #36 → #37 → #38 → #39 → #41 → #44.  
Build #40 alongside #35–#39. The frontend can be developed in parallel against mocked contracts. Defer #42 and #43 if critical gates are at risk.

## Budget envelope (monthly, estimates only)
| Category | Planning allowance |
|---|---:|
| Web + API + background compute | $50–90 |
| PostgreSQL + backups | $90–160 |
| Object storage, logs, egress | $15–35 |
| Model inference + embeddings | $80–140 |
| Contingency | $25–65 |
| **Total range** | **$260–490** |

These are budget allocations, **not provider quotes**. Verify actual regional prices before provisioning; minimum always-on database costs can exceed allowances. Start with low limits and a cost dashboard. Use hard application-level quotas; cloud budget alerts do not enforce a spending cap.

## Beta load assumptions
500 daily visitors × 2 chat requests/visitor = up to 1,000 requests/day (~30,000/month); the real mix is unknown. Limit anonymous chat, cap output tokens, cache safe public results, and set maximum worker/API concurrency. Load-test bursts rather than only daily averages.

## Launch gates (mandatory)
- Python tests, Knowledge Base validator, Next.js build and lint pass on release commit.
- Staging and production URLs respond; health, CORS, TLS, rollback tested.
- No unpublished or private submission appears in public retrieval.
- Reviewer authorization and audit events tested; contributor cannot approve own content.
- Spanish/English 100-question evaluation includes unsupported-sensitive-query refusals and source verification; no fabricated citation URLs.
- Rate limiting, model budget caps, monitoring, backups and restore drill completed.
- Privacy, attribution, accessibility and incident contacts reviewed.
- Public release is **go/no-go**, not automatic on calendar date.

## Decisions needed from project owner
- Production domain and access to cloud billing/account.
- Preferred Google Cloud region after latency/cost check.
- Identity provider and who will serve as the initial authorized reviewers.
- Model/API key and spending limits.
- Data retention and copyright/redistribution policy.

## First engineering PR
Start #34 by adding environment templates, Cloud Run Dockerfiles, deploy workflow with least-privilege authentication, smoke tests, and staging runbook. Do not put cloud secrets in repository or automatically deploy to production without approval.
