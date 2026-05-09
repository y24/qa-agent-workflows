# orchestrator.md

# Test Design Review Orchestrator

## 目的

テスト設計成果物レビューを、入力整理、設計構造レビュー、観点・カバレッジレビュー、テストケース品質レビュー、結果統合の順に進める。

ユーザーが明示的に継続を指示しない限り、各Stepの出力後に停止してレビューを待つ。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 01 | レビュー対象と入力情報の整理 | レビュー依頼、対象成果物、根拠資料 | `01_input_summary.md` | `steps/step_01_review_scope_and_input_summary_guide.md` | `templates/input_summary_template.md` |
| 02 | 構造・トレーサビリティレビュー | Step 01成果物、テスト設計書、根拠資料 | `02_design_structure_review.md` | `steps/step_02_design_structure_traceability_review_guide.md` | `templates/design_structure_review_template.md` |
| 03 | 観点・条件・カバレッジレビュー | Step 01-02成果物、観点表、根拠資料 | `03_viewpoint_coverage_review.md` | `steps/step_03_test_viewpoint_and_coverage_review_guide.md` | `templates/viewpoint_coverage_review_template.md` |
| 04 | テストケース品質レビュー | Step 01-03成果物、テストケース一覧 | `04_testcase_quality_review.md` | `steps/step_04_testcase_quality_review_guide.md` | `templates/testcase_quality_review_template.md` |
| 05 | レビュー結果の統合・成果物化 | Step 02-04成果物、issue log | `05_review_report.md`, `05_issue_log.md` | `steps/step_05_review_result_packaging_guide.md` | `templates/review_report_template.md`, `templates/issue_log_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- レビュー対象、根拠資料、参考資料、未確認資料を区別する。
- 各Stepで発見したissueは、Step内成果物に記録し、Step 05で統合する。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。
- ユーザーが最初に一括実行を依頼した場合のみ、Step 05まで継続してよい。

## 共通参照

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`
- `../../../shared/output_style.md`
- `../../../shared/output_location_policy.md`
- `../../../shared/test_design_granularity_policy.md`

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 01 | `rules.md`, `steps/step_01_review_scope_and_input_summary_guide.md`, `templates/input_summary_template.md` | `templates/issue_log_template.md` |
| 02 | `rules.md`, `steps/step_02_design_structure_traceability_review_guide.md`, `templates/design_structure_review_template.md` | `references/severity_priority_criteria.md` |
| 03 | `rules.md`, `steps/step_03_test_viewpoint_and_coverage_review_guide.md`, `templates/viewpoint_coverage_review_template.md` | `references/review_viewpoint_catalog.md`, `references/severity_priority_criteria.md` |
| 04 | `rules.md`, `steps/step_04_testcase_quality_review_guide.md`, `templates/testcase_quality_review_template.md` | `references/severity_priority_criteria.md` |
| 05 | `rules.md`, `steps/step_05_review_result_packaging_guide.md`, `templates/review_report_template.md`, `templates/issue_log_template.md` | `references/severity_priority_criteria.md`, `references/output_schema_examples.md` |

## 応答形式

```markdown
# Step XX: <ステップ名>

## 入力
- 

## 実行結果
<対象Stepの成果物>

## Issue / 要レビュー
- 

## 完了判定
- 完了 / 一部完了 / 要追加入力
```

## 再実行

- 既存IDは可能な限り維持する。
- 変更した指摘、削除した指摘、統合した指摘の理由を記録する。
- 前段成果物の修正が後続Stepに影響する場合は、再実行が必要なStepを明示する。

## 完了条件

- レビュー対象、根拠資料、対象範囲、対象外範囲が明確である。
- 主要指摘に対象箇所、根拠、理由、重要度、優先度、推奨対応がある。
- 未確認事項、判断保留、改善提案が分類されている。
- 最終報告に修正判断に使えるサマリと次アクションがある。
