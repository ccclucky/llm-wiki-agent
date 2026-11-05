---
name: cclucky-llm-wiki
display_name: CCLUCKY 个人知识库
display_name_en: CCLUCKY LLM Wiki
description: Capture, ingest, query, update, lint, and map a Notion-backed personal knowledge wiki through the agent's connected Notion MCP tools.
description_zh: 通过 Agent 已连接的 Notion MCP，统一管理个人知识库，支持资料收集、知识沉淀、查询更新和质量检查。
description_en: Maintain a Notion-backed personal wiki across connected AI agents.
version: 0.2.0
author: CCLUCKY
examples_zh:
  - "把这篇文章沉淀到我的知识库"
  - "查询我之前记录的项目决策"
  - "检查知识库里的孤立页面和矛盾"
examples_en:
  - "Ingest this article into my wiki"
  - "Find the project decision I recorded earlier"
  - "Check the wiki for orphan pages and contradictions"
---

# CCLUCKY LLM Wiki

A portable Agent Skill for a shared, Notion-backed personal knowledge base.

**Capture material in Rows through Inbox → run Ingest → the agent maintains the wiki.**

This repository distributes the knowledge-management workflow. Notion is the canonical store. The agent host owns the MCP connection.

## Architecture and responsibility boundaries

- **This Skill defines the workflow:** capture, ingest, query, update, lint, and graph.
- **The agent host owns MCP:** each agent/client configures and authorizes its own Notion MCP connection.
- **Notion is the data layer:** agents belonging to the same user work against the same Notion workspace.
- **This repository is not a runtime service:** it contains no MCP server, OAuth flow, Notion API backend, database, user knowledge, or local wiki engine.

The default connection is Notion's official remote MCP endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

The user connects this endpoint in each agent's normal MCP settings. The Skill does not configure, start, install, authorize, or manage the MCP server. Do not ask the user for a Notion token, start a local stdio process, or silently fall back to direct Notion API calls.

Do not require the user to clone this repository for daily use. Install the same Skill in each compatible agent and connect each agent to the user's Notion workspace.

## Connection preflight

Before the first knowledge operation in a session:

1. Inspect the tools exposed by the connected Notion MCP. Discover the available search, page read, database/data-source query, create/update, block editing, and page-mention operations. Tool names and coverage vary by client; do not assume exact names.
2. Confirm that the connection supports the read/write operations required by the user's request.
3. Search for the exact root page **CCLUCKY Knowledge OS**. Do not create another root page if it is missing; report an access or connection problem.
4. Locate the **Inbox** workspace page under the root, then locate its nested **Rows** database. Inbox is the user-facing workbench; Rows is the canonical original-material database.
5. Fetch the Rows database/data-source schema before creating or updating database records. Use the actual property names and types returned by Notion.
6. Locate the existing **Sources**, **Entities**, **Concepts**, **Syntheses**, and **System** sections under the root. If System contains an Agent Context Protocol or current operating rules, read the relevant parts before writing.
7. Read only the pages relevant to the current task. Do not load the entire workspace by default.

If Notion MCP is unavailable, explain that the user must connect the official remote Notion MCP endpoint in this agent first. Do not try to configure it on the user's behalf. Do not fall back to local Markdown, another workspace, or a newly created knowledge base.

Read [references/notion-schema.md](references/notion-schema.md) when discovering the workspace or Rows schema.

## Intent routing

| User intent | Workflow |
|---|---|
| "把这个放进知识库" / "ingest this" / "/ingest" | [Ingest](references/ingest.md) |
| "查一下我之前记录的..." / "query the wiki" / "/query" | [Query and update](references/query-update.md) |
| "更新项目知识" / "update the wiki" | [Query and update](references/query-update.md) |
| "检查知识库" / "lint" / "/lint" | [Maintenance](references/maintenance.md) |
| "查看知识关系" / "build graph" / "/graph" | [Maintenance](references/maintenance.md) |

The portable cross-agent interface is natural language. A single Agent Skill does not register /ingest, /query, /lint, and /graph as native slash commands in every client. If a client provides command aliases, they may map to these workflows; otherwise invoke this Skill by its installed name or simply describe the task.

## Operating rules

- Preserve original source material in the Rows database before transforming it.
- Distinguish verified facts, user statements, source claims, assistant analysis, and hypotheses.
- Attach provenance to material claims: source page, source date, URL or document reference when available.
- Search for existing pages before creating new ones. Update canonical pages instead of creating near-duplicates.
- Use Notion-native page mentions for internal wiki links. Plain text titles and ordinary URL hyperlinks do not create Notion backlinks.
- A single native page mention creates an inbound backlink on the mentioned page. Do not add reciprocal mentions merely to simulate backlinks; add them only when both directions carry meaningful context.
- Create links only when the relationship is useful and supported. Label inferred relationships as inferred; never present them as sourced facts.
- Do not silently overwrite conflicting claims. Preserve both claims, their sources and dates, and flag the conflict.
- Keep raw sources immutable after capture. Corrections belong in a note or a new source version.
- Do not delete Rows records or knowledge pages during normal ingestion or maintenance.
- Use the smallest safe Notion edit. Fetch before editing; prefer targeted updates over replacing whole pages.
- When a workflow cannot be completed because a tool is unavailable, report exactly which step is blocked. Do not pretend it was completed.

## Detailed workflows

The following Markdown links are the canonical references. The @references declarations additionally enable WorkBuddy's sub-resource loader.

- Ingest: [references/ingest.md](references/ingest.md)
- Query and update: [references/query-update.md](references/query-update.md)
- Lint and graph: [references/maintenance.md](references/maintenance.md)
- Notion schema: [references/notion-schema.md](references/notion-schema.md)
- Multi-agent safety and privacy: [references/security-and-concurrency.md](references/security-and-concurrency.md)

@references/ingest.md
@references/query-update.md
@references/maintenance.md
@references/notion-schema.md
@references/security-and-concurrency.md

## Completion report

After an operation, briefly report:
- what source was captured or what question was answered;
- which canonical pages were created or updated;
- which native page links were added and whether backlinks were verified;
- whether contradictions, duplicates, or missing evidence were found;
- for ingestion, whether the Rows record is Pending, Processing, Processed, or Needs Review.

Never report "bidirectional links verified" unless the agent actually checked the native mentions or backlinks.
