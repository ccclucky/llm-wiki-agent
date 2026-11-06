---
name: kb-graph
description: "Map relationships among CCLUCKY Knowledge OS pages using actual Notion-native mentions and backlinks; identify hubs, gaps, cross-domain links, temporal changes, and contradictions."
display_name: "KB Graph"
display_name_en: "kb-graph"
description_zh: "分析知识页面之间的显式和推断关系、枢纽与断连节点。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-graph."
version: "0.3.1"
author: "CCLUCKY"
---

# KB Graph

Use this Skill when the user asks to map, visualize, or understand relationships across their knowledge base.

## Before starting

1. Load **knowledge-context** using the host's native Skill mechanism before operating:

   - If the host exposes a Skill tool, call it with `knowledge-context`.
   - If the host uses Notion MCP Skills, find `knowledge-context` in `notion_get_enabled_skills` and load it with `notion_download_skill` using its page ID. If the host already injected it automatically, apply the injected context without downloading it again.
   - If neither mechanism is available, stop and report that the shared context could not be loaded; do not guess the workspace model or safety rules.
2. Read [references/graph.md](references/graph.md).
3. Discover whether this Notion MCP can inspect inbound backlinks and enumerate relevant pages.

## Workflow

- Build the map from actual canonical pages and native mentions/backlinks.
- Distinguish explicit, inferred, contradictory, and temporal relationships.
- Label inferred relationships with their evidence and confidence; never present them as facts.
- Identify important hubs, isolated pages, and cross-domain connections.
- If the MCP cannot enumerate all pages or backlinks, report the graph as partial.
- Keep the default run read-only. Do not create pages or links simply to make a graph look complete.

## Output

Provide a readable relationship map, key hubs, weakly connected pages, contradictions, evidence links, and coverage limitations. A visual diagram is optional; correctness and traceability take priority.
