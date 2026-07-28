---
name: write-wp-cloud-docs
description: Draft, edit, restructure, or review WP Cloud documentation in Markdown. Applies the bundled WP Cloud writing standards with or without the maintenance repository. Does not publish or synchronize content.
---

# Write WP Cloud documentation

Produce accurate, useful WP Cloud documentation in Markdown. Maintainers remain responsible for publication decisions, and subject-matter reviewers remain responsible for sensitive technical claims.

## Load the writing system

Read these bundled references before writing:

- `references/style-guide.md`
- `references/article-templates.md`
- `references/terminology.md`

Apply the authority order in `references/style-guide.md`. Do not let general writing guidance override verified WP Cloud behavior, maintainer decisions, bundled terminology and templates, or the WP Cloud and Automattic-aligned house style.

Read `references/review-output.md` when the request is a review or when an edit introduces a disputed claim, substantive removal, or unresolved maintainer question.

## Detect the working context

Use repository mode when the current workspace contains both `data/docs.csv` and `content/`:

1. Identify the document by key, title, path, or filename.
2. Read its row in `data/docs.csv` and its canonical Markdown file in `content/`.
3. Read directly related documents when the change affects boundaries, prerequisites, terminology, or links. Do not load the whole corpus.
4. Preserve existing approved corrections and technical meaning.

Use standalone mode when those repository files are unavailable:

1. Use the draft, source material, product facts, and intended reader supplied by the user.
2. State which essential context is missing when it prevents an accurate result.
3. Do not invent repository metadata, product behavior, commands, limits, UI labels, or support policy.

The skill must not require WordPress, Studio, a live site, migration exports, or private source archives.

## Select the mode

- `draft`: Create a new article from supplied, verified context.
- `edit`: Improve an existing article without changing its core reader intent or technical meaning.
- `restructure`: Apply an approved split, merge, move, or taxonomy change.
- `review`: Report material problems without rewriting unless asked.

Infer the mode from the request. Ask only when the choice changes the target document, public meaning, or approved taxonomy.

## Write from evidence

- For an edit, start from the complete canonical Markdown article.
- For a draft, use the complete source set the user assigns. If no authoritative source exists, separate verified facts from open questions.
- For a restructure, account for every useful procedure, example, warning, caveat, and troubleshooting detail across the affected documents.
- Preserve an existing technical claim unless current evidence or a maintainer establishes that it is wrong. Lack of fresh corroboration alone is not a removal reason.
- Never turn generic WordPress or WordPress.com behavior into WP Cloud behavior without WP Cloud evidence.

## Apply terminology and ownership

- Treat `WP Cloud partner`, `partner`, `host partner`, `client`, `client host`, `host client`, `partner client`, and `partner host` as names for the same organization: a hosting provider that uses WP Cloud. Do not present them as separate actors or account types.
- Prefer `WP Cloud partner` or `partner` in general prose. Use another partner, client, or host variant when it matches an API field, account boundary, feature, interface, or source term, or when it helps readers recognize the terminology. Establish the equivalence on the first useful mention when an article uses more than one variant.
- Qualify `client` when it could mean an HTTP or API client. Use `WP Cloud client`, `client host`, `API integration`, `requesting application`, or another precise actor. Do not use `client` for the partner's downstream customer.
- Describe WP Cloud as a cloud infrastructure platform specialized in WordPress hosting that provides WordPress-as-a-Service for client-host-level operations. WP Cloud models client accounts and sites, not a partner's end customers.
- Describe the WP Cloud API and its API keys as operating on sites in the partner's client account, subject to the access restrictions configured for each key. Never imply that an end customer has a WP Cloud API identity, API key, or direct API access.
- Assign end-customer identity, customer-to-site ownership mapping, downstream access control, and downstream billing to the partner and the partner's own systems, panels, and workflows.
- When editing an existing article, correct conflicting role or ownership language throughout the affected article. Preserve exact product names such as `WP Cloud Partner Portal` and `Client SSH`, current API terms, contractual labels, and service-model names.

## Maintain repository relationships

In repository mode:

- Keep the stable document key and filename unless the user explicitly changes identity.
- Update `data/docs.csv` when title, path, hierarchy, status, risk, related documents, summary, or maintainer notes change.
- Treat `related_keys` as metadata. Do not add a `Related documentation` section to article copy.
- Use same-site `/docs/.../` links only for paths present in the catalog.
- Run `python3 tools/docs.py check` after changes.

Do not change taxonomy or document relationships silently. Explain any required metadata change with the article result.

## Protect technical and sensitive content

Flag new, changed, or disputed claims involving API behavior, authentication, security, credentials, access, destructive or recovery operations, platform limits, policy, billing, production-impacting commands, or support commitments.

Never include private links, credentials, customer data, internal operations, partner- or client-specific details presented as platform defaults, or editorial notes in article copy. Use obvious placeholders in examples.

Do not claim that a document passed technical, maintainer, legal, security, or publication review unless the supplied context records that approval.

## Produce the result

For `draft`, `edit`, or `restructure`, return:

1. The complete Markdown article or the applied repository changes.
2. Any necessary catalog changes.
3. A short list of unresolved technical or maintainer decisions, if any.

For `review`, return only material findings: factual contradictions, source loss, unsafe claims, broken instructions or links, incomplete reader outcomes, and metadata or relationship errors. Omit routine style preferences.

Do not publish, import, synchronize, or change a site. Those actions require a separate workflow and explicit authorization for the exact destination and scope.
