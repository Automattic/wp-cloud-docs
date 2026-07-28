from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("docs_tool", ROOT / "tools/docs.py")
assert SPEC and SPEC.loader
docs_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docs_tool)


class DocsToolTests(unittest.TestCase):
    def fixture(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "data").mkdir()
        (root / "content").mkdir()
        skill = root / "skills/write-wp-cloud-docs"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: write-wp-cloud-docs\n---\n\n# Skill\n", encoding="utf-8"
        )
        for reference in docs_tool.SKILL_REFERENCES:
            (skill / reference).write_text("# Reference\n", encoding="utf-8")
        for guidance in docs_tool.PUBLIC_GUIDANCE:
            (root / guidance).parent.mkdir(parents=True, exist_ok=True)
            (root / guidance).write_text("# Guidance\n", encoding="utf-8")
        return root

    def write_catalog(self, root: Path, rows: list[dict[str, str]]) -> None:
        with (root / "data/docs.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=docs_tool.CATALOG_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def row(self, **overrides: str) -> dict[str, str]:
        row = {field: "" for field in docs_tool.CATALOG_FIELDS}
        row.update(
            {
                "key": "doc-example",
                "kind": "article",
                "title": "Example",
                "sidebar_title": "Example",
                "slug": "example",
                "path": "/docs/example/",
                "article_type": "overview",
                "disposition": "maintain",
                "status": "approved",
            }
        )
        row.update(overrides)
        return row

    def test_repository_is_valid(self) -> None:
        result = docs_tool.validate_repository(ROOT)
        self.assertEqual((), result.errors)
        self.assertEqual(120, result.local_count)
        self.assertEqual(2, result.external_count)
        self.assertNotIn("source_keys", docs_tool.CATALOG_FIELDS)

    def test_missing_markdown_fails(self) -> None:
        root = self.fixture()
        self.write_catalog(root, [self.row()])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("missing content/doc-example.md" in error for error in result.errors))

    def test_duplicate_key_fails(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Example\n", encoding="utf-8")
        self.write_catalog(root, [self.row(), self.row(path="/docs/other/")])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("duplicate key doc-example" in error for error in result.errors))

    def test_catalog_rows_with_missing_or_extra_cells_fail_cleanly(self) -> None:
        root = self.fixture()
        header = ",".join(docs_tool.CATALOG_FIELDS)
        for label, row in (
            ("missing", "value"),
            ("extra", ",".join([""] * len(docs_tool.CATALOG_FIELDS)) + ",extra"),
        ):
            with self.subTest(label=label):
                (root / "data/docs.csv").write_text(f"{header}\n{row}\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "row (?:is missing|has extra) cells"):
                    docs_tool.load_catalog(root)

    def test_unknown_parent_and_related_key_fail(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Example\n", encoding="utf-8")
        self.write_catalog(root, [self.row(parent_key="missing-parent", related_keys="missing-related")])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("unknown parent_key missing-parent" in error for error in result.errors))
        self.assertTrue(any("unknown related key missing-related" in error for error in result.errors))

    def test_broken_internal_link_fails(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text(
            "# Example\n\nSee [Missing](/docs/missing/).\n", encoding="utf-8"
        )
        self.write_catalog(root, [self.row()])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("unresolved internal link /docs/missing/" in error for error in result.errors))

    def test_private_marker_fails(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text(
            "# Example\n\nSee private://source.\n", encoding="utf-8"
        )
        self.write_catalog(root, [self.row()])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("contains private marker 'private://'" in error for error in result.errors))

    def test_catalog_private_marker_has_row_and_field_context(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Example\n", encoding="utf-8")
        self.write_catalog(root, [self.row(notes="See github.a8c.com/example.")])
        result = docs_tool.validate_repository(root)
        self.assertTrue(
            any("data/docs.csv:2: doc-example.notes" in error for error in result.errors)
        )

    def test_internal_source_identifier_and_editorial_heading_fail(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text(
            "# Example\n\n## Editorial metadata\n\nSource p2-1234.\n", encoding="utf-8"
        )
        self.write_catalog(root, [self.row()])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("private editorial heading" in error for error in result.errors))
        self.assertTrue(any("internal source identifier" in error for error in result.errors))

    def test_credential_patterns_fail_in_markdown_and_catalog(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text(
            "# Example\n\n-----BEGIN PRIVATE KEY-----\n", encoding="utf-8"
        )
        self.write_catalog(root, [self.row(notes="github_pat_" + "A" * 40)])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("private key block" in error for error in result.errors))
        self.assertTrue(any("GitHub fine-grained token" in error for error in result.errors))

    def test_prohibited_attribution_fails_in_skill_and_guidance(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Example\n", encoding="utf-8")
        self.write_catalog(root, [self.row()])
        skill = root / "skills/write-wp-cloud-docs/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "ASD-" + "STE100\n", encoding="utf-8")
        (root / "README.md").write_text("# Guidance\n\n" + "no-" + "ai-slop\n", encoding="utf-8")
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("prohibited attribution" in error for error in result.errors))
        self.assertTrue(any("README.md" in error for error in result.errors))

    def test_additional_text_file_is_safety_scanned(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Example\n", encoding="utf-8")
        self.write_catalog(root, [self.row()])
        (root / "notes").mkdir()
        (root / "notes/leak.json").write_text('{"url": "private://example"}\n', encoding="utf-8")
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("notes/leak.json" in error for error in result.errors))

    def test_nested_content_file_is_rejected(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Example\n", encoding="utf-8")
        self.write_catalog(root, [self.row()])
        (root / "content/archive").mkdir()
        (root / "content/archive/notes.md").write_text("# Notes\n", encoding="utf-8")
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("unexpected file in content directory" in error for error in result.errors))

    def test_markdown_title_must_match_catalog(self) -> None:
        root = self.fixture()
        (root / "content/doc-example.md").write_text("# Different title\n", encoding="utf-8")
        self.write_catalog(root, [self.row()])
        result = docs_tool.validate_repository(root)
        self.assertTrue(any("does not match catalog title" in error for error in result.errors))

    def test_find_document_supports_key_and_unique_title_text(self) -> None:
        rows = [self.row(), self.row(key="doc-other", title="Other", path="/docs/other/")]
        self.assertEqual("doc-example", docs_tool.find_document(rows, "doc-example")["key"])
        self.assertEqual("doc-other", docs_tool.find_document(rows, "Other")["key"])

    def test_skill_rejects_legacy_dependency(self) -> None:
        root = self.fixture()
        skill = root / "skills/write-wp-cloud-docs/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "data/content-matrix.csv\n", encoding="utf-8")
        errors = docs_tool.validate_skill(root)
        self.assertTrue(any("content-matrix.csv" in error for error in errors))

    def test_skill_carries_partner_client_ownership_model(self) -> None:
        skill_dir = ROOT / "skills/write-wp-cloud-docs"
        package_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(skill_dir.rglob("*"))
            if path.is_file() and path.suffix in {".md", ".yaml"}
        )
        for term in (
            "WP Cloud partner",
            "host partner",
            "client host",
            "host client",
            "partner client",
            "partner host",
            "WordPress-as-a-Service",
            "customer-to-site ownership mapping",
            "downstream access control",
            "downstream billing",
        ):
            with self.subTest(term=term):
                self.assertIn(term, package_text)
        self.assertIn(
            "End customers are not represented in the WP Cloud API and do not have direct access to it.",
            package_text,
        )

    def test_skill_carries_public_style_authority_and_clarity_contract(self) -> None:
        skill_dir = ROOT / "skills/write-wp-cloud-docs"
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        templates_text = (skill_dir / "references/article-templates.md").read_text(encoding="utf-8")
        style_text = (skill_dir / "references/style-guide.md").read_text(encoding="utf-8")
        terminology_text = (skill_dir / "references/terminology.md").read_text(encoding="utf-8")
        review_text = (skill_dir / "references/review-output.md").read_text(encoding="utf-8")

        authority_order = (
            "Current, verified WP Cloud behavior and explicit maintainer decisions.",
            "This bundled terminology, the article templates, and the WP Cloud and Automattic-aligned house style.",
            "The clear-writing rules stated in this guide.",
        )
        positions = [style_text.index(rule) for rule in authority_order]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("Apply the authority order", skill_text)
        self.assertIn("20 words as a review signal", style_text)
        self.assertIn("25 words for a descriptive sentence", style_text)
        self.assertIn("Remove formulaic filler", style_text)
        self.assertIn("make the smallest change", style_text)
        self.assertIn("Preserve a genuine technical contrast", style_text)
        self.assertIn("review signals, not findings by themselves", review_text)
        self.assertIn("Do not score a document or infer whether AI wrote it.", review_text)
        self.assertNotIn("Source keys", templates_text)
        self.assertNotIn("WP Cloud " + "Field Guide", terminology_text)
        for prohibited in docs_tool.PROHIBITED_ATTRIBUTIONS:
            self.assertNotIn(prohibited, (skill_text + style_text + review_text).lower())

    def test_ci_uses_least_privilege_checkout(self) -> None:
        workflow = (ROOT / ".github/workflows/docs-check.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertNotIn("pull_request_target", workflow)


if __name__ == "__main__":
    unittest.main()
