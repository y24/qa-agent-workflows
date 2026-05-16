# defect-analysis Orchestrator

## 目的

`$defect-analysis` の5Stepを順番に実行し、不具合チケットを後続テスト設計で使える知見へ変換する。

複数Stepをユーザーが明示しない限り、一度に進めない。各Stepの出力後はレビュー待ちで停止する。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 分析対象スコープ整理 | 不具合チケット一覧、項目定義、対象範囲 | `01_analysis_scope_summary.md` | `steps/step_01_analysis_scope_guide.md` | `templates/analysis_scope_summary_template.md` |
| 2 | 不具合ファクト抽出・正規化 | Step 1成果物、対象チケット | `02_defect_fact_table.md` | `steps/step_02_defect_fact_extraction_guide.md` | `templates/defect_fact_table_template.md` |
| 3 | 不具合分類・傾向集計 | Step 2成果物 | `03_defect_trend_analysis.md` | `steps/step_03_defect_classification_trend_guide.md` | `templates/defect_trend_analysis_template.md` |
| 4 | 品質リスク・弱点パターン抽出 | Step 3成果物、代表チケット | `04_quality_risk_insights.md` | `steps/step_04_quality_risk_insight_guide.md` | `templates/quality_risk_insight_template.md` |
| 5 | 後続テスト設計向けガイダンス化 | Step 4成果物、既存テスト資産 | `05_test_design_guidance.md` | `steps/step_05_test_design_guidance_guide.md` | `templates/test_design_guidance_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 前Step成果物を主入力にし、元チケットの再参照は根拠確認に必要な範囲へ限定する。
- チケットにない原因、仕様、期待結果、テスト条件を事実として創作しない。
- 推測、仮説、確認事項、未確定事項は明示する。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。

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
| 1 | `rules.md`, `steps/step_01_analysis_scope_guide.md`, `templates/analysis_scope_summary_template.md` | `templates/issue_log_template.md` |
| 2 | `rules.md`, `steps/step_02_defect_fact_extraction_guide.md`, `templates/defect_fact_table_template.md` | `references/defect_classification_taxonomy.md` |
| 3 | `rules.md`, `steps/step_03_defect_classification_trend_guide.md`, `templates/defect_trend_analysis_template.md` | `references/defect_classification_taxonomy.md` |
| 4 | `rules.md`, `steps/step_04_quality_risk_insight_guide.md`, `templates/quality_risk_insight_template.md` | `references/insight_interpretation_policy.md` |
| 5 | `rules.md`, `steps/step_05_test_design_guidance_guide.md`, `templates/test_design_guidance_template.md` | `references/test_design_mapping_notes.md` |

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
- `Ticket ID -> Defect ID -> Trend ID -> Risk ID -> Guidance ID` の対応を追跡できる。
- 根拠チケットIDがない品質リスクやテスト設計示唆は、推測または仮説として分離されている。
- 未確認事項、除外条件、情報不足、分類保留が最終成果物に引き継がれている。
