# step3_normalization_guide.md

# Step 3: 正規化・統合ガイド

## 目的

`raw_extraction.md` の生情報を、重複、表記揺れ、関連情報、矛盾、不足を整理し、後続Stepで扱いやすい正規化仕様一覧にする。

このStepでは矛盾を勝手に解消せず、詳細テストケースも作らない。

## 入力

- `raw_extraction.md`
- `document_inventory.md`
- `rules.md`

## 出力

- `normalized_spec_inventory.md`
- 形式: `templates/normalized_spec_inventory_template.md`

## 手順

1. Raw IDを確認し、同一仕様、関連仕様、別仕様を判断する。
2. 表記揺れ、用語違い、重複、旧版由来、参考資料由来を整理する。
3. 正規化仕様に Spec ID、カテゴリ、仕様内容、状態、確度、参照Raw ID、参照元を付与する。
4. 矛盾、不足、粒度不足、未確定、根拠弱の仕様を分離する。
5. Step 4でテスト設計インプット化できる仕様と、断定してはいけない仕様を引き継ぐ。

## 判断基準

- 正規化・統合・状態管理: `references/normalization_rules.md`
- 根拠と確度: `references/evidence_and_confidence_rules.md`
- 推測禁止と矛盾扱い: `references/anti_hallucination_rules.md`

## このStepでやらないこと

- 矛盾の独断解消
- 入力にない仕様値の補完
- テストケース作成
- 期待結果の断定

## 完了条件

- 正規化仕様に Spec ID、参照Raw ID、参照元がある
- 統合、表記揺れ、矛盾、不足、未確定、根拠弱が区別されている
- Step 4への引き継ぎが整理されている

## 停止

`normalized_spec_inventory.md` を出力したら停止する。ユーザーから明示的な指示があるまで Step 4 へ進まない。
