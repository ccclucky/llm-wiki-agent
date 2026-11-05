import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "cclucky-llm-wiki"


def runtime_markdown_files():
    return sorted((ROOT / "references").rglob("*.md"))


def public_markdown_files():
    fixed = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "SKILL.md"]
    discovered = []
    docs = ROOT / "docs"
    if docs.exists():
        discovered.extend(docs.rglob("*.md"))
    discovered.extend(runtime_markdown_files())
    return sorted({path for path in [*fixed, *discovered] if path.is_file()})


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_has_standard_required_fields(self):
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

    def test_all_skill_references_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"\]\((references/[^)]+)\)", skill)
        references.extend(
            reference[1:]
            for reference in re.findall(r"(?m)^(@references/\S+)$", skill)
        )
        self.assertTrue(references)
        for reference in references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

    def test_workbuddy_package_contains_only_runtime_skill_files(self):
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

            expected = {
                f"{PACKAGE_ROOT}/SKILL.md",
                *{
                    f"{PACKAGE_ROOT}/references/{path.relative_to(ROOT / 'references').as_posix()}"
                    for path in runtime_markdown_files()
                },
            }
            self.assertEqual(names, expected)

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

    def test_skill_declares_host_managed_remote_notion_mcp(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("https://mcp.notion.com/mcp", skill)
        self.assertIn("agent host", skill.lower())
        self.assertIn("start, install", skill.lower())
        self.assertIn("does not configure", skill.lower())

    def test_legacy_local_runtime_has_been_removed(self):
        for path in (
            ROOT / "tools",
            ROOT / "legacy",
            ROOT / "raw",
            ROOT / "wiki",
            ROOT / "graph",
            ROOT / "pyproject.toml",
            ROOT / "requirements.txt",
            ROOT / "docs" / "notion-setup.md",
        ):
            with self.subTest(path=path):
                self.assertFalse(path.exists())

    def test_gitignore_covers_only_local_build_and_secret_artifacts(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", gitignore)
        self.assertIn("/dist/", gitignore)
        self.assertNotIn("/raw/*", gitignore)
        self.assertNotIn("/wiki/*", gitignore)


if __name__ == "__main__":
    unittest.main()
