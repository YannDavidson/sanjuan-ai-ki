# Security Policy

SanJuan AI is a civic technology project that handles public-source retrieval and user questions. Security and trust matter even during beta.

## Supported versions

During beta, only the default branch and latest beta release are supported.

| Version | Supported |
| --- | --- |
| latest beta | Yes |
| older commits | No |

## Reporting a vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Instead, contact the project maintainer privately. If a dedicated security email is added later, this file should be updated with that address.

When reporting, include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Affected files or endpoints
- Suggested fix, if known

## What counts as a security issue?

Examples:

- Exposure of secrets or credentials
- Unsafe CORS configuration
- API abuse vectors
- Prompt injection risks that cause unsafe source claims
- Path traversal or file access problems
- Dependency vulnerabilities
- User data leakage
- Stored XSS or frontend injection

## Public-source safety

SanJuan AI should only ingest public sources. Do not add private, restricted, paywalled, or confidential data to the repository or ingestion pipeline.

## Sensitive-topic safety

For legal, tax, health, permit, emergency, immigration, court, police, or public-benefit questions, SanJuan AI should avoid unsupported claims and cite official sources.
