---
name: testcase-viewpoint-extraction
description: Use when extracting test intent, abstract test viewpoints, viewpoint catalogs, and traceability from existing test cases. Do not use to generate new tests from requirements alone.
---

# Testcase Viewpoint Extraction

## Purpose

Analyze existing test cases, extract their intent and reusable QA viewpoints, and produce a traceable viewpoint catalog.

## Inputs

- Existing test case lists, test procedures, expected results, or test management exports
- Related screen specs or requirements, if available

## Outputs

- `01_testcase_inventory.md`
- `01_input_issues.md`
- `02_intent_and_viewpoint_candidates.md`
- `02_extraction_issues.md`
- `03_viewpoint_catalog.md`
- `03_cataloging_issues.md`
- `04_final_traceability_matrix.md`
- `04_final_issue_log.md`
- `04_final_summary.md`

## Workflow

1. Input normalization and testcase inventory
2. Intent and viewpoint candidate extraction
3. Abstract viewpoint cataloging
4. Traceability check and finalization

Stop after each step and wait for user review unless the user explicitly asks to continue.

## References

- Common rules: `rules.md`
- Flow control: `orchestrator.md`
- Step guides: `steps/`
- Definitions and policies: `references/`
- Output templates: `templates/`

## Guardrails

- Derive viewpoints from existing test cases, not from unrelated requirements.
- Keep low-confidence interpretations in issue logs or review items.
- Exclude unsupported viewpoints from final outputs unless explicitly marked for review.
