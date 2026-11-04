# CCLUCKY LLM Wiki

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A portable Agent Skill for a shared Notion-backed LLM Wiki.**

Capture material in one shared Notion RAW inbox, ask any connected agent to ingest it, and let the agent maintain Sources, Entities, Concepts, Syntheses, and native Notion backlinks.

The intended daily experience stays simple:

~~~text
把这篇文章沉淀到我的知识库
/ingest
~~~

The Skill is the workflow. Notion MCP is the connection. Notion is the canonical knowledge store.

## Final usage model

~~~text
Claude Code ─┐
Codex ───────┼── each agent installs this Skill
Other agents ┘    and connects its own Notion MCP
                         │
                         ▼
                CCLUCKY LLM Wiki Skill
                ingest / query / update
                lint / graph
                         │
                         ▼
                Shared Notion Workspace
                RAW → Sources / Entities
                    → Concepts / Syntheses
~~~

- **No repository clone is required for daily use.**
- **No custom MCP server is required.**
- Each agent configures its own Notion MCP connection and authorizes the same workspace.
- Each agent installs the same Skill package from this repository.
- All agents read and write the same Notion pages and RAW database.

## Install

The current development branch can be installed with the Skills CLI:

~~~bash
npx skills add https://github.com/ccclucky/llm-wiki-agent/tree/feat/notion-first-agent-skill -g -a claude-code -a codex
~~~

After this branch is merged into main, the shorter command is:

~~~bash
npx skills add ccclucky/llm-wiki-agent -g -a claude-code -a codex
~~~

For another compatible agent, select it with the Skills CLI if supported, or copy **SKILL.md** and the **references/** directory into its supported skills directory.

Then connect that agent to Notion using the official remote MCP endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

Complete the agent-specific authorization and grant access to the **CCLUCKY Knowledge OS** root page, including Inbox, RAW, Sources, Entities, Concepts, Syntheses, and System.

Client-specific MCP setup is intentionally outside this repository. See [docs/agent-setup.md](docs/agent-setup.md).

## Use

Once the Skill and Notion MCP are connected, use natural language:

| Intent | Example |
|---|---|
| Ingest | "把这篇文章沉淀到我的知识库" |
| Query | "结合知识库中已有的项目经验，分析一个技术方案" |
| Update | "把刚才确定的项目决策同步到知识库" |
| Lint | "检查知识库里的孤立页面、重复页面和矛盾" |
| Graph | "梳理 Agent、项目和技术概念之间的关系" |

Natural language is the portable cross-agent interface. Some clients can add /ingest, /query, /lint, and /graph aliases, but installing one Skill does not register those slash commands in every client.

## Knowledge model

The Skill discovers the workspace by page titles; it does not hardcode private page IDs.

- **RAW** — one shared Notion database under Inbox. Preserve source material before processing.
- **Sources** — source summaries, provenance, key claims, and evidence.
- **Entities** — people, organizations, products, repositories, projects, and systems.
- **Concepts** — reusable methods, technical principles, frameworks, and mental models.
- **Syntheses** — conclusions and comparisons built from multiple sources.
- **System** — operating rules, navigation, architecture decisions, and maintenance notes.

Internal relationships must use Notion-native page mentions. A native mention creates a backlink on the mentioned page. Plain text titles and ordinary URL hyperlinks are not a substitute.

See:
- [SKILL.md](SKILL.md) — main Skill instructions
- [references/ingest.md](references/ingest.md) — capture and ingest workflow
- [references/query-update.md](references/query-update.md) — query and update workflow
- [references/maintenance.md](references/maintenance.md) — lint and graph
- [references/notion-schema.md](references/notion-schema.md) — workspace schema
- [references/security-and-concurrency.md](references/security-and-concurrency.md) — privacy and multi-agent safety
- [docs/notion-ingest-acceptance.md](docs/notion-ingest-acceptance.md) — end-to-end and cross-agent acceptance checklist

## What this fork contains

The repository contains reusable instructions and optional legacy local-mode tooling. It does **not** contain the user's private knowledge, Notion credentials, workspace IDs, or a hosted service.

- **Primary:** Notion-first Agent Skill in SKILL.md and references/.
- **Legacy local/Obsidian mode:** existing Python tools under tools/ can still process local Markdown files when explicitly requested. It is not the default shared multi-agent workflow.
- **Legacy Notion publisher:** tools/notion_sync.py mirrors local Markdown to Notion in one direction. It is not used by the Notion-first Skill and does not provide bidirectional sync. See [docs/legacy-notion-publisher.md](docs/legacy-notion-publisher.md).

## Privacy boundary

This is a public repository. Never commit RAW sources, personal wiki exports, private project documents, workspace-specific Notion IDs, OAuth tokens, API keys, cookies, or local sync state. Local raw/wiki/graph output is user data, not project source code.

The Skill never asks agents to upload personal knowledge into this GitHub repository. Each user keeps their knowledge in their own Notion workspace.

## License

MIT License — see [LICENSE](LICENSE).