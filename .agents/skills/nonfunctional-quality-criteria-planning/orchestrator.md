# orchestrator.md

# 非機能品質クライテリア策定・確認計画化 Orchestrator

## 目的

`$nonfunctional-quality-criteria-planning` の5Stepを順番に実行し、非機能関連情報、品質懸念、優先度、品質クライテリア、確認方針をIDで接続する。

複数Stepをユーザーが明示しない限り、一度に進めない。各Stepの出力後はレビュー待ちで停止する。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 入力文書整理・非機能関連情報抽出 | 入力文書 | `01_input_scope_summary.md` | `steps/step_01_input_scope_summary_guide.md` | `templates/input_scope_summary_template.md` |
| 2 | 品質懸念・リスク抽出 | Step 1成果物 | `02_quality_concern_register.md` | `steps/step_02_quality_concern_extraction_guide.md` | `templates/quality_concern_register_template.md` |
| 3 | 重要度評価・確認対象選別 | Step 2成果物 | `03_prioritized_quality_concern_register.md` | `steps/step_03_quality_concern_prioritization_guide.md` | `templates/prioritized_quality_concern_register_template.md` |
| 4 | 品質クライテリア策定 | Step 3成果物 | `04_quality_criteria_catalog.md` | `steps/step_04_quality_criteria_design_guide.md` | `templates/quality_criteria_catalog_template.md` |
| 5 | 確認方針・テスト計画化 | Step 4成果物 | `05_confirmation_policy_and_test_planning.md` | `steps/step_05_confirmation_policy_planning_guide.md` | `templates/confirmation_policy_and_test_planning_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 前Step成果物を主入力にし、元文書の再参照は根拠確認に必要な範囲へ限定する。
- 入力文書にない仕様、品質要求、リスク、数値目標、確認条件を事実として創作しない。
- 推測、仮説、確認事項、未確定事項は明示する。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。

## 共通参照

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`
- `../../../shared/output_style.md`
- `../../../shared/input_document_handling.md`
- `../../../shared/test_design_granularity_policy.md`

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 1 | `rules.md`, `steps/step_01_input_scope_summary_guide.md`, `templates/input_scope_summary_template.md` | `references/quality_characteristic_scope_notes.md` |
| 2 | `rules.md`, `steps/step_02_quality_concern_extraction_guide.md`, `templates/quality_concern_register_template.md` | `references/quality_characteristic_scope_notes.md` |
| 3 | `rules.md`, `steps/step_03_quality_concern_prioritization_guide.md`, `templates/prioritized_quality_concern_register_template.md` | `references/risk_and_concern_scale_definition.md` |
| 4 | `rules.md`, `steps/step_04_quality_criteria_design_guide.md`, `templates/quality_criteria_catalog_template.md` | `references/criteria_design_principles.md` |
| 5 | `rules.md`, `steps/step_05_confirmation_policy_planning_guide.md`, `templates/confirmation_policy_and_test_planning_template.md` | `references/confirmation_method_catalog.md`, `references/automation_recommendation_guide.md` |

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
- `Concern ID -> Criteria ID -> Confirmation ID` の対応が追跡できる。
- P0/P1の品質懸念が品質クライテリアと確認方針へ接続されている。
- テスト、レビュー、静的解析、運用確認、自動化方針への割り当て理由が説明されている。
- 未確認事項が途中で消えず、最終成果物に引き継がれている。
