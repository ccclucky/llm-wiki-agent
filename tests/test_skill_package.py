import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_has_required_fields(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: cclucky-llm-wiki$")
        self.assertRegex(frontmatter, r"(?m)^description: .+")

    def test_referenced_workflow_files_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"\]\((references/[^)]+)\)", skill)
        self.assertTrue(references)
        for reference in references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

    def test_public_skill_contains_no_workspace_ids_or_secrets(self):
        paths = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
        content = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertIsNone(re.search(r"(?i)\b[0-9a-f]{32}\b", content))
        self.assertIsNone(re.search(r"(?i)(secret_|sk-[a-z0-9]{16,}|AIzaSy[a-z0-9_-]{16,})", content))

    def test_legacy_local_schema_is_preserved(self):
        from tools._utils import SCHEMA_FILE

        self.assertTrue(SCHEMA_FILE.is_file())

    def test_local_user_data_is_ignored(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/raw/*", gitignore)
        self.assertIn("/wiki/*", gitignore)
        self.assertIn("/graph/*", gitignore)


if __name__ == "__main__":
    unittest.main()
