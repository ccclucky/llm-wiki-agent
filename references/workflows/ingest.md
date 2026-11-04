# Ingest

Trigger: `/ingest`, "ingest this", or "process this RAW item".

1. Resolve RAW and select the requested item; do not process the whole queue without permission.
2. Set processing status if supported.
3. Fetch full source and provenance.
4. Read schema and search existing Sources, Entities, Concepts, Syntheses.
5. Create/update a source record with summary, claims, evidence, dates, unresolved issues.
6. Extract durable entities/concepts; do not create pages for every noun.
7. Update canonical pages or create genuinely missing ones.
8. Add native Notion page mentions in useful directions: source ↔ entity/concept; link related pages when meaningful.
9. Verify important links through backlinks. Plain URLs and text labels are not backlinks.
10. Update navigation/index if used.
11. Mark processed only after writes and verification succeed. Partial failures remain retryable.
12. Report pages created/updated, backlinks verified, conflicts, failures.

Idempotency: search existing source IDs/URLs and canonical titles before creating. Prefer updating canonical pages.
