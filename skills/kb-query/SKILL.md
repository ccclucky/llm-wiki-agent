---
name: kb-query
description: "Search the CCLUCKY Knowledge OS and answer questions using canonical pages, original sources, provenance, and dated evidence. Use when the user asks what their wiki knows or wants an answer grounded in prior knowledge."
display_name: "KB Query"
display_name_en: "kb-query"
description_zh: "检索 CCLUCKY Knowledge OS，基于原始来源和证据回答问题。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-query."
version: "0.3.1"
author: "CCLUCKY"
---

# KB Query

Use this Skill when the user wants to retrieve or reason over knowledge already stored in the CCLUCKY Knowledge OS.

## Before starting

1. Load **knowledge-context** using the host's native Skill mechanism before operating:

   - If the host exposes a Skill tool, call it with `knowledge-context`.
   - If the host uses Notion MCP Skills, find `knowledge-context` in `notion_get_enabled_skills` and load it with `notion_download_skill` using its page ID. If the host already injected it automatically, apply the injected context without downloading it again.
   - If neither mechanism is available, stop and report that the shared context could not be loaded; do not guess the workspace model or safety rules.
2. Read [references/query.md](references/query.md).
3. Confirm the connected Notion MCP exposes search and page-read operations.

## Workflow

- Search canonical knowledge pages first; Rows is the original-material archive, not the default answer layer.
- Resolve aliases and related Entities / Concepts / Syntheses.
- Follow native mentions/backlinks to relevant Sources and original Rows records where needed.
- Prefer primary evidence and relevant dates. Do not treat the most recently edited page as automatically authoritative.
- Separate verified facts, user statements, source claims, analysis, and hypotheses.
- Cite or link the underlying Notion source pages wherever the client supports it.
- Do not write a new Synthesis unless the user asks to preserve the answer.

## Output

Answer the question directly, distinguish evidence from interpretation, identify gaps/conflicts, and link the most relevant source pages. Do not dump entire pages unless requested.
