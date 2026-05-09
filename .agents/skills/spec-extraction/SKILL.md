---
name: spec-extraction
description: Use when extracting, normalizing, and reviewing test-design inputs from development documents, requirements, screen specs, API specs, design notes, or domain documents. Do not use to create detailed test cases directly.
---

# 仕様抽出 skill

## 目的

開発文書から事実を抽出し、後続のQA設計で使えるように、根拠付きで正規化された入力情報へ整理する。

## 入力

- 要件、設計書、画面仕様、API仕様、ドメインルール、リリースノート、その他の開発文書
- ユーザーが指定した文書スコープや優先度

## 出力

- `document_inventory.md`
- `raw_extraction.md`
- `normalized_spec_inventory.md`
- `test_design_input_catalog.md`
- `gap_and_review_report.md`

## ワークフロー

1. 文書インベントリ作成
2. 原文ベースの事実抽出
3. 正規化と統合
4. テスト設計入力カタログ化
5. ギャップとレビュー事項の整理

ユーザーが明示的に継続を指示しない限り、各ステップ完了後に停止し、レビューを待つ。

## 参照ファイル

- 共通ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- 証拠・分類・正規化の基準: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 不足している仕様を事実として推測補完しない。
- 情報源、証拠、IDのトレーサビリティを維持する。
- この skill では詳細テストケースを作成しない。
- 矛盾、欠落、粒度不足は明示的に記録する。
