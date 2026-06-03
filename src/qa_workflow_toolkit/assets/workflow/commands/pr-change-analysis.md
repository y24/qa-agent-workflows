---
description: PR変更分析ワークフローを開始する
argument-hint: <Azure DevOps Pull RequestのURL（複数可）>
---

# PR Change Analysis Workflow

Use the `pr-change-analysis` skill.

User request:
{{arguments}}

Follow the workflow described in the skill.
Fetch Azure DevOps PR information via the Azure DevOps MCP as described in the skill's references.
Step 1 through the Step 2 diff reports for all PRs may proceed without stopping; stop for review after all diff reports are produced.
Do not proceed to the next major step (Step 3, Step 4) until the user explicitly approves.
Use the output location policy when the user does not specify an output path.
