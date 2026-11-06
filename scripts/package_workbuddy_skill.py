#!/usr/bin/env python3
"""Build one WorkBuddy-importable ZIP per Agent Skill in skills/."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def discover_skills() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        raise FileNotFoundError(f"Missing Skills directory: {SKILLS_DIR}")
    skills = sorted(
        path for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if not skills:
        raise RuntimeError("No Skills found. Expected skills/<name>/SKILL.md.")
    return skills


def package_skill(skill_dir: Path, output: Path) -> int:
    skill_file = skill_dir / "SKILL.md"
    frontmatter = skill_file.read_text(encoding="utf-8").split("---", 2)
    if len(frontmatter) < 3:
        raise ValueError(f"Missing YAML frontmatter: {skill_file}")
    match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter[1])
    if not match or match.group(1) != skill_dir.name:
        raise ValueError(f"Skill name must match directory: {skill_dir.name}")

    files = [skill_file]
    agents = skill_dir / "agents" / "openai.yaml"
    if agents.is_file():
        files.append(agents)
    references = skill_dir / "references"
    if references.is_dir():
        files.extend(sorted(references.rglob("*")))
    files = [path for path in files if path.is_file()]

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(skill_dir).as_posix()
            archive.write(path, f"{skill_dir.name}/{relative}")
    return len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill",
        help="Build only this Skill directory (e.g. kb-ingest). Defaults to all Skills.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist",
        help="Directory for generated ZIP files (default: dist/).",
    )
    args = parser.parse_args()

    skills = discover_skills()
    if args.skill:
        skills = [path for path in skills if path.name == args.skill]
        if not skills:
            parser.error(f"Unknown Skill '{args.skill}'. Available: "
                         + ", ".join(path.name for path in discover_skills()))

    total_files = 0
    for skill_dir in skills:
        output = args.output_dir / f"cclucky-{skill_dir.name}-workbuddy.zip"
        count = package_skill(skill_dir, output)
        total_files += count
        print(f"Created {output} with {count} files.")

    print(f"Built {len(skills)} Skill package(s), {total_files} files total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
