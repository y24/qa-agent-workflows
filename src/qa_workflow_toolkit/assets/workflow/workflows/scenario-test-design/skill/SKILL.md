---
name: scenario-test-design
description: Use when designing scenario tests from requirements, business rules, screen specs, domain documents, business flows, or extracted specification inventories. Do not use for simple unit-level test generation or risk assessment-only work.
---

# シナリオテスト設計 skill

## 目的

入力情報、業務フロー、シナリオ観点、シナリオ候補を段階的に整理し、レビュー可能な形でシナリオテストを設計する。

## 入力

- 要件、画面仕様、業務プロセス資料、ドメインルール、過去障害、仕様抽出結果
- `$spec-extraction` の成果物がある場合は、その出力

## 出力

- `01_input_summary.md`
- `02_business_flows.md`
- `03_scenario_viewpoints.md`
- `04_scenario_candidates.md`
- `05_test_cases.md`

## ワークフロー

1. 入力情報の要約
2. 業務フローと利用シーンの整理
3. シナリオ観点の抽出
4. シナリオ候補の設計
5. テストケースの詳細化と優先度付け

ユーザーが明示的に継続を指示しない限り、各ステップ完了後に停止し、レビューを待つ。

## 参照ファイル

- 共通方針:
  - `../../shared/common_contract.md`
  - `../../shared/evidence_and_confidence_policy.md`
  - `../../shared/ambiguity_and_issue_log_policy.md`
  - `../../shared/review_gate_policy.md`
  - `../../shared/traceability_policy.md`
  - `../../shared/output_style.md`
  - `../../shared/output_location_policy.md`
  - `../../shared/test_design_granularity_policy.md`
- skill固有ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- 判断基準と補助定義: `references/`
- 出力テンプレートと補助テンプレート: `templates/`

## ガードレール

- シナリオ観点とシナリオ候補のレビュー前に、詳細テストケースを作成しない。
- 画面操作、期待結果、業務ルールを根拠なく創作しない。
- シナリオ、観点、業務フロー、テストケースのIDトレーサビリティを維持する。
