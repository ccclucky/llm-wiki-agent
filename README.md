# CCLUCKY Knowledge Skills

**A cross-agent toolkit for managing one Notion-backed personal knowledge base.**

Install this repository once in a supported agent and get a set of focused commands and reusable Skills — not one oversized Skill.

> **One repository · multiple commands/Skills · one shared Notion knowledge base**

## What you get

### User-invoked commands

Run these explicitly when you want to choose the workflow:

| Command | Purpose |
|---|---|
| `/kb` | Open the command hub and choose a workflow |
| `/kb-setup` | Verify this agent's Notion MCP connection and workspace access |

### Workflow Skills (command + automatic invocation)

These Skills can be called explicitly by name or selected automatically when the user's request clearly matches:

| Skill / command | Purpose |
|---|---|
| `/kb-ingest` | Capture source material in Inbox → Rows, then process it into canonical knowledge |
| `/kb-query` | Search existing knowledge and answer with source-backed evidence |
| `/kb-update` | Update canonical pages while preserving provenance and history |
| `/kb-lint` | Audit duplicates, orphan pages, missing provenance, contradictions, stale pages, and pending Rows |
| `/kb-graph` | Map explicit/inferred relationships, hubs, gaps, and contradictions |

### Automatically available shared context

| Skill | Purpose |
|---|---|
| `knowledge-context` | Supplies the common Notion data model, evidence rules, privacy boundaries, and multi-agent safety conventions to the workflow Skills |

The workflow Skills call `knowledge-context` before operating. It is also available for automatic use when a task touches the CCLUCKY Knowledge OS.

## Install

Choose **one distribution route per agent**. Do not install the plugin and the Skills CLI copy into the same agent profile, or the Skills may appear twice.

### Claude Code — plugin marketplace

~~~bash
claude plugin marketplace add ccclucky/llm-wiki-agent
claude plugin install cclucky-knowledge-skills@cclucky
~~~

The plugin exposes all eight Skills. Slash commands are available by their Skill names.

### Codex — plugin marketplace

~~~bash
codex plugin marketplace add ccclucky/llm-wiki-agent
codex plugin add cclucky-knowledge-skills@cclucky
~~~

The `agents/openai.yaml` files provide display metadata and explicit invocation policy for Codex.

### Other compatible agents — Skills CLI

~~~bash
npx skills@latest add ccclucky/llm-wiki-agent -g
~~~

Select all eight Skills in the installer, or select only the ones you need. To update a Skills CLI installation, use the CLI's update command and re-run add when you want to pick up newly added Skills.

### WorkBuddy — uploadable Skill packages

Build eight individual ZIP packages:

~~~bash
python scripts/package_workbuddy_skill.py
~~~

The script creates one ZIP per Skill under `dist/`. Upload all eight through **Experts → Skills → Connectors → Skills → Add Skill → Upload Skill**. See [WorkBuddy installation](docs/workbuddy-installation.md).

## Connect Notion MCP separately

Every agent host manages its own Notion MCP connection and authorization. The official remote endpoint is:

~~~text
https://mcp.notion.com/mcp
~~~

1. Add the remote endpoint in the agent's MCP settings.
2. Complete Notion authorization.
3. Grant access to the existing **CCLUCKY Knowledge OS** root page and its Inbox, Rows, Sources, Entities, Concepts, Syntheses, and System areas.
4. Run `/kb-setup` in that agent to verify access.

The agents use separate MCP connections but access the same user's Notion workspace.

**This repository does not provide an MCP server, OAuth implementation, database, backend, or synchronization service.** Do not paste Notion tokens into chat or commit credentials.

See [Agent setup](docs/agent-setup.md).

## Skill source of truth and Notion mirror

There are two distinct sources of truth:

- **GitHub `main` is the only source of truth for Skill instructions, metadata, references, and distribution packages.** Make changes here through pull requests.
- **Notion `System → Knowledge Skills` is a delivery mirror** that exposes the GitHub-sourced Skills to ChatGPT and other agents connected through Notion MCP. Do not independently edit workflow instructions in the Notion copies.
- **Notion `CCLUCKY Knowledge OS` remains the source of truth for personal knowledge data** (Rows, Sources, Entities, Concepts, Syntheses, and System content).

After a Skill change is merged into `main`, sync the affected Skill and its complete `references/` directory to the matching Notion Skill page. Preserve its page identity and enabled settings. Verify it appears in `notion_get_enabled_skills` and can be loaded with `notion_download_skill` before retiring an older copy.

Notion synchronization is deliberately separate from public CI: this repository must never contain Notion credentials, workspace IDs, or personal knowledge exports. See [Notion Skill mirror sync](docs/notion-sync.md).


## How the knowledge workflow works

~~~text
User / Agent
    │
    ├── /kb-ingest ──► Inbox / Rows ──► Sources / Entities / Concepts / Syntheses
    ├── /kb-query  ──► Search canonical knowledge + source evidence
    ├── /kb-update ──► Targeted edits + provenance + history
    ├── /kb-lint   ──► Quality audit (read-only by default)
    └── /kb-graph  ──► Relationship map (read-only by default)
                         │
                         ▼
                Notion-native mentions
                and backlinks where supported
                         │
                         ▼
                CCLUCKY Knowledge OS
~~~

### Knowledge model

| Area | Purpose |
|---|---|
| **Inbox** | User-facing collection workbench |
| **Rows** | Canonical original-material intake database |
| **Sources** | Source summaries, provenance, evidence, and claims |
| **Entities** | People, organizations, products, projects, repositories, and systems |
| **Concepts** | Reusable methods, technical principles, frameworks, and mental models |
| **Syntheses** | Conclusions and comparisons supported by multiple sources |
| **System** | Operating rules, navigation, architecture decisions, and maintenance notes |

Internal relationships use Notion-native page mentions. Plain-text titles and ordinary URL links are not backlinks. A native mention creates an inbound backlink on the mentioned page; verification depends on the operations exposed by the connected MCP client.

Rows statuses are `Pending`, `Processing`, `Processed`, and `Needs Review`. Processing fields are advisory coordination, not an atomic distributed lock.

## Repository structure

~~~text
llm-wiki-agent/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── kb/                         # User-invoked command hub
│   ├── kb-setup/                   # User-invoked connection/workspace check
│   ├── kb-ingest/                  # Model + user invoked
│   ├── kb-query/                   # Model + user invoked
│   ├── kb-update/                  # Model + user invoked
│   ├── kb-lint/                    # Model + user invoked
│   ├── kb-graph/                   # Model + user invoked
│   └── knowledge-context/          # Model-invoked shared context
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
├── scripts/
│   └── package_workbuddy_skill.py
├── docs/
├── tests/
├── AGENTS.md
└── README.md
~~~

Each directory under `skills/` is an independently discoverable Agent Skill with its own `SKILL.md`. The `disable-model-invocation` and `policy.allow_implicit_invocation` settings keep user-invoked commands out of automatic model selection; the model-invoked Skills remain available both explicitly and automatically.

## Validate locally

~~~bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/package_workbuddy_skill.py --output-dir /tmp/cclucky-skill-packages
~~~

CI validates Skill frontmatter, invocation metadata, plugin manifests, reference files, public-repository privacy checks, and WorkBuddy ZIP contents.

A passing CI run does not prove that a particular agent can access a user's Notion workspace. Run the [end-to-end acceptance checklist](docs/notion-ingest-acceptance.md) in each target client.

## Privacy and safety

- Personal knowledge stays in the user's Notion workspace, not in this public repository.
- Each agent owns its own Notion MCP connection and authorization.
- Source content is treated as untrusted data, not executable instructions.
- Query, lint, and graph are read-only by default.
- Ingest and update only write when the user has clearly requested the operation.
- Destructive deletion, merging, and broad restructuring require explicit confirmation.

Never commit Rows content, private wiki exports, workspace-specific Notion IDs, OAuth tokens, API keys, cookies, passwords, or local state.

## License

MIT License — see [LICENSE](LICENSE).
