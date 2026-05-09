# step_01_input_normalization_guide.md

# Step 01: 入力整理・テストケース正規化ガイド

## 目的

既存テストケースを棚卸しし、後続Stepで意図・観点を抽出できる形へ正規化する。

このStepでは意図抽出、観点候補化、抽象観点化を行わない。

## 入力

- 既存テストケース一覧、手順、期待結果、テスト管理ツール出力
- 必要に応じて関連仕様、画面仕様、要件

## 出力

- `01_testcase_inventory.md`
- `01_input_issues.md`
- 形式: `templates/testcase_inventory_template.md`, `templates/issue_log_template.md`

## 手順

1. 入力ファイル、対象範囲、未処理範囲を整理する。
2. 各テストケースに TC ID、名称、前提、手順、期待結果、関連仕様、状態を付与する。
3. 重複、欠落、曖昧、粒度不揃い、根拠不足を issue として記録する。
4. 後続Stepで使う正規化済みテストケース一覧を作成する。

## 判断基準

- 用語定義: `references/definitions.md`
- 曖昧さとissue化: `references/ambiguity_policy.md`
- 入力正規化・大量ケース分割: `references/input_normalization_policy.md`

## このStepでやらないこと

- テスト意図の推定
- 観点候補の抽出
- 抽象観点カタログ化
- 根拠のない仕様補完

## 完了条件

- 正規化済みテストケースに TC ID と元入力への追跡がある
- 欠落、曖昧、重複、未処理範囲が issue として記録されている
- Step 02で意図抽出に使える粒度になっている

## 停止

`01_testcase_inventory.md` と `01_input_issues.md` を出力したら停止する。
