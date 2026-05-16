# step5_gap_review_guide.md

# Step 5: 不明点・矛盾・不足のレビューガイド

## 目的

これまでの成果物を確認し、テスト設計前に解消または引き継ぐべきギャップ、矛盾、不足、曖昧さ、未確定事項を整理する。

## 入力

- `document_inventory.md`
- `raw_extraction.md`
- `normalized_spec_inventory.md`
- `test_design_input_catalog.md`
- `rules.md`

## 出力

- `gap_and_review_report.md`
- 形式: `templates/gap_and_review_report_template.md`

## 手順

1. 各成果物の未確定、矛盾、不足、粒度不足、根拠弱、未処理範囲を確認する。
2. ギャップに Gap ID、種別、関連ID、内容、影響、優先度、推奨対応を付与する。
3. 優先度Highの確認事項、矛盾一覧、不足一覧、曖昧な記述、未確定事項、参照元が弱い情報を整理する。
4. 後続テスト設計で断定してはいけない項目と、確認後に更新すべき成果物を明示する。
5. 最終的な引き継ぎ事項と完了判定をまとめる。

## 判断基準

- ギャップ分類、優先度、レビュー観点: `references/gap_review_policy.md`
- 推測禁止、矛盾扱い: `references/anti_hallucination_rules.md`

## このStepでやらないこと

- ギャップの独断解消
- 詳細テストケース作成
- 仕様未確定事項の補完

## 完了条件

- ギャップ、矛盾、不足、曖昧さ、未確定事項が一覧化されている
- 後続テスト設計で断定してはいけない事項が明示されている
- 更新が必要な成果物と確認先が整理されている

## 停止

`gap_and_review_report.md` を出力したら、この skill の主要Stepは完了とする。
