---
description: .tempのファイルをraw向けMarkdownへ変換する
argument-hint: <対象または質問>
---

# LLM Wiki convert

User request:
{{arguments}}

## 目的

`.temp/` に置かれた変換前ファイルを `markitdown` コマンドでMarkdownへ変換し、`raw/` に配置する。

## 手順

1. `.temp/` の対象ファイルを確認する。
2. 出力先を `raw/<元ファイル名のstem>.md` として決める。
3. `markitdown "<input>" -o "<output>"` を実行する。
4. 変換後のMarkdownを軽く確認し、明らかな変換欠落や文字化けを記録する。
5. `log.md` に `## [YYYY-MM-DD] convert | <file>` 形式で追記する。

## ガードレール

- `raw/` に同名ファイルがある場合、ユーザー確認なしに上書きしない。
- `markitdown` が利用できない場合は、インストールが必要なことを報告し、代替変換を勝手に実行しない。
