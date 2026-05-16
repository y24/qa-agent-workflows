# step3_scenario_viewpoint_guide.md

# Step 3: シナリオ観点の抽出ガイド

## 目的

`02_business_flows.md` をもとに、シナリオ候補設計で扱うべき抽象的な確認観点を整理する。

このStepではシナリオ候補やテストケースを作成しない。

## 入力

- `02_business_flows.md`
- `01_input_summary.md`
- `rules.md`
- 必要に応じて元文書の該当箇所

## 出力

- `03_scenario_viewpoints.md`
- 形式: `templates/03_scenario_viewpoints_template.md`

## 手順

1. 重要な業務フロー、利用シーン、分岐・例外、データ状態を確認する。
2. 業務目的、状態変化、ロール・権限、データ整合性、出力・連携、例外、過去不具合の観点を抽出する。
3. 各観点に Viewpoint ID、カテゴリ、関連フロー、関連利用シーン、確認したいこと、重要な理由、根拠を付与する。
4. 観点を粗すぎず細かすぎない粒度へ調整する。
5. 未カバー・保留観点、確認事項、Step 4への引き継ぎを整理する。

## 判断基準

- 観点カテゴリ、粒度、重要度: `references/scenario_viewpoint_policy.md`
- 業務フロー粒度の前提: `references/business_flow_policy.md`

## このStepでやらないこと

- シナリオ候補の具体化
- テスト手順や期待結果の作成
- 具体的なテストデータ値の作成
- 入力にない業務ルールの補完

## 完了条件

- シナリオ観点に Viewpoint ID があり、BF ID / US ID と紐づいている
- 観点の重要理由と根拠が記載されている
- Step 4でシナリオ候補に変換できる粒度になっている
- 未カバー・保留観点と確認事項が明示されている

## 停止

`03_scenario_viewpoints.md` を出力したら停止する。ユーザーから明示的な指示があるまで Step 4 へ進まない。
