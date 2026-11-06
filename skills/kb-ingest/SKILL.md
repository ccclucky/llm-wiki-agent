---
name: kb-ingest
description: "Capture material the user wants to preserve into Inbox → Rows, then process it into canonical Sources, Entities, Concepts, and Syntheses. Use when the user asks to save, ingest, capture, or process knowledge."
display_name: "KB Ingest"
display_name_en: "kb-ingest"
description_zh: "将用户明确要求保存的资料写入 Inbox → Rows，并沉淀为规范知识页面。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-ingest."
version: "0.3.2"
author: "CCLUCKY"
---

# KB Ingest

Use this Skill when the user explicitly wants source material or a decision preserved in the CCLUCKY Knowledge OS.

## Before starting

1. Load the locally installed **knowledge-context** Skill through the host's native Skill mechanism (for example, the Skill tool). If the host has already injected it, do not load it again. If it is not installed, stop and ask the user to install it alongside this workflow Skill.
2. Read [references/ingest.md](references/ingest.md).
3. Confirm the connected Notion MCP exposes the operations required for the requested workflow. If a required operation is unavailable, explain the limitation before claiming completion.

## Workflow

- Accept pasted text, a conversation summary the user explicitly asks to preserve, an accessible file, a URL, research, meeting notes, project updates, or decisions.
- For a URL or external document, retrieve the actual source through an available browser/search tool. Never claim to have read inaccessible content.
- Preserve the original material in **Inbox → Rows** before transforming it.
- Search for duplicates and existing canonical pages before creating records.
- Process only the requested source or explicitly requested Pending records. Do not start an unbounded batch.
- Create/update only durable Source, Entity, Concept, or Synthesis pages that add value.
- Use Notion-native page mentions and verify links/backlinks when the MCP supports it.
- Mark a Rows item Processed only after required validation. Otherwise use Needs Review and explain why.

## Completion report

Report the Rows record, pages created/updated, important links, provenance/contradictions, backlink verification status, and final Rows status. Never report success for an incomplete workflow.
