#!/usr/bin/env python3
"""Build a WorkBuddy-importable ZIP from the canonical Skill and references."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "cclucky-llm-wiki"


def package_skill(output: Path) -> int:
    skill = ROOT / "SKILL.md"
    references = ROOT / "references"
    if not skill.is_file():
        raise FileNotFoundError(f"Missing Skill entrypoint: {skill}")
    if not references.is_dir():
        raise FileNotFoundError(f"Missing Skill references directory: {references}")

    files = [skill, *sorted(references.rglob("*.md"))]
    if not files[1:]:
        raise RuntimeError("The Skill package must include its reference documents.")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            archive.write(path, f"{PACKAGE_ROOT}/{relative}")

    return len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / "cclucky-llm-wiki-workbuddy.zip",
        help="Output ZIP path (default: dist/cclucky-llm-wiki-workbuddy.zip)",
    )
    args = parser.parse_args()
    count = package_skill(args.output)
    print(f"Created {args.output} with {count} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
