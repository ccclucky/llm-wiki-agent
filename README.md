# CCLUCKY LLM Wiki

**A portable Agent Skill for a personal knowledge base powered by Notion.**

Use the same knowledge-management workflow from different AI agents. Each agent connects to the same Notion workspace through its own Notion MCP connection; the Skill tells the agent how to capture, organize, retrieve, and maintain knowledge.

> **The Skill is the workflow. Notion is the source of truth. The agent host owns the MCP connection.**

## Quick start

You need both the Skill and a working Notion MCP connection.

1. **Install the Skill** in each agent you want to use.
2. **Connect Notion MCP** separately in each agent and authorize access to the existing **CCLUCKY Knowledge OS** page.
3. Start a conversation and ask naturally, for example: `把这篇文章沉淀到我的知识库`.

No repository clone is needed for normal daily use. WorkBuddy users only need a clone when building the uploadable ZIP package locally.

## How it works

~~~text
                         One shared Notion workspace
                                      ▲
                                      │
        ┌─────────────────────────────┼────────────────────────────┐
        │                             │                            │
   Claude Code                     Codex                       WorkBuddy
        │                             │                            │
   CCLUCKY Skill                 CCLUCKY Skill                CCLUCKY Skill
        │                             │                            │
   Notion MCP                    Notion MCP                   Notion MCP
   (authorized                  (authorized                  (authorized
    by this agent)                by this agent)                by this agent)
        └─────────────────────────────┼────────────────────────────┘
                                      │
                           CCLUCKY Knowledge OS
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
             Inbox / Rows                         Knowledge areas
          Original material intake          Sources / Entities / Concepts
                                            Syntheses / System
~~~

### Ingestion flow

There are two ways to submit material:

- **Direct capture:** give an agent text, a file, a URL, a research note, or a decision and ask it to ingest the material. The agent first preserves the original material in **Inbox → Rows**, then processes it.
- **Manual intake:** add a record to the **Rows** database yourself. Ask an agent to ingest it or process pending records.

The agent checks for duplicates, reads relevant existing knowledge, creates or updates canonical pages, adds Notion-native page mentions, verifies the result where the connected MCP supports it, and updates the Rows status.

~~~text
Material ──► Inbox / Rows ──► Ingest ──► Sources / Entities / Concepts
                                  │                    │
                                  └── status & summary └── native mentions
                                                          and backlinks
~~~

## Knowledge model

The Skill discovers the existing workspace by page title. It does not hardcode private Notion page or database IDs.

| Area | Purpose |
|---|---|
| **Inbox** | User-facing collection workbench |
| **Rows** | Canonical intake database; preserves original material and processing status |
| **Sources** | Source summaries, provenance, evidence, and claims |
| **Entities** | People, organizations, products, projects, repositories, and systems |
| **Concepts** | Reusable methods, technical principles, frameworks, and mental models |
| **Syntheses** | Conclusions and comparisons supported by multiple sources |
| **System** | Operating rules, navigation, architecture decisions, and maintenance notes |

Internal wiki relationships use **Notion-native page mentions**. A native mention creates an inbound backlink on the mentioned page; plain-text titles and ordinary URL links are not equivalent. The Skill asks agents to verify backlinks when the connected MCP exposes that capability.

Rows records use four statuses:

- `Pending` — captured and waiting for processing.
- `Processing` — currently being handled by an agent.
- `Processed` — processing and required validation completed.
- `Needs Review` — blocked, incomplete, or requiring human review.

The status fields help agents coordinate, but they are **not an atomic distributed lock**. The Skill explicitly requires agents to re-fetch records and avoid concurrent edits.

## Install the Skill

### Claude Code and Codex

Install from the public repository with the Skills CLI:

~~~bash
npx skills add ccclucky/llm-wiki-agent -g -a claude-code -a codex
~~~

### WorkBuddy

Build the WorkBuddy-compatible ZIP from a clone of this repository:

~~~bash
python scripts/package_workbuddy_skill.py
~~~

Upload the generated file:

~~~text
dist/cclucky-llm-wiki-workbuddy.zip
~~~

In WorkBuddy, open **Experts → Skills → Connectors → Skills → Add Skill → Upload Skill**.

See [WorkBuddy installation](docs/workbuddy-installation.md).

### Other compatible agents

Use the client's documented Skill installation method. If the client does not support the Skills CLI or package import, copy **SKILL.md** and **references/** into its supported skills directory.

## Connect Notion MCP

Configure Notion MCP independently in every agent/client. The official remote endpoint used by this project is:

~~~text
https://mcp.notion.com/mcp
~~~

In the agent's MCP settings:

1. Add the remote Notion MCP endpoint using the transport supported by that client.
2. Complete Notion's authorization flow.
3. Grant access to the existing **CCLUCKY Knowledge OS** root page and its required children/databases.
4. Verify that the agent can search, read, create, and update the Rows database and knowledge pages.

Each agent owns its own connection and authorization, even though all agents access the same user's Notion workspace.

**This repository does not provide or configure an MCP server.** It does not implement OAuth, store Notion credentials, run a local wiki backend, or synchronize separate knowledge stores. Do not paste Notion tokens into chat or commit credentials to this repository.

See [Agent setup](docs/agent-setup.md).

## Use it

Once the Skill and Notion MCP are connected, use natural language:

| Task | Example |
|---|---|
| Ingest | 把这篇文章沉淀到我的知识库 |
| Process intake | 处理 Rows 里待处理的资料 |
| Query | 结合知识库中已有的项目经验，分析这个技术方案 |
| Update | 把刚才确定的项目决策同步到知识库 |
| Lint | 检查知识库里的孤立页面、重复页面和矛盾 |
| Graph | 梳理 Agent、项目和技术概念之间的关系 |

Natural language is the portable interface across clients. Installing a Skill does **not** automatically register native `/ingest`, `/query`, `/lint`, or `/graph` slash commands in every agent.

## Repository structure

~~~text
llm-wiki-agent/
├── SKILL.md                         # Portable Agent Skill entrypoint
├── references/
│   ├── ingest.md                    # Capture, ingest, validate, and recover
│   ├── query-update.md              # Query and maintain canonical knowledge
│   ├── maintenance.md               # Lint and graph workflows
│   ├── notion-schema.md             # Workspace and Rows schema contract
│   └── security-and-concurrency.md  # Privacy and multi-agent safety
├── scripts/
│   └── package_workbuddy_skill.py   # Build the WorkBuddy ZIP
├── docs/
│   ├── agent-setup.md
│   ├── workbuddy-installation.md
│   └── notion-ingest-acceptance.md
├── tests/
├── AGENTS.md
└── README.md
~~~

The runtime Skill is **SKILL.md + references/**. Documentation describes installation and acceptance. The packaging script only bundles the runtime Skill for WorkBuddy.

## Validation and compatibility

Run the repository checks locally:

~~~bash
python -m unittest discover -s tests -v
python scripts/package_workbuddy_skill.py
~~~

No third-party Python dependencies are required.

CI validates the Skill contract, references, privacy checks, and WorkBuddy package build. **A passing CI run does not prove that a particular agent can access a user's Notion workspace.** Run the [end-to-end acceptance checklist](docs/notion-ingest-acceptance.md) independently in every client, including Rows writes, native mentions, and backlink verification where available.

## Design boundaries

- **Not a local wiki engine:** the legacy Obsidian/local Markdown runtime and one-way publisher are not part of this project.
- **Not an MCP server:** the agent host configures and authorizes its own Notion MCP connection.
- **Not a data repository:** personal knowledge stays in the user's Notion workspace, not in GitHub.
- **Not a destructive sync tool:** source material is preserved; conflicts and uncertain updates are surfaced for review.

Never commit original Rows content, personal wiki exports, private project documents, workspace-specific Notion IDs, OAuth tokens, API keys, cookies, passwords, or local state.

## License

MIT License — see [LICENSE](LICENSE).
