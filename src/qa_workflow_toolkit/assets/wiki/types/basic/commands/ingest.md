---
description: Extract evidence from raw sources and organize it into wiki pages
argument-hint: <target or question>
---

# LLM Wiki ingest

User request:
{{arguments}}

## Purpose

Read primary sources in `raw/`, extract durable knowledge, and organize it into the correct wiki pages while preserving evidence and traceability.

## Page Placement

- `wiki/articles/`: Create or update one source summary page per primary source.
- `wiki/concepts/`: Create or update synthesized pages for reusable concepts, methods, domains, entities, or research areas. Use these only when the content is useful beyond one source.
- `wiki/queries/`: Use only when the ingest is driven by a specific question whose answer should be filed.

## Article Page Shape

Use this minimum structure for new `wiki/articles/` pages:

- `# <Source Title>`
- `## Source`
- `## Summary`
- `## Key Facts`
- `## Claims And Evidence`
- `## Concepts And Entities`
- `## Open Questions`

## Concept Page Shape

Use this minimum structure for new `wiki/concepts/` pages:

- `# <Concept Name>`
- `## Definition`
- `## Evidence`
- `## Related Sources`
- `## Related Concepts`
- `## Open Questions`

## Steps

1. Identify the target source or source set. If no target is specified, inspect `raw/`, `index.md`, and `log.md` to find un-ingested sources.
2. Check whether each source is already represented in `index.md` and whether a matching `wiki/articles/` page exists.
3. Extract source title, author or owner if available, date if available, key facts, claims, entities, concepts, relationships, constraints, and unresolved questions.
4. Create or update the matching `wiki/articles/` page for each source.
5. Create or update `wiki/concepts/` pages only for concepts that are reusable or supported by multiple sources.
6. Update `index.md`: Sources, Article Pages, Concept Pages, and Open Questions as needed.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] ingest | <source>`.
8. Report what changed, which files were touched, and any unresolved issues.

## Guardrails

- Mark content not present in the source as `Inference:`.
- If you find a contradiction, record it as a contradiction instead of overwriting it away.
- For large updates, summarize the changes to the user and wait for confirmation.
- Do not create many thin concept pages. Prefer updating an existing concept page unless a separate page will improve retrieval.
- Do not delete existing wiki content unless it is clearly duplicated or the user asked for cleanup. Mark superseded or contradicted content instead.
