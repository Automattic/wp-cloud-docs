# Contributing

Contributions to WP Cloud documentation are welcome.

## Before editing

1. Find the document with `python3 tools/docs.py list` or `python3 tools/docs.py show <query>`.
2. Read its catalog row and the complete Markdown file.
3. Read directly related documents when the change affects terminology, prerequisites, boundaries, or links.
4. For agent-assisted work, follow `skills/write-wp-cloud-docs/SKILL.md`.

## Editing rules

- Keep the stable document key and filename unless a maintainer approves an identity change.
- Preserve verified technical meaning. Flag sensitive or disputed technical claims for maintainer or subject-matter review.
- Update the catalog when public metadata changes.
- Use `/docs/.../` links only for paths present in the catalog.
- Do not add credentials, customer data, nonpublic URLs, internal operations, provenance notes, or editorial metadata.
- Do not change publication status or claim review approval without recorded maintainer evidence.

## Validate the change

Run:

```bash
python3 tools/docs.py check
python3 tools/docs.py check-skill
python3 -m unittest discover -s tests
```

Open a pull request that explains the reader outcome, identifies any catalog changes, and calls out technical claims that need specialist review.

Repository synchronization and live-site publication are maintained separately and are not part of a documentation contribution.
