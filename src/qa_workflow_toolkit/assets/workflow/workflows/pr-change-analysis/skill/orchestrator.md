# pr-change-analysis Orchestrator

## 目的

`$pr-change-analysis` の4Stepを順番に実行し、Azure DevOpsのPull Requestを、QAが読める差分レポートと、リスク・テスト観点の分析レポートへ変換する。

入力PRは複数の場合がある。Step 2とStep 3はPRごとに繰り返し、Step 4で横断的に集約する。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 対象PR特定・情報収集スコープ整理 | PR URL群、ユーザー指定 | `00_collection_plan.md` | `steps/step_01_collection_scope_guide.md` | `templates/collection_plan_template.md` |
| 2 | 全PRの変更内容理解・差分レポート作成 | Step 1成果物、各PRのMCP取得結果 | 各PR `<pr-slug>/diff_report.md` | `steps/step_02_change_comprehension_diff_report_guide.md` | `templates/diff_report_template.md` |
| 3 | PRごとのリスク・テスト観点分析 | Step 2成果物、必要時に元差分 | 各PR `<pr-slug>/analysis_report.md` | `steps/step_03_risk_and_test_viewpoint_guide.md` | `templates/analysis_report_template.md` |
| 4 | 横断サマリ作成（複数PR時のみ） | Step 2・3成果物 | `summary.md` | `steps/step_04_cross_pr_summary_guide.md` | `templates/cross_pr_summary_template.md` |

## 進行と停止ルール

- Step 1からStep 2までは一気に進めてよい。すなわち、収集計画を立て、対象PRすべての差分レポートを作成するところまで停止せずに進められる。
- 全PRの差分レポートを出力したら停止し、レビューを待つ。
- Step 3（全PRのリスク・テスト観点分析）の前後で停止する。ユーザーの続行指示があるまでStep 4へ進まない。
- 対象PRが1件のときはStep 4を省略するか、`summary.md` をそのPRの要約に縮退してよい。
- 現在のStepに必要なファイルだけを参照する。前Step成果物を主入力にし、元差分の再取得は根拠確認に必要な範囲へ限定する。
- 差分・Description・コメント・作業項目にない挙動、意図、原因、テスト条件を創作しない。
- 推測、仮説、確認事項、未確定事項、取得できなかった範囲は明示する。

## MCP取得ルール

- Azure DevOps の情報取得はすべて `references/azure_devops_mcp_usage.md` のツールと手順に従う。
- 取得失敗、権限不足、差分が大きすぎる、バイナリ等は捏造で埋めず、`issue_log.md` とレポートのカバー範囲に記録する。

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
| 1 | `rules.md`, `steps/step_01_collection_scope_guide.md`, `templates/collection_plan_template.md`, `references/azure_devops_mcp_usage.md` | `templates/issue_log_template.md` |
| 2 | `rules.md`, `steps/step_02_change_comprehension_diff_report_guide.md`, `templates/diff_report_template.md`, `references/azure_devops_mcp_usage.md`, `references/qa_translation_guide.md`, `references/change_type_taxonomy.md` | `templates/issue_log_template.md` |
| 3 | `rules.md`, `steps/step_03_risk_and_test_viewpoint_guide.md`, `templates/analysis_report_template.md`, `references/nonfunctional_risk_catalog.md` | `references/qa_translation_guide.md` |
| 4 | `rules.md`, `steps/step_04_cross_pr_summary_guide.md`, `templates/cross_pr_summary_template.md` | `references/nonfunctional_risk_catalog.md` |

## 応答形式

```markdown
# Step X: <ステップ名>

## 使用した入力

-

## 取得・カバー範囲

- 取得できたもの:
- 取得できなかった/制限があったもの:

## 成果物

<対象Stepの成果物（PRごとの場合はPR単位で示す）>

## 確認事項

-

## 次に進む前のレビュー観点

-
```

## 完了条件

- Step 1からStep 3までの成果物が、対象PRごとに作成されている。
- 対象PRが複数の場合、Step 4の `summary.md` が作成されている。
- `PR -> Change ID -> Risk ID -> Viewpoint ID` の対応を追跡できる。
- 根拠となる変更箇所がないリスク・観点は、推測または仮説として分離されている。
- 取得できなかった範囲、情報不足、確認事項が最終成果物と `issue_log.md` に引き継がれている。
