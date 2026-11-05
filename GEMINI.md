# Gemini CLI instructions

The default mode is the shared Notion-backed CCLUCKY LLM Wiki.

Read [SKILL.md](SKILL.md) before handling any wiki task. Follow its intent routing and load the relevant workflow from references/.

Use the connected Notion MCP to access the shared Rows database nested under the Inbox workspace and canonical wiki pages. Do not use local raw/ or wiki/ as a fallback.

Notion MCP connection and authorization are configured by the user in Gemini CLI settings; this repository does not manage them. If the connection is unavailable or lacks permission, explain what is needed and stop.

The Python tools under tools/ remain available only when the user explicitly requests legacy local/Obsidian mode.