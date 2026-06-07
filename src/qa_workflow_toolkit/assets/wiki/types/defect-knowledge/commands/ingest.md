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
- `wiki/usecases/`: Create or update a usecase page when a defect's reproduction reveals a usage scenario (use case) worth keeping as reusable knowledge, or when multiple defects share the same usage flow.

## Report Page Shape

Use this minimum structure for new `wiki/reports/` pages:

- `# <Defect Title or ID>`
- `## Source`
- `## Summary` — what the defect was, in one or two sentences.
- `## Phenomenon` — the observed symptom or behavior, as the source describes it.
- `## Cause` — the root cause stated or demonstrated by the source. If the source does not state one, write "Unknown (not stated in source)".
- `## Affected Area` — the feature, screen, component, or area involved.
- `## Conditions / Trigger` — how or when the defect occurred, only as far as the source states.
- `## Reproduction Steps` — the steps to reproduce, as the source states them; omit if the source does not provide them.
- `## Resolution` — the fix or countermeasure, only if the source states it; otherwise omit.
- `## Derived Viewpoints` — links to the `wiki/viewpoints/` pages extracted from this defect.
- `## Derived Usecases` — links to the `wiki/usecases/` pages generalized from this defect's reproduction, if any.
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

## Usecase Page Shape

Use this minimum structure for new `wiki/usecases/` pages:

- `# <Usecase Name>`
- `## Usage Scenario` — the actor, goal, and flow the user was performing, generalized only from the reproduction steps and conditions the source defects actually state.
- `## Defect Link` — how this usage scenario relates to the defect(s) that revealed it (for example, the step where the defect occurred).
- `## Sources` — the `raw/` reports and `wiki/reports/` pages this usecase was generalized from.
- `## Related Viewpoints` — links to `wiki/viewpoints/` pages relevant to this scenario, if any.
- `## Open Questions`

## Steps

1. Identify the target source or source set. If no target is specified, inspect `raw/`, `index.md`, and `log.md` to find un-ingested reports.
2. Check whether each source is already represented in `index.md` and whether a matching `wiki/reports/` page exists.
3. Summarize each defect report: phenomenon, cause, affected area, conditions, and reproduction steps. Create or update the matching `wiki/reports/` page. Keep the phenomenon and cause clearly separated, and mark the cause as unknown when the source does not state it.
4. Extract reusable lessons and test viewpoints by generalizing the patterns the defects reveal. Create or update `wiki/viewpoints/` pages only for viewpoints that are reusable or shared across multiple defects.
5. When a defect's reproduction steps or conditions reveal a usage scenario (use case) worth keeping as knowledge, generalize it — the actor, goal, and flow — and create or update a `wiki/usecases/` page. Do this only when the scenario is reusable; otherwise leave it out. Link the usecase from the report's `Derived Usecases` section.
6. Update `index.md`: Sources, Report Pages, Viewpoint Pages, Usecase Pages, and Open Questions as needed.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] ingest | <source>`.
8. Report what changed, which files were touched, and any unresolved issues.

## Guardrails

- Do not write any phenomenon, cause, condition, or lesson that the source does not support. When in doubt, leave it out and note it under Open Questions.
- Never upgrade a guessed cause into a stated one. A symptom without a documented root cause stays "Unknown".
- Derive a usage scenario only by generalizing the reproduction steps and conditions the source states. Do not invent actors, goals, or flow steps that the reproduction does not support. When a defect's reproduction does not reveal a reusable scenario, do not create a usecase page at all.
- If you find a contradiction between reports, record it as a contradiction instead of overwriting it away.
- For large updates, summarize the changes to the user and wait for confirmation.
- Do not create many thin viewpoint or usecase pages. Prefer updating an existing page unless a separate page will improve reuse.
- Do not delete existing wiki content unless it is clearly duplicated or the user asked for cleanup. Mark superseded or contradicted content instead.
