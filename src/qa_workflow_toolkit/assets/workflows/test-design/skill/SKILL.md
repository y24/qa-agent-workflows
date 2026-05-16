---
name: test-design
description: Use when starting an end-to-end QA test design workflow that may combine specification extraction, scenario design, risk-based design, non-functional criteria planning, and review. This skill routes to the appropriate installed QA workflow skill instead of replacing them.
---

# テスト設計 総合入口 skill

## 目的

入力資料からテスト設計を開始するための総合入口として、必要なQA workflow skillを選択し、段階的に実行する。

このskillは詳細手順を内包しない。対象に応じて以下の個別skillを参照する。

- `../spec-extraction/SKILL.md`
- `../scenario-test-design/SKILL.md`
- `../risk-based-test-design/SKILL.md`
- `../nonfunctional-quality-criteria-planning/SKILL.md`
- `../test-design-review/SKILL.md`
- `../testcase-viewpoint-extraction/SKILL.md`
- `../defect-analysis/SKILL.md`

## 共通方針

作業開始前に以下を確認する。

- `../../shared/common_contract.md`
- `../../shared/evidence_and_confidence_policy.md`
- `../../shared/ambiguity_and_issue_log_policy.md`
- `../../shared/traceability_policy.md`
- `../../shared/review_gate_policy.md`
- `../../shared/output_location_policy.md`
- `../../shared/terminology.md`

## 進め方

1. 入力文書、ユーザー依頼、既存成果物を棚卸しする。
2. 目的に合う個別skillを選ぶ。
3. 選択理由、使用するskill、最初のStep、確認事項をユーザーへ提示する。
4. ユーザーが明示的に継続を指示した場合だけ、選択したskillの手順に沿って進める。

## skill選択の目安

| 目的 | 使用skill |
|---|---|
| 仕様情報の抽出、正規化、棚卸し | `spec-extraction` |
| 業務フローやシナリオからテストケースを設計 | `scenario-test-design` |
| リスク候補の抽出、評価、優先度付け | `risk-based-test-design` |
| 非機能品質の懸念と確認方針を設計 | `nonfunctional-quality-criteria-planning` |
| 既存テスト設計のレビュー | `test-design-review` |
| 既存テストケースから観点を抽出 | `testcase-viewpoint-extraction` |
| 不具合チケットから傾向と後続テスト示唆を抽出 | `defect-analysis` |

## ガードレール

- 入力不足のまま、仕様、期待結果、業務ルール、テスト条件を創作しない。
- 個別skillのStepを飛ばさない。
- 主要Step完了後はレビューを待つ。
