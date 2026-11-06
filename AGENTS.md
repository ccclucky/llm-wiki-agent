# Repository contributor instructions

This repository distributes a **suite of independent, composable Notion knowledge Skills**.

Before changing it, inspect the affected Skill's SKILL.md, its local references, and the invocation conventions below.

## Architecture

- Each directory under `skills/` is an independently installable Agent Skill.
- Each Skill has a `SKILL.md`; Codex UI/invocation metadata lives in `agents/openai.yaml`.
- `kb` and `kb-setup` are user-invoked. They must have `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.
- Workflow Skills are model-invoked and may also be invoked explicitly.
- `knowledge-context` is the shared model-invoked context Skill. Workflow Skills call it by name through the Skill tool before operating.
- Claude/Codex plugin metadata is under `.claude-plugin/`.
- WorkBuddy packages are built individually from each Skill directory.

## Non-negotiable boundaries

- Notion is the source of truth.
- Each agent host configures and authorizes its own Notion MCP connection.
- Do not add a custom MCP server, OAuth implementation, Notion backend, database, local wiki engine, or sync service.
- Do not hardcode workspace-specific Notion IDs or credentials.
- Do not commit personal knowledge, source content, exports, tokens, or local state.
- Query, lint, and graph stay read-only by default.
- Destructive page deletion, merge, or broad restructuring requires explicit user confirmation.

## Invocation conventions

- User-invoked Skills are reachable only when the human types their command. A user-invoked Skill may call a model-invoked Skill, but must never call another user-invoked Skill.
- Model-invoked Skills may be selected automatically when their descriptions match the task. Keep descriptions specific and include meaningful trigger context.
- Cross-Skill dependencies must explicitly say to call the Skill tool with the named Skill. Do not rely on a bare `/skill-name` mention or cross-folder relative links.
- Shared data model and safety rules belong in `knowledge-context`; workflow-specific procedures belong with their owning Skill.

## Validation

~~~bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/package_workbuddy_skill.py --output-dir /tmp/cclucky-skill-packages
~~~

Keep the plugin manifest's Skill paths synchronized with the actual `skills/*/` directories.
