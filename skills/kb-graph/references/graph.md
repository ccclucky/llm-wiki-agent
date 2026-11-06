# Knowledge graph workflow

Build a relationship map from actual canonical Notion pages and native mentions/backlinks.

## Relationship types

- **Explicit:** source-backed native page mention with an explanation.
- **Inferred:** plausible relationship suggested by synthesis; label as inferred and include confidence/reason.
- **Contradictory:** claims conflict; retain both source references.
- **Temporal:** a status or relationship changed over time.

Never write inferred edges as sourced facts. Do not create pages merely because an edge mentions a missing title.

## Process

1. Define the graph scope (a project, topic, entity, or bounded part of the workspace).
2. Discover relevant canonical pages and fetch their content.
3. Inspect native mentions and inbound backlinks where the MCP supports them.
4. Build nodes and typed edges from observed evidence.
5. Identify hubs, isolated/weakly connected pages, cross-domain connections, temporal changes, and contradictions.
6. If the MCP cannot enumerate all pages or backlinks, state that the graph is partial.

## Output

Return:
- key entities and concepts;
- most connected hubs;
- important cross-domain connections;
- isolated pages worth reviewing;
- unresolved/contradictory relationships;
- evidence links and coverage limitations.

A visual graph is optional. A correct, inspectable relationship map is more important than an attractive but incomplete visualization.

## Repair policy

The graph workflow is read-only by default. Do not create pages or links to make a graph look complete. If the user explicitly asks to repair the graph, confirm the scope and use only source-supported links. Ask before destructive or ambiguous changes.
