<!-- generated-by: qa-workflow-toolkit -->
<!-- wiki-name: [[wiki_name]] -->
<!-- wiki-type: [[wiki_type]] -->

# [[wiki_name]] Defect Knowledge Wiki

This repository is a Markdown knowledge base maintained by LLM agents. Its goal is to accumulate knowledge about **past defects** (過去の不具合) so the same product can prevent recurrence of similar defects and feed risk-based test design with durable, evidence-backed knowledge instead of rediscovering it every time.

The raw evidence is past defect reports — bug reports, incident reports, root-cause analyses, and similar artifacts that describe what went wrong and why. From them, the wiki keeps two layers of knowledge: summaries of each defect report, and reusable lessons and test viewpoints extracted to prevent the same class of defect from happening again.

## Structure

- `raw/`: Converted or collected defect reports (bug reports, incident reports, root-cause analyses, etc.). Treat them as immutable evidence by default.
- `.temp/`: Temporary staging area for files before conversion into `raw/`.
- `wiki/`: Knowledge pages created and updated by LLM agents. New pages must go into one of the subfolders below.
- `wiki/reports/`: Summaries of defect reports. Use one page per defect (or per report), focused on the phenomenon, cause, and affected area that the source actually states.
- `wiki/viewpoints/`: Reusable lessons and test viewpoints extracted from the defects. Use these to capture how a class of defect can be prevented or detected, so future test design and risk assessment can reuse them.
- `index.md`: Content index for the whole wiki. Check it first before ingest or query work.
- `log.md`: Append-only chronological log for ingest, query, lint, and convert operations.
- Agent-specific commands: Slash commands for wiki operations.

## Core Policies

- **No speculation. This is the most important rule.** Adding information that is not a fact is fatal for defect knowledge. Never invent, guess, or infer phenomena, causes, conditions, affected areas, fixes, lessons, requirements, relationships, dates, or numbers that the defect reports do not state or directly demonstrate.
- Distinguish the phenomenon (what was observed) from the cause (why it happened). Only record a cause when the source states or demonstrates it. If a report describes a symptom but not a root cause, record the cause as unknown rather than guessing one.
- Every report summary, lesson, and viewpoint must be traceable to a specific source under `raw/` or to an existing wiki page. If a statement has no evidence, do not write it.
- A lesson or test viewpoint is generalized from what a defect report concretely describes. Generalizing the angle a real defect reveals (for example, "boundary handling of the same input field across screens") is allowed and expected. Adding a lesson that no defect report supports is not allowed.
- When something is unknown, missing, or ambiguous, record it explicitly under Open Questions instead of filling the gap with a plausible guess.
- Do not modify `raw/` content without explicit user instruction. Normal edits should target `wiki/`, `index.md`, and `log.md`.
- Make contradictions, possibly outdated reports, and insufficient evidence explicit rather than silently resolving them.
- Do not leave reusable knowledge only in a one-off answer. When useful, create or update a page under `wiki/`.

## Page Placement Rules

- Create or update `wiki/reports/<defect-slug>.md` when summarizing a single defect report. Do not mix unrelated defects into the same page.
- Create or update `wiki/viewpoints/<viewpoint-slug>.md` when a lesson or test viewpoint is reusable beyond the single defect it came from, or when multiple defect reports share the same underlying pattern.
- If a page could fit multiple folders, choose by purpose: a record of what a defect report contains goes to `reports`, and a reusable recurrence-prevention angle goes to `viewpoints`.
- Keep filenames short, lowercase, hyphen-separated, and stable. Rename only when the current name is misleading.

## Operations

- `/convert`: Convert files in `.temp/` to Markdown with `markitdown` and place them in `raw/`.
- `/ingest`: Read defect reports in `raw/`, summarize each one into `wiki/reports/`, and extract reusable recurrence-prevention lessons and test viewpoints into `wiki/viewpoints/`.
- `/query`: Answer from `index.md` and related pages to support recurrence prevention and risk-based test design, then reflect durable findings back into the wiki.
- `/lint`: Check contradictions, orphan pages, missing index entries, unsupported (speculative) content, and missed updates.
