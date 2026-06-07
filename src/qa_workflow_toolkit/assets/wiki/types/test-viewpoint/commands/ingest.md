---
description: Summarize source documents and extract reusable test viewpoints into the wiki
argument-hint: <target or question>
---

# Test Viewpoint Wiki ingest

User request:
{{arguments}}

## Purpose

Read source documents in `raw/` (test plans, test design documents, test cases, and similar artifacts), summarize what they say about testing, extract reusable test viewpoints, and record product-specific terms. The accumulated viewpoints are meant to support future test design and test strategy for the same product.

## No Speculation

This is the most important rule of this wiki. Adding non-factual information to test viewpoints is fatal.

- Only write what the source documents state or directly demonstrate.
- A viewpoint must be a generalization of an angle that a real source document describes or verifies. Generalizing is allowed; inventing is not.
- Never add conditions, expected results, requirements, or viewpoints that no source supports.
- When information is missing or ambiguous, record it under Open Questions instead of guessing.

## Page Placement

- `wiki/documents/`: Create or update one summary page per source document.
- `wiki/viewpoints/`: Create or update a viewpoint page when a testing angle is reusable beyond its source, or when multiple sources share it.
- `wiki/glossary/`: Create or update a term page when you learn a product-specific term, feature name, role, state, or convention.

## Document Page Shape

Use this minimum structure for new `wiki/documents/` pages:

- `# <Source Title>`
- `## Source`
- `## Document Type` — for example test plan, test design document, or test case set.
- `## Scope` — the feature, screen, or area the document covers.
- `## What It Says About Testing` — concrete summary of the scope, conditions, expected results, plans, or strategy stated in the source.
- `## Derived Viewpoints` — links to the `wiki/viewpoints/` pages extracted from this source.
- `## Open Questions`

## Viewpoint Page Shape

Use this minimum structure for new `wiki/viewpoints/` pages:

- `# <Viewpoint Name>`
- `## Viewpoint` — the testing angle, stated so it can be reused.
- `## Why It Matters` — only if the source evidence supports it; otherwise omit.
- `## Sources` — the `raw/` documents and `wiki/documents/` pages this viewpoint was generalized from.
- `## Applicability` — where this viewpoint can be reused, stated only as far as evidence allows.
- `## Open Questions`

## Glossary Page Shape

Use this minimum structure for new `wiki/glossary/` pages:

- `# <Term>`
- `## Definition` — as the source uses it.
- `## Source` — where the term appears.

## Steps

1. Identify the target source or source set. If no target is specified, inspect `raw/`, `index.md`, and `log.md` to find un-ingested sources.
2. Check whether each source is already represented in `index.md` and whether a matching `wiki/documents/` page exists.
3. Summarize what each source document says about testing: scope, conditions, expected results, plans, or strategy. Create or update the matching `wiki/documents/` page.
4. Extract reusable test viewpoints by generalizing the angles the source documents describe or verify. Create or update `wiki/viewpoints/` pages only for viewpoints that are reusable or shared across multiple sources.
5. Record product-specific terms into `wiki/glossary/` pages.
6. Update `index.md`: Sources, Document Pages, Viewpoint Pages, Glossary, and Open Questions as needed.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] ingest | <source>`.
8. Report what changed, which files were touched, and any unresolved issues.

## Guardrails

- Do not write any viewpoint, condition, or expected result that the source does not support. When in doubt, leave it out and note it under Open Questions.
- If you find a contradiction between sources, record it as a contradiction instead of overwriting it away.
- For large updates, summarize the changes to the user and wait for confirmation.
- Do not create many thin viewpoint pages. Prefer updating an existing viewpoint page unless a separate page will improve reuse.
- Do not delete existing wiki content unless it is clearly duplicated or the user asked for cleanup. Mark superseded or contradicted content instead.
