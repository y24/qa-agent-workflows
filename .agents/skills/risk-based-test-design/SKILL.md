---
name: risk-based-test-design
description: Use when identifying product risks, assessing impact and likelihood, prioritizing test scope, and deriving risk-based test strategy or testcase outlines. Do not use when the user only wants scenario flow design without risk assessment.
---

# リスクベースドテスト設計 skill

## 目的

プロダクトリスクを抽出・評価し、リスクに基づくテスト優先度を決める。優先度の高いリスクは、テスト方針とテストケース骨子へ落とし込む。

## 入力

- 要件、設計書、画面仕様、API仕様、アーキテクチャメモ、過去障害、運用制約、仕様抽出結果
- 既存のリスク一覧、またはユーザーから提示された懸念事項

## 出力

- `01_input_scope_summary.md`
- `02_risk_candidate_list.md`
- `03_risk_register.md`
- `04_risk_based_test_strategy.md`
- `05_testcase_outline_and_traceability.md`

## ワークフロー

1. 入力ソースの正規化とスコープ確認
2. リスク候補の抽出
3. リスク評価と優先度付け
4. リスクベースのテスト方針作成
5. テストケース骨子とトレーサビリティの作成

ユーザーが明示的に継続を指示しない限り、各ステップ完了後に停止し、レビューを待つ。

## 参照ファイル

- 共通方針:
  - `../../../shared/common_contract.md`
  - `../../../shared/evidence_and_confidence_policy.md`
  - `../../../shared/ambiguity_and_issue_log_policy.md`
  - `../../../shared/review_gate_policy.md`
  - `../../../shared/traceability_policy.md`
  - `../../../shared/output_style.md`
  - `../../../shared/input_document_handling.md`
  - `../../../shared/test_design_granularity_policy.md`
- skill固有ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- リスク分類と評価基準: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 根拠と前提を示さずにリスクスコアを付けない。
- 評価できないリスクは、無理に採点せず `未解決`、`情報不足`、`対象外` として扱う。
- ユーザーが明示的に求めない限り、この skill では実行手順レベルの詳細テストケースまで作り込まない。
