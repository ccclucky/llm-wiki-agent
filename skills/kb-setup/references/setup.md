# Agent and workspace setup verification

This is a read-only setup check. It verifies that the current agent can use the existing Notion workspace; it does not configure MCP or create a new workspace.

## Verify the host connection

1. Discover available Notion MCP tools: search, fetch, database/data-source query, schema inspection, create/update, block editing, native mention, and backlink inspection.
2. Confirm the connected account can search and read.
3. Find the exact root page **CCLUCKY Knowledge OS**. If absent, report access/search failure; do not create another root.
4. Find **Inbox** and its nested **Rows** database.
5. Fetch the live Rows schema and compare its properties/statuses with the expected model.
6. Confirm access to **Sources**, **Entities**, **Concepts**, **Syntheses**, and **System**.
7. Determine which read/write/link/backlink capabilities are exposed by this MCP client. Do not test by creating throwaway user data.

## MCP ownership

Each agent host configures and authorizes its own Notion MCP connection. The official remote endpoint is:

`https://mcp.notion.com/mcp`

If no Notion MCP tools are available, instruct the user to connect this endpoint in the agent's own settings and rerun the setup check. Do not ask for a token or attempt to configure the connection through this Skill.

## Report

For each capability, report Available, Unavailable, or Not exposed. Separate verified access from capabilities inferred from tool descriptions. List the exact next action for any blocker.
