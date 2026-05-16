---
name: defect-analysis
description: Use when analyzing existing defect or bug tickets to extract facts, classify defect trends, identify quality risks and weak patterns, and convert the findings into guidance for future test design, regression testing, review viewpoints, test data design, or exploratory testing. Do not use when the user only wants to triage individual tickets without trend analysis or future test-design guidance.
---

# 不具合分析 skill

## 目的

既存の不具合チケットを、分類して終わらせず、後続のテスト設計で再利用できる知見へ変換する。

不具合チケットから事実情報を抽出し、分類・傾向集計、品質リスク・弱点パターンの解釈、テスト設計向けガイダンス化までを段階的に行う。

## 入力

- 不具合チケット一覧、バグ票、障害票、問い合わせ票のうち分析対象に含めるもの
- チケット項目定義、ステータス定義、重要度・優先度の定義
- 対象プロダクト、対象バージョン、対象機能、対象期間
- 開発フェーズ、テストフェーズ、リリース後運用などの文脈
- 既存テスト設計、テスト観点、回帰テスト、テストデータ、レビュー観点

## 出力

- `01_analysis_scope_summary.md`
- `02_defect_fact_table.md`
- `03_defect_trend_analysis.md`
- `04_quality_risk_insights.md`
- `05_test_design_guidance.md`
- `issue_log.md`

## ワークフロー

1. 分析対象スコープ整理
2. 不具合ファクト抽出・正規化
3. 不具合分類・傾向集計
4. 品質リスク・弱点パターン抽出
5. 後続テスト設計向けガイダンス化

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
- 分類軸と変換方針: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- チケットに書かれていない原因、仕様、期待結果、再発防止策を事実として扱わない。
- 分類不能な不具合を無理に分類せず、`情報不足`、`分類保留`、`対象外` として扱う。
- 品質リスクやテスト設計示唆には、根拠チケットIDまたは前Step成果物IDを残す。
- 傾向分析とテスト設計示唆を同じStepで混ぜず、解釈の根拠を明示する。
