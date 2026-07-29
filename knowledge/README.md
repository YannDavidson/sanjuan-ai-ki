# SanJuan Knowledge Graph

This directory is an Obsidian-compatible, Git-backed civic knowledge graph for Puerto Rico.

It is an additive layer between raw evidence and answer generation:

```txt
official sources
  → raw documents and chunks
  → reviewed Markdown graph nodes
  → compiled graph index
  → retrieval and cited answers
```

The graph does **not** replace raw-source retrieval. Every agency, service, topic, or location node must retain traceable source citations.

## Vault structure

```txt
knowledge/
├── agencies/
├── services/
├── topics/
├── locations/
├── _indexes/
└── _templates/
```

## Node requirements

Each Markdown node uses YAML frontmatter and should include:

- stable `id`
- `title`
- `node_type`
- language and geography
- trust and review status
- official source citations
- explicit graph relationships
- Markdown body with Obsidian wiki links where useful

## Validate

```bash
python -m packages.knowledge.validate_graph --pretty
```

## Compile

```bash
python -m packages.knowledge.build_graph --pretty
```

The compiler writes the machine-readable graph to:

```txt
data/knowledge/graph.json
```

## Open in Obsidian

Open the repository's `knowledge/` directory as an Obsidian vault. Obsidian will render links such as:

```md
[[Departamento de Transportación y Obras Públicas]]
[[Renew a Puerto Rico Driver License]]
```

No Obsidian plugin is required for the foundation. Git remains the source of version history and pull requests remain the review mechanism.

## Review statuses

- `draft`: incomplete or exploratory
- `machine_compiled`: generated from evidence but not yet reviewed by a person
- `human_reviewed`: approved by a named reviewer
- `stale`: due for evidence review

## Safety rule

A graph node may organize and summarize cited evidence, but it must never invent fees, deadlines, eligibility requirements, office hours, forms, or procedures.
