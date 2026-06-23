# Test Fixtures

This directory contains deterministic, network-free corpus fixtures for SanJuan AI tests.

The fixtures are intentionally small and safe to commit. They are not official Puerto Rico guidance. They exist only to verify retrieval behavior in CI.

## Corpus layout

```txt
fixtures/corpus/
├── raw/
│   └── demo_business_registration.json
└── chunks/
    └── demo_business_registration.chunks.json
```

The chunk fixture preserves the same citation metadata shape used by generated chunks:

- `source_id`
- `source_name`
- `source_url`
- `title`
- `category`
- `geography`
- `language`
- `trust_level`
- `citation`

Vector fixtures are generated during tests from the committed chunk fixture so the expected vector behavior remains deterministic without committing large vector arrays.
