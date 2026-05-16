# step5_testcase_outline_guide.md

# Step 5: テストケース骨子・トレーサビリティ作成ガイド

## 目的

`04_risk_based_test_strategy.md` をもとに、リスクベースドテストのテストケース骨子とトレーサビリティを作成する。

このStepでは詳細な画面操作、具体的な入力値、メッセージ文言までは作成しない。詳細テストケース作成工程へ渡せる骨子に留める。

## 入力

- `04_risk_based_test_strategy.md`
- `03_risk_register.md`
- `rules.md`
- 必要に応じて `02_risk_candidate_list.md`、`01_input_scope_summary.md`、元文書の該当箇所

## 出力

- `05_testcase_outline_and_traceability.md`
- 形式: `templates/testcase_traceability_template.md`

## 手順

1. Step 4のテスト観点を、どの条件で何を確認するかが分かるテストケース骨子へ変換する。
2. 優先度に応じてテストケース数と粒度を調整する。P0/P1は明示的に残し、P2/P3は統合・簡易化を検討する。
3. TC ID、テストケース名、対応Risk ID、対応Viewpoint ID、目的、前提条件、入力条件・操作条件、期待結果概要、実行優先度、備考を整理する。
4. 1つのケースに複数リスクを統合する場合は、統合理由と注意点を記録する。
5. 未カバーリスク、対象外、代替確認、保留、受容を理由付きで整理する。
6. `Risk ID -> Viewpoint ID -> TC ID` の対応表を作成する。
7. 詳細テストケース化時に確認すべきテストデータ、期待結果、画面操作、未解決仕様を引き継ぐ。

## 判断基準

- 骨子粒度、分割・統合、カバレッジ: `references/testcase_outline_policy.md`
- レビュー観点: `references/review_checklist.md`

## このStepでやらないこと

- 詳細な画面操作手順の作成
- 具体的なテストデータ値の大量作成
- エラーメッセージ文言の完全一致定義
- 自動化スクリプト、実行スケジュール、工数見積り、担当者割り当て
- テスト管理ツールへの登録形式変換

## 完了条件

- テストケース骨子に TC ID、対応Risk ID、対応Viewpoint ID、目的、前提条件、入力条件、期待結果概要、実行優先度がある
- リスク、観点、テストケースの対応関係が追跡できる
- P0/P1リスクのカバレッジが確認されている
- 未カバーリスク、統合・簡略化した確認、詳細化時の注意事項が整理されている

## 停止

`05_testcase_outline_and_traceability.md` を出力したら、この skill の主要Stepは完了とする。必要な次工程は詳細テストケース作成、テストデータ設計、実行順序設計、レビュー、管理ツール投入用変換として扱う。
