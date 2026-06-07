---
description: Convert staged defect reports in .temp into evidence Markdown under raw
argument-hint: <target or question>
---

# Defect Knowledge Wiki convert

User request:
{{arguments}}

## Purpose

Convert staged defect reports from `.temp/` (bug reports, incident reports, root-cause analyses, etc.) into Markdown evidence files under `raw/`. The converted file becomes a primary source for later ingest work.

## Steps

1. Identify the target file in `.temp/`. If the user did not specify a file, list likely candidates and choose only when the intent is clear.
2. Set the output path to `raw/<source-file-stem>.md`. Use a short, stable, lowercase slug when the original filename is noisy.
3. Before conversion, check whether the output path already exists.
4. Run `markitdown "<input>" -o "<output>"`.
5. Inspect the converted Markdown for empty output, missing major sections, broken tables, broken links, or mojibake. Defect reports are often spreadsheets or ticket exports, so verify that tables and key columns (phenomenon, cause, steps to reproduce, severity, status, etc.) survived the conversion.
6. If conversion quality is acceptable, leave the file in `raw/` and report the path. If quality is poor, keep the file but record the issue clearly.
7. Append an entry to `log.md` in the format `## [YYYY-MM-DD] convert | <file>`.

## Guardrails

- If a file with the same name already exists in `raw/`, do not overwrite it without user confirmation.
- If `markitdown` is unavailable, report that installation is required and do not run an alternative conversion on your own.
- Do not summarize, reinterpret, or extract lessons from the source during conversion. Source interpretation belongs in `/ingest`.
