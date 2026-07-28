# WP Cloud documentation style guide

Write documentation that is accurate, direct, usable without institutional context, and safe to publish.

## Authority

Use writing guidance in this order:

1. Current, verified WP Cloud behavior and explicit maintainer decisions.
2. This bundled terminology, the article templates, and the WP Cloud and Automattic-aligned house style.
3. The clear-writing rules stated in this guide.

Reader benefit and technical accuracy take priority over mechanical rules. The skill states every adopted rule here and does not require access to an external guide or skill.

## Reader and purpose

- Identify the reader's task or question before choosing a structure.
- Lead with the answer, action, prerequisite, or boundary promised by the title.
- Use one coherent reader intent per article. Split only when a section has its own searchable question, prerequisites, risks, and useful independent outcome.
- State the practical outcome or boundary in the introduction. Avoid marketing openings and history lessons.
- Treat a WP Cloud partner, host partner, client, client host, host client, partner client, and partner host as the same organization. Prefer `partner` in general prose, and use another variant when an API, account boundary, feature, interface, or source calls for it.
- Name the actor when responsibilities differ between the WP Cloud partner or client host, the partner's downstream customer, an end user, and WP Cloud Support.
- In API workflows, make the partner, its panel, or its automation the API actor. An end customer may initiate a request through the partner's product, but the end customer does not have a WP Cloud API identity or direct API access.

## Structure

- Use one H1 title, H2 sections for primary topics, and H3 only when a section needs meaningful subdivision.
- Keep the heading hierarchy accessible. Do not skip heading levels.
- Use sentence case for titles and headings.
- Start procedures with the result and essential prerequisites, then use numbered imperative steps.
- Put an expected state beside the action that creates it. Add a separate verification section only when checking the result is a distinct task.
- Put warnings immediately before the risky action.
- End when the reader's outcome is complete. Do not add routine support or related-document sections.
- Keep list items grammatically parallel and punctuate comparable items consistently.
- Make the text sufficient without an image or video. Give informative images useful alt text and decorative images empty alt text.

Category and topic hubs contain one short orientation paragraph. Their child lists come from navigation metadata, not authored Markdown.

## Accuracy and evidence

- Treat commands, API examples, configuration, limits, availability, security behavior, billing, policy, and support promises as technical claims.
- Treat client-account scope, customer ownership, site ownership mapping, access boundaries, and billing responsibility as technical claims.
- Preserve exact syntax, capitalization, request fields, response values, filenames, and UI labels.
- Use obvious placeholders such as `<site-id>` and `<api-key>` and explain where values come from.
- Link endpoint schemas to the WP Cloud API reference instead of duplicating them.
- Do not guess a replacement for an uncertain term or claim. Preserve the original in the working draft and raise a concrete question.
- Generic WordPress or another hosting product may suggest what to verify; it does not prove WP Cloud behavior.

## Procedures and examples

- State required access, identifiers, tools, starting state, customer impact, and reversibility when they matter.
- Put one instruction in each numbered step unless actions must occur at the same time.
- Put a condition the reader must know before the action it governs.
- Keep commands copyable and separate commands from output.
- Name asynchronous states such as accepted, running, completed, and failed when readers must interpret them.
- Show only the response fields needed for the task and mark truncated output.
- Use callouts sparingly: Warning for harm, Important for a failure-causing prerequisite, Note for relevant context, and Tip for an optional improvement.
- In a warning, name the hazard or consequence and the action that prevents it.

## Links and relationships

- Use descriptive link text.
- Link the first useful mention in a section when a reader may arrive there directly.
- Link maintained content instead of duplicating its explanation.
- Keep contextual links in Markdown and related-document recommendations in catalog metadata.
- Verify URLs and catalog paths; never guess a slug.

## Search and retrieval

- Make each H2 understandable on its own.
- Repeat a specific noun when a pronoun would be ambiguous.
- Put prerequisites and limits in the first sentences of the section they govern.
- Include common reader phrasing near the official term when it improves discovery without keyword stuffing.

## Clear, natural writing

- Use plain American English, active voice, and the serial comma.
- Prefer concrete actors, actions, resources, measurements, states, and results over abstractions.
- Use `you` only when the reader is the actor.
- Use one term for one meaning. Do not alternate among synonyms for variety.
- Prefer direct verbs and simple verb forms. Use passive voice when the actor is unknown or when active voice would change the technical meaning.
- Keep one main idea in a sentence and one topic in a paragraph.
- Use 20 words as a review signal for a procedural instruction and 25 words for a descriptive sentence. These are not pass-or-fail limits. Split a sentence only when doing so improves clarity or action order.
- Prefer periods or lists to semicolons in prose. Do not treat a semicolon in code, a table, a quotation, or exact technical text as a defect.
- Use `must` for a requirement, `can` for ability or permission, `might` for possibility, and `should` for a recommendation.
- Use literal, globally understandable language. Avoid idioms, slang, culture-specific references, and humor that readers may not understand.
- Bold exact interface labels. Use code formatting for commands, code, API fields and values, filenames, and placeholders.
- Spell out zero through nine; use numerals for 10 and above, except in code, versions, status codes, measurements, and interface values.
- Use `log in` and `set up` as verbs; use `login` and `setup` as nouns or adjectives.
- Define an acronym on first use unless the title defines it or the intended reader can reasonably be expected to know it.

Concision removes clutter, not facts needed to act safely. Preserve useful context, procedures, examples, warnings, caveats, limits, and troubleshooting detail.

Remove formulaic filler:

- When editing, make the smallest change that fixes the problem. Keep clear sentences, useful structure, and natural cadence that already fit this house style. Do not polish every paragraph into the same shape.
- Do not pad an introduction, restate a heading, announce what a section will cover, or add a conclusion that repeats the article.
- Do not add generic benefits, excessive transitions, process narration, or headings and lists that do not help the reader complete the task.
- State the supported claim directly. Avoid formulaic contrasts, repeated negative fragments, dramatic reveals, self-answered questions, and setups such as `Here's the thing` or `What most people miss`. Preserve a genuine technical contrast, exclusion, or negative requirement.
- Replace importance claims and superficial analysis with a verified fact, mechanism, consequence, or measurement. Do not invent specificity. Replace unsupported attribution such as `experts agree` or `studies show` with a named public source, or raise a maintainer question outside the article.
- Avoid stacked fragments and repeated sentence or paragraph shapes that create a robotic rhythm. Use a colon for a list, label, quotation, or necessary explanation, not for dramatic effect.
- Do not mention prompts, AI generation, source assembly, or editorial workflow in article copy.
- Rewrite stock phrases such as `delve into`, `navigate the landscape`, `game-changing`, `cutting-edge`, and metaphorical uses of `unlock`. Preserve `unlock` when it is an exact API, UI, or product action.
- Avoid `utilize`, `leverage`, `in order to`, `allows you to`, `simple`, `easy`, `just`, `obviously`, `powerful`, `robust`, `seamless`, `comprehensive`, `click here`, and time-sensitive words such as `new` without a date or version. When one is technically necessary or part of an exact name, preserve it.
- Stop when the reader's outcome is complete. Do not add a recap, generic next steps, a fake-profound closing, or an invitation to explore more.

## Safety

Do not include credentials, private hosts or repositories, internal channels, customer data, partner- or client-specific behavior presented as a platform default, prerelease claims, or unsupported roadmap statements.

Flag changes involving authentication, access, security, APIs, destructive operations, recovery, migrations, billing, policy, platform limits, supported versions, availability, and production troubleshooting for technical or maintainer review.

Keep authoring notes and unresolved questions outside article copy. Do not claim approval or publication status without recorded maintainer evidence.

## Final check

- The title, introduction, and first section agree on the article's purpose.
- The reader can complete the task or understand the boundary without guessing a critical permission, value, state, or warning.
- Partner and client-host terms identify the same organization, and no passage gives a downstream customer a WP Cloud account or API identity.
- The partner's responsibility for customer identity, customer-to-site mapping, downstream access, and downstream billing remains clear when those concerns are relevant.
- Technical claims and examples have appropriate evidence.
- Internal or sensitive material is absent or explicitly flagged outside the article.
- Internal links point to catalog paths and related keys resolve.
- Each H2 remains accurate when retrieved on its own.
- The article reads naturally, contains no formulaic filler or invented jargon, and keeps necessary technical detail.
- A general style preference has not changed an exact WP Cloud term, product fact, maintainer decision, UI label, API field, command, or code example.
