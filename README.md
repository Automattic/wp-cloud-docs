# WP Cloud documentation

This repository is the public source for the WP Cloud Markdown documentation corpus. It contains the articles, navigation catalog, contributor guidance, writing skill, and checks used to maintain the documentation.

## Repository contents

- `content/` contains one Markdown file for each local document.
- `data/docs.csv` is the navigation and maintenance catalog. A local row's `key` matches its Markdown filename.
- `skills/write-wp-cloud-docs/` contains the preferred writing and review workflow for documentation agents.
- `tools/docs.py` lists, inspects, relates, and validates documents.
- `tests/` verifies the catalog, corpus, safety boundary, and skill package.

The repository intentionally does not contain internal provenance, private source archives, synchronization tooling, or live-site publication tooling.

## Find a document

List the catalog:

```bash
python3 tools/docs.py list
```

Show one record by key, title text, or documentation path:

```bash
python3 tools/docs.py show doc-api-quick-start
```

Inspect its related records:

```bash
python3 tools/docs.py related doc-api-quick-start
```

## Make a documentation change

Edit the canonical file in `content/`. Update `data/docs.csv` when the title, path, hierarchy, status, risk, related documents, summary, or public maintainer note changes. Keep document keys and filenames stable unless a maintainer explicitly approves an identity change.

For agent-assisted work, use [`skills/write-wp-cloud-docs/SKILL.md`](skills/write-wp-cloud-docs/SKILL.md). The skill is self-contained and works directly with the public corpus and catalog.

Validate the result:

```bash
python3 tools/docs.py check
python3 tools/docs.py check-skill
python3 -m unittest discover -s tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

## License

The documentation, writing skill, tools, and tests are licensed under GPL-2.0-or-later. See [LICENSE](LICENSE).
