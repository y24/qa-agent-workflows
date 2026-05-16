# step5_testcase_detail_guide.md

# Step 5: テストケース化・優先度付けガイド

## 目的

`04_scenario_candidates.md` をもとに、実行可能なテストケースへ詳細化し、優先度とトレーサビリティを整理する。

## 入力

- `04_scenario_candidates.md`
- `03_scenario_viewpoints.md`
- `02_business_flows.md`
- `rules.md`

## 出力

- `05_test_cases.md`
- 形式: `templates/05_test_cases_template.md`

## 手順

1. 採用候補シナリオを確認し、テストケース化する対象を決める。
2. 各テストケースに TC ID、対応Scenario ID、Viewpoint ID、Flow ID、目的、前提条件、テストデータ条件、手順概要、期待結果概要を付与する。
3. 優先度、テスト種別、実行観点、関連リスク、根拠を整理する。
4. P0/P1や重要業務フローは、必要に応じて正常系、分岐、例外、境界、状態、ロール差、出力・連携に分ける。
5. 詳細化しすぎる具体値、文言完全一致、画面操作細部は、必要事項として引き継ぐ。
6. シナリオ候補、観点、フロー、テストケースの対応表を作成する。
7. 未テスト、対象外、保留、代替確認を理由付きで整理する。

## 判断基準

- テストケース粒度、分割・統合、期待結果、優先度: `references/testcase_detail_policy.md`
- レビュー観点: `references/review_policy.md`

## このStepでやらないこと

- テスト管理ツール固有の登録形式への変換
- 自動化スクリプト作成
- テスト実行スケジュールや担当者割り当て
- 入力文書にない画面操作、文言、データ値の断定

## 完了条件

- テストケースが実行可能な概要粒度で整理されている
- TC ID と Scenario ID / Viewpoint ID / Flow ID の対応が追跡できる
- 優先度と理由が記載されている
- 未テスト、対象外、保留、代替確認の扱いが明示されている
- 詳細テスト設計や実行準備へ渡せる確認事項が残っている

## 停止

`05_test_cases.md` を出力したら、この skill の主要Stepは完了とする。
