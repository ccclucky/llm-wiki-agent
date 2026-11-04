# WorkBuddy installation

This guide uses WorkBuddy's documented local Skill import flow. It does not require a custom Connector package because the Skill uses the Notion MCP connection that the user configures in WorkBuddy.

## 1. Build the WorkBuddy Skill package

From a clone of this repository:

~~~bash
python scripts/package_workbuddy_skill.py
~~~

The script creates:

`dist/cclucky-llm-wiki-workbuddy.zip`

The ZIP contains one package root, `cclucky-llm-wiki/`, with:
- `SKILL.md`
- `references/*.md`

The Skill frontmatter includes WorkBuddy's marketplace metadata fields while retaining the standard `name` and `description` fields used by other compatible agents.

## 2. Import it in WorkBuddy

1. Open **Experts → Skills → Connectors → Skills**.
2. Click **Add Skill → Upload Skill**.
3. Select `dist/cclucky-llm-wiki-workbuddy.zip`.
4. Wait for the Skill security check and installation to finish.
5. Start a new conversation and ask: "把这篇文章沉淀到我的知识库" or "检查知识库里的孤立页面和矛盾".

Uploaded or created Skills are stored in WorkBuddy's user configuration directory by default and can be used across projects. If a Skill should be limited to one project, WorkBuddy also supports a project-level skills directory. Prefer UI upload unless you have a client-specific reason to manage the directory manually.

## 3. Connect Notion MCP separately

The Skill does not include a Notion server or credentials. In WorkBuddy, configure a separate Notion MCP connection using its MCP settings and the official remote endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

Use the remote Streamable HTTP connection option if offered, complete the Notion authorization flow, and grant the integration access to the existing **CCLUCKY Knowledge OS** root page and its required children/databases.

WorkBuddy documents support for MCP transports including HTTP/SSE/stdio and for local Skill import. The exact MCP UI fields may vary by client version. Do not paste a Notion token into the Skill, chat, or public repository.

## 4. Verify the integration

In a new WorkBuddy conversation, ask it to:
1. identify the installed CCLUCKY LLM Wiki Skill;
2. find CCLUCKY Knowledge OS and read Agent Context Protocol;
3. locate RAW and read its current schema;
4. confirm it can create/update a RAW page and a Source page;
5. confirm it can create a native Notion page mention and query backlinks.

Then run the [end-to-end acceptance checklist](notion-ingest-acceptance.md) using a real, non-sensitive source the user wants to preserve, or a test source explicitly approved by the user.

A Skill being visible in WorkBuddy does not prove Notion MCP is connected. If read/write, native mention, or backlink operations are unavailable, record the exact limitation in the private LLM Wiki project page and do not claim full acceptance.


## Official WorkBuddy references

- [WorkBuddy Skills: import, storage, security checks](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills)
- [WorkBuddy Open Platform: Skill package structure and frontmatter](https://open.workbuddy.cn/en/docs/skill)
- [WorkBuddy Open Platform: MCP + Skill and Connector formats](https://open.workbuddy.cn/docs/connector)
