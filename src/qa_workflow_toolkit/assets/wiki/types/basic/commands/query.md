---
description: Answer a question from the wiki and optionally file the result
argument-hint: <target or question>
---

# LLM Wiki query

User request:
{{arguments}}

## Purpose

Answer the user question from existing wiki knowledge first. Use `raw/` only when the wiki is insufficient or when source verification is necessary. Preserve reusable answers under `wiki/queries/` when they would help future agents.

## Answer Requirements

- Start with the direct answer when the evidence supports one.
- Separate `Evidence`, `Inference`, and `Unverified` information when the distinction matters.
- Cite the wiki page or raw source paths that support important statements.
- If the wiki does not contain enough evidence, say what is missing and which source should be checked next.

## Filing Rules

- File the answer under `wiki/queries/<question-slug>.md` when the answer is non-trivial, likely reusable, or synthesizes multiple pages.
- Do not file trivial answers, temporary status checks, or answers with no durable knowledge value.
- When filing, include the original question, concise answer, evidence, unverified items, and follow-up opportunities.

## Steps

1. Read `index.md` and identify relevant article, concept, and query pages.
2. Read the necessary `wiki/` pages. Check `raw/` only when the wiki is incomplete, contradictory, or too vague.
3. Produce the answer with evidence paths and clear uncertainty markers.
4. Decide whether the result should be filed under `wiki/queries/`.
5. If filing, create or update the query page and update the Query Pages table in `index.md`.
6. If the query reveals missing concepts or stale summaries, propose updates to `wiki/articles/` or `wiki/concepts/`.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] query | <question>`.
