# Connect an agent to CCLUCKY LLM Wiki

The repository distributes the Skill. It is not a server and does not need to be cloned for daily use.

## 1. Install the Skill

### Claude Code and Codex

~~~bash
npx skills add ccclucky/llm-wiki-agent -g -a claude-code -a codex
~~~

### WorkBuddy

WorkBuddy imports a local Skill package through its UI. Build the package from a clone of this repository:

~~~bash
python scripts/package_workbuddy_skill.py
~~~

Then open **Experts → Skills → Connectors → Skills → Add Skill → Upload Skill** and upload the generated ZIP. See [the WorkBuddy guide](workbuddy-installation.md).

### Other compatible agents

Use the client's documented Skill installation method. If it supports neither the Skills CLI nor package import, copy **SKILL.md** and **references/** into its supported skills directory.

## 2. Connect Notion MCP

Configure the agent's own Notion MCP connection using that agent's normal MCP settings.

Official remote MCP endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

Use the client's supported remote MCP transport, complete Notion authorization, and grant access to the **CCLUCKY Knowledge OS** root page and its required children/databases.

This is a remote MCP endpoint. The agent host connects to it; users normally do not need to launch a local stdio process or install a custom Notion server. The Skill does not configure MCP, manage OAuth, or share credentials between agents. Never paste a Notion token into chat or commit it to this repository.

## 3. Verify access

Ask the agent to verify it can:
- find CCLUCKY Knowledge OS;
- read the Rows database nested under Inbox and its schema;
- create a Rows record;
- read and update pages under Sources, Entities, Concepts, Syntheses, and System;
- create native Notion page mentions;
- inspect backlinks when the client's MCP exposes that operation.

Exact MCP tool names and capabilities differ by client. The Skill instructs the agent to discover the available tools rather than assuming a fixed tool naming scheme.

## 4. Run end-to-end acceptance

Follow [the Notion Ingest acceptance checklist](notion-ingest-acceptance.md) independently in each client. Skill discovery alone is not enough: verify Rows writes, native mentions, backlinks, and status completion through that client's actual Notion MCP connection.

Use a real, non-sensitive source the user wants to preserve, or a test source the user has explicitly approved. Do not create throwaway personal-knowledge records merely to test the connection.

Record per-client results in the private LLM Wiki project page in Notion. Do not commit workspace-specific page IDs, private source content, or client acceptance results to this public repository.

## No repository clone required for daily use

The portable entrypoint across clients is natural language. A single Skill does not guarantee native /ingest or /query slash commands; those aliases are client-specific. After installation, normal use is conversational:
- 把这篇文章沉淀到我的知识库
- 查询我之前记录的某个技术主题
- 更新某个项目的知识
- 检查知识库里的孤立页面和矛盾

## Troubleshooting

- **Skill loads but cannot find the workspace:** verify the Notion MCP account and page permissions.
- **Workspace found but Rows database missing:** locate the exact Rows database nested under the Inbox workbench; do not create a duplicate without checking with the user.
- **Read works but write fails:** check whether the Notion MCP connection has edit access.
- **Agent has no Notion MCP tools:** configure the official remote Notion MCP endpoint in that agent first. Do not fall back to local files and claim shared knowledge access.
- **Backlinks cannot be inspected:** native page mentions still create Notion backlinks, but report verification as unavailable rather than claiming it was checked.
