---
name: cclucky-llm-wiki
display_name: CCLUCKY 个人知识库
display_name_en: CCLUCKY LLM Wiki
description: Capture, ingest, query, update, lint, and map a Notion-backed personal knowledge wiki. Use when the user asks to save knowledge, ingest a source, recall a project decision, search prior knowledge, or audit wiki relationships.
description_zh: 统一管理共享 Notion 个人知识库，支持 Inbox 收集、知识沉淀、查询更新和质量检查。
description_en: Maintain a shared Notion-backed personal wiki across connected AI agents.
version: 0.1.0
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

A shared, Notion-backed LLM Wiki. Preserve the simple workflow of the original Obsidian LLM Wiki:

**Put material in Inbox → run Ingest → the agent maintains the wiki.**

This repository distributes the workflow as one portable Skill. It does not host a server, store user knowledge, manage Notion credentials, or configure an agent's MCP connection.

## Non-negotiable architecture

- **Notion is the canonical store.** All agents work against the same Notion workspace and the same Inbox database.
- **The connected Notion MCP is the transport.** Use the current agent's available Notion MCP tools. Tool names vary between clients; discover their capabilities rather than assuming exact names.
- **This Skill is the workflow.** It defines how to capture, ingest, query, update, lint, and map knowledge.
- **Do not use the repository's local raw/ or wiki/ folders as the default knowledge store.** They belong to the legacy local/Obsidian mode only.
- **Do not require the user to clone this repository for daily use.** Install this Skill in each compatible agent and connect that agent to the same Notion workspace.
- **Do not build or require a custom MCP server.** Each agent owner configures its own Notion MCP connection.
- Never claim an operation succeeded until the Notion MCP confirms it.

## Connection preflight

Before the first operation in a session:

1. Confirm that a Notion MCP connection is available and supports the required read/write operations.
2. Search for the exact root page **CCLUCKY Knowledge OS**. Do not create another root page if it is missing; report an access or connection problem.
3. Locate the **Inbox · 原始资料收件箱** database directly under the root. The separate **Inbox · 使用说明** page is navigation and instructions only.
4. Fetch the Inbox database/data-source schema before creating or updating database records.
5. Locate the existing **Sources**, **Entities**, **Concepts**, **Syntheses**, and **System** sections under the root page.
6. Read only the pages relevant to the current task. Do not load the entire workspace by default.

If Notion MCP is not connected, explain that the user must connect Notion in this agent first. Do not silently fall back to local Markdown, another workspace, or a newly created knowledge base.

Read [references/notion-schema.md](references/notion-schema.md) when discovering the workspace or Inbox schema.

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

- Preserve original source material in the Inbox database before transforming it.
- Distinguish verified facts, user statements, source claims, assistant analysis, and hypotheses.
- Attach provenance to material claims: source page, source date, URL or document reference when available.
- Search for existing pages before creating new ones. Update canonical pages instead of creating near-duplicates.
- Use Notion-native page mentions for internal wiki links. Plain text titles and ordinary URL hyperlinks do not create Notion backlinks.
- A single native page mention creates an inbound backlink on the mentioned page. Do not add reciprocal mentions merely to simulate backlinks; add them only when both directions carry meaningful context.
- Create links only when the relationship is useful and supported. Label inferred relationships as inferred; never present them as sourced facts.
- Do not silently overwrite conflicting claims. Preserve both claims, their sources and dates, and flag the conflict.
- Keep raw sources immutable after capture. Corrections belong in a note or a new source version.
- Do not delete Inbox records or knowledge pages during normal ingestion or maintenance.
- Use the smallest safe Notion edit. Fetch before editing; prefer targeted updates over replacing whole pages.
- When a workflow cannot be completed because a tool is unavailable, report exactly which step is blocked. Do not pretend it was completed.

## Detailed workflows

The following Markdown links are the canonical references. The `@references/` declarations additionally enable WorkBuddy's sub-resource loader.

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
- which native page links were added;
- whether contradictions, duplicates, or missing evidence were found;
- whether the Inbox record is Inbox, Processing, Processed, or Needs Review.

Never report "bidirectional links verified" unless the agent actually checked the native mentions or backlinks.
