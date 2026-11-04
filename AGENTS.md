# Agent instructions

This repository's default workflow is the **Notion-first CCLUCKY LLM Wiki Skill**.

Before any knowledge-base task, read [SKILL.md](SKILL.md) and the relevant file under [references/](references/).

## Default behavior

- Use the connected Notion MCP and the user's shared Notion workspace.
- Follow the RAW → Ingest → Sources / Entities / Concepts / Syntheses workflow.
- Use native Notion page mentions for internal links so Notion can create backlinks.
- Treat Notion as the canonical knowledge store.
- Do not read or write local raw/ or wiki/ as the default workflow.
- Do not ask the user to clone this repository for daily use.
- Do not configure or manage the agent's Notion MCP connection; that is client-specific setup.

If Notion MCP is unavailable or lacks access, stop and explain the connection/permission needed. Never claim that local files were synced to the shared wiki.

## Legacy local mode

The Python tools under tools/ and the local raw/wiki/ layout are retained for users who explicitly request the original local/Obsidian workflow. They are not the default and must not be used as a fallback for shared Notion access. See docs/legacy-local-mode.md.