# CCLUCKY LLM Wiki

**A portable Agent Skill for a Notion-backed personal knowledge base.**

Capture material in Notion's Rows database through the Inbox workbench, ask any connected agent to ingest it, and let the agent maintain Sources, Entities, Concepts, Syntheses, and native Notion backlinks.

The daily experience stays simple:

~~~text
把这篇文章沉淀到我的知识库
~~~

**The Skill is the workflow. The agent host owns the MCP connection. Notion is the canonical knowledge store.**

## Architecture

~~~text
Claude Code ─┐
Codex ───────┼── install the same CCLUCKY LLM Wiki Skill
WorkBuddy ───┘                 │
                               ▼
                     Agent's Notion MCP connection
                     configured by the user
                               │
                               ▼
                      User's Notion workspace
                      shared by that user's agents
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
             Inbox workbench             Knowledge areas
                 │                  Sources / Entities
                 ▼                  Concepts / Syntheses
             Rows database                 System
~~~

### Responsibility boundaries

| Component | Responsibility |
|---|---|
| This repository | Portable Skill instructions, workflow references, and a small WorkBuddy packaging script |
| Agent host | Install the Skill; configure and authorize its own Notion MCP connection |
| Notion MCP | Expose Notion search, read, write, and page-linking operations to the agent |
| Notion workspace | Store the user's original material and maintained knowledge |

- No repository clone is required for daily use.
- No custom MCP server, local backend, database, or OAuth implementation is required.
- Each agent connects independently to the same user's Notion workspace.
- The repository never stores the user's knowledge, workspace IDs, or credentials.

## Install

### Claude Code and Codex

Install the Skill from the public repository:

~~~bash
npx skills add ccclucky/llm-wiki-agent -g -a claude-code -a codex
~~~

### WorkBuddy

WorkBuddy imports a local Skill package through its UI. Build the package from a clone of this repository:

~~~bash
python scripts/package_workbuddy_skill.py
~~~

Then open **Experts → Skills → Connectors → Skills → Add Skill → Upload Skill** and upload:

~~~text
dist/cclucky-llm-wiki-workbuddy.zip
~~~

See [docs/workbuddy-installation.md](docs/workbuddy-installation.md) for details.

### Other compatible agents

Use the client's documented Skill installation method. If the client is not supported by the Skills CLI, copy **SKILL.md** and **references/** into its supported skills directory.

## Connect Notion MCP

Configure Notion MCP separately in every agent/client. The default supported endpoint is Notion's official remote MCP service:

~~~text
https://mcp.notion.com/mcp
~~~

Use the agent's remote MCP connection settings, complete Notion authorization, and grant access to the **CCLUCKY Knowledge OS** root page and its Inbox, Rows, Sources, Entities, Concepts, Syntheses, and System areas.

This is a remote MCP connection; normally the agent connects to the endpoint rather than launching a local stdio server. Exact setup and authorization steps are client-specific. This repository does not configure MCP, manage OAuth, or share credentials between agents.

See [docs/agent-setup.md](docs/agent-setup.md) and the [end-to-end acceptance checklist](docs/notion-ingest-acceptance.md).

## Use

Once the Skill and Notion MCP are connected, use natural language:

| Intent | Example |
|---|---|
| Ingest | 把这篇文章沉淀到我的知识库 |
| Query | 结合知识库中已有的项目经验，分析一个技术方案 |
| Update | 把刚才确定的项目决策同步到知识库 |
| Lint | 检查知识库里的孤立页面、重复页面和矛盾 |
| Graph | 梳理 Agent、项目和技术概念之间的关系 |

Natural language is the portable cross-agent interface. A Skill does not automatically register native slash commands in every client.

## Knowledge model

The Skill discovers the workspace by page titles; it never hardcodes private page IDs.

- **Inbox** — the user-facing workbench and collection dashboard.
- **Rows** — the single shared Notion database nested under Inbox. Preserve original source material in each row before processing.
- **Sources** — source summaries, provenance, key claims, and evidence.
- **Entities** — people, organizations, products, repositories, projects, and systems.
- **Concepts** — reusable methods, technical principles, frameworks, and mental models.
- **Syntheses** — conclusions and comparisons built from multiple sources.
- **System** — operating rules, navigation, architecture decisions, and maintenance notes.

Internal relationships use Notion-native page mentions. A native mention creates a backlink on the mentioned page; plain text titles and ordinary URL hyperlinks are not substitutes.

See [SKILL.md](SKILL.md) and the detailed [workflow references](references/).

## Repository contents

~~~text
SKILL.md                         # Portable Agent Skill entrypoint
references/                      # Ingest, query/update, maintenance, schema, safety
scripts/package_workbuddy_skill.py
docs/                             # Agent setup, WorkBuddy install, acceptance checklist
tests/                            # Contract and package tests
~~~

The runtime Skill consists of **SKILL.md + references/**. The docs explain installation and acceptance; the script only packages those runtime files for WorkBuddy.

## Validate locally

~~~bash
python -m unittest discover -s tests -v
python scripts/package_workbuddy_skill.py
~~~

No third-party Python dependencies are required.

## Privacy boundary

This is a public repository containing reusable instructions and packaging code only. Never commit original Rows source material, personal wiki exports, private project documents, workspace-specific Notion IDs, OAuth tokens, API keys, cookies, or local state.

The Skill never asks agents to upload personal knowledge into this GitHub repository. Each user retains ownership and control of their own Notion workspace.

## License

MIT License — see [LICENSE](LICENSE).
