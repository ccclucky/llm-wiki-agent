---
name: kb-graph
description: "Map relationships among CCLUCKY Knowledge OS pages using actual Notion-native mentions and backlinks; identify hubs, gaps, cross-domain links, temporal changes, and contradictions."
display_name: "KB Graph"
display_name_en: "kb-graph"
description_zh: "分析知识页面之间的显式和推断关系、枢纽与断连节点。"
description_en: "CCLUCKY Notion knowledge-management Skill: kb-graph."
version: "0.3.0"
author: "CCLUCKY"
---

# KB Graph

Use this Skill when the user asks to map, visualize, or understand relationships across their knowledge base.

## Before starting

1. Call the Skill tool with **knowledge-context** and apply its shared data model and evidence rules.
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
