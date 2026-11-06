# Repository contributor instructions

This repository distributes a **suite of independent, composable Notion knowledge Skills**.

Before changing it, inspect the affected Skill's SKILL.md, its local references, and the invocation conventions below.

## Architecture

- Each directory under `skills/` is an independently installable Agent Skill.
- Each Skill has a `SKILL.md`; Codex UI/invocation metadata lives in `agents/openai.yaml`.
- `kb` and `kb-setup` are user-invoked. They must have `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.
- Workflow Skills are model-invoked and may also be invoked explicitly.
- `knowledge-context` is the shared model-invoked context Skill. Workflow Skills must load it through the host's native Skill mechanism before operating; see the cross-host instructions in each workflow Skill.
- Claude/Codex plugin metadata is under `.claude-plugin/`.
- WorkBuddy packages are built individually from each Skill directory.

## Non-negotiable boundaries

- Notion is the source of truth for the user's personal knowledge data.
- GitHub `main` is the sole source of truth for distributable Skill instructions, metadata, and references; Notion's `System → Knowledge Skills` database is only a delivery mirror.
- Each agent host configures and authorizes its own Notion MCP connection.
- Do not add a custom MCP server, OAuth implementation, Notion backend, database, local wiki engine, or sync service.
- Do not hardcode workspace-specific Notion IDs or credentials.
- Do not commit personal knowledge, source content, exports, tokens, or local state.
- Query, lint, and graph stay read-only by default.
- Destructive page deletion, merge, or broad restructuring requires explicit user confirmation.

## Invocation conventions

- User-invoked Skills are reachable only when the human types their command. A user-invoked Skill may call a model-invoked Skill, but must never call another user-invoked Skill.
- Model-invoked Skills may be selected automatically when their descriptions match the task. Keep descriptions specific and include meaningful trigger context.
- Cross-Skill dependencies must explicitly describe how to load the named Skill through the host's native mechanism. Use the Skill tool where available; for Notion MCP-connected agents, use `notion_get_enabled_skills` and `notion_download_skill`. Do not rely on a bare `/skill-name` mention or cross-folder relative links.
- After merging Skill changes to `main`, update the matching Notion mirror page and references. Never edit the Notion copy as an independent source.
- Shared data model and safety rules belong in `knowledge-context`; workflow-specific procedures belong with their owning Skill.

## Validation

~~~bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/package_workbuddy_skill.py --output-dir /tmp/cclucky-skill-packages
~~~

Keep the plugin manifest's Skill paths synchronized with the actual `skills/*/` directories.
