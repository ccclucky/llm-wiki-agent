# Legacy one-way Notion publisher

> This document applies only to the optional local/Obsidian workflow. The Notion-first CCLUCKY LLM Wiki Skill does not use this publisher.

## Sync model

- Local Markdown in wiki/ is canonical.
- tools/notion_sync.py publishes a browsable mirror to Notion.
- It creates category pages and mirrors local Markdown pages.
- It tracks the blocks it created and replaces only those blocks.
- It does not pull Notion edits back into Markdown.
- It does not automatically delete remote pages when local files disappear.

Do not use this workflow if Notion is intended to be the canonical knowledge store.

## Setup

1. Create a Notion internal integration.
2. Share the intended root page with that integration.
3. Keep the integration secret outside the repository, in a local secret manager or untracked environment file.
4. Configure NOTION_API_KEY and NOTION_PARENT_PAGE_ID only in the local shell/environment.

Never place tokens in CLAUDE.md, AGENTS.md, source code, prompts, issues, or Git.

## Preview and publish

~~~bash
python tools/notion_sync.py --dry-run
python tools/notion_sync.py --limit 3
python tools/notion_sync.py
~~~

Use the small limit first and inspect the result in Notion before publishing the full local wiki.

## State and limitations

- .notion-sync-state.json is workspace-specific local state and must not be committed or shared.
- Notion edits are not pulled back.
- Local Markdown remains the source of truth in this legacy mode.
- The current Skill's Notion-first workflow is separate and uses each agent's own Notion MCP connection.