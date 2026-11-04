# Install CCLUCKY LLM Wiki Skill

Normal users do not need to clone this repository or run its Python tools.

1. Connect that Agent's Notion MCP and authorize access to the existing CCLUCKY Knowledge OS workspace.
2. Install the `cclucky-llm-wiki` Skill from [SKILL.md](../SKILL.md) using the Agent's supported Skill installation method.
3. Ask the Agent to find the Knowledge OS home page, read Agent Context Protocol, identify RAW, and verify it can create native Notion page mentions and inspect backlinks.
4. If RAW is absent, or native mention/backlink capabilities are missing, the Agent must report the gap. Do not consider setup complete.

Use:
- "把这篇文章收进我的知识库。"
- "处理 RAW 里这条待处理资料。"
- "结合知识库里 Maintainer 和 Eval 的历史回答。"
- "检查知识库的孤立页面和断链。"

No local clone, Python environment, or separate server is required for normal use.
