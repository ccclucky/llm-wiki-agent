# Ingest workflow

The user experience must remain simple: provide material, say "ingest" or "/ingest", and let the agent maintain the wiki.

## 1. Accept the source

Sources may be:
- text pasted into the conversation;
- a conversation summary the user explicitly asks to preserve;
- a local attachment or file accessible to the agent;
- an external article, paper, repository, issue, pull request, or web page;
- meeting notes, project updates, decisions, or research notes.

Use the source content actually available to the agent. Do not claim to have read an attachment or URL that was not accessible. For a URL, retrieve the page using an appropriate connected browser/search tool before ingesting it; preserve the URL as provenance.

## 2. Capture into RAW first

1. Discover the shared RAW database using the workspace structure in [notion-schema.md](notion-schema.md).
2. Fetch the data source schema before writing.
3. Search RAW for a likely duplicate using source URL, title, and content fingerprint where available.
4. If the same source already exists, update or reference that record rather than creating a duplicate. If it was already Processed and the content is unchanged, report that it is already ingested.
5. Create a RAW database page with:
   - Name: concise source title;
   - Status: Inbox;
   - Source Type: the closest supported type;
   - Source URL / Source Date when known;
   - Captured By: current agent/client;
   - Tags: only useful tags;
   - Content Hash: optional stable fingerprint.
6. Put the original source text in the RAW page body. For a file, attach it or include the extracted content; for a very large source, preserve the file/reference and a clear extraction note. Never silently truncate without saying so.

Do not start knowledge transformation before the original material is safely captured.

## 3. Claim the item

Before processing, re-fetch the RAW record.

- If Status is Processed, check whether the content changed before reprocessing.
- If Status is Processing and Processing By identifies another agent, do not process it concurrently. Report that another agent has claimed it.
- If Status is Processing but the recorded start is clearly stale, inspect the record and its partial output. Only reclaim it after determining that the previous run is no longer active.
- Set Status to Processing, Processing By to the current agent/client, Processing Started At to now, and clear stale Processing Notes.

Notion does not provide a transaction or compare-and-swap lock through every MCP client. This status protocol reduces collisions but is not a perfect distributed lock. Avoid simultaneous ingest runs for the same RAW record.

## 4. Understand the source against existing knowledge

Search the wiki before creating anything. Read:
- the relevant source and project pages;
- relevant entity and concept pages;
- relevant existing syntheses;
- System guidance if the source changes a workflow or architecture.

Extract:
- core summary;
- material claims and evidence;
- people, organizations, products, projects, repositories, and systems;
- reusable concepts, mechanisms, methods, and decisions;
- dates and temporal scope;
- implications and open questions;
- contradictions with existing knowledge;
- useful links to existing pages.

Keep these distinctions explicit:
- **Verified fact:** directly supported by a reliable source.
- **User statement:** explicitly supplied by the user; preserve as user-reported.
- **Source claim:** asserted by a source but not independently verified.
- **Analysis:** reasoning derived from evidence.
- **Hypothesis:** plausible but unverified.

Do not promote speculation to fact. Do not create a new entity or concept for every passing mention; create pages for durable, reusable, or repeatedly referenced knowledge.

## 5. Update the Wiki

### Source page

Create or update one page under Sources. Include:
- title, source date, source type, original URL/file reference;
- concise summary;
- key claims with provenance;
- important evidence or short quotations;
- related entities and concepts;
- contradictions and uncertainty;
- capture/ingest date.

### Entity pages

Create or update only durable entities. Maintain:
- what the entity is;
- aliases and identifiers when relevant;
- verified facts and dated changes;
- related sources;
- relationships to other entities and concepts.

### Concept pages

Create or update reusable concepts. Maintain:
- concise definition;
- mechanism or structure;
- boundaries and common misunderstandings;
- practical examples;
- related entities and concepts;
- source evidence and unresolved questions.

### Syntheses and overview

Create a synthesis only when the new material contributes to a multi-source conclusion, comparison, or answer worth reusing. Do not create a synthesis page for every routine source. Update an existing synthesis when the evidence materially changes.

## 6. Build native links

For every important connection:
1. Resolve the exact existing Notion page by searching and fetching it.
2. Add a Notion-native page mention in a meaningful Connections / Related Sources section.
3. Include a short explanation of why the pages are related.
4. If a target page does not exist, decide whether it merits a new Entity or Concept page; do not create pages merely to satisfy a link.
5. Re-fetch or use the available backlinks operation to verify that the target page shows the new inbound reference.

One native mention creates the target page's backlink. Do not add redundant reciprocal mentions. The wiki graph is the network of canonical pages and their native mentions/backlinks.

Prefer a few high-value links over link spam. Do not link every repeated word.

## 7. Validate and complete

Before marking the RAW record Processed:
- verify the source page exists;
- verify every created/updated page exists;
- verify internal references resolve to real Notion pages;
- check for duplicate pages;
- check that key claims retain provenance;
- verify important backlinks when the client supports it;
- record contradictions or review requirements.

Then update the RAW record:
- Status: Processed if complete; otherwise Needs Review;
- Processed At: current time if complete;
- Ingest Summary: concise summary of what changed;
- Processing By: current agent/client;
- Processing Notes: warnings, unresolved items, or recovery details.

Never delete the RAW record after successful ingestion.

## 8. User-facing result

Report the source captured, key pages created/updated, high-value links added, contradictions, and any incomplete verification. Do not dump the entire generated wiki content unless requested.