---
name: nonfunctional-quality-criteria-planning
description: Use when extracting non-functional quality concerns from requirements or design documents, defining quality criteria, selecting confirmation or measurement methods, and preparing inputs for test planning. Focuses on performance efficiency, compatibility, usability, reliability, security, maintainability, and portability. Do not use when the user only wants functional scenario tests, detailed test cases, or risk scoring without quality criteria planning.
---

# 非機能品質クライテリア策定 skill

## 目的

開発文書や前段成果物から、非機能品質の懸念を抽出し、テスト計画やテスト設計に組み込める品質クライテリアへ段階的に整理する。

この skill では、いきなり性能テスト、セキュリティテストなどの手段を決めない。まず「何を満たせば品質として十分と言えるか」を定義し、その後に確認方法、測定方法、テスト計画への反映方針を決める。

## 対象品質特性

- 性能効率性
- 互換性
- 使用性
- 信頼性
- セキュリティ
- 保守性
- 移植性

機能適合性は主対象外とし、必要な場合は機能テストやシナリオテストの入力として扱う。

## 入力

- 要件定義、基本設計、画面仕様、API仕様、帳票仕様、バッチ仕様、外部IF仕様、運用設計、インフラ構成、制約事項
- 利用者、利用状況、利用環境、端末、ブラウザ、OS、DB、ネットワーク、権限、データ量、運用時間帯などの情報
- `$spec-extraction`、`$risk-based-test-design`、`$scenario-test-design` の前段成果物
- 既存の非機能要求、品質要求、SLA、NFR、テスト計画、品質懸念メモ

## 出力

- `01_input_scope_summary.md`
- `02_quality_concern_extraction.md`
- `03_quality_criteria_candidates.md`
- `04_confirmation_policy.md`
- `05_quality_criteria_catalog.md`

## ワークフロー

1. 入力文書の整理と対象スコープ定義
2. 品質特性別の懸念・要求候補の抽出
3. 品質クライテリア候補の設計
4. 目標値・確認方法・テスト方針への落とし込み
5. 整合性レビューと最終カタログ化

ユーザーが明示的に継続を指示しない限り、各ステップ完了後に停止し、レビューを待つ。

## 参照ファイル

- 共通方針:
  - `../../../shared/common_contract.md`
  - `../../../shared/evidence_and_confidence_policy.md`
  - `../../../shared/ambiguity_and_issue_log_policy.md`
  - `../../../shared/review_gate_policy.md`
  - `../../../shared/traceability_policy.md`
  - `../../../shared/output_style.md`
  - `../../../shared/output_location_policy.md`
  - `../../../shared/input_document_handling.md`
  - `../../../shared/test_design_granularity_policy.md`
- skill固有ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- 品質特性、確認方法、測定、自動化判断: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 入力にない非機能要求、基準値、データ量、利用環境を事実として創作しない。
- 「性能効率性だから性能テスト」のように、品質特性から確認手段を短絡的に決めない。
- 定量目標が未提示の場合は、勝手に秒数、件数、閾値を設定せず、`要確認` または `仮説` として扱う。
- 品質クライテリアは、詳細テストケースより上位の粒度で、確認可能な表現にする。
