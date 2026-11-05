# Notion workspace and schema

## Canonical workspace

Discover pages by title; do not hardcode page IDs in this public Skill.

- Root: **CCLUCKY Knowledge OS**
- Workspace page: **Inbox** (the user-facing collection dashboard, directly under Knowledge OS)
- Intake database: **Rows** (the single canonical original-material database nested under Inbox)
- Knowledge sections under the root: **Sources**, **Entities**, **Concepts**, **Syntheses**, **System**

The workspace may evolve. Always search and fetch the current page/database before relying on its structure.

## Rows database properties

Fetch the database's data source and use its exact property names and types.

| Property | Type | Purpose |
|---|---|---|
| Name | Title | Human-readable source title |
| Status | Select | Pending / Processing / Processed / Needs Review |
| Source Type | Select | Conversation / Article / Document / Meeting / Code/PR / Idea / Other |
| Source URL | URL | Original external source, if any |
| Source Date | Date | Date of the source, if known |
| Processed At | Date | Successful ingest completion time |
| Captured By | Rich text | Agent/client that captured the item |
| Processing By | Rich text | Agent currently processing the item |
| Processing Started At | Date | Processing start time |
| Processing Notes | Rich text | Error, recovery, or review note |
| Tags | Multi-select | Work / Personal / Technology / Career / Research / Project |
| Ingest Summary | Rich text | Short processing result |
| Content Hash | Rich text | Optional stable content fingerprint |

The Notion page body of each Rows record holds the original content or a durable source reference plus enough captured text to preserve what was ingested. Do not store a large source only in a short metadata property.

Notion's system-created page timestamp is the capture time; do not try to write to it.

## Knowledge page destinations

- Source summaries and provenance → Sources
- Stable people, organizations, products, projects, repositories → Entities
- Reusable methods, technical principles, frameworks, mental models → Concepts
- Multi-source conclusions, comparisons, answers worth preserving → Syntheses
- Operating rules, indexes, architecture decisions, and system logs → System

These are containers, not a rigid taxonomy. If the correct page already exists elsewhere, update it rather than duplicating it.

## Page linking and backlinks

Internal relationships must be represented with Notion-native page mentions, not plain title text and not ordinary external-link syntax.

Before writing Notion-flavored Markdown, read the Notion Markdown specification exposed by the connected MCP (commonly the resource `notion://docs/notion-flavored-markdown-spec`). Use its documented mention syntax and actual page URLs returned by fetch/search.

A native mention from Page A to Page B automatically creates a backlink on Page B. Verify backlinks with the available backlink operation when supported. If the client cannot inspect backlinks, state that the mention was created but backlink verification was unavailable.

Never invent a Notion page URL or mention target.