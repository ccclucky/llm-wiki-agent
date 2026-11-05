# Notion setup

> **Legacy documentation.** These steps configure the old local-Markdown-to-Notion publisher. They are not required for the Notion-first CCLUCKY LLM Wiki Skill.

For normal multi-agent use, each agent connects its own Notion MCP and installs the shared Skill. See [agent-setup.md](agent-setup.md).

The old one-way publisher remains available only for users who explicitly use the legacy local/Obsidian mode. It requires a Notion integration token and root page ID, then runs tools/notion_sync.py. It does not pull Notion edits back, does not provide native bidirectional wiki maintenance, and is not used by the Skill.

See [legacy-notion-publisher.md](legacy-notion-publisher.md) for the preserved legacy setup instructions.