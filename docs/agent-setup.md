# Connect an agent to CCLUCKY LLM Wiki

The repository distributes the Skill. It is not a server and does not need to be cloned for daily use.

## One-time setup per agent

1. Install the **cclucky-llm-wiki** Skill from this repository using the agent's supported Agent Skills installer, or copy the Skill package (SKILL.md plus references/) into that agent's skills directory.
2. Configure that agent's own Notion MCP connection using the agent's normal MCP settings.
3. Use Notion's official remote MCP endpoint: https://mcp.notion.com/mcp
4. Complete OAuth/authorization in that agent and grant access to the **CCLUCKY Knowledge OS** root page, including Inbox, RAW, Sources, Entities, Concepts, Syntheses, and System.
5. Ask the agent to verify it can find and read the RAW database **RAW · 原始资料收件箱** and can create/update pages.

Exact configuration steps differ by client and are intentionally not embedded here. This project does not manage client-specific MCP settings or credentials.

## No repository clone required

After installation, normal use is conversational:
- "把这篇文章沉淀到我的知识库"
- "查询我之前关于 Agent Eval 的记录"
- "更新 Maintainer 项目的知识"
- "检查知识库里的孤立页面和矛盾"

The Skill uses the connected Notion MCP. The user does not need to clone the repository, maintain local Markdown files, or create a separate RAW inbox for each agent.

## Troubleshooting

- **Skill loads but cannot find the workspace:** verify the Notion MCP account and page permissions.
- **Workspace found but RAW missing:** locate the exact RAW database under Inbox; do not create a duplicate without checking with the user.
- **Read works but write fails:** check whether the Notion MCP connection has edit access.
- **Agent has no Notion MCP tools:** configure Notion MCP in that agent first. Do not fall back to local files and claim shared knowledge access.
- **Backlinks cannot be inspected:** native page mentions still create Notion backlinks, but report verification as unavailable rather than claiming it was checked.