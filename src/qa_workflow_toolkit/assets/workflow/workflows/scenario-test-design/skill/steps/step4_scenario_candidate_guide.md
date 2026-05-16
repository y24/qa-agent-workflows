# step4_scenario_candidate_guide.md

# Step 4: シナリオ候補の設計ガイド

## 目的

`03_scenario_viewpoints.md` をもとに、詳細テストケース化の候補となる業務シナリオを設計する。

このStepでは詳細な操作手順、具体的な入力値、期待結果の全文までは作成しない。

## 入力

- `03_scenario_viewpoints.md`
- `02_business_flows.md`
- `01_input_summary.md`
- `rules.md`

## 出力

- `04_scenario_candidates.md`
- 形式: `templates/04_scenario_candidates_template.md`

## 手順

1. 高重要度の観点と重要フローを確認する。
2. 観点を業務フロー単位に束ね、中核正常系、分岐、例外、データ状態、ロール・権限、出力・連携、締め・取消・再実行、過去不具合再現の候補を設計する。
3. 各シナリオ候補に Scenario ID、種類、業務目的、対象ロール、前提条件、使用データ概要、大まかな流れ、確認ポイントを付与する。
4. 関連Flow ID、Use Scene ID、Viewpoint ID、データ状態、リスク、根拠を紐づける。
5. 優先度、採用判断、統合・除外候補を整理する。
6. 未カバー観点と確認事項を記録し、Step 5へ引き継ぐ。

## 判断基準

- シナリオ候補の種類、粒度、優先度、採用判断: `references/scenario_candidate_policy.md`
- 観点粒度: `references/scenario_viewpoint_policy.md`

## このStepでやらないこと

- 詳細テストケースの作成
- 画面単位の詳細操作手順
- 具体的なテストデータ値の大量作成
- 期待結果の文言・表示値の詳細化
- 根拠のないシナリオの断定

## 完了条件

- シナリオ候補に Scenario ID、関連Flow ID、関連Viewpoint ID、優先度、採用判断がある
- 中核正常系、重要分岐、例外、データ状態、ロール・権限、出力・連携が必要範囲でカバーされている
- 未カバー観点、統合・除外候補、確認事項が明示されている
- Step 5でテストケース化できる粒度になっている

## 停止

`04_scenario_candidates.md` を出力したら停止する。ユーザーから明示的な指示があるまで Step 5 へ進まない。
