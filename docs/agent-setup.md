# Connect an agent to CCLUCKY LLM Wiki

The repository distributes the Skill. It is not a server and does not need to be cloned for daily use.

## One-time setup per agent

### 1. Install the Skill

Using the Skills CLI, install the current development branch:

~~~bash
npx skills add https://github.com/ccclucky/llm-wiki-agent/tree/feat/notion-first-agent-skill -g
~~~

After the branch is merged into main:

~~~bash
npx skills add ccclucky/llm-wiki-agent -g
~~~

You can target supported agents explicitly, for example with -a claude-code or -a codex. For clients not supported by the CLI, copy SKILL.md and references/ into that client's skills directory.

### 2. Connect Notion MCP

Configure that agent's own Notion MCP connection using the agent's normal MCP settings.

Official remote MCP endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

Complete OAuth/authorization in that agent and grant access to the **CCLUCKY Knowledge OS** root page, including Inbox, RAW, Sources, Entities, Concepts, Syntheses, and System.

### 3. Verify access

Ask the agent to verify it can:
- find CCLUCKY Knowledge OS;
- read the RAW database RAW · 原始资料收件箱 and its schema;
- create a RAW record;
- read and update pages under Sources, Entities, Concepts, Syntheses, and System;
- create native Notion page mentions.

Exact MCP configuration steps differ by client and are intentionally not embedded here. This project does not manage client-specific MCP settings or credentials.

### 4. Run end-to-end acceptance

Follow [the Notion Ingest acceptance checklist](notion-ingest-acceptance.md) independently in each client. Skill discovery alone is not enough: verify RAW writes, native mentions, backlinks, and status completion through that client's actual Notion MCP connection.

Use a real, non-sensitive source the user wants to preserve, or a test source the user has explicitly approved. Do not create throwaway personal-knowledge records merely to test the connection.

Record per-client results in the private LLM Wiki project page in Notion. Do not commit workspace-specific page IDs, private source content, or client acceptance results to this public repository.

## No repository clone required

The portable entrypoint across clients is natural language. A single Skill does not guarantee native /ingest or /query slash commands; those aliases are client-specific. After installation, normal use is conversational:
- "把这篇文章沉淀到我的知识库"
- "查询我之前记录的某个技术主题"
- "更新某个项目的知识"
- "检查知识库里的孤立页面和矛盾"

The Skill uses the connected Notion MCP. The user does not need to clone the repository, maintain local Markdown files, or create a separate RAW inbox for each agent.

## Troubleshooting

- **Skill loads but cannot find the workspace:** verify the Notion MCP account and page permissions.
- **Workspace found but RAW missing:** locate the exact RAW database under Inbox; do not create a duplicate without checking with the user.
- **Read works but write fails:** check whether the Notion MCP connection has edit access.
- **Agent has no Notion MCP tools:** configure Notion MCP in that agent first. Do not fall back to local files and claim shared knowledge access.
- **Backlinks cannot be inspected:** native page mentions still create Notion backlinks, but report verification as unavailable rather than claiming it was checked.
