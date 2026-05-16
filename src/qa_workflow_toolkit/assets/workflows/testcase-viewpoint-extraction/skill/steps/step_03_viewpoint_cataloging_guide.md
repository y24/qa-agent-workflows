# step_03_viewpoint_cataloging_guide.md

# Step 03: 抽象観点カタログ化ガイド

## 目的

`02_intent_and_viewpoint_candidates.md` の観点候補を、再利用可能な抽象観点カタログへ統合・分類する。

## 入力

- `02_intent_and_viewpoint_candidates.md`
- `02_extraction_issues.md`
- `01_testcase_inventory.md`
- `rules.md`

## 出力

- `03_viewpoint_catalog.md`
- `03_cataloging_issues.md`
- 形式: `templates/viewpoint_catalog_template.md`, `templates/issue_log_template.md`

## 手順

1. 類似する観点候補を確認し、同一観点、関連観点、別観点を判断する。
2. 抽象観点に Viewpoint ID、観点名、カテゴリ、説明、適用条件、期待される確認、根拠TCを付与する。
3. 抽象化しすぎ、個別名の残しすぎ、根拠不足を調整する。
4. カテゴリを付与し、分類保留やレビュー要の観点を issue に残す。
5. Step 04で確認すべき未対応候補、低確度観点、レビュー推奨事項を引き継ぐ。

## 判断基準

- 抽象化レベル、統合・分割: `references/abstraction_policy.md`
- 観点カテゴリ: `references/viewpoint_category_seed.md`
- 曖昧さとレビュー要否: `references/ambiguity_policy.md`

## このStepでやらないこと

- 根拠TCのない観点を確定扱いする
- 新規観点を要件から創作する
- 詳細テストケースを作成する

## 完了条件

- 抽象観点に Viewpoint ID、カテゴリ、根拠TC、推定度、レビュー要否がある
- 観点候補との対応が追跡できる
- 未対応・保留・レビュー要の観点が issue に残っている

## 停止

`03_viewpoint_catalog.md` と `03_cataloging_issues.md` を出力したら停止する。
