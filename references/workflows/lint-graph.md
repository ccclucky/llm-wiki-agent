# Lint and Graph

Deterministic checks:
- RAW items stuck in processing or pending beyond agreed threshold.
- Duplicate source URLs/stable IDs and duplicate canonical titles.
- Missing provenance, orphan pages, missing expected backlinks.
- Native mentions to deleted/inaccessible pages and stale metadata.

Semantic checks:
- Contradictory claims with source references.
- Unsupported facts, conflicting dates/statuses, duplicate concepts.
- Repeatedly mentioned entities without canonical pages.

Graph rules:
- Explicit native page mentions are confirmed edges.
- AI-suggested relations are inferred and carry confidence/epistemic labels.
- Never silently promote inferred edges to confirmed facts.
- Do not create pages just to eliminate orphans.
- Report issues and suggested repairs separately.
