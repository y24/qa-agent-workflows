---
description: Audit viewpoint evidence, consistency, indexing, and page placement
argument-hint: <target or question>
---

# Test Viewpoint Wiki lint

User request:
{{arguments}}

## Purpose

Audit the wiki as a durable, evidence-backed store of test viewpoints. The top priority is catching speculative or unsupported content, because non-factual viewpoints make future test design unreliable.

## Checks

- No speculation: every viewpoint, summary, and glossary entry traces to a source under `raw/` or another wiki page. Flag any statement that no source supports.
- Index coverage: every `wiki/testcases/`, `wiki/viewpoints/`, and `wiki/glossary/` page appears in the right table in `index.md`.
- Filesystem consistency: every page listed in `index.md` exists.
- Page placement: testcase pages summarize one source, viewpoint pages capture reusable angles, and glossary pages define terms.
- Traceability: each viewpoint page lists the source test cases it was generalized from.
- Contradictions: viewpoints, conditions, terms, or expected results do not conflict silently across pages.
- Freshness: recent `log.md` ingest and query entries are reflected in `index.md` and the relevant wiki pages.
- Reuse quality: page names and summaries are specific enough for future test design to choose the right viewpoint.

## Output

Organize findings in this format:

- `Priority`: High, Medium, or Low. Treat speculative or unsupported content as High.
- `File`: Target file or missing path.
- `Issue`: What is wrong.
- `Evidence`: What proves the issue.
- `Proposed Fix`: Concrete change to make.

Append an entry to `log.md` in the format `## [YYYY-MM-DD] lint | <scope>`.

Do not make large corrective edits during lint unless the user explicitly asked for fixes. Small index or log corrections are acceptable when the intent is clear.
