---
name: nonfunctional-quality-criteria-planning
description: Use when deriving nonfunctional quality concerns, risk-weighted quality criteria, confirmation policies, automation recommendations, and test-plan integration proposals from requirements, design documents, screen specs, system architecture, operations notes, or prior incidents. Covers performance efficiency, compatibility, usability, reliability, security, maintainability, and portability. Do not use when the user only wants functional scenario tests, existing testcase viewpoint extraction, or general risk-based test design without nonfunctional quality criteria.
---

# 非機能品質クライテリア策定・確認計画化 skill

## 目的

開発ドキュメントから非機能品質に関係する前提、制約、品質懸念を抽出し、重要度に応じて品質クライテリアと確認方針へ落とし込む。

最終成果物は、テスト計画、レビュー計画、静的解析、運用確認、自動化方針へ組み込める粒度にする。

## 対象品質特性

- 性能効率性
- 互換性
- 使用性
- 信頼性
- セキュリティ
- 保守性
- 移植性

機能適合性は原則対象外とする。安全性は、業務、法令、人身、環境への影響がある場合のみ補足扱いにする。

## 入力

- プロジェクト計画書、要件定義書、画面仕様、システム構成、運用構成、業務フロー
- 既存障害、問い合わせ、制約事項、既存の非機能要件、テスト制約
- 前Step成果物、またはユーザーが提示した品質懸念、リスク、受入基準案

## 出力

- `01_input_scope_summary.md`
- `02_quality_concern_register.md`
- `03_prioritized_quality_concern_register.md`
- `04_quality_criteria_catalog.md`
- `05_confirmation_policy_and_test_planning.md`

## ワークフロー

1. 入力文書のスコープ整理・非機能関連情報の抽出
2. 非機能リスク・品質懸念の抽出
3. 重要度評価・確認対象の選別
4. 品質クライテリア策定
5. クライテリア確認方針・テスト計画組み込み案の策定

ユーザーが明示的に継続を指示しない限り、各Step完了後に停止し、レビューを待つ。

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
- 品質特性、評価、確認方法、自動化判断: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 根拠のない非機能要求、品質懸念、数値基準、テスト条件を創作しない。
- 「非機能だから専用テスト」と決めつけず、テスト、機能テスト組み込み、レビュー、静的解析、運用確認から妥当な確認方法を選ぶ。
- 品質クライテリアは、対象、条件、判定基準、確認方法、根拠、未確定事項が追跡できる形にする。
- 詳細テストケースを大量生成せず、まず確認方針とテスト計画への組み込み案に留める。
