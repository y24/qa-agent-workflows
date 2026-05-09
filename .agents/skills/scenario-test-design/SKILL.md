---
name: scenario-test-design
description: Use when designing scenario tests from requirements, business rules, screen specs, domain documents, business flows, or extracted specification inventories. Do not use for simple unit-level test generation or risk assessment-only work.
---

# Scenario Test Design

## Purpose

Design scenario tests through staged analysis of input summaries, business flows, scenario viewpoints, scenario candidates, and detailed executable test cases.

## Inputs

- Requirements, screen specs, business process documents, domain rules, past defects, or extracted spec inventories
- Existing outputs from `$spec-extraction`, if available

## Outputs

- `01_input_summary.md`
- `02_business_flows.md`
- `03_scenario_viewpoints.md`
- `04_scenario_candidates.md`
- `05_test_cases.md`

## Workflow

1. Input summary
2. Business flow and use scene organization
3. Scenario viewpoint extraction
4. Scenario candidate design
5. Test case detailing and prioritization

Stop after each step and wait for user review unless the user explicitly asks to continue.

## References

- Common rules: `rules.md`
- Flow control: `orchestrator.md`
- Step guides: `steps/`
- Decision policies: `references/`
- Output and support templates: `templates/`

## Guardrails

- Do not create test cases before the scenario viewpoints and candidates are reviewed.
- Do not invent screen operations, expected results, or business rules.
- Keep scenario, viewpoint, business flow, and test case IDs traceable.
