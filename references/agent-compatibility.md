# Agent compatibility

The Skill is the portable instruction layer. Notion MCP is configured separately in each Agent.

- Required Notion capabilities: search/retrieve, create/update pages, append blocks, create native page mentions. Backlink inspection is required before claiming backlinks are verified.
- Install using the client's documented Skill mechanism; there is no universal install command.
- Normal use does not require cloning this repository, Python, a local server, or a local RAW/Wiki copy.
- If an Agent cannot load Skills but supports project instructions, provide a small adapter pointing to this canonical Skill. Do not fork the schema or workflow.
- If capabilities are missing, report the gap; do not silently replace native mentions with ordinary links.
