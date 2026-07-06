# Contributing to SanJuan AI KI

Thank you for your interest in contributing to SanJuan AI.

SanJuan AI is a bilingual, citation-first civic intelligence project for Puerto Rico. Contributions should improve trust, clarity, safety, source quality, or usability.

## Ways to contribute

Good first contributions include:

- Verifying official Puerto Rico sources
- Suggesting new sources
- Improving English/Spanish glossary terms
- Improving documentation
- Adding tests
- Improving agency-specific loaders
- Capturing screenshots or demo GIFs
- Reporting confusing or unsafe answers
- Improving the web UI

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
5. Run tests before opening a pull request.

## Source contributions

When adding a new public source, include:

- Source name
- URL
- Category
- Geography
- Language
- Trust level
- Source type
- Update frequency, if known
- Notes explaining why the source matters

Prefer official Puerto Rico government or institutional sources when possible.

## Safety rules

Do not add behavior that invents:

- legal guidance
- tax requirements
- medical advice
- permit requirements
- emergency instructions
- immigration guidance
- public benefit eligibility
- fees, deadlines, office hours, or forms without source evidence

For sensitive topics, SanJuan AI should cite official sources and admit uncertainty when evidence is missing.

## Pull request checklist

Before opening a PR:

- [ ] `pytest -q` passes
- [ ] `npm run build` passes in `apps/web` when frontend code changes
- [ ] Docs are updated when needed
- [ ] No secrets or private data are committed
- [ ] New sources are public and citation-friendly
- [ ] Sensitive-topic behavior remains safe

## Code style

The project currently prioritizes simple, readable Python and TypeScript. Keep modules small, explicit, and easy to test.

## Questions

Open a GitHub issue with the `question` label or start a discussion when GitHub Discussions are enabled.
