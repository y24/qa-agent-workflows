# システムテスト戦略策定 Orchestrator

## 目的

`$system-test-strategy-planning` の5Stepを順番に実行し、開発文書からシステムテスト戦略、テスト種別、テスト観点、付属マトリクスへ段階的につなぐ。

複数Stepをユーザーが明示しない限り、一度に進めない。各Stepの出力後はレビュー待ちで停止する。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 入力文書整理・対象スコープ確認 | 入力文書 | `01_input_scope_summary.md` | `steps/step_01_input_scope_summary_guide.md` | `templates/input_scope_summary_template.md` |
| 2 | カバレッジ候補抽出 | Step 1成果物 | `02_system_test_coverage_analysis.md` | `steps/step_02_coverage_analysis_guide.md` | `templates/system_test_coverage_analysis_template.md` |
| 3 | テスト種別選定・戦略整理 | Step 2成果物 | `03_test_type_strategy.md` | `steps/step_03_test_type_strategy_guide.md` | `templates/test_type_strategy_template.md` |
| 4 | テスト観点策定 | Step 3成果物 | `04_test_viewpoint_policy.md` | `steps/step_04_test_viewpoint_policy_guide.md` | `templates/test_viewpoint_policy_template.md` |
| 5 | 戦略計画書・付属資料最終化 | Step 4成果物 | `05_system_test_strategy_plan.md`, `appendix_quality_characteristic_matrix.md`, `appendix_viewpoint_traceability.md` | `steps/step_05_final_packaging_guide.md` | `templates/system_test_strategy_plan_template.md`, `templates/quality_characteristic_matrix_template.md`, `templates/viewpoint_traceability_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 前Step成果物を主入力にし、元文書の再参照は根拠確認に必要な範囲へ限定する。
- 入力文書にない要件、非機能要求、テスト種別、テスト観点、環境、閾値、テスト条件を事実として創作しない。
- 推測、仮説、確認事項、未確定事項は明示する。ただし、根拠のない仮説を最終方針へ採用しない。
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
| 1 | `rules.md`, `steps/step_01_input_scope_summary_guide.md`, `templates/input_scope_summary_template.md` | `references/system_test_scope_policy.md` |
| 2 | `rules.md`, `steps/step_02_coverage_analysis_guide.md`, `templates/system_test_coverage_analysis_template.md` | `references/iso25010_quality_characteristics.md`, `references/system_test_scope_policy.md` |
| 3 | `rules.md`, `steps/step_03_test_type_strategy_guide.md`, `templates/test_type_strategy_template.md` | `references/test_type_catalog.md`, `references/iso25010_quality_characteristics.md` |
| 4 | `rules.md`, `steps/step_04_test_viewpoint_policy_guide.md`, `templates/test_viewpoint_policy_template.md` | `references/viewpoint_traceability_policy.md`, `references/test_type_catalog.md` |
| 5 | `rules.md`, `steps/step_05_final_packaging_guide.md`, final templates | `references/iso25010_quality_characteristics.md`, `references/viewpoint_traceability_policy.md` |

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
- システムテスト計画書の戦略部分として、対象、対象外、非機能カバレッジ、テスト種別、テスト観点、品質特性マトリクス、観点トレーサビリティが説明されている。
- 各テスト観点に、根拠となる入力文書または前段成果物IDが紐づいている。
- 入力に根拠のない補完が、最終方針として混入していない。
- 具体的なテストケース、スケジュール、体制、工数が成果物に含まれていない。
