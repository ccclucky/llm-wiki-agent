# Install and connect an agent

The repository is a Skill suite. Each agent installs the Skills, then independently connects its own Notion MCP.

## Choose one installation route per agent

Do not install both the plugin and the Skills CLI copy into the same agent profile.

### Claude Code plugin

~~~bash
claude plugin marketplace add ccclucky/llm-wiki-agent
claude plugin install cclucky-knowledge-skills@cclucky
~~~

### Codex plugin

~~~bash
codex plugin marketplace add ccclucky/llm-wiki-agent
codex plugin add cclucky-knowledge-skills@cclucky
~~~

### Skills CLI for other compatible agents

~~~bash
npx skills@latest add ccclucky/llm-wiki-agent -g
~~~

Select the Skills you want. For a complete experience, install all eight.

### WorkBuddy

Build and upload the eight individual packages. Follow [WorkBuddy installation](workbuddy-installation.md).

## Connect Notion MCP

Configure the agent's own Notion MCP connection in its normal settings.

Official remote endpoint:

~~~text
https://mcp.notion.com/mcp
~~~

Complete Notion authorization and grant access to the existing **CCLUCKY Knowledge OS** root page and its required child pages/databases.

This is a remote MCP endpoint. The agent host connects to it; users normally do not need to launch a local stdio process. The Skills do not configure MCP, manage OAuth, or share credentials between agents. Never paste a Notion token into chat or commit it to this repository.

## Verify

Run `/kb-setup` in the newly configured agent. Verify that it can:
- find CCLUCKY Knowledge OS;
- read Inbox → Rows and inspect the live data-source schema;
- access Sources, Entities, Concepts, Syntheses, and System;
- expose the required read/write operations;
- create Notion-native page mentions;
- inspect backlinks when supported.

Do not create throwaway personal-knowledge records just to test. For a real end-to-end check, use a non-sensitive source the user wants to preserve or a test source explicitly approved by the user, then follow [the acceptance checklist](notion-ingest-acceptance.md).

## Troubleshooting

- **Skills missing:** check that the plugin/Skills CLI install completed and restart or refresh the agent as required.
- **Duplicate commands:** remove either the plugin install or the Skills CLI copy from that agent profile.
- **Workspace missing:** verify Notion MCP authorization and page permissions; do not create a duplicate root.
- **Read works but write fails:** check the integration's edit permissions.
- **Backlinks unavailable:** report the limitation; do not replace native mentions with ordinary text links and claim equivalence.
