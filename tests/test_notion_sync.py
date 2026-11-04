import unittest

from tools.notion_sync import (
    markdown_to_blocks,
    page_title,
    rich_text_runs,
    section_for,
    strip_frontmatter,
)


class MarkdownConversionTests(unittest.TestCase):
    def test_frontmatter_is_removed(self):
        source = '---\ntitle: "A Concept"\ntype: concept\n---\n\n# Body\nText'
        self.assertEqual(strip_frontmatter(source), "# Body\nText")

    def test_title_uses_frontmatter_then_filename(self):
        source = '---\ntitle: "Agent Harness"\n---\n\nBody'
        self.assertEqual(page_title("concepts/harness.md", source), "Agent Harness")
        self.assertEqual(page_title("sources/my-paper.md", "Body"), "My Paper")

    def test_section_mapping(self):
        self.assertEqual(section_for("sources/paper.md"), "Sources")
        self.assertEqual(section_for("concepts/agent.md"), "Concepts")
        self.assertEqual(section_for("overview.md"), "System")
        self.assertEqual(section_for("misc/note.md"), "Other")

    def test_markdown_structures(self):
        fence = chr(96) * 3
        source = (
            "---\ntitle: Demo\n---\n"
            "# Heading\n\nA paragraph.\n\n"
            "- first\n- second\n\n"
            "1. one\n2. two\n\n"
            "> a quote\n\n"
            + fence + "python\nprint('hello')\n" + fence + "\n\n---\n"
        )
        blocks = markdown_to_blocks(source)
        types = [block["type"] for block in blocks]
        self.assertIn("heading_1", types)
        self.assertEqual(types.count("bulleted_list_item"), 2)
        self.assertEqual(types.count("numbered_list_item"), 2)
        self.assertIn("quote", types)
        self.assertIn("code", types)
        self.assertIn("divider", types)

    def test_wikilink_resolves_to_notion_page(self):
        runs = rich_text_runs(
            "See [[Agent Harness]] for details.",
            {"agent harness": "1234-5678"},
        )
        linked = [run for run in runs if run["text"].get("link")]
        self.assertEqual(len(linked), 1)
        self.assertEqual(linked[0]["text"]["content"], "Agent Harness")
        self.assertTrue(linked[0]["text"]["link"]["url"].endswith("12345678"))

    def test_unresolved_wikilink_is_preserved_as_text(self):
        runs = rich_text_runs("See [[Missing Page]].", {})
        self.assertEqual("".join(run["text"]["content"] for run in runs), "See [[Missing Page]].")

    def test_long_text_is_split_into_notion_safe_runs(self):
        runs = rich_text_runs("x" * 4501)
        self.assertEqual([len(run["text"]["content"]) for run in runs], [2000, 2000, 501])


if __name__ == "__main__":
    unittest.main()
