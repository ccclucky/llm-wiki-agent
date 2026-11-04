#!/usr/bin/env python3
"""Validate the public Skill package without accessing user data."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "references/workspace-setup.md",
    "references/knowledge-schema.md",
    "references/privacy-provenance.md",
    "references/agent-compatibility.md",
    "references/workflows/capture.md",
    "references/workflows/ingest.md",
    "references/workflows/query.md",
    "references/workflows/update.md",
    "references/workflows/lint-graph.md",
]

def main():
    errors = []
    for item in REQUIRED:
        path = ROOT / item
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append(f"Missing or empty: {item}")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or not re.search(r"(?m)^name:\s*cclucky-llm-wiki$", skill):
        errors.append("Invalid Skill frontmatter/name")
    for item in REQUIRED[1:]:
        if item not in skill:
            errors.append(f"SKILL.md missing reference: {item}")
    forbidden = re.compile(r"(?i)(ntn_[A-Za-z0-9]{20,}|secret_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,})")
    for item in REQUIRED:
        path = ROOT / item
        if path.exists() and forbidden.search(path.read_text(encoding="utf-8")):
            errors.append(f"Possible credential in {item}")
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors))
        return 1
    print(f"Skill package valid: {len(REQUIRED)} files checked.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
