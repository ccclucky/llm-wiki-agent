# Legacy local / Obsidian mode

The original LLM Wiki Agent was designed around a local Markdown vault. That mode remains available for users who explicitly want a local Obsidian wiki.

It is **not** the default CCLUCKY multi-agent workflow. It does not provide one shared knowledge store across independent agents.

## Layout

- raw/ — local source material
- wiki/ — generated Markdown sources, entities, concepts, syntheses, index, and log
- graph/ — generated graph data and HTML visualization
- tools/ — Python utilities for ingest, query, lint, health, refresh, and graph generation

These directories are local user data and are excluded from Git. Do not force-add their contents to this public repository. The original local workflow schema is preserved at legacy/LOCAL_WIKI_SCHEMA.md; the root agent instruction files now point to the Notion-first Skill.

## Basic commands

From a local clone, after installing the optional dependencies required by the tools:

~~~bash
python tools/ingest.py raw/my-source.md
python tools/query.py "What does the wiki say about this topic?"
python tools/health.py
python tools/lint.py
python tools/build_graph.py --open
~~~

This mode uses local Markdown as its canonical store. The user is responsible for local backups and for keeping the vault private.

## Notion distinction

The legacy publisher in tools/notion_sync.py is a one-way Markdown-to-Notion mirror. It is not bidirectional and must not be confused with the Notion-first Skill.

For the shared multi-agent workflow, install SKILL.md in each agent and connect each agent's own Notion MCP to the same workspace.