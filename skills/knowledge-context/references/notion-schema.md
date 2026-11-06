# Notion workspace and schema

## Canonical workspace

Discover pages by title; never hardcode private Notion IDs.

- Root: **CCLUCKY Knowledge OS**
- Workbench: **Inbox** (user-facing collection dashboard under the root)
- Intake database: **Rows** (canonical original-material database nested under Inbox)
- Knowledge areas: **Sources**, **Entities**, **Concepts**, **Syntheses**, **System**

Always fetch current pages, database/data-source URLs, property names, and types. The workspace can evolve.

## Rows properties

Fetch the live data-source schema and use exact property names and types.

| Property | Type | Purpose |
|---|---|---|
| Name | Title | Human-readable source title |
| Status | Select | Pending / Processing / Processed / Needs Review |
| Source Type | Select | Conversation / Article / Document / Meeting / Code/PR / Idea / Other |
| Source URL | URL | Original external source |
| Source Date | Date | Source date, if known |
| Processed At | Date | Successful completion time |
| Captured By | Rich text | Agent/client that captured the item |
| Processing By | Rich text | Agent currently processing the item |
| Processing Started At | Date | Processing start time |
| Processing Notes | Rich text | Error, recovery, or review note |
| Tags | Multi-select | Useful topic/category tags |
| Ingest Summary | Rich text | Short processing result |
| Content Hash | Rich text | Optional stable fingerprint |

The Rows page body holds the original content or a durable source reference plus enough captured text to preserve what was ingested. Do not store a large source only in a short metadata property.

## Knowledge destinations

- Source summaries and provenance → Sources
- Stable people, organizations, products, projects, repositories → Entities
- Reusable methods, technical principles, frameworks, mental models → Concepts
- Multi-source conclusions, comparisons, reusable answers → Syntheses
- Operating rules, indexes, architecture decisions, system logs → System

These are containers, not rigid taxonomy. Update an existing canonical page instead of duplicating it.

## Native mentions and backlinks

Use Notion-native page mentions for internal relationships, not plain title text or ordinary hyperlinks.

Read the Notion Markdown specification exposed by the connected MCP (commonly `notion://docs/notion-flavored-markdown-spec`) before writing mentions. Use documented syntax and exact page URLs returned by Notion.

A native mention from Page A to Page B creates an inbound backlink on Page B. Verify backlinks with the available operation. If the client cannot inspect backlinks, state that the mention was created but verification was unavailable. Never invent a page URL or target.
