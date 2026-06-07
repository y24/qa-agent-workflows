---
description: Audit wiki consistency, evidence, indexing, and page placement
argument-hint: <target or question>
---

# LLM Wiki lint

User request:
{{arguments}}

## Purpose

Audit the wiki as a durable knowledge base. Focus on issues that make future answers harder, less traceable, or less reliable.

## Checks

- Index coverage: every `wiki/articles/`, `wiki/concepts/`, and `wiki/queries/` page appears in the right table in `index.md`.
- Filesystem consistency: every page listed in `index.md` exists.
- Page placement: article pages summarize one primary source, concept pages synthesize reusable knowledge, and query pages preserve answers to concrete questions.
- Evidence quality: important claims cite `raw/` sources or other wiki pages.
- Contradictions: important concepts, dates, entities, or relationships do not conflict silently across pages.
- Freshness: recent `log.md` ingest and query entries are reflected in `index.md` and the relevant wiki pages.
- Retrieval quality: page names and summaries are specific enough for future agents to choose the right page.

## Output

Organize findings in this format:

- `Priority`: High, Medium, or Low.
- `File`: Target file or missing path.
- `Issue`: What is wrong.
- `Evidence`: What proves the issue.
- `Proposed Fix`: Concrete change to make.

Append an entry to `log.md` in the format `## [YYYY-MM-DD] lint | <scope>`.

Do not make large corrective edits during lint unless the user explicitly asked for fixes. Small index or log corrections are acceptable when the intent is clear.
