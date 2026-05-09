# step_04_quality_criteria_design_guide.md

# Step 4: 品質クライテリア策定ガイド

## 目的

Step 3でクライテリア化対象となった品質懸念について、「何を満たせば品質上許容できるか」を定義する。

## 入力

- `03_prioritized_quality_concern_register.md`
- 対応する入力文書、前Stepの根拠、既存非機能要件

## 出力

- `04_quality_criteria_catalog.md`
- 形式: `templates/quality_criteria_catalog_template.md`

## 手順

1. P0/P1を優先し、必要に応じてP2の一部も対象にする。
2. 対象機能、画面、処理、データ、運用、環境条件を明確にする。
3. 品質クライテリアを、観測・判定できる表現にする。
4. 判定基準、目標値、許容範囲は入力根拠を確認して書く。根拠がない場合は未確定にする。
5. 測定・確認方法の候補は短く記録するが、詳細な計画化はStep 5に残す。
6. 対応する品質懸念ID、根拠、未確定事項を必ず残す。
7. クライテリア化しない懸念は、理由と後続での扱いを記録する。

## 判断基準

- クライテリアの書き方、数値基準、未確定事項: `references/criteria_design_principles.md`
- 品質特性の範囲: `references/quality_characteristic_scope_notes.md`

## このStepでやらないこと

- 詳細な確認手順やテストケース作成
- 自動化推奨度の詳細判断
- 入力にない数値基準の断定
- 低優先度懸念の過剰なクライテリア化

## 完了条件

- 各クライテリアが対応する品質懸念IDを持つ。
- 対象、条件、判定基準、根拠、未確定事項が明示されている。
- 数値目標の根拠有無が区別されている。
- Step 5で確認方針を設計できる粒度になっている。

## 停止

`04_quality_criteria_catalog.md` を出力したら停止する。ユーザーから明示的な指示があるまで Step 5 へ進まない。
