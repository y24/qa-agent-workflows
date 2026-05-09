---
name: risk-based-test-design
description: Use when identifying product risks, assessing impact and likelihood, prioritizing test scope, and deriving risk-based test strategy or testcase outlines. Do not use when the user only wants scenario flow design without risk assessment.
---

# Risk-Based Test Design

## Purpose

Identify and assess product risks, decide risk-based test priorities, and translate high-priority risks into test strategy and testcase outlines.

## Inputs

- Requirements, design documents, screen specs, API specs, architecture notes, past defects, operational constraints, or extracted spec inventories
- Existing risk lists or user-provided risk concerns, if available

## Outputs

- `01_input_scope_summary.md`
- `02_risk_candidate_list.md`
- `03_risk_register.md`
- `04_risk_based_test_strategy.md`
- `05_testcase_outline_and_traceability.md`

## Workflow

1. Input source normalization and scope confirmation
2. Risk candidate extraction
3. Risk assessment and prioritization
4. Risk-based test strategy
5. Testcase outline and traceability generation

Stop after each step and wait for user review unless the user explicitly asks to continue.

## References

- Common rules: `rules.md`
- Flow control: `orchestrator.md`
- Step guides: `steps/`
- Risk taxonomy and scoring: `references/`
- Output templates: `templates/`

## Guardrails

- Do not score risks without stating evidence and assumptions.
- Keep unassessable risks as unresolved or out-of-scope rather than forcing a score.
- Do not over-detail executable test procedures in this skill unless explicitly requested.
