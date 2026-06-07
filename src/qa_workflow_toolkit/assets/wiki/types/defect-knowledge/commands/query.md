---
description: Answer a recurrence-prevention or risk-based test question from accumulated defect knowledge
argument-hint: <target or question>
---

# Defect Knowledge Wiki query

User request:
{{arguments}}

## Purpose

Answer the user question from the accumulated defect knowledge first, to support recurrence prevention and risk-based test design for the same product. Use `raw/` only when the wiki is insufficient or when source verification is necessary. Reflect durable findings back into the wiki.

## No Speculation

- Answer only from what the defect reports and wiki pages support.
- Do not invent phenomena, causes, defect patterns, or coverage claims to make the answer look more complete.
- Keep the distinction between phenomenon and documented cause. Do not present an inferred cause as a fact.
- If the wiki lacks evidence for part of the question, say so and point to which source should be checked or ingested next.

## Answer Requirements

- Start with the direct answer when the evidence supports one.
- Separate `Evidence` from `Unknown / Missing` information when the distinction matters.
- Cite the `wiki/` page or `raw/` source paths that support important statements.
- When proposing test viewpoints or risk areas, only reuse lessons already supported by defect reports, and mark anything beyond that as a gap rather than a fact.

## Filing Rules

- When a query produces a reusable recurrence-prevention lesson that the defects support, file or update it under `wiki/viewpoints/`.
- When a query produces a reusable usage scenario (use case) generalized from defect reproduction, file or update it under `wiki/usecases/`.
- When a query surfaces a defect that is not yet summarized, propose a new `wiki/reports/` page or note it for ingest.
- Do not file trivial answers, temporary status checks, or anything not grounded in source evidence.

## Steps

1. Read `index.md` and identify relevant report, viewpoint, and usecase pages.
2. Read the necessary `wiki/` pages. Check `raw/` only when the wiki is incomplete, contradictory, or too vague.
3. Produce the answer with evidence paths and clear markers for unknown or missing information.
4. Decide whether any result should be filed under `wiki/viewpoints/` or `wiki/usecases/`, or recorded as a missing `wiki/reports/` page.
5. If filing, create or update the page and update the matching table in `index.md`.
6. If the query reveals missing lessons or stale report summaries, propose updates to `wiki/reports/` or `wiki/viewpoints/`.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] query | <question>`.
