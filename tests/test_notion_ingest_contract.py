import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class NotionIngestContractTests(unittest.TestCase):
    def test_rows_statuses_match_the_shared_database_contract(self):
        schema = read("skills/knowledge-context/references/notion-schema.md")
        for status in ("Pending", "Processing", "Processed", "Needs Review"):
            with self.subTest(status=status):
                self.assertIn(status, schema)

        for prop in (
            "Name", "Status", "Source Type", "Source URL", "Source Date",
            "Captured By", "Processing By", "Processing Started At",
            "Processing Notes", "Tags", "Ingest Summary", "Processed At",
            "Content Hash",
        ):
            with self.subTest(property=prop):
                self.assertIn(prop, schema)

    def test_original_source_is_captured_before_processing(self):
        ingest = read("skills/kb-ingest/references/ingest.md")
        capture = ingest.index("## 2. Capture into Rows first")
        claim = ingest.index("## 3. Claim the item")
        self.assertLess(capture, claim)
        self.assertIn("Status = Pending", ingest)
        self.assertIn("Set Status = Processing", ingest)
        self.assertIn("original source text in the Rows page body", ingest)

    def test_processed_requires_native_mentions_and_validation(self):
        ingest = read("skills/kb-ingest/references/ingest.md")
        links = ingest.index("## 6. Build native links")
        validate = ingest.index("## 7. Validate and complete")
        self.assertLess(links, validate)
        self.assertIn("Notion-native page mentions", ingest)
        self.assertIn("Verify backlinks", ingest)
        self.assertIn("Status = Processed only if complete; otherwise Needs Review", ingest)
        self.assertIn("Never delete the Rows record", ingest)
        self.assertIn("from the Rows record to its resulting Source page", ingest)

    def test_processing_fields_are_not_a_distributed_lock(self):
        ingest = read("skills/kb-ingest/references/ingest.md")
        safety = read("skills/knowledge-context/references/security-and-concurrency.md")
        self.assertIn("not a perfect distributed lock", ingest)
        self.assertIn("not a guaranteed distributed lock", safety)
        self.assertIn("atomic compare-and-swap", safety)

    def test_acceptance_guide_is_part_of_the_public_suite(self):
        readme = read("README.md")
        guide = ROOT / "docs/notion-ingest-acceptance.md"
        self.assertTrue(guide.is_file())
        self.assertIn("notion-ingest-acceptance.md", readme)
        content = guide.read_text(encoding="utf-8")
        for term in ("Inbox", "Backlinks", "Claude Code", "Codex", "WorkBuddy"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), content.lower())

    def test_public_acceptance_guide_contains_no_workspace_ids_or_tokens(self):
        content = read("docs/notion-ingest-acceptance.md")
        self.assertIsNone(re.search(r"(?i)\b[0-9a-f]{32}\b", content))
        self.assertIsNone(re.search(r"(?i)(secret_|ntn_[a-z0-9]{16,}|ghp_[a-z0-9]{30,})", content))


if __name__ == "__main__":
    unittest.main()
