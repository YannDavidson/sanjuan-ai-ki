# API Abuse Protection Plan

SanJuan AI is designed as a public-facing Puerto Rico knowledge API. Before public launch, `/ask` needs basic protection against accidental refresh loops, bot traffic, and expensive repeated requests.

## Current MVP protection

The FastAPI backend includes a dependency-free in-memory sliding-window limiter for `/ask`.

Environment variables:

```bash
SANJUAN_RATE_LIMIT_ENABLED=true
SANJUAN_ASK_RATE_LIMIT_PER_MINUTE=30
```

Default behavior:

- `/ask` is limited per client identifier.
- `/health` remains open for uptime checks.
- `/sources` remains open for the public source registry.
- Successful `/ask` responses include:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
- Blocked `/ask` responses return HTTP `429` with:
  - `Retry-After`
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`

## Client identity

The MVP limiter uses the best available request identity:

1. `X-Forwarded-For` first IP
2. `X-Real-IP`
3. direct client host
4. fallback `unknown-client`

This is acceptable for a simple deployment behind a trusted platform proxy, but headers can be spoofed if the API is exposed directly without a trusted proxy or edge layer.

## Limitations

The current limiter is intentionally simple:

- State is stored in process memory.
- Counters reset on deploy/restart.
- It does not synchronize across multiple workers or replicas.
- It is not enough for serious production abuse defense.
- It does not distinguish authenticated users because authentication does not exist yet.

## Recommended production controls

For a public launch, keep the in-app limiter but add at least one external layer:

### Option A: Edge / hosting platform rate limiting

Use Vercel, Cloudflare, Fastly, Render proxy rules, or another edge provider to limit by IP and path before traffic reaches FastAPI.

Recommended starting policy:

```txt
/ask: 30 requests per minute per IP
/sources: 120 requests per minute per IP
/health: allow uptime monitors, but block obvious floods
```

### Option B: API gateway

Use an API gateway if SanJuan AI later exposes paid or partner APIs.

Useful features:

- per-key limits
- quotas
- burst control
- logging
- abuse analytics
- origin restrictions

### Option C: Redis-backed limiter

When the backend scales beyond one process/replica, replace the in-memory limiter with Redis or another shared store.

Target behavior:

- per-IP anonymous limits
- per-user or per-key authenticated limits
- route-specific limits
- shared counters across replicas
- structured logging for blocked requests

## Future enhancements

- Add request body size limits.
- Add optional API key support for institutional users.
- Add bot/challenge protection at the edge.
- Add usage logs with privacy-preserving aggregation.
- Add separate limits for high-cost retrieval/generation once LLM generation is connected.
- Add admin configuration for emergency throttling during spikes.

## Launch checklist

Before public exposure:

- Set `SANJUAN_ENV=production`.
- Set `SANJUAN_CORS_ORIGINS` to the deployed web origin only.
- Keep `SANJUAN_RATE_LIMIT_ENABLED=true`.
- Set a conservative `SANJUAN_ASK_RATE_LIMIT_PER_MINUTE`.
- Put the API behind a trusted proxy or platform domain.
- Add edge/API-gateway rate limiting when traffic grows.
- Confirm `/health`, `/sources`, and `/ask` behavior after deployment.
