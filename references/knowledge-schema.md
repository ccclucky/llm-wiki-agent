# Knowledge schema

Use the schema already present in the user's workspace. This fallback model is not permission to create duplicate databases.

| Area | Purpose |
|---|---|
| RAW | Original material waiting to be processed |
| Sources | Traceable evidence and provenance |
| Entities | People, teams, companies, products, projects, repositories |
| Concepts | Reusable ideas, methods, technologies, principles |
| Syntheses | Cross-source analysis and durable answers |
| System | Protocols, schemas, operating rules |

Source metadata: title, source type/origin, captured_at, authored_at/occurred_at when known, status (pending/processing/processed/failed), stable source ID/fingerprint, resulting source page.

Knowledge page metadata: canonical title, type, concise definition, claims with provenance, related native page mentions, created_at and last_verified_at where supported.

Evidence labels:
- Source fact — directly supported by a cited source.
- User-confirmed — explicitly stated or confirmed by the user.
- Agent synthesis — reasoned conclusion based on cited evidence.
- Hypothesis — plausible but unverified.
- Unknown — insufficient or conflicting evidence.

Canonicalization: search exact title, aliases, and synonyms before creating. Compare identity, scope, and provenance. Do not merge similarly named entities without evidence.
