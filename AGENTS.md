# Repository contributor instructions

This repository distributes one portable, Notion-first Agent Skill.

Before changing the project, read [SKILL.md](SKILL.md) and the relevant files under [references/](references/).

## Scope

- **Runtime entrypoint:** SKILL.md.
- **Runtime procedures:** references/.
- **Packaging:** scripts/ contains only deterministic packaging needed by clients such as WorkBuddy.
- **Documentation:** docs/ contains installation and acceptance guidance; it is not a runtime dependency.
- **External dependency:** each agent host configures and authorizes its own Notion MCP connection.

## Architecture constraints

- Do not add a custom MCP server, OAuth implementation, Notion API backend, database, local wiki engine, or synchronization service.
- Do not add client-specific instructions when the same behavior can be expressed in the portable Skill.
- Do not hardcode workspace-specific Notion page IDs or credentials.
- Do not commit user knowledge, source documents, workspace exports, tokens, or private project data.
- Keep the Skill usable by a new agent that has only this Skill and its own authorized Notion MCP connection.

## Validation

Run:

~~~bash
python -m unittest discover -s tests -v
python scripts/package_workbuddy_skill.py --output /tmp/cclucky-llm-wiki-workbuddy.zip
~~~

The generated package must contain only SKILL.md and the referenced runtime documents.
