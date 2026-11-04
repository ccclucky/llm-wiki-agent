Ingest source material into the shared Notion-backed CCLUCKY LLM Wiki.

Usage: /wiki-ingest $ARGUMENTS

Treat this as an alias for the Ingest workflow in SKILL.md and references/ingest.md.

- $ARGUMENTS may be source text, a URL, an attachment, a local file explicitly supplied by the user, or an existing Inbox record.
- Capture the source in the shared Notion database RAW · 原始资料收件箱 first.
- Then process it into Sources, Entities, Concepts, and (when warranted) Syntheses.
- Use Notion-native page mentions for internal links and validate backlinks when supported.
- Do not use the repository's local raw/ or wiki/ folders unless the user explicitly requests legacy local/Obsidian mode.
- If Notion MCP is unavailable, ask the user to connect it; do not claim completion.