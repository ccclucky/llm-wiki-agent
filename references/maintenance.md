# Wiki maintenance: lint and graph

## Lint

Run lint when the user asks, periodically after a batch of ingests, or when the knowledge base appears inconsistent.

Check:

1. **Orphan pages:** pages with no meaningful inbound backlinks and no clear role as a root/index page.
2. **Broken references:** internal mentions that no longer resolve, or plain-text references that should be native mentions.
3. **Duplicate pages:** same entity/concept represented by multiple canonical pages.
4. **Missing provenance:** material claims without a source or a clear user-reported label.
5. **Contradictions:** incompatible claims, dates, statuses, or decisions across sources.
6. **Stale pages:** canonical pages not updated despite newer authoritative source material.
7. **Missing knowledge pages:** a durable entity or concept appears repeatedly but has no canonical page.
8. **Thin hubs:** highly connected pages with too little explanatory content.
9. **Unprocessed Inbox records:** records left in Inbox or Processing for too long, including stale Processing claims.

Do not equate low link count with bad quality. Some source pages are naturally leaves; some concepts are hubs. Report context, not just counts.

Output a compact report with severity, affected pages, evidence, and suggested repairs. Do not automatically delete or merge pages. Ask before destructive changes.

## Graph

Build a knowledge relationship map from actual Notion pages and native mentions/backlinks.

Represent relationship types distinctly:
- **Explicit:** a source-backed native page mention with an explanation.
- **Inferred:** a plausible relationship suggested by synthesis, clearly labelled as inferred and accompanied by a confidence/reason.
- **Contradictory:** claims that conflict, with both source references retained.
- **Temporal:** a status or relationship changed over time.

Do not write inferred edges as if they were explicit facts. Do not create pages just because a graph edge mentions a missing title.

When the Notion client supports backlinks, use them to inspect inbound links. If it cannot enumerate all pages or backlinks, state that the graph is partial. Do not claim to have built a complete graph from search results alone.

Return:
- most connected entities/concepts;
- isolated or weakly connected pages worth reviewing;
- important cross-domain connections;
- unresolved or contradictory relationships;
- limitations in the available Notion MCP operations.

A visual graph is optional. A correct, inspectable relationship map is more important than an attractive but incomplete visualization.

## Repair policy

Safe automatic repairs:
- add a missing native mention when the target page is unambiguous and the relationship is source-supported;
- add missing provenance to a page when the exact source is known;
- update an index/navigation page after creating a canonical page.

Require user confirmation:
- delete pages or RAW records;
- merge pages where information could be lost;
- resolve a substantive contradiction;
- rewrite a user's stated position or decision;
- move large groups of pages or change workspace structure.