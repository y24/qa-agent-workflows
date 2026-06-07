---
description: Summarize defect reports and extract recurrence-prevention viewpoints into the wiki
argument-hint: <target or question>
---

# Defect Knowledge Wiki ingest

User request:
{{arguments}}

## Purpose

Read defect reports in `raw/` (bug reports, incident reports, root-cause analyses, and similar artifacts), summarize each defect into `wiki/reports/`, and extract reusable lessons and test viewpoints into `wiki/viewpoints/`. The accumulated knowledge is meant to prevent recurrence of similar defects and to support risk-based test design for the same product.

## No Speculation

This is the most important rule of this wiki. Adding non-factual information to defect knowledge is fatal.

- Only write what the defect reports state or directly demonstrate.
- Distinguish the phenomenon (what was observed) from the cause (why it happened). Record a cause only when the source states or demonstrates it; otherwise record the cause as unknown.
- A lesson or viewpoint must be a generalization of a pattern that a real defect report reveals. Generalizing is allowed; inventing is not.
- Never add phenomena, causes, conditions, fixes, or lessons that no source supports.
- When information is missing or ambiguous, record it under Open Questions instead of guessing.

## Page Placement

- `wiki/reports/`: Create or update one summary page per defect report.
- `wiki/viewpoints/`: Create or update a viewpoint page when a recurrence-prevention lesson or test angle is reusable beyond its single defect, or when multiple defects share the same underlying pattern.

## Report Page Shape

Use this minimum structure for new `wiki/reports/` pages:

- `# <Defect Title or ID>`
- `## Source`
- `## Summary` — what the defect was, in one or two sentences.
- `## Phenomenon` — the observed symptom or behavior, as the source describes it.
- `## Cause` — the root cause stated or demonstrated by the source. If the source does not state one, write "Unknown (not stated in source)".
- `## Affected Area` — the feature, screen, component, or area involved.
- `## Conditions / Trigger` — how or when the defect occurred, only as far as the source states.
- `## Resolution` — the fix or countermeasure, only if the source states it; otherwise omit.
- `## Derived Viewpoints` — links to the `wiki/viewpoints/` pages extracted from this defect.
- `## Open Questions`

## Viewpoint Page Shape

Use this minimum structure for new `wiki/viewpoints/` pages:

- `# <Lesson or Viewpoint Name>`
- `## Viewpoint` — the test angle or lesson that helps prevent or detect this class of defect, stated so it can be reused.
- `## Defect Pattern` — the class of defect this guards against, generalized from the source defects.
- `## Why It Matters` — only if the source evidence supports it; otherwise omit.
- `## Sources` — the `raw/` reports and `wiki/reports/` pages this viewpoint was generalized from.
- `## Applicability` — where this viewpoint can be reused, stated only as far as evidence allows.
- `## Open Questions`

## Steps

1. Identify the target source or source set. If no target is specified, inspect `raw/`, `index.md`, and `log.md` to find un-ingested reports.
2. Check whether each source is already represented in `index.md` and whether a matching `wiki/reports/` page exists.
3. Summarize each defect report: phenomenon, cause, affected area, and conditions. Create or update the matching `wiki/reports/` page. Keep the phenomenon and cause clearly separated, and mark the cause as unknown when the source does not state it.
4. Extract reusable lessons and test viewpoints by generalizing the patterns the defects reveal. Create or update `wiki/viewpoints/` pages only for viewpoints that are reusable or shared across multiple defects.
5. Update `index.md`: Sources, Report Pages, Viewpoint Pages, and Open Questions as needed.
6. Append an entry to `log.md` in the format `## [YYYY-MM-DD] ingest | <source>`.
7. Report what changed, which files were touched, and any unresolved issues.

## Guardrails

- Do not write any phenomenon, cause, condition, or lesson that the source does not support. When in doubt, leave it out and note it under Open Questions.
- Never upgrade a guessed cause into a stated one. A symptom without a documented root cause stays "Unknown".
- If you find a contradiction between reports, record it as a contradiction instead of overwriting it away.
- For large updates, summarize the changes to the user and wait for confirmation.
- Do not create many thin viewpoint pages. Prefer updating an existing viewpoint page unless a separate page will improve reuse.
- Do not delete existing wiki content unless it is clearly duplicated or the user asked for cleanup. Mark superseded or contradicted content instead.
