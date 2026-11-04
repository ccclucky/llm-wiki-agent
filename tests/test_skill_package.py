import re
import unittest
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

    def test_referenced_workflow_files_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"\]\((references/[^)]+)\)", skill)
        self.assertTrue(references)
        for reference in references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

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

    def test_ingest_validates_backlinks_before_marking_processed(self):
        ingest = (ROOT / "references" / "ingest.md").read_text(encoding="utf-8")
        self.assertIn("verify important backlinks", ingest)
        self.assertIn("Status: Processed", ingest)
        self.assertLess(
            ingest.index("verify important backlinks"),
            ingest.index("Status: Processed"),
        )
        self.assertIn("Needs Review", ingest)

    def test_raw_schema_documents_the_shared_status_contract(self):
        schema = (ROOT / "references" / "notion-schema.md").read_text(encoding="utf-8")
        for value in ("Inbox", "Processing", "Processed", "Needs Review"):
            with self.subTest(status=value):
                self.assertIn(value, schema)
        for prop in ("Processing By", "Processing Started At", "Processing Notes",
                     "Ingest Summary", "Processed At", "Content Hash"):
            with self.subTest(property=prop):
                self.assertIn(prop, schema)

    def test_security_documents_non_atomic_processing_claim(self):
        security = (ROOT / "references" / "security-and-concurrency.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("not a guaranteed distributed lock", security)
        self.assertIn("Re-fetch", security)

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
