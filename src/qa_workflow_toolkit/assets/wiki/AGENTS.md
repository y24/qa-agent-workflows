<!-- generated-by: qa-workflow-toolkit -->
<!-- wiki-name: [[wiki_name]] -->

# [[wiki_name]] LLM Wiki

このリポジトリは、LLMが継続的に保守するMarkdown wikiです。

## 構成

- `raw/`: 変換済みまたは取得済みの一次ソース。原則として不変の根拠として扱う。
- `.temp/`: `raw/` へ変換する前の一時置き場。
- `wiki/`: LLMが作成・更新する知識ページ。
- `index.md`: wiki全体の内容索引。ingestやqueryの前に最初に確認する。
- `log.md`: ingest、query、lint、convertの時系列ログ。追記専用で扱う。
- `.agents/skills/`: 操作用skill。
- `.roo/commands/`: RooCode用slash command。

## 基本方針

- 根拠のない事実、要件、関係性、日付、数値を創作しない。
- 事実、推測、前提、未確認事項、提案を分けて記述する。
- 重要な記述には、可能な限り `raw/` 内のファイルや `wiki/` ページへの参照を添える。
- `raw/` の内容はユーザーの明示指示なしに変更しない。通常の編集対象は `wiki/`、`index.md`、`log.md` とする。
- 新しい知識は一度きりの回答で終わらせず、必要に応じて `wiki/` にページ化または既存ページへ統合する。
- 矛盾、古い可能性のある記述、根拠不足、未解決の前提は明示する。

## Operations

- `/convert`: `.temp/` のファイルを `markitdown` でMarkdown化し、`raw/` に配置する。
- `/ingest`: `raw/` のソースを読み、要約・エンティティ・概念・関係を `wiki/` に統合する。
- `/query`: `index.md` と関連ページから回答を作り、必要な発見はwikiへ反映候補として示す。
- `/lint`: 矛盾、孤立ページ、索引漏れ、根拠不足、更新漏れを点検する。
