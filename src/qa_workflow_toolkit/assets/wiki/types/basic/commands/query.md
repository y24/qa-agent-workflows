---
description: wikiを根拠に質問へ回答する
argument-hint: <対象または質問>
---

# LLM Wiki query

User request:
{{arguments}}

## 目的

`index.md` と `wiki/` の関連ページを優先して質問に回答し、根拠と未確認事項を明示する。

## 手順

1. `index.md` を読み、関連しそうなページとソースを特定する。
2. 必要な `wiki/` ページを読み、足りない場合のみ `raw/` の確認を提案または実施する。
3. 回答では、事実、推測、未確認事項を分けて書く。
4. 回答からwikiへ残す価値がある知見が生まれた場合は、更新候補を提示する。
5. `log.md` に `## [YYYY-MM-DD] query | <question>` 形式で追記する。
