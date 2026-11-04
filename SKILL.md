---
name: cclucky-llm-wiki
description: Maintain a Notion-backed LLM Wiki. Capture raw material, ingest it into linked source/entity/concept pages, query knowledge, update facts, and audit wiki integrity. Use whenever the user asks to save, remember, ingest, retrieve, connect, update, or audit durable knowledge.
---
# CCLUCKY LLM Wiki

This Skill defines the knowledge workflow. The Agent's own connected Notion MCP provides storage access. This repository does not configure OAuth, manage credentials, or require cloning for normal use.

## Preflight
1. Confirm Notion MCP is connected and authorized for the user's existing CCLUCKY Knowledge OS workspace.
2. Read the Knowledge OS home page and Agent Context Protocol to discover actual section/database IDs and conventions. Never guess IDs or create a parallel workspace.
3. Discover the configured RAW inbox. If none exists, ask permission to create one in the existing workspace; an explicitly designated Inbox page may be used temporarily.
4. Confirm search, retrieve, create/update page, append block, native page mention, and backlink inspection capabilities. Report gaps honestly. Never ask the user to paste tokens into chat.

## Canonical model
- Notion is the sole canonical shared knowledge store.
- RAW: immutable intake queue for unprocessed source material.
- Sources: traceable evidence and provenance.
- Entities: people, organizations, products, projects, repositories.
- Concepts: reusable ideas, methods, systems, technologies.
- Syntheses: cross-source analysis worth preserving.
- System: protocols, schemas, governance.
- Do not create local wiki copies or treat this public repository as a user's knowledge store.

## User intents
- **Capture**: preserve supplied material in RAW as pending, with title, origin/URL, capture date, and original content/attachment.
- **Ingest**: process selected pending RAW items, extract durable knowledge, create/update canonical pages, establish native links, verify backlinks, then mark processed.
- **Query**: search and retrieve relevant pages, follow links/provenance, answer with Notion page references.
- **Update**: amend canonical pages, preserve material history, record provenance and temporal context.
- **Lint**: find orphans, missing backlinks, broken references, duplicates, stale/unsupported/conflicting facts, and stuck RAW items.
- **Graph**: inspect confirmed relationships and separately label inferred relationships.

## Ingest procedure
1. Process only the item the user selected; do not drain the entire queue without permission.
2. Check stable source URL/ID/fingerprint to avoid duplicate ingestion.
3. Read the full source and preserve origin/date.
4. Search existing canonical pages before creating new ones.
5. Distinguish source facts, user-confirmed statements, agent synthesis, hypotheses, and unknowns.
6. Create/update the source record and relevant entity/concept pages. Avoid creating a page for every noun.
7. Create **native Notion page mentions** (rich-text mention objects referencing page IDs) for relationships. Plain text, Markdown `[[WikiLinks]]`, and ordinary URL hyperlinks do not create the required Notion backlinks.
8. Link source → entities/concepts and entities/concepts → source where meaningful. Add relationship explanations and types where schema permits: supports, mentions, depends_on, contradicts, implements, part_of, related_to.
9. Verify important inbound backlinks using Notion's backlink capability. If absent, inspect and repair the block. Never claim a backlink succeeded without verification.
10. Mark RAW processed only after all writes and checks succeed. Leave partial failures retryable.
11. Summarize pages created/updated, relationships verified, conflicts, and failures.

## Multi-agent consistency
All Agents use the same workspace and canonical pages. Before writing, fetch latest page content and last-edited timestamp. Re-read before writing if concurrent edits are suspected; reconcile rather than overwrite. Search before creating and make writes idempotent. Each Agent authorizes its own Notion MCP connection. This Skill does not share credentials.

## Privacy
This is a public repository. Never put personal RAW material, personal profile data, employer-internal documents, private examples, Notion tokens, OAuth credentials, cookies, passwords, private keys, or connection strings here. Personal knowledge stays in the user's private Notion workspace. Ask before deleting pages, merging uncertain identities, or overwriting material history.

## Tool adaptation
Notion MCP tool names differ across clients. Map workflows to the connected tools actually available. Do not assume a capability exists. If native mentions or backlink inspection are unavailable, state that full bidirectional Wiki behavior cannot be guaranteed; do not silently degrade to plain links.

## Detailed workflows
- [Workspace setup](references/workspace-setup.md)
- [Knowledge schema](references/knowledge-schema.md)
- [Capture](references/workflows/capture.md)
- [Ingest](references/workflows/ingest.md)
- [Query](references/workflows/query.md)
- [Update](references/workflows/update.md)
- [Lint and Graph](references/workflows/lint-graph.md)
- [Privacy and provenance](references/privacy-provenance.md)
- [Agent compatibility](references/agent-compatibility.md)
