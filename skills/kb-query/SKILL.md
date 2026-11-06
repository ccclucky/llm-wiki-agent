---
name: kb-query
description: "Search the CCLUCKY Knowledge OS and answer questions using canonical pages, original sources, provenance, and dated evidence. Use when the user asks what their wiki knows or wants an answer grounded in prior knowledge."
display_name: "KB Query"
display_name_en: "kb-query"
description_zh: "检索 CCLUCKY Knowledge OS，基于原始来源和证据回答问题。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-query."
version: "0.3.2"
author: "CCLUCKY"
---

# KB Query

Use this Skill when the user wants to retrieve or reason over knowledge already stored in the CCLUCKY Knowledge OS.

## Before starting

1. Load the locally installed **knowledge-context** Skill through the host's native Skill mechanism (for example, the Skill tool). If the host has already injected it, do not load it again. If it is not installed, stop and ask the user to install it alongside this workflow Skill.
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
