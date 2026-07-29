# SanJuan Knowledge Graph

The SanJuan Knowledge Graph is a Git-backed, Obsidian-compatible layer that organizes official Puerto Rico evidence into connected agency, service, topic, and location nodes.

## Position in the system

```txt
Source registry
  ↓
Ingestion and crawling
  ↓
Raw documents and chunks
  ↓
SanJuan Knowledge Graph
  ↓
Compiled JSON graph index
  ↓
Hybrid retrieval and cited answers
```

The graph is additive. Raw official evidence remains the source of truth.

## Node model

Each node is a Markdown file with YAML frontmatter validated by `packages/knowledge/schema.py`.

Core fields:

- `id`
- `title`
- `node_type`
- `language`
- `geography`
- `trust_level`
- `review_status`
- `sources`
- `relations`
- `last_verified`
- reviewer metadata

Every non-index node must include at least one source citation.

## Relationships

Relations are explicit directed edges:

```yaml
relations:
  - relation: provides
    target: service-renew-driver-license-pr
```

The compiler resolves those edges against node IDs and reports unresolved targets.

## Commands

Validate the vault:

```bash
python -m packages.knowledge.validate_graph --pretty
```

Build the machine-readable graph:

```bash
python -m packages.knowledge.build_graph --pretty
```

Default output:

```txt
data/knowledge/graph.json
```

## Obsidian workflow

1. Open `knowledge/` as an Obsidian vault.
2. Browse agency, service, topic, and location folders.
3. Follow wiki links between related nodes.
4. Edit or review Markdown through a Git branch.
5. Run the validator.
6. Submit a pull request.
7. Change `review_status` to `human_reviewed` only when a named reviewer has verified the cited evidence.

## Review policy

- `draft`: incomplete node
- `machine_compiled`: evidence-organized but not manually approved
- `human_reviewed`: manually verified and attributed
- `stale`: evidence should be refreshed

## Safety and provenance

The graph may summarize and connect evidence, but it must not become an uncited source of truth. Fees, deadlines, eligibility, documents, forms, office hours, and procedures must be traceable to current official evidence.

Future retrieval should search graph nodes for structure and raw chunks for supporting evidence before generating an answer.
