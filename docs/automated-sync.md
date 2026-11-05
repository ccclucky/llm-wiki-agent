# Legacy local scheduled ingestion

> This document applies only to the optional local/Obsidian mode. It is not part of the default Notion-first multi-agent workflow.

The Notion-first workflow uses one shared RAW database in Notion. Each agent connects through its own Notion MCP and runs the CCLUCKY LLM Wiki Skill. No local cron job or repository synchronization is required for normal use.

## Local mode only

If you explicitly choose the legacy local mode, you may schedule local ingestion of files from a private vault into the repository's local raw/ directory, then run:

~~~bash
python tools/ingest.py raw/path/to/source.md
python tools/heal.py
~~~

Keep the local raw/, wiki/, graph/, logs, and generated output private. They are ignored by Git. Never force-add them to this public repository.

## Credential safety

Do not hardcode API keys or tokens in shell scripts, plist files, cron entries, repository files, or logs. Use an operating-system secret manager or a protected environment injection mechanism. Rotate any credential that has been exposed.

## Recommendation

For shared multi-agent use, do not adapt this local scheduler. Install SKILL.md in each agent and connect each agent to the same Notion workspace through its own Notion MCP connection.