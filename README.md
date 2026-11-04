# LLM Wiki Agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A portable LLM Wiki Skill for Notion-connected agents.** Connect your Agent to your own Notion workspace, install this Skill, then capture material and ask the Agent to ingest it. The Agent maintains sources, entities, concepts, syntheses, and native page-to-page relationships in the shared Notion Wiki.

> Normal use does not require cloning this repository, running a local server, or keeping a local Markdown wiki. Each Agent connects its own Notion MCP integration; this repository provides the shared workflow and knowledge-governance Skill.

## Quick Start — Notion-backed Skill

1. Connect the Agent's Notion MCP integration and authorize the existing Knowledge OS workspace.
2. Install the portable Skill from [SKILL.md](SKILL.md) using the Agent's supported Skill installation method.
3. Follow [the installation and verification guide](docs/skill-installation.md).

Every Agent uses the same Notion workspace and canonical pages. The Skill does not manage OAuth or store credentials.

## Daily Use

Ask naturally:

- "把这篇文章收进我的知识库。"
- "处理 RAW 里这条待处理资料。"
- "结合知识库里 Maintainer 和 Eval 的历史回答。"
- "检查知识库的孤立页面和断链。"

The Skill guides Capture, Ingest, Query, Update, Lint, and Graph workflows. Native Notion page mentions—not plain text titles or ordinary hyperlinks—are required for verified backlinks.

## Skill Structure

- `SKILL.md` — portable entry point and operating rules
- `references/workflows/` — Capture, Ingest, Query, Update, Lint, Graph
- `references/knowledge-schema.md` — RAW / Sources / Entities / Concepts / Syntheses / System
- `references/workspace-setup.md` — one-time per-Agent Notion connection checks
- `references/privacy-provenance.md` — public-repository and data-safety rules
- `scripts/validate_skill.py` — validates the public Skill package without accessing user data

## Legacy Local Wiki Mode

The repository still contains the upstream local Markdown implementation and its Python tools (`raw/`, `wiki/`, `tools/`, and Claude Code slash commands). This is retained for compatibility and upstream development; it is **not** the canonical storage path for the Notion-backed multi-Agent workflow.

Do not put personal RAW material or private Wiki pages in this public repository. Local data paths are ignored by Git where possible. The existing Notion publishing script is a legacy one-way publisher, not the implementation of the new Notion-first Skill workflow.

## Development

Validate the Skill package:

```bash
python scripts/validate_skill.py
```

See [docs/skill-installation.md](docs/skill-installation.md) for setup and capability verification.
