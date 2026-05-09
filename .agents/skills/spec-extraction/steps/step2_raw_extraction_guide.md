# step2_raw_extraction_guide.md

# Step 2: 事実情報の抽出ガイド

## 目的

`document_inventory.md` と入力文書をもとに、テスト設計に使いうる原文ベースの事実情報を抽出する。

このStepでは抽出情報を正規化・統合しない。原文に基づく生情報を、根拠付きで残す。

## 入力

- `document_inventory.md`
- 対象入力文書
- `rules.md`

## 出力

- `raw_extraction.md`
- 形式: `templates/raw_extraction_template.md`

## 手順

1. 抽出対象範囲を確認する。
2. 機能、画面、項目、API、バッチ、データ、業務ルール、バリデーション、状態遷移、計算、権限、例外、非機能、未解決事項などを抽出する。
3. 各抽出項目に Raw ID、カテゴリ、原文要約、参照元、確度、状態を付与する。
4. 曖昧・未確定な記述、抽出しなかった情報、未処理範囲を記録する。
5. Step 3で正規化すべき重複、表記揺れ、矛盾候補を引き継ぐ。

## 判断基準

- 抽出カテゴリ: `references/extraction_category_definitions.md`
- 抽出時の根拠・確度: `references/evidence_and_confidence_rules.md`
- 推測禁止: `references/anti_hallucination_rules.md`

## このStepでやらないこと

- 仕様の統合・正規化
- 矛盾の独断解消
- 不足仕様の補完
- 詳細テストケース作成

## 完了条件

- 抽出情報が Raw ID と参照元を持つ
- 推測、曖昧、未確定、根拠弱の情報が区別されている
- Step 3で正規化すべき候補が整理されている

## 停止

`raw_extraction.md` を出力したら停止する。ユーザーから明示的な指示があるまで Step 3 へ進まない。
