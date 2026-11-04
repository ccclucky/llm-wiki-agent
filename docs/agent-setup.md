# Connect an agent to CCLUCKY LLM Wiki

The repository distributes the Skill. It is not a server and does not need to be cloned for daily use.

## 1. Install the Skill

### Claude Code and Codex

Using the Skills CLI, install the current development branch:

~~~bash
npx skills add https://github.com/ccclucky/llm-wiki-agent/tree/feat/notion-first-agent-skill -g -a claude-code -a codex
~~~

After the branch is merged into main:

~~~bash
npx skills add ccclucky/llm-wiki-agent -g -a claude-code -a codex
~~~

### WorkBuddy

WorkBuddy imports a local Skill package through its UI; do not use the Skills CLI command above for WorkBuddy.

1. Build the package from the repository root:

   ~~~bash
   python scripts/package_workbuddy_skill.py
   ~~~

2. In WorkBuddy, open **Experts → Skills → Connectors → Skills → Add Skill → Upload Skill**.
3. Upload `dist/cclucky-llm-wiki-workbuddy.zip`.
4. Complete WorkBuddy's Skill security check. Review any high-risk warning rather than blindly approving it.
5. Start a new conversation and ask WorkBuddy to invoke **CCLUCKY LLM Wiki**.

The package contains only `SKILL.md` and its referenced `references/` resources. WorkBuddy stores uploaded Skills in the user configuration area for use across projects; project-only Skills can instead live in that project's skills directory. Use the UI import path above so WorkBuddy manages the location.

See [the detailed WorkBuddy guide](workbuddy-installation.md).

### Other compatible agents

Use the client's documented Skill installation method. If it supports neither the Skills CLI nor package import, copy `SKILL.md` and `references/` into its supported skills directory.

## 2. Connect Notion MCP

Configure that agent's own Notion MCP connection using the agent's normal MCP settings.

Official remote MCP endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

Complete OAuth/authorization in that agent and grant access to the **CCLUCKY Knowledge OS** root page, including the Inbox database, Inbox · 使用说明, Sources, Entities, Concepts, Syntheses, and System.

The Skill does not configure MCP, manage OAuth, or share credentials between agents. Never paste a Notion token into chat or commit it to this repository.

## 3. Verify access

Ask the agent to verify it can:
- find CCLUCKY Knowledge OS;
- read the Inbox · 原始资料收件箱 database and its schema;
- create an Inbox record;
- read and update pages under Sources, Entities, Concepts, Syntheses, and System;
- create native Notion page mentions;
- inspect backlinks when the client's MCP exposes that operation.

Exact MCP configuration steps differ by client and are intentionally not embedded here. This project does not manage client-specific MCP settings or credentials.

## 4. Run end-to-end acceptance

Follow [the Notion Ingest acceptance checklist](notion-ingest-acceptance.md) independently in each client. Skill discovery alone is not enough: verify Inbox writes, native mentions, backlinks, and status completion through that client's actual Notion MCP connection.

Use a real, non-sensitive source the user wants to preserve, or a test source the user has explicitly approved. Do not create throwaway personal-knowledge records merely to test the connection.

Record per-client results in the private LLM Wiki project page in Notion. Do not commit workspace-specific page IDs, private source content, or client acceptance results to this public repository.

## No repository clone required for daily use

The portable entrypoint across clients is natural language. A single Skill does not guarantee native /ingest or /query slash commands; those aliases are client-specific. After installation, normal use is conversational:
- "把这篇文章沉淀到我的知识库"
- "查询我之前记录的某个技术主题"
- "更新某个项目的知识"
- "检查知识库里的孤立页面和矛盾"

The Skill uses the connected Notion MCP. The user does not need to clone the repository, maintain local Markdown files, or create a separate Inbox database for each agent.

## Troubleshooting

- **Skill loads but cannot find the workspace:** verify the Notion MCP account and page permissions.
- **Workspace found but Inbox database missing:** locate the exact Inbox database directly under Knowledge OS; do not create a duplicate without checking with the user.
- **Read works but write fails:** check whether the Notion MCP connection has edit access.
- **Agent has no Notion MCP tools:** configure Notion MCP in that agent first. Do not fall back to local files and claim shared knowledge access.
- **Backlinks cannot be inspected:** native page mentions still create Notion backlinks, but report verification as unavailable rather than claiming it was checked.
