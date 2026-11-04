import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def public_markdown_files():
    """Return public-facing Markdown docs, including nested references and examples."""
    fixed = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "GEMINI.md",
        ROOT / "SKILL.md",
    ]
    discovered = []
    for directory in ("docs", "references", "examples", "legacy"):
        root = ROOT / directory
        if root.exists():
            discovered.extend(root.rglob("*.md"))
    return sorted({path for path in [*fixed, *discovered] if path.is_file()})


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_has_required_fields(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: cclucky-llm-wiki$")
        self.assertRegex(frontmatter, r"(?m)^description: .+")

    def test_workbuddy_frontmatter_has_required_marketplace_metadata(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---", 2)[1]
        for field in (
            "display_name",
            "display_name_en",
            "description_zh",
            "description_en",
            "version",
            "author",
        ):
            with self.subTest(field=field):
                self.assertRegex(frontmatter, rf"(?m)^{field}: .+")

    def test_referenced_workflow_files_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"\]\((references/[^)]+)\)", skill)
        references.extend(re.findall(r"(?m)^@references/(\S+)$", skill))
        self.assertTrue(references)
        for reference in references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

    def test_workbuddy_package_contains_skill_and_all_references(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "cclucky-llm-wiki-workbuddy.zip"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "package_workbuddy_skill.py"),
                    "--output",
                    str(output),
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
            self.assertIn("cclucky-llm-wiki/SKILL.md", names)
            for reference in sorted((ROOT / "references").rglob("*.md")):
                archive_path = (
                    "cclucky-llm-wiki/" + reference.relative_to(ROOT).as_posix()
                )
                with self.subTest(reference=archive_path):
                    self.assertIn(archive_path, names)

    def test_public_docs_contain_no_workspace_ids_or_secrets(self):
        workspace_id_patterns = [
            re.compile(r"(?i)\b[0-9a-f]{32}\b"),
            re.compile(
                r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                r"[0-9a-f]{4}-[0-9a-f]{12}\b"
            ),
        ]
        secret_patterns = [
            re.compile(
                r"(?i)\b(?:ntn|secret|ghp|github_pat|xox[baprs])_"
                r"[A-Za-z0-9_-]{16,}\b"
            ),
            re.compile(r"(?i)\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}\b"),
            re.compile(r"\bAIzaSy[A-Za-z0-9_-]{16,}\b"),
        ]

        for path in public_markdown_files():
            content = path.read_text(encoding="utf-8")
            for pattern in workspace_id_patterns:
                with self.subTest(path=path, pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(content))
            for pattern in secret_patterns:
                with self.subTest(path=path, pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(content))

    def test_legacy_local_schema_is_preserved(self):
        from tools._utils import SCHEMA_FILE

        self.assertTrue(SCHEMA_FILE.is_file())

    def test_local_user_data_is_ignored(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/raw/*", gitignore)
        self.assertIn("/wiki/*", gitignore)
        self.assertIn("/graph/*", gitignore)
        self.assertIn("/dist/", gitignore)


if __name__ == "__main__":
    unittest.main()
