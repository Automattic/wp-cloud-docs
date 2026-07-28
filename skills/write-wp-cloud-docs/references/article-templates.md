# WP Cloud article templates

Choose a template by reader intent, not source length or author role. These are decision guides, not mandatory heading lists. Add Requirements, Before you begin, or Verify only when the content needs a distinct section.

## Overview

Use for a feature, behavior, architecture, or boundary.

```markdown
# [Subject]

[Define the subject and its practical outcome or boundary.]

## How [subject] works

[Explain the stable model, actors, states, or data flow.]

## Manage or use [subject]

[Give the main actions or link focused procedures.]
```

The reader should understand what the subject does, where its boundary sits, and where to go next.

## How-to

Use for one known task with a shortest safe path.

```markdown
# [Imperative verb] [task]

[State the result, main effect, and brief prerequisite.]

## [Perform the task]

1. [Imperative step.]
2. [Imperative step with the exact command, request, or label.]
3. [Imperative step.]

[State the expected result when it is not obvious.]
```

Add rollback, alternatives, timing, or failure handling only when the task needs them.

## Tutorial

Use for a guided workflow that teaches choices while producing a result.

```markdown
# [Build or complete the outcome]

[State what the reader will produce, understand, and need before starting.]

## [First stage]

[Explain why the stage matters, then give the steps and expected result.]

## [Next stage]

[Continue the workflow with the relevant choices and evidence.]
```

The reader should finish with both a working result and a usable mental model.

## Recipe

Use for a compact solution to a specific technical condition.

```markdown
# [Imperative task] [condition]

[Name the situation, assumptions, and result.]

## [Apply the solution]

[Provide the minimal configuration or commands.]

## Verify the result

[Include only when verification is a distinct check.]
```

## Reference

Use for facts, fields, values, limits, commands, or compatibility details readers consult selectively.

```markdown
# [Reference subject]

[Define scope and authority.]

## [Lookup group]

[Use a table, list, or focused subsections with exact values.]
```

Keep workflow guidance in contextual articles and endpoint schemas in the generated API reference.

## Troubleshooting

Use for a symptom-led diagnosis and resolution.

```markdown
# Troubleshoot [symptom]

[State the observable symptom and affected scope.]

## Confirm the symptom

[Collect the smallest useful evidence.]

## Check [likely cause]

[Explain the check, interpretation, and safe action.]

## Verify recovery

[Confirm the expected state when a separate recovery check is needed.]
```

Order checks by safety and diagnostic value. Do not assert a cause before evidence supports it.

## Category hub

Use the category name as the H1 and add one short paragraph that defines the category's coverage and boundary. Do not author child lists, procedures, or a table of contents.

## Topic hub

Use the topic name as the H1. Add a concise orientation to the child subjects and the decision that helps a reader choose among them. Keep the hub shorter than the articles it routes to.

## Actor and ownership check

For articles involving the API, account access, site lifecycle, customer workflows, or billing:

- Treat `partner`, `host partner`, `client`, `client host`, `host client`, `partner client`, and `partner host` as equivalent names for the hosting provider that uses WP Cloud.
- Identify the partner, the partner's panel, or the partner's automation as the actor that calls the WP Cloud API.
- If an end customer initiates an action through the partner's product, describe the partner-owned interface or workflow that translates the request into a WP Cloud operation.
- Keep customer identity, customer-to-site ownership mapping, downstream access control, and downstream billing in the partner's systems. Do not invent an end-customer object, account, API key, or direct API access in WP Cloud.
- Preserve exact product, API, interface, contractual, and service-model names even when they use one of the equivalent terms.

## Metadata guidance

In repository mode, maintain the document's row in `data/docs.csv`:

- Stable key and kind.
- Canonical and sidebar titles.
- Slug, path, category, parent, and navigation order.
- Article type, disposition, and editorial status.
- Technical and public-safety review state.
- Related keys, summary, and maintainer notes.

Do not put this metadata in article copy. Do not add a Related documentation section; maintain `related_keys` instead.
