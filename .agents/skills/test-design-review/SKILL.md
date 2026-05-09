---
name: test-design-review
description: Use when reviewing existing test design deliverables, test design documents, test case lists, coverage matrices, or QA review requests to extract evidence-based issues, gaps, traceability problems, testcase quality concerns, and prioritized review findings. Do not use to create a new test design from requirements alone.
---

# テスト設計レビュー skill

## 目的

既存のテスト設計書、テスト観点表、テスト条件、テストケース一覧をレビューし、問題、不足、改善点を根拠付きで抽出する。主目的はテスト設計の作り直しではなく、レビュー判断の根拠を残すことである。

## 入力

- レビュー対象のテスト設計書、テスト観点表、テスト条件、テストケース一覧
- 要件定義書、設計書、画面仕様書、業務仕様書、API仕様書
- テスト計画書、レビュー依頼内容、変更点、過去障害、不具合情報
- 前段 skill の成果物がある場合は、仕様インベントリ、リスク一覧、観点カタログなど

## 出力

- `01_input_summary.md`
- `02_design_structure_review.md`
- `03_viewpoint_coverage_review.md`
- `04_testcase_quality_review.md`
- `05_review_report.md`
- `05_issue_log.md`

## ワークフロー

1. レビュー対象と入力情報の整理
2. テスト設計書の構造・トレーサビリティレビュー
3. テスト観点・テスト条件・カバレッジレビュー
4. テストケース品質レビュー
5. レビュー結果の統合・優先度付け・成果物化

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
  - `../../../shared/test_design_granularity_policy.md`
- skill固有ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- レビュー観点と判定基準: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 根拠資料にない仕様、業務ルール、期待結果を創作しない。
- 不足と断定できない場合は、未確認事項または確認依頼として扱う。
- テストケースを勝手に大量生成しない。
- 改善例を出す場合は、元成果物との差分が分かるようにする。
- 指摘には対象箇所、根拠、理由、重要度、優先度を可能な限り付ける。
