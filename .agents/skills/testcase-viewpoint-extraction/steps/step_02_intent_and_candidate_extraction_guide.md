# step_02_intent_and_candidate_extraction_guide.md

# Step 02: 意図・観点候補の抽出ガイド

## 目的

`01_testcase_inventory.md` をもとに、各テストケースのテスト意図と観点候補を抽出する。

このStepでは抽象観点カタログへ統合しない。

## 入力

- `01_testcase_inventory.md`
- `01_input_issues.md`
- `rules.md`

## 出力

- `02_intent_and_viewpoint_candidates.md`
- `02_extraction_issues.md`
- 形式: `templates/intent_and_candidate_template.md`, `templates/issue_log_template.md`

## 手順

1. 各TCの前提、操作、期待結果から主意図と副次意図を読み取る。
2. 意図ごとに観点候補、根拠TC、推定度、レビュー要否を付与する。
3. 低確度、曖昧、根拠不足、複数解釈は issue に記録する。
4. Step 03で抽象化・統合すべき候補を引き継ぐ。

## 判断基準

- 意図・観点候補の定義: `references/definitions.md`
- 曖昧さ・推定度・レビュー要否: `references/ambiguity_policy.md`
- 抽象化前の候補粒度: `references/abstraction_policy.md`

## このStepでやらないこと

- 抽象観点IDの確定
- 観点カテゴリの最終分類
- 根拠TCのない観点の確定
- 新しいテストケース作成

## 完了条件

- 各候補に根拠TC、意図、観点候補、推定度、レビュー要否がある
- 曖昧な候補や根拠不足が issue に残っている
- Step 03で統合・抽象化できる候補一覧になっている

## 停止

`02_intent_and_viewpoint_candidates.md` と `02_extraction_issues.md` を出力したら停止する。
