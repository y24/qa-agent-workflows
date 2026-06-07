---
description: rawソースをwikiへ統合する
argument-hint: <対象または質問>
---

# LLM Wiki ingest

User request:
{{arguments}}

## 目的

`raw/` のソースを読み、根拠を保ったまま `wiki/`、`index.md`、`log.md` に統合する。

## 手順

1. 対象ソースを特定し、既にingest済みか `log.md` と `index.md` で確認する。
2. ソースの主要事実、主張、エンティティ、概念、日付、未確認事項を抽出する。
3. `wiki/` に新規ページを作るか、既存ページを更新する。重要な記述には参照元を添える。
4. `index.md` の Sources と Wiki Pages を更新する。
5. `log.md` に `## [YYYY-MM-DD] ingest | <source>` 形式で追記する。

## ガードレール

- ソースにない内容は `推測:` と明記する。
- 矛盾を見つけた場合は上書きで消さず、矛盾として記録する。
- 大きな更新では、変更内容をユーザーへ要約して確認を待つ。
