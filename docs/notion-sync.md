# Notion Skill mirror sync

## Ownership

Keep the two systems' responsibilities separate:

- **GitHub `ccclucky/llm-wiki-agent`, branch `main`:** canonical source for Skill names, descriptions, instructions, references, metadata, tests, and distribution packages.
- **Notion `System → Knowledge Skills`:** delivery mirror for Notion AI and agents connected through Notion MCP. Do not treat these pages as an independent editing source.
- **Notion `CCLUCKY Knowledge OS`:** canonical store for the user's personal knowledge. The Skill repository must never contain this data.

## Sync after a GitHub merge

For each changed Skill directory:

1. Read the merged Skill directory from GitHub `main`, including `SKILL.md` and every file under `references/`.
2. Locate the matching page in Notion's **Knowledge Skills** database. Preserve the existing page ID and enabled/automatic-use settings.
3. Replace the Skill body and its supporting files with the exact content from the merged GitHub version. Preserve the `references/` folder structure and relative paths.
4. Update the Notion database's Description property from the Skill frontmatter.
5. Verify the page body, source commit/version metadata, and every reference file.
6. Confirm the Skill appears in `notion_get_enabled_skills` and can be loaded through `notion_download_skill`.
7. Only after verification, disable any superseded Skill copy. Do not delete the old page unless the user explicitly requests deletion.

## Cross-agent behavior

- Each agent host has its own Notion MCP authorization.
- A Skill may be installed locally through the Skills CLI or a client plugin, and separately mirrored into Notion for Notion-connected agents.
- User-invoked behavior and slash-command aliases are client-specific. The Notion mirror must preserve explicit-only intent through its automatic-use setting.
- Workflow Skills must load `knowledge-context` through the host's native mechanism: the Skill tool where available, or `notion_get_enabled_skills` + `notion_download_skill` for Notion MCP-connected agents.

## Verification and failure handling

- A successful GitHub CI run verifies the repository package, not the user's private Notion mirror.
- Never claim a Notion sync succeeded based only on a GitHub commit.
- If a Notion write or file import fails, keep the previous enabled version active and report the exact missing step.
- Do not commit Notion page IDs, signed URLs, workspace IDs, tokens, private source material, or personal knowledge exports to GitHub.

## Current mirror

The current Notion mirror is managed in the user's workspace under **System → Knowledge Skills**. Page IDs are intentionally not recorded in this public repository.
