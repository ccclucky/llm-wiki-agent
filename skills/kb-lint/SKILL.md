---
name: kb-lint
description: "Audit the CCLUCKY Knowledge OS for duplicate and orphan pages, broken links, missing provenance, contradictions, stale knowledge, thin hubs, and unprocessed Rows. Use when the user asks to inspect or improve knowledge quality."
display_name: "KB Lint"
display_name_en: "kb-lint"
description_zh: "检查知识库重复、孤立页面、来源缺失、矛盾和待处理资料。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-lint."
version: "0.3.1"
author: "CCLUCKY"
---

# KB Lint

Use this Skill when the user asks to audit, validate, diagnose, or assess knowledge-base quality.

## Before starting

1. Load **knowledge-context** using the host's native Skill mechanism before operating:

   - If the host exposes a Skill tool, call it with `knowledge-context`.
   - If the host uses Notion MCP Skills, find `knowledge-context` in `notion_get_enabled_skills` and load it with `notion_download_skill` using its page ID. If the host already injected it automatically, apply the injected context without downloading it again.
   - If neither mechanism is available, stop and report that the shared context could not be loaded; do not guess the workspace model or safety rules.
2. Read [references/lint.md](references/lint.md).
3. Discover which search, query, page-read, and backlink operations this Notion MCP actually supports.

## Workflow

- Define the audit scope before scanning. If the user does not specify one, start with a bounded audit and state its scope.
- Inspect canonical pages and Rows status fields; do not infer full-workspace coverage from partial search results.
- Classify findings by severity and provide page-level evidence.
- Distinguish genuine defects from legitimate leaf pages or historical records.
- Keep the default run read-only. Suggest repairs but do not delete, merge, or rewrite pages.
- If the user explicitly requests repairs, perform only safe, clearly scoped changes; seek confirmation for destructive or ambiguous changes.

## Output

Provide scope, coverage limitations, severity, affected pages, evidence, suggested repairs, and whether any repair was actually performed.
