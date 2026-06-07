---
description: Answer a test design or strategy question from the accumulated viewpoints
argument-hint: <target or question>
---

# Test Viewpoint Wiki query

User request:
{{arguments}}

## Purpose

Answer the user question from the accumulated test viewpoints first, to support future test design and test strategy for the same product. Use `raw/` only when the wiki is insufficient or when source verification is necessary. Reflect durable findings back into the wiki.

## No Speculation

- Answer only from what the sources and wiki pages support.
- Do not invent viewpoints, conditions, or coverage claims to make the answer look more complete.
- If the wiki lacks evidence for part of the question, say so and point to which source should be checked or ingested next.

## Answer Requirements

- Start with the direct answer when the evidence supports one.
- Separate `Evidence` from `Unknown / Missing` information when the distinction matters.
- Cite the `wiki/` page or `raw/` source paths that support important statements.
- When proposing viewpoints for a new feature, only reuse viewpoints already supported by source documents, and mark anything beyond that as a gap rather than a fact.

## Filing Rules

- When a query produces a reusable viewpoint that the sources support, file or update it under `wiki/viewpoints/`.
- When a query clarifies a product-specific term, file or update it under `wiki/glossary/`.
- Do not file trivial answers, temporary status checks, or anything not grounded in source evidence.

## Steps

1. Read `index.md` and identify relevant document, viewpoint, and glossary pages.
2. Read the necessary `wiki/` pages. Check `raw/` only when the wiki is incomplete, contradictory, or too vague.
3. Produce the answer with evidence paths and clear markers for unknown or missing information.
4. Decide whether any result should be filed under `wiki/viewpoints/` or `wiki/glossary/`.
5. If filing, create or update the page and update the matching table in `index.md`.
6. If the query reveals missing viewpoints or stale summaries, propose updates to `wiki/documents/` or `wiki/viewpoints/`.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] query | <question>`.
