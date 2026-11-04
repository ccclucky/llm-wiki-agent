# Notion setup

This is the first Notion integration milestone for CCLUCKY's fork.

## Current sync model

The initial implementation is deliberately one-way:

- Git-tracked Markdown in wiki/ remains the canonical source of truth.
- Notion is the browsable, searchable presentation layer.
- The sync process creates category pages and mirrors each Markdown page below them.
- Only content blocks previously created by this tool are replaced. Other blocks manually added to a mirrored page are not deleted.
- Remote Notion pages are never automatically deleted when a local Markdown file disappears.

This avoids a premature bidirectional-sync design that could silently overwrite edits or lose knowledge. A later milestone can promote Notion to the canonical store after conflict handling and round-trip fidelity are implemented.

## 1. Create a Notion integration

1. Open the Notion integrations page: https://www.notion.so/profile/integrations
2. Create an internal integration, for example CCLUCKY Knowledge Wiki.
3. Copy its secret. Treat it like a password; never commit it or paste it into an issue.
4. In the new Notion workspace, create a root page named CCLUCKY Knowledge OS.
5. Open that page's menu, choose Connections, and add the integration you created.
6. Copy the root page ID from the page URL. The ID is the 32-character identifier, with or without hyphens.

The integration must be connected to the root page. Merely creating an integration does not grant it access to pages.

## 2. Configure environment variables

Set these variables in the shell where you run the agent:

- NOTION_API_KEY: the internal integration secret.
- NOTION_PARENT_PAGE_ID: the ID of the CCLUCKY Knowledge OS root page.

Example for a temporary shell session:

~~~bash
export NOTION_API_KEY="secret_..."
export NOTION_PARENT_PAGE_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
~~~

Do not put the token in CLAUDE.md, AGENTS.md, source code, or Git. Use your operating system's secret manager or an untracked local environment file for persistent configuration.

## 3. Preview and sync

Run a preview first:

~~~bash
python tools/notion_sync.py --dry-run
~~~

For a small first test, publish only three Markdown pages:

~~~bash
python tools/notion_sync.py --limit 3
~~~

After checking the result in Notion, publish the full wiki:

~~~bash
python tools/notion_sync.py
~~~

Use --force to rebuild all mirrored page contents:

~~~bash
python tools/notion_sync.py --force
~~~

## 4. Page layout

The script creates these category pages below the root page as needed:

- System: index, overview, and activity log
- Sources
- Entities
- Concepts
- Syntheses
- Other

Markdown headings, paragraphs, lists, quotes, code fences, dividers, external Markdown links, and resolvable [[wikilinks]] are converted to Notion blocks or page links.

## 5. State and safety

The local file .notion-sync-state.json maps Markdown paths to Notion page IDs and tracks the content blocks created by this tool. It is excluded from Git.

Keep this file backed up locally. Do not share one state file across different Notion workspaces. The script refuses to use a different root page ID with an existing state file.

The sync is incremental: unchanged Markdown pages are skipped. It does not delete remote pages when local pages are removed. Do not manually edit the mirrored content blocks; edit the Markdown source and sync again. Manually added blocks are preserved.

## Known limitations in this milestone

- One-way Markdown-to-Notion publishing only; Notion edits are not pulled back.
- Markdown tables and complex inline formatting are preserved as readable text but are not fully converted into native Notion table/rich-text structures.
- Remote state is tracked locally; if the local state file is lost, existing pages cannot yet be safely reconciled automatically.
- This integration has not been validated against the user's new workspace until the integration token and root page are configured.

These limitations are intentional and should be addressed before Notion becomes the canonical storage layer.
