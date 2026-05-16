# step4_test_design_input_guide.md

# Step 4: テスト設計インプット化ガイド

## 目的

`normalized_spec_inventory.md` をもとに、後続のテスト設計で利用できる確認対象、条件、観点、リスク、注意事項を整理する。

このStepでは詳細テストケースを作成しない。

## 入力

- `normalized_spec_inventory.md`
- `raw_extraction.md`
- `document_inventory.md`
- `rules.md`

## 出力

- `test_design_input_catalog.md`
- 形式: `templates/test_design_input_catalog_template.md`

## 手順

1. テスト設計インプット化できる仕様を選別する。
2. テスト対象、確認すべき仕様、テスト観点、条件・前提、入力データ観点、期待結果の種類を整理する。
3. 関連コンポーネント、優先度、リスク、根拠、確度を付与する。
4. 仕様未確定、矛盾あり、期待結果を断定してはいけない項目を分離する。
5. Step 5でレビューすべきギャップ、優先確認事項、注意事項を引き継ぐ。

## 判断基準

- テスト設計インプット化と優先度: `references/test_design_input_policy.md`
- 期待結果・入力データの制限: `references/anti_hallucination_rules.md`

## このStepでやらないこと

- 具体的なテストケース、操作手順、具体値データの作成
- 入力文書にない期待結果の断定
- 矛盾や未確定事項の解消

## 完了条件

- Test Design Input ID が付与されている
- Spec ID、Raw ID、参照元への追跡が残っている
- 後続テスト設計で使う観点と注意事項が整理されている
- 断定禁止・確認事項が分離されている

## 停止

`test_design_input_catalog.md` を出力したら停止する。ユーザーから明示的な指示があるまで Step 5 へ進まない。
