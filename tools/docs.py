#!/usr/bin/env python3
"""Inspect and validate the WP Cloud Markdown documentation repository."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = Path("data/docs.csv")
CONTENT_DIR = Path("content")
SKILL_DIR = Path("skills/write-wp-cloud-docs")

CATALOG_FIELDS = (
    "key",
    "kind",
    "title",
    "sidebar_title",
    "slug",
    "path",
    "external_url",
    "category",
    "parent_key",
    "nav_order",
    "article_type",
    "disposition",
    "status",
    "technical_risk",
    "technical_status",
    "public_safety_status",
    "related_keys",
    "summary",
    "notes",
)
LOCAL_KINDS = {"article", "category_hub", "topic_hub"}
EXTERNAL_KIND = "canonical_external"
DISPOSITIONS = {"maintain", "defer"}
EDITORIAL_STATUSES = {
    "approved",
    "ready_for_review",
    "needs_technical_review",
    "not_started",
    "not_applicable",
}
PRIVATE_MARKERS = (
    "private://",
    "github.a8c.com",
    "wpcloudfieldguide.wordpress.com",
    "/users/",
    "slack.com/archives/",
)
PROHIBITED_ATTRIBUTIONS = (
    "asd-ste100",
    "simplified technical english",
    "no-ai-slop",
    "google developer documentation style guide",
    "ai-like filler",
    "wp cloud field guide",
)
EDITORIAL_HEADINGS = (
    "## Editorial metadata",
    "## Source and shaping notes",
)
INTERNAL_SOURCE_ID = re.compile(r"(?<![A-Za-z0-9])(?:fg|p2)-\d+(?![A-Za-z0-9])", re.IGNORECASE)
CREDENTIAL_PATTERNS = (
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("API secret", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b")),
)
PUBLIC_GUIDANCE = (
    Path("README.md"),
    Path("CONTRIBUTING.md"),
    Path("AGENTS.md"),
    Path("LICENSE"),
    Path(".gitignore"),
    Path(".github/workflows/docs-check.yml"),
)
SKILL_REFERENCES = (
    "references/style-guide.md",
    "references/article-templates.md",
    "references/terminology.md",
    "references/review-output.md",
)
LEGACY_SKILL_REFERENCES = (
    "../../docs/",
    "content-matrix.csv",
    "source-inventory.csv",
    "link-inventory.csv",
    "qa-disposition.csv",
    "migration/pilot",
    "tools/studio_docs.py",
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


class CheckResult(NamedTuple):
    errors: tuple[str, ...]
    catalog_count: int
    local_count: int
    external_count: int

    @property
    def ok(self) -> bool:
        return not self.errors


def split_keys(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def normalize_docs_path(value: str) -> str:
    path = value.split("#", 1)[0].split("?", 1)[0].strip()
    return path.rstrip("/") + "/" if path else ""


def safety_violations(text: str) -> list[str]:
    violations: list[str] = []
    lowered = text.lower()
    for marker in PRIVATE_MARKERS:
        if marker in lowered:
            violations.append(f"private marker {marker!r}")
    for attribution in PROHIBITED_ATTRIBUTIONS:
        if attribution in lowered:
            violations.append(f"prohibited attribution {attribution!r}")
    for heading in EDITORIAL_HEADINGS:
        if heading.lower() in lowered:
            violations.append(f"private editorial heading {heading!r}")
    if match := INTERNAL_SOURCE_ID.search(text):
        violations.append(f"internal source identifier {match.group(0)!r}")
    for label, pattern in CREDENTIAL_PATTERNS:
        if pattern.search(text):
            violations.append(f"credential-shaped value ({label})")
    return violations


def read_utf8_text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def load_catalog(root: Path = ROOT) -> list[dict[str, str]]:
    path = root / CATALOG_PATH
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != CATALOG_FIELDS:
            raise ValueError(
                f"{CATALOG_PATH}: expected fields {', '.join(CATALOG_FIELDS)}"
            )
        rows: list[dict[str, str]] = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"{CATALOG_PATH}:{line_number}: row has extra cells")
            missing = [field for field, value in row.items() if value is None]
            if missing:
                raise ValueError(
                    f"{CATALOG_PATH}:{line_number}: row is missing cells for {', '.join(missing)}"
                )
            rows.append(row)
        return rows


def validate_skill(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skill_dir = root / SKILL_DIR
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_file.relative_to(root)}: missing skill entry point"]

    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "name: write-wp-cloud-docs" not in text:
        errors.append(f"{SKILL_DIR / 'SKILL.md'}: invalid skill frontmatter")

    for relative in SKILL_REFERENCES:
        path = skill_dir / relative
        if not path.is_file():
            errors.append(f"{path.relative_to(root)}: missing bundled reference")

    package_files = [path for path in sorted(skill_dir.rglob("*")) if path.is_file()]
    package_paths = [
        (path, text)
        for path in package_files
        if (text := read_utf8_text(path)) is not None
    ]
    package_text = "\n".join(text for _, text in package_paths).lower()
    for marker in LEGACY_SKILL_REFERENCES:
        if marker.lower() in package_text:
            errors.append(f"{SKILL_DIR}: contains legacy dependency {marker!r}")
    for path, text in package_paths:
        for violation in safety_violations(text):
            errors.append(f"{path.relative_to(root)}: contains {violation}")
    return errors


def validate_guidance(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in PUBLIC_GUIDANCE:
        path = root / relative
        if not path.is_file():
            errors.append(f"{relative}: missing public file")
            continue
        for violation in safety_violations(path.read_text(encoding="utf-8")):
            errors.append(f"{relative}: contains {violation}")
    return errors


def validate_additional_text_files(root: Path = ROOT) -> list[str]:
    """Scan future text files outside the fixed public maintenance surface."""
    errors: list[str] = []
    excluded = {Path("tools/docs.py"), Path("tests/test_docs.py")}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative in excluded or ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        text = read_utf8_text(path)
        if text is None:
            continue
        for violation in safety_violations(text):
            errors.append(f"{relative}: contains {violation}")
    return errors


def validate_repository(root: Path = ROOT) -> CheckResult:
    errors: list[str] = []
    try:
        rows = load_catalog(root)
    except (OSError, ValueError) as error:
        return CheckResult((str(error),), 0, 0, 0)

    by_key: dict[str, dict[str, str]] = {}
    by_path: dict[str, str] = {}
    for line_number, row in enumerate(rows, start=2):
        key = row["key"].strip()
        kind = row["kind"].strip()
        if not key:
            errors.append(f"{CATALOG_PATH}:{line_number}: key is required")
            continue
        if key in by_key:
            errors.append(f"{CATALOG_PATH}:{line_number}: duplicate key {key}")
        else:
            by_key[key] = row
        if kind not in LOCAL_KINDS | {EXTERNAL_KIND}:
            errors.append(f"{key}: unsupported kind {kind!r}")
        if row["disposition"] not in DISPOSITIONS:
            errors.append(f"{key}: unsupported disposition {row['disposition']!r}")
        if row["status"] not in EDITORIAL_STATUSES:
            errors.append(f"{key}: unsupported editorial status {row['status']!r}")
        for field, value in row.items():
            for violation in safety_violations(value):
                errors.append(
                    f"{CATALOG_PATH}:{line_number}: {key or '<missing-key>'}.{field}: contains {violation}"
                )

        docs_path = normalize_docs_path(row["path"])
        if kind in LOCAL_KINDS and not docs_path:
            errors.append(f"{key}: local document path is required")
        if kind in LOCAL_KINDS and not row["summary"].strip():
            errors.append(f"{key}: local document summary is required")
        if kind == EXTERNAL_KIND and not row["external_url"].strip():
            errors.append(f"{key}: external_url is required")
        if docs_path:
            if docs_path in by_path:
                errors.append(
                    f"{key}: duplicate path {docs_path} (also {by_path[docs_path]})"
                )
            else:
                by_path[docs_path] = key

    local_rows = {key: row for key, row in by_key.items() if row["kind"] in LOCAL_KINDS}
    content_dir = root / CONTENT_DIR
    content_files = [path for path in sorted(content_dir.rglob("*")) if path.is_file()]
    files = {path.stem: path for path in content_files if path.parent == content_dir and path.suffix == ".md"}
    for path in content_files:
        if path.parent != content_dir or path.suffix != ".md":
            errors.append(f"{path.relative_to(root)}: unexpected file in content directory")

    for key, row in local_rows.items():
        path = content_dir / f"{key}.md"
        if not path.is_file():
            errors.append(f"{key}: missing {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        match = H1.search(text)
        if not match:
            errors.append(f"{path.relative_to(root)}: missing H1 title")
        elif match.group(1).strip() != row["title"].strip():
            errors.append(
                f"{path.relative_to(root)}: H1 {match.group(1)!r} does not match catalog title {row['title']!r}"
            )
        if row["kind"] == "category_hub" and re.search(r"^##\s+", text, re.MULTILINE):
            errors.append(f"{path.relative_to(root)}: category hub must remain a short orientation")

        for violation in safety_violations(text):
            errors.append(f"{path.relative_to(root)}: contains {violation}")

        for destination in MARKDOWN_LINK.findall(text):
            destination = destination.strip().strip("<>")
            if destination.startswith("/docs/"):
                normalized = normalize_docs_path(destination)
                if normalized not in by_path:
                    errors.append(
                        f"{path.relative_to(root)}: unresolved internal link {destination}"
                    )

    for key, path in files.items():
        if key not in local_rows:
            errors.append(f"{path.relative_to(root)}: no local-document catalog row")

    for key, row in by_key.items():
        parent = row["parent_key"].strip()
        if parent and parent not in by_key:
            errors.append(f"{key}: unknown parent_key {parent}")
        elif row["kind"] == "category_hub" and parent:
            errors.append(f"{key}: category_hub cannot have a parent")
        elif row["kind"] in {"article", "topic_hub"} and not parent:
            errors.append(f"{key}: {row['kind']} requires a parent hub")
        elif row["kind"] == "topic_hub" and parent and by_key[parent]["kind"] != "category_hub":
            errors.append(f"{key}: topic_hub parent {parent} is not a category_hub")
        elif row["kind"] == "article" and parent and by_key[parent]["kind"] not in {
            "category_hub",
            "topic_hub",
        }:
            errors.append(f"{key}: article parent {parent} is not a hub")

        nav_order = row["nav_order"].strip()
        if nav_order and (not nav_order.isdigit() or int(nav_order) < 1):
            errors.append(f"{key}: nav_order must be a positive integer")

        related_keys = split_keys(row["related_keys"])
        if len(related_keys) != len(set(related_keys)):
            errors.append(f"{key}: related_keys contains duplicates")
        for related in related_keys:
            if related not in by_key:
                errors.append(f"{key}: unknown related key {related}")
            if related == key:
                errors.append(f"{key}: cannot relate to itself")

    errors.extend(validate_skill(root))
    errors.extend(validate_guidance(root))
    errors.extend(validate_additional_text_files(root))
    return CheckResult(
        tuple(sorted(set(errors))),
        len(rows),
        len(local_rows),
        sum(row["kind"] == EXTERNAL_KIND for row in rows),
    )


def find_document(rows: list[dict[str, str]], query: str) -> dict[str, str]:
    exact = [row for row in rows if row["key"] == query]
    if exact:
        return exact[0]
    needle = query.casefold()
    matches = [
        row
        for row in rows
        if needle in row["title"].casefold()
        or needle in row["path"].casefold()
        or needle in row["sidebar_title"].casefold()
    ]
    if not matches:
        raise ValueError(f"no document matches {query!r}")
    if len(matches) > 1:
        keys = ", ".join(row["key"] for row in matches[:10])
        raise ValueError(f"{query!r} is ambiguous: {keys}")
    return matches[0]


def print_record(row: dict[str, str]) -> None:
    for field in CATALOG_FIELDS:
        if row[field]:
            print(f"{field}: {row[field]}")


def command_list(rows: list[dict[str, str]], status: str | None) -> None:
    selected = rows if not status else [row for row in rows if row["status"] == status]
    for row in sorted(selected, key=lambda item: (item["path"], item["key"])):
        destination = row["path"] or row["external_url"]
        print(f"{row['key']}\t{row['status']}\t{row['title']}\t{destination}")


def command_related(rows: list[dict[str, str]], query: str) -> None:
    row = find_document(rows, query)
    by_key = {item["key"]: item for item in rows}
    print(f"{row['key']}\t{row['title']}")
    print("related-to")
    for key in split_keys(row["related_keys"]):
        related = by_key[key]
        print(f"{related['key']}\t{related['title']}\t{related['path'] or related['external_url']}")
    print("referenced-by")
    for source in sorted(rows, key=lambda item: item["key"]):
        if row["key"] in split_keys(source["related_keys"]):
            print(f"{source['key']}\t{source['title']}\t{source['path'] or source['external_url']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="validate the catalog, Markdown, links, and skill")
    subparsers.add_parser("check-skill", help="validate the self-contained skill package")
    list_parser = subparsers.add_parser("list", help="list catalog documents")
    list_parser.add_argument("--status", help="filter by exact editorial status")
    show_parser = subparsers.add_parser("show", help="show one catalog record")
    show_parser.add_argument("query", help="document key, title text, or path text")
    related_parser = subparsers.add_parser("related", help="show one document's related records")
    related_parser.add_argument("query", help="document key, title text, or path text")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "check":
        result = validate_repository(ROOT)
        if result.errors:
            for error in result.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(
            f"OK: {result.local_count} Markdown documents and {result.external_count} external destinations "
            f"across {result.catalog_count} catalog rows"
        )
        return 0
    if args.command == "check-skill":
        errors = validate_skill(ROOT)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("OK: write-wp-cloud-docs is self-contained")
        return 0

    try:
        rows = load_catalog(ROOT)
        if args.command == "list":
            command_list(rows, args.status)
        elif args.command == "show":
            print_record(find_document(rows, args.query))
        elif args.command == "related":
            command_related(rows, args.query)
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
