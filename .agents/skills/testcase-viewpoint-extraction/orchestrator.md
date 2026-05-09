# orchestrator.md

# Testcase Viewpoint Extraction Orchestrator

## 目的

既存テストケースからテスト意図、観点候補、抽象観点カタログ、トレーサビリティを段階的に作成する。

ユーザーが明示的に継続を指示しない限り、各Stepの出力後に停止してレビューを待つ。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 01 | 入力整理・テストケース正規化 | 既存テストケース | `01_testcase_inventory.md`, `01_input_issues.md` | `steps/step_01_input_normalization_guide.md` | `templates/testcase_inventory_template.md` |
| 02 | 意図・観点候補の抽出 | Step 01成果物 | `02_intent_and_viewpoint_candidates.md`, `02_extraction_issues.md` | `steps/step_02_intent_and_candidate_extraction_guide.md` | `templates/intent_and_candidate_template.md` |
| 03 | 抽象観点カタログ化 | Step 02成果物 | `03_viewpoint_catalog.md`, `03_cataloging_issues.md` | `steps/step_03_viewpoint_cataloging_guide.md` | `templates/viewpoint_catalog_template.md` |
| 04 | トレーサビリティ確認・最終化 | Step 01-03成果物 | `04_final_traceability_matrix.md`, `04_final_issue_log.md`, `04_final_summary.md` | `steps/step_04_traceability_and_finalization_guide.md` | `templates/traceability_matrix_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 既存テストケースを根拠にし、無関係な要件から観点を創作しない。
- 推定、曖昧さ、根拠不足、レビュー要否を明示する。
- issueを隠さない。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。

## 共通参照

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`
- `../../../shared/output_style.md`
- `../../../shared/test_design_granularity_policy.md`

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 01 | `rules.md`, `steps/step_01_input_normalization_guide.md`, `templates/testcase_inventory_template.md`, `templates/issue_log_template.md` | `references/input_normalization_policy.md`, `references/ambiguity_policy.md` |
| 02 | `rules.md`, `steps/step_02_intent_and_candidate_extraction_guide.md`, `templates/intent_and_candidate_template.md` | `references/definitions.md`, `references/ambiguity_policy.md`, `references/abstraction_policy.md` |
| 03 | `rules.md`, `steps/step_03_viewpoint_cataloging_guide.md`, `templates/viewpoint_catalog_template.md` | `references/abstraction_policy.md`, `references/viewpoint_category_seed.md`, `references/viewpoint_category_policy.md` |
| 04 | `rules.md`, `steps/step_04_traceability_and_finalization_guide.md`, `templates/traceability_matrix_template.md`, `templates/issue_log_template.md` | `references/finalization_policy.md`, `references/ambiguity_policy.md` |

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
- 追加、削除、統合、分割の理由を記録する。
- 後続成果物がある場合は影響範囲と再実行が必要なStepを明示する。

## 完了条件

- `TC ID -> Intent ID -> Candidate ID -> Viewpoint ID` の追跡ができる。
- 低推定度、レビュー要、未対応、除外、保留が説明されている。
- 最終サマリに利用上の注意と次アクションがある。
