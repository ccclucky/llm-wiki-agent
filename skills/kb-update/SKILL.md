---
name: kb-update
description: "Update or correct existing CCLUCKY Knowledge OS pages using new user-provided information or evidence while preserving provenance, history, and related links. Use when the user explicitly asks to update wiki knowledge."
display_name: "KB Update"
display_name_en: "kb-update"
description_zh: "更新已有知识页面，保留来源、历史和关联关系。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-update."
version: "0.3.0"
author: "CCLUCKY"
---

# KB Update

Use this Skill when the user asks to update, correct, supersede, or reconcile existing knowledge.

## Before starting

1. Call the Skill tool with **knowledge-context** and apply its shared workspace, provenance, safety, and concurrency rules.
2. Read [references/update.md](references/update.md).
3. Confirm the connected Notion MCP exposes page read and targeted update operations.

## Workflow

- Find and fetch the canonical page before editing.
- Determine whether the new information adds a fact, changes status, supersedes a decision, or conflicts with existing evidence.
- Preserve history and dates when meaningful; never silently erase a prior decision.
- Attach provenance through a native mention to the supporting Rows or Source page.
- Update related pages only when materially affected.
- Use targeted edits, re-fetch after writing, and verify important links.
- Do not create a duplicate canonical page just because the requested page is hard to find.

## Safety

Do not delete, merge, or broadly restructure pages unless the user explicitly approves the exact change. Never overwrite conflicting claims without preserving both sources and flagging the conflict.

## Completion report

List the canonical pages changed, what changed, provenance added, unresolved conflicts, and verification results.
