# Claude Code instructions

The default mode is the shared Notion-backed CCLUCKY LLM Wiki.

Read [SKILL.md](SKILL.md) before handling any wiki task. Follow its intent routing and load the relevant workflow from references/.

The legacy slash commands in .claude/commands/ are compatibility aliases only. They must invoke the Notion-first Skill workflow, not the local raw/wiki file workflow.

Do not assume this repository is the user's knowledge store. Do not use local raw/ or wiki/ unless the user explicitly requests legacy local/Obsidian mode.

Notion MCP connection and authorization are configured by the user in Claude Code settings; this repository does not manage them. If no usable Notion MCP is connected, stop and explain the setup requirement.