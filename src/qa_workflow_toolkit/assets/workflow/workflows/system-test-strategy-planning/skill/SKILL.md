---
name: system-test-strategy-planning
description: Use when planning a system test strategy from development documents. Produces a system test strategy plan covering evidence-based non-functional coverage, multiple test types, test viewpoints, an ISO/IEC 25010 quality characteristic matrix, and viewpoint traceability. Do not use when the user wants detailed test cases, schedules, staffing, or unsupported assumptions.
---

# システムテスト戦略策定 skill

## 目的

要件定義、仕様書、設計書などの開発文書を根拠に、システムテストフェーズで何をどの方針で確認するかを整理する。

最終成果物は、テスト設計担当者が詳細なテスト設計・テスト実行計画へ展開できる「システムテスト計画書」の戦略部分とする。スケジュール、体制、工数、担当者割当は扱わない。

## 入力

- 要件定義、業務要件、システム要件、非機能要件
- 基本設計、画面仕様、API仕様、外部IF仕様、帳票仕様、バッチ仕様
- 運用設計、インフラ構成、移行方針、制約事項、SLA、品質要求
- `$spec-extraction`、`$nonfunctional-quality-criteria-planning`、`$risk-based-test-design`、`$scenario-test-design` の前段成果物

## 出力

- `01_input_scope_summary.md`
- `02_system_test_coverage_analysis.md`
- `03_test_type_strategy.md`
- `04_test_viewpoint_policy.md`
- `05_system_test_strategy_plan.md`
- `appendix_quality_characteristic_matrix.md`
- `appendix_viewpoint_traceability.md`

## ワークフロー

1. 入力文書整理とシステムテスト対象スコープ確認
2. システムテストで扱うべきカバレッジ候補の抽出
3. テスト種別の選定と戦略整理
4. テスト種別ごとのテスト観点策定
5. 戦略計画書と付属資料の最終化

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
  - `../../shared/input_document_handling.md`
  - `../../shared/test_design_granularity_policy.md`
- skill固有ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- システムテスト範囲、テスト種別、ISO/IEC 25010、トレーサビリティ: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 入力文書に記載されていない内容を推測で補完しない。
- 非機能要求、テスト条件、環境、データ量、閾値、障害条件、権限ルールを根拠なしに作らない。
- すべての非機能やテスト種別を網羅するために、根拠のない観点を追加しない。
- この skill では具体的なテストケース、手順、期待結果の詳細化を行わない。
- スケジュール、体制、役割分担、工数見積もりは出力対象外とする。
