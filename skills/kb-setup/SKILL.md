---
name: kb-setup
description: "Verify this agent's existing Notion MCP connection and discover the CCLUCKY Knowledge OS workspace, permissions, and Rows schema. Does not configure MCP or create workspace content."
display_name: "KB Setup"
display_name_en: "kb-setup"
description_zh: "检查当前 Agent 的 Notion MCP 连接、知识库权限和 Rows 数据结构，不负责配置 MCP。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-setup."
version: "0.3.0"
author: "CCLUCKY"
disable-model-invocation: true
---

# KB Setup

Run this only when the user explicitly invokes `/kb-setup`.

## Purpose

Perform a read-only preflight for this agent's connection to the user's existing Notion knowledge base. This is a verification workflow, not an MCP installer or workspace migration.

## Process

1. Inspect the Notion tools available in this agent. Discover search, page fetch, database/data-source query, schema inspection, page creation/update, native mention, and backlink capabilities. Do not assume tool names.
2. Confirm the connected account can search and read Notion pages. Do not ask for tokens or credentials.
3. Find the exact root page **CCLUCKY Knowledge OS**. If absent, report the access/search issue; never create a second root.
4. Find **Inbox** under the root and the **Rows** database nested under Inbox.
5. Read the live Rows database/data-source schema and compare its properties/statuses with the expected model.
6. Check that **Sources**, **Entities**, **Concepts**, **Syntheses**, and **System** are accessible.
7. Check write capability without creating test data: inspect the available tool scopes/permissions. Do not perform a test write unless the user separately requests an end-to-end test and approves the test source.
8. Report each capability as Available, Unavailable, or Not exposed by this MCP client.

## MCP boundary

The agent host owns its own Notion MCP connection and authorization. The official remote endpoint is `https://mcp.notion.com/mcp`.

This Skill does not configure, start, install, authorize, or repair MCP. If no Notion tools are available, tell the user to connect the official remote Notion MCP endpoint in the agent's own settings, then rerun `/kb-setup`.

## Safety

- Read-only by default.
- Do not create, rename, move, delete, or modify Notion pages/databases.
- Do not expose workspace-specific IDs in public output or commit them to this repository.
- Do not fall back to local Markdown or another workspace.
- Do not claim a write or backlink capability was tested if it was only inferred from tool descriptions.

## Output

Provide a concise readiness report:
- MCP connection and authorization visibility;
- Knowledge OS / Inbox / Rows discovery;
- Rows schema compatibility;
- access to each knowledge area;
- available read/write/native-mention/backlink capabilities;
- blockers and the exact next action required.
