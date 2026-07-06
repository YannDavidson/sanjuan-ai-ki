# Spanish-First Bilingual Retrieval

Puerto Rico public information is mostly Spanish-first, while users may ask questions in English, Spanish, or a mix of both.

SanJuan AI now includes an MVP bilingual retrieval layer that improves matching across English and Spanish without external translation APIs.

## What changed

Added:

- `packages/retrieval/bilingual.py`
- bilingual query expansion
- accent normalization
- English ↔ Spanish civic glossary terms
- bilingual keyword retrieval scoring
- bilingual local vector text expansion
- tests for mixed-language retrieval behavior

## How it works

The bilingual layer uses a deterministic glossary for common Puerto Rico civic/service terms.

Examples:

```txt
business → negocio, empresa, comerciante, comercio
registration → registro, registrar, inscripción, corporaciones
permits → permisos, permiso, autorizaciones
taxes → impuestos, hacienda, contribuciones
services → servicios, trámites, gestiones
health → salud, médico, hospital
weather → tiempo, clima, pronóstico
```

Spanish queries are expanded in the other direction:

```txt
permisos → permits, permissions, authorizations
comerciante → merchant, business, taxpayer
hacienda → treasury, tax, taxes
tramites → procedures, services, filings
```

## Keyword retrieval

Keyword search now:

- expands the user query before scoring
- expands chunk text with bilingual terms derived from text and metadata
- normalizes accents, so `trámites` and `tramites` can match
- gives a small boost to Spanish chunks because Puerto Rico official content is often Spanish-first

Run:

```bash
python -m packages.retrieval.keyword_search "business registration Puerto Rico" --pretty
python -m packages.retrieval.keyword_search "registro de negocio comerciante Puerto Rico" --pretty
```

## Local vector retrieval

Local vector search now:

- builds vectors from bilingual-expanded chunk text
- includes source metadata in expansion
- expands query text before vector search
- marks generated vector stores with `bilingual_expansion: true`

Run:

```bash
python -m packages.retrieval.local_vector_search build --pretty
python -m packages.retrieval.local_vector_search search "permisos comerciante Puerto Rico" --pretty
```

## Hybrid retrieval

Hybrid retrieval benefits automatically because it combines keyword and vector retrieval.

```bash
python -m packages.retrieval.hybrid_search "business registration Puerto Rico" --pretty
python -m packages.retrieval.hybrid_search "registro de negocio Puerto Rico" --pretty
```

## Current limitation

This is not machine translation. It is a safe MVP glossary-based expansion layer.

It works best for common civic terms like:

- services / servicios
- permits / permisos
- taxes / impuestos
- business registration / registro de negocio
- corporations / corporaciones
- health / salud
- emergency / emergencia
- weather / clima / tiempo

Future upgrades can add:

- bilingual embedding models
- query translation through a trusted model
- Spanish stemming/lemmatization
- source-language-aware ranking
- synonym dictionaries by agency
