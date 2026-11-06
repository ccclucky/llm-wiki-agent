import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
USER_INVOKED = {"kb", "kb-setup"}
EXPECTED_SKILLS = {
    "kb",
    "kb-setup",
    "kb-ingest",
    "kb-query",
    "kb-update",
    "kb-lint",
    "kb-graph",
    "knowledge-context",
}


def skill_dirs():
    return sorted(
        path for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )


def public_markdown_files():
    return sorted(
        path for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "dist" not in path.parts
    )


def frontmatter(path):
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise AssertionError(f"Missing frontmatter: {path}")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise AssertionError(f"Unclosed frontmatter: {path}")
    return parts[1], parts[2]


class SkillSuiteTests(unittest.TestCase):
    def test_expected_independent_skills_exist(self):
        self.assertEqual({path.name for path in skill_dirs()}, EXPECTED_SKILLS)
        self.assertFalse((ROOT / "SKILL.md").exists())

    def test_every_skill_has_valid_identity_and_description(self):
        names = set()
        for directory in skill_dirs():
            metadata, _ = frontmatter(directory / "SKILL.md")
            name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", metadata)
            description = re.search(r"(?m)^description:\s*.+$", metadata)
            with self.subTest(skill=directory.name):
                self.assertIsNotNone(name)
                self.assertEqual(name.group(1), directory.name)
                self.assertIsNotNone(description)
                self.assertNotIn(directory.name, names)
                names.add(directory.name)

    def test_invocation_policy_matches_between_harnesses(self):
        for directory in skill_dirs():
            metadata, _ = frontmatter(directory / "SKILL.md")
            codex = (directory / "agents" / "openai.yaml").read_text(encoding="utf-8")
            user_invoked = directory.name in USER_INVOKED
            with self.subTest(skill=directory.name):
                if user_invoked:
                    self.assertIn("disable-model-invocation: true", metadata)
                    self.assertIn("allow_implicit_invocation: false", codex)
                else:
                    self.assertNotIn("disable-model-invocation: true", metadata)
                    self.assertNotIn("allow_implicit_invocation: false", codex)

    def test_workflow_skills_call_shared_context_skill(self):
        for name in ("kb-ingest", "kb-query", "kb-update", "kb-lint", "kb-graph"):
            content = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertIn("Load the locally installed **knowledge-context** Skill", content)
                self.assertIn("host's native Skill mechanism", content)
                self.assertNotIn("notion_get_enabled_skills", content)
                self.assertNotIn("notion_download_skill", content)

    def test_skills_do_not_depend_on_notion_skill_registry(self):
        for path in public_markdown_files():
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertNotIn("notion_get_enabled_skills", content)
                self.assertNotIn("notion_download_skill", content)
        self.assertFalse((ROOT / "docs/notion-sync.md").exists())

    def test_skill_local_references_exist(self):
        for directory in skill_dirs():
            content = (directory / "SKILL.md").read_text(encoding="utf-8")
            references = re.findall(r"\]\((references/[^)]+)\)", content)
            for reference in references:
                with self.subTest(skill=directory.name, reference=reference):
                    self.assertTrue((directory / reference).is_file())

    def test_plugin_manifests_cover_all_skills(self):
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        expected = {f"./skills/{name}" for name in EXPECTED_SKILLS}
        self.assertEqual(set(plugin["skills"]), expected)
        self.assertEqual(marketplace["plugins"][0]["name"], plugin["name"])

    def test_workbuddy_build_creates_one_standalone_zip_per_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/package_workbuddy_skill.py"),
                    "--output-dir",
                    str(output_dir),
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            archives = sorted(output_dir.glob("*.zip"))
            self.assertEqual(len(archives), len(EXPECTED_SKILLS))
            for archive_path in archives:
                skill_name = archive_path.name.removeprefix("cclucky-").removesuffix("-workbuddy.zip")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                self.assertIn(f"{skill_name}/SKILL.md", names)
                self.assertIn(f"{skill_name}/agents/openai.yaml", names)
                for name in names:
                    self.assertTrue(name.startswith(f"{skill_name}/"))

    def test_workbuddy_build_can_target_one_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/package_workbuddy_skill.py"),
                    "--skill",
                    "kb-ingest",
                    "--output-dir",
                    str(output_dir),
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            archives = list(output_dir.glob("*.zip"))
            self.assertEqual([p.name for p in archives], ["cclucky-kb-ingest-workbuddy.zip"])

    def test_public_markdown_contains_no_workspace_ids_or_secrets(self):
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
            for pattern in workspace_id_patterns + secret_patterns:
                with self.subTest(path=path, pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(content))

    def test_legacy_single_skill_layout_is_removed(self):
        for path in (ROOT / "references", ROOT / "tools", ROOT / "legacy", ROOT / "raw", ROOT / "wiki", ROOT / "graph"):
            with self.subTest(path=path):
                self.assertFalse(path.exists())

    def test_gitignore_covers_local_build_and_secret_artifacts(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", gitignore)
        self.assertIn("/dist/", gitignore)


if __name__ == "__main__":
    unittest.main()
