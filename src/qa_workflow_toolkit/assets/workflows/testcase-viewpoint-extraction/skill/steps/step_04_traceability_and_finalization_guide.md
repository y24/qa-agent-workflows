# step_04_traceability_and_finalization_guide.md

# Step 04: トレーサビリティ確認・最終化ガイド

## 目的

テストケース、意図、観点候補、抽象観点の対応関係を確認し、最終成果物として整理する。

## 入力

- `01_testcase_inventory.md`
- `02_intent_and_viewpoint_candidates.md`
- `03_viewpoint_catalog.md`
- 各 issue ファイル
- `rules.md`

## 出力

- `04_final_traceability_matrix.md`
- `04_final_issue_log.md`
- `04_final_summary.md`
- 形式: `templates/traceability_matrix_template.md`, `templates/issue_log_template.md`

## 手順

1. `TC ID -> Intent ID -> Candidate ID -> Viewpoint ID` の対応を確認する。
2. 根拠TCのない抽象観点、未対応候補、低推定度、レビュー要の項目を整理する。
3. issue を統合し、解決済み・対応不要・未解決を分ける。
4. 最終トレーサビリティ表、最終issue log、最終サマリを作成する。
5. 除外・保留・レビュー推奨の理由を明示する。

## 判断基準

- トレーサビリティと最終化: `references/finalization_policy.md`
- issue統合: `references/ambiguity_policy.md`
- 用語定義: `references/definitions.md`

## このStepでやらないこと

- 新しい観点の追加
- 根拠のない観点の確定
- 低推定度の内容の断定
- issue の隠蔽

## 完了条件

- 最終トレーサビリティで TC、意図、候補、観点が追跡できる
- 未対応、除外、保留、レビュー要が説明されている
- 最終サマリに利用上の注意と次アクションがある

## 停止

最終3成果物を出力したら、この skill の主要Stepは完了とする。
