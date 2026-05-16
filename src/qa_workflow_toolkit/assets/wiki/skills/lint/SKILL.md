---
name: lint
description: Use when checking the health and consistency of the LLM wiki.
---

# lint skill

## 目的

wikiの矛盾、根拠不足、索引漏れ、孤立ページ、古い記述、未解決事項を点検する。

## 点検観点

- `index.md` に存在しない `wiki/` ページがないか。
- `index.md` に存在するが実体のないページがないか。
- 重要概念が複数ページで矛盾していないか。
- 根拠リンクや参照元が不足していないか。
- `log.md` の最近のingest結果がwikiに反映されているか。

## 出力

指摘は優先度、対象ファイル、根拠、提案修正に分けて整理する。
`log.md` に `## [YYYY-MM-DD] lint | <scope>` 形式で追記する。
