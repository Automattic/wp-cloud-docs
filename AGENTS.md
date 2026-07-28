# Agent guidance

Use `skills/write-wp-cloud-docs/SKILL.md` for drafting, editing, restructuring, or reviewing WP Cloud documentation.

Work directly with the shared repository files:

- Canonical articles: `content/<document-key>.md`
- Navigation and public metadata: `data/docs.csv`
- Writing rules and terminology: `skills/write-wp-cloud-docs/references/`

Start with the smallest useful context:

```bash
python3 tools/docs.py list
python3 tools/docs.py show <key-or-title>
python3 tools/docs.py related <key-or-title>
```

After changes, run:

```bash
python3 tools/docs.py check
python3 tools/docs.py check-skill
python3 -m unittest discover -s tests
```

Do not publish, import, synchronize, push, or change a live site unless the user separately authorizes that exact action and destination. Never invent technical facts, approval state, catalog metadata, or private provenance.
