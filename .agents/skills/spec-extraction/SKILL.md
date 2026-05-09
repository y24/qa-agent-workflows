---
name: spec-extraction
description: Use when extracting, normalizing, and reviewing test-design inputs from development documents, requirements, screen specs, API specs, design notes, or domain documents. Do not use to create detailed test cases directly.
---

# Spec Extraction

## Purpose

Extract facts from development documents and transform them into traceable, normalized inputs for later QA design work.

## Inputs

- Requirements, design documents, screen specs, API specs, domain rules, release notes, or related development documents
- User-specified document scope and priority, if provided

## Outputs

- `document_inventory.md`
- `raw_extraction.md`
- `normalized_spec_inventory.md`
- `test_design_input_catalog.md`
- `gap_and_review_report.md`

## Workflow

1. Document inventory
2. Raw fact extraction
3. Normalization and consolidation
4. Test design input cataloging
5. Gap and review report

Stop after each step and wait for user review unless the user explicitly asks to continue.

## References

- Common rules: `rules.md`
- Flow control: `orchestrator.md`
- Step guides: `steps/`
- Evidence and category references: `references/`
- Output templates: `templates/`

## Guardrails

- Do not infer missing specifications as facts.
- Keep source evidence and IDs traceable.
- Do not create detailed test cases in this skill.
- Mark contradictions, missing information, and insufficient detail explicitly.
