# Knowledge-base lint workflow

Run lint when the user asks, after a batch of ingests, or when the knowledge base appears inconsistent.

## Checks

1. **Orphan pages:** no meaningful inbound backlinks and no clear index/root role.
2. **Broken references:** internal mentions that no longer resolve, or plain-text references that should be native mentions.
3. **Duplicate pages:** the same entity/concept represented by multiple canonical pages.
4. **Missing provenance:** material claims without a source or clear user-reported label.
5. **Contradictions:** incompatible claims, dates, statuses, or decisions across sources.
6. **Stale pages:** canonical pages not updated despite newer authoritative material.
7. **Missing knowledge pages:** durable entities/concepts repeatedly mentioned but lacking a canonical page.
8. **Thin hubs:** highly connected pages with too little explanatory content.
9. **Unprocessed Rows:** Pending or Processing records left too long, including stale claims.

Do not equate low link count with poor quality. Source pages may naturally be leaves; some concepts are hubs. Report context, not just counts.

## Scope and evidence

- Define the audit scope. If unspecified, begin with a bounded audit and state its scope.
- Use actual Notion pages, schema, and backlinks where available.
- Do not claim full-workspace coverage from partial search results.
- Each finding must include severity, affected page, evidence, and suggested repair.
- Distinguish confirmed defects from suspected issues.

## Default is read-only

Do not automatically delete or merge pages. Suggest repairs first.

If the user explicitly asks for repairs:
- safe, unambiguous additions (e.g. a missing native mention with clear evidence) may be made within the requested scope;
- ask before deleting/merging pages, resolving substantive contradictions, rewriting user decisions, or restructuring many pages.

## Report

Provide audit scope, coverage limitations, severity, affected pages, evidence, recommended repair, and whether any repair was actually performed.
