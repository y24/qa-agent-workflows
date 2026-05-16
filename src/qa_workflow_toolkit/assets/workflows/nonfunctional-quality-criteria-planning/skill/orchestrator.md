# 非機能品質クライテリア策定 Orchestrator

## 目的

`$nonfunctional-quality-criteria-planning` の5Stepを順番に実行し、各Stepの成果物を後続Stepの入力としてつなぐ。

複数Stepをユーザーが明示しない限り、一度に進めない。各Stepの出力後はレビュー待ちで停止する。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 入力文書整理・対象スコープ定義 | 入力文書 | `01_input_scope_summary.md` | `steps/step_01_input_scope_summary_guide.md` | `templates/input_scope_summary_template.md` |
| 2 | 品質特性別の懸念・要求候補抽出 | Step 1成果物 | `02_quality_concern_extraction.md` | `steps/step_02_quality_concern_extraction_guide.md` | `templates/quality_concern_extraction_template.md` |
| 3 | 品質クライテリア候補設計 | Step 2成果物 | `03_quality_criteria_candidates.md` | `steps/step_03_quality_criteria_candidate_design_guide.md` | `templates/quality_criteria_candidates_template.md` |
| 4 | 目標値・確認方法・テスト方針整理 | Step 3成果物 | `04_confirmation_policy.md` | `steps/step_04_target_and_confirmation_policy_guide.md` | `templates/confirmation_policy_template.md` |
| 5 | 整合性レビュー・最終カタログ化 | Step 4成果物 | `05_quality_criteria_catalog.md` | `steps/step_05_consistency_catalog_review_guide.md` | `templates/quality_criteria_catalog_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 前Step成果物を主入力にし、元文書の再参照は根拠確認に必要な範囲へ限定する。
- 入力文書にない品質要求、品質基準、目標値、測定条件、テスト条件を事実として創作しない。
- 推測、仮説、確認事項、未確定事項は明示する。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。
- 実行成果物の出力先は `../../shared/output_location_policy.md` に従う。

## 共通参照

- `../../shared/common_contract.md`
- `../../shared/evidence_and_confidence_policy.md`
- `../../shared/ambiguity_and_issue_log_policy.md`
- `../../shared/review_gate_policy.md`
- `../../shared/traceability_policy.md`
- `../../shared/output_style.md`
- `../../shared/output_location_policy.md`
- `../../shared/input_document_handling.md`
- `../../shared/test_design_granularity_policy.md`

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 1 | `rules.md`, `steps/step_01_input_scope_summary_guide.md`, `templates/input_scope_summary_template.md` | `references/quality_characteristic_scope_notes.md` |
| 2 | `rules.md`, `steps/step_02_quality_concern_extraction_guide.md`, `templates/quality_concern_extraction_template.md` | `references/quality_characteristic_scope_notes.md` |
| 3 | `rules.md`, `steps/step_03_quality_criteria_candidate_design_guide.md`, `templates/quality_criteria_candidates_template.md` | `references/evidence_and_measurement_notes.md` |
| 4 | `rules.md`, `steps/step_04_target_and_confirmation_policy_guide.md`, `templates/confirmation_policy_template.md` | `references/confirmation_method_catalog.md`, `references/automation_recommendation_notes.md`, `references/evidence_and_measurement_notes.md` |
| 5 | `rules.md`, `steps/step_05_consistency_catalog_review_guide.md`, `templates/quality_criteria_catalog_template.md` | `references/quality_characteristic_scope_notes.md`, `references/confirmation_method_catalog.md` |

## 応答形式

```markdown
# Step X: <ステップ名>

## 使用した入力

-

## 成果物

<対象Stepの成果物>

## 確認事項

-

## 次に進む前のレビュー観点

-
```

## 完了条件

- Step 1からStep 5までの成果物が作成されている。
- 品質特性、対象、懸念、品質クライテリア、確認方法、根拠、未確認事項が追跡できる。
- 根拠のない基準値や確認方法が、事実として混入していない。
- 未確認事項が途中で消えず、最終成果物に引き継がれている。
