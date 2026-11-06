# WorkBuddy installation

WorkBuddy imports Skills individually. This repository therefore builds one ZIP per Skill rather than one oversized package.

## 1. Build all Skill packages

From a clone of this repository:

~~~bash
python scripts/package_workbuddy_skill.py
~~~

The script creates eight ZIP files under `dist/`, one for each directory under `skills/`.

To build only one:

~~~bash
python scripts/package_workbuddy_skill.py --skill kb-ingest
~~~

To choose another output directory:

~~~bash
python scripts/package_workbuddy_skill.py --output-dir /tmp/cclucky-skill-packages
~~~

Each ZIP contains one package root with:
- `SKILL.md`;
- `agents/openai.yaml` when present;
- that Skill's local `references/` files.

## 2. Import all eight Skills

For the complete suite, repeat the following for each generated ZIP:

1. Open **Experts → Skills → Connectors → Skills**.
2. Click **Add Skill → Upload Skill**.
3. Select one ZIP from `dist/`.
4. Wait for the security check and installation to finish.
5. Repeat until all eight Skills are installed.

Install these names:
- `kb`
- `kb-setup`
- `kb-ingest`
- `kb-query`
- `kb-update`
- `kb-lint`
- `kb-graph`
- `knowledge-context`

The first two are user-invoked commands. Workflow Skills can be invoked explicitly and may also be selected automatically. `knowledge-context` supplies the shared data model and safety rules.

## 3. Connect Notion MCP separately

The Skills do not include a Notion server or credentials. Configure a separate remote MCP connection in WorkBuddy using:

~~~text
https://mcp.notion.com/mcp
~~~

Complete Notion authorization and grant access to the existing **CCLUCKY Knowledge OS** root page and required child pages/databases.

## 4. Verify

In a new conversation:
1. Run `/kb` and confirm the command hub lists all workflows.
2. Run `/kb-setup` and verify workspace access.
3. Ask a knowledge question and confirm `knowledge-context` is available.
4. Use a real, non-sensitive source or an approved test source to verify `/kb-ingest`.
5. Verify query/update/lint/graph behavior within the user's chosen scope.

A Skill being visible does not prove Notion MCP is connected. Record capability gaps; do not claim full acceptance if read/write/native mention/backlink operations are unavailable.
