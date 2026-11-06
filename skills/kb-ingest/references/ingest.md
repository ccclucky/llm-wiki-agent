# Ingest workflow

The user experience should remain simple: provide material and ask the agent to save or ingest it. The agent preserves the source in Rows before transforming it.

## 1. Accept the source

Supported sources include:
- text pasted into the conversation;
- a conversation summary the user explicitly asks to preserve;
- a local attachment or file accessible to the agent;
- an external article, paper, repository, issue, pull request, or web page;
- meeting notes, project updates, decisions, or research notes.

Use only content actually available to the agent. For URLs, retrieve the page with an available browser/search tool before ingesting; preserve the URL as provenance. Never claim to have read inaccessible content.

There are two intake patterns:
- **Direct capture:** the user supplies material in chat/file/URL. Create a Rows record, then process it.
- **Manual Rows drop:** the user already created a Rows record. Find and process it without creating a duplicate.

If the user asks to process Pending records, query them and process sequentially. Respect records claimed by another agent. Bound the batch and report its scope; do not start an unbounded run.

## 2. Capture into Rows first

1. Discover the Rows database nested under Inbox.
2. Fetch the live data-source schema and use exact property names/types.
3. Search for duplicates by URL, title, and content fingerprint where available.
4. If the same source exists, update/reference that record. If already Processed and unchanged, report that it is already ingested.
5. Create a Rows record with Name, Status = Pending, Source Type, Source URL/Date when known, Captured By, useful Tags, and optional Content Hash.
6. Put the original source text in the Rows page body. For files, attach or extract content; for large sources preserve the file/reference and explain any extraction limits. Never silently truncate.

Do not transform the knowledge before the original material is safely captured.

## 3. Claim the item

Re-fetch the Rows record before processing.
- If Processed, check whether the source changed before reprocessing.
- If Processing by another agent, stop and report the claim.
- If Processing appears stale, inspect partial output and determine whether the prior run is inactive before reclaiming.
- Set Status = Processing, Processing By = current agent/client, Processing Started At = now, and clear stale Processing Notes.

Notion MCP clients may not provide transactions or compare-and-swap. This protocol reduces collisions but is not a perfect distributed lock.

## 4. Understand the source

Search existing knowledge first. Read only relevant Sources, Entities, Concepts, Syntheses, project pages, and System guidance.

Extract summary, evidence-backed claims, entities, concepts, decisions, dates, implications, open questions, contradictions, and useful links.

Keep these distinctions explicit:
- **Verified fact:** directly supported by a reliable source.
- **User statement:** explicitly supplied by the user; preserve as user-reported.
- **Source claim:** asserted by a source but not independently verified.
- **Analysis:** reasoning derived from evidence.
- **Hypothesis:** plausible but unverified.

Do not create a page for every passing mention. Create durable, reusable, or repeatedly referenced knowledge only.

## 5. Update canonical knowledge

### Source
Create/update one Source page with title, source date/type, original URL/file reference, summary, key claims and provenance, evidence, related entities/concepts, contradictions/uncertainty, and ingest date.

### Entities
Create/update only durable people, organizations, products, projects, repositories, and systems. Preserve aliases, verified facts, dated changes, related sources, and relationships.

### Concepts
Create/update reusable methods, technical principles, frameworks, and mental models. Include definition, mechanism, boundaries, examples, sources, related concepts, and open questions.

### Syntheses
Create a synthesis only when material contributes to a multi-source conclusion, comparison, or reusable answer. Do not create one for every routine source.

## 6. Build native links

- Resolve the exact target Notion page from search/fetch.
- Add Notion-native page mentions in a meaningful Connections / Related Sources section.
- Explain why the pages are related.
- Do not invent targets or link every repeated word.
- Verify backlinks when the client exposes that capability; otherwise say verification was unavailable.

For Rows ingestion, add a native mention from the Rows record to its resulting Source page and from the Source page back to the Rows record as provenance. These directions serve distinct navigation purposes.

## 7. Validate and complete

Before setting Processed:
- verify the Source page and every created/updated page exists;
- verify internal references resolve;
- check duplicates;
- ensure key claims retain provenance;
- verify important backlinks where supported;
- record contradictions or review requirements.

Then set Status = Processed only if complete; otherwise Needs Review. Populate Processed At, Ingest Summary, Processing By, and Processing Notes as appropriate. Never delete the Rows record.

## 8. User-facing result

Report the captured source, Rows record, pages created/updated, high-value links, contradictions, verification limitations, and final status. Do not dump the full generated wiki content unless requested.
