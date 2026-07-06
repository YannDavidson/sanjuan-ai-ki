# `/ask` Structured Answer Format

The `/ask` endpoint now returns both a backward-compatible text answer and a structured answer object.

## Response fields

Existing fields remain:

```json
{
  "answer": "Direct answer plus summary text",
  "language": "en",
  "confidence": "low",
  "citations": [],
  "sources": [],
  "safety_note": null,
  "ingestion_status": {}
}
```

New field:

```json
{
  "structured_answer": {
    "direct_answer": "Clear direct answer based on retrieved evidence.",
    "steps_to_follow": [],
    "requirements": [],
    "official_citations": [],
    "last_updated": null,
    "confidence": "low",
    "related_agencies": [],
    "official_source_warning": null
  }
}
```

## Design principles

SanJuan AI should never invent official requirements, fees, dates, eligibility rules, or procedures.

The structured answer builder is extractive for the MVP. It uses retrieved evidence snippets and source metadata to produce:

- direct answer
- steps to follow
- requirements
- official citations
- last updated date from fetched citation timestamps
- confidence score
- related agencies
- official-source warning for sensitive topics

## Sensitive topics

For questions about permits, taxes, health, emergencies, public benefits, police, courts, legal topics, or immigration, the answer includes an official-source warning.

If there is not enough official evidence, SanJuan AI returns a safe fallback instead of guessing.

## Related agencies

Related agencies are inferred only from retrieved source metadata. The backend does not invent agency relationships.

## Current limitation

The answer builder is not yet a full LLM summarizer. It is a deterministic MVP layer over retrieved evidence. This makes it safe and testable while the corpus and retrieval quality improve.
