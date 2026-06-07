---
description: Audit defect evidence, consistency, indexing, and page placement
argument-hint: <target or question>
---

# Defect Knowledge Wiki lint

User request:
{{arguments}}

## Purpose

Audit the wiki as a durable, evidence-backed store of defect knowledge. The top priority is catching speculative or unsupported content, because non-factual phenomena, causes, or lessons make recurrence prevention and risk-based test design unreliable.

## Checks

- No speculation: every report summary, lesson, and viewpoint traces to a source under `raw/` or another wiki page. Flag any statement that no source supports.
- Phenomenon vs. cause: each report page keeps the observed phenomenon separate from the cause, and any cause not stated by the source is marked as unknown rather than guessed.
- Index coverage: every `wiki/reports/` and `wiki/viewpoints/` page appears in the right table in `index.md`.
- Filesystem consistency: every page listed in `index.md` exists.
- Page placement: report pages summarize one defect, and viewpoint pages capture reusable recurrence-prevention angles.
- Traceability: each viewpoint page lists the defect reports it was generalized from.
- Contradictions: phenomena, causes, conditions, or lessons do not conflict silently across pages.
- Freshness: recent `log.md` ingest and query entries are reflected in `index.md` and the relevant wiki pages.
- Reuse quality: page names and summaries are specific enough for future test design and risk assessment to choose the right viewpoint.

## Output

Organize findings in this format:

- `Priority`: High, Medium, or Low. Treat speculative or unsupported content as High.
- `File`: Target file or missing path.
- `Issue`: What is wrong.
- `Evidence`: What proves the issue.
- `Proposed Fix`: Concrete change to make.

Append an entry to `log.md` in the format `## [YYYY-MM-DD] lint | <scope>`.

Do not make large corrective edits during lint unless the user explicitly asked for fixes. Small index or log corrections are acceptable when the intent is clear.
