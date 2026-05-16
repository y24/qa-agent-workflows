<!-- generated-by: qa-workflow-toolkit -->
<!-- toolkit-version: 0.1.0 -->

# QA Agent Workflows

このプロジェクトでは、QA業務向けAI agent workflow assetsを利用する。

## Common Rules

- 要件、仕様、リスク、テスト条件を根拠なしに創作しない。
- 事実、推測、前提、未確認事項、提案を分けて扱う。
- 入力文書、前段成果物、IDへのトレーサビリティを可能な限り残す。
- 複数ステップのworkflowは、ユーザーが明示的に継続を指示しない限り、主要ステップごとに停止してレビューを待つ。
- 成果物はユーザー指定の出力先を優先し、指定がない場合は `.agents/shared/output_location_policy.md` に従う。
- 詳細な共通方針は `.agents/shared/`、個別workflowは `.agents/skills/` を参照する。

## Available Workflow Assets

RooCodeの slash command は `.roo/commands/` に配置される。
各commandは対応する `.agents/skills/<workflow>/SKILL.md` を入口として使用する。
