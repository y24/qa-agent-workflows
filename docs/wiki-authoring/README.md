# Wiki Type Authoring Guide

このディレクトリは、`qa-workflow-toolkit` に新しい wiki type asset を追加する場合、または既存 wiki type の AGENTS / command / 初期ファイルを再構成する場合の保守方針をまとめる。
通常の wiki 運用時に必ず読むルールではなく、wiki type asset を作成・レビューする人または agent が参照する文書である。

## 文書の位置づけ

| 配置先 | 役割 |
|---|---|
| `AGENTS.md` | リポジトリ全体の常時適用ルール。詳細な wiki type 作成手順は置かない。 |
| `docs/wiki-authoring/` | wiki type asset の追加、再構成、レビューに関する保守者向け方針。 |
| `src/qa_workflow_toolkit/assets/wiki/types/<wiki-type>/wiki_type.json` | CLI が wiki type を列挙・選択するための manifest。 |
| `src/qa_workflow_toolkit/assets/wiki/types/<wiki-type>/AGENTS.md` | `qatool wiki init` で対象リポジトリの `AGENTS.md` として配置される wiki type 固有ルール。 |
| `src/qa_workflow_toolkit/assets/wiki/types/<wiki-type>/commands/` | agent 別 command ディレクトリへ配置される wiki 操作用 command。 |
| `src/qa_workflow_toolkit/assets/wiki/types/<wiki-type>/index.md` | wiki 初期化時に配置される索引テンプレート。 |
| `src/qa_workflow_toolkit/assets/wiki/types/<wiki-type>/log.md` | wiki 初期化時に配置されるログテンプレート。 |

## 基本原則

- wiki type 固有の目的、手順、判断基準は `assets/wiki/types/<wiki-type>/` 配下に閉じ込める。
- CLI 本体に wiki type 固有の表示名、説明、手順、判断基準を埋め込まない。
- wiki type の選択肢は `wiki_type.json` から生成する。
- 既存の command 名 `convert`、`ingest`、`query`、`lint` は可能な限り維持する。
- `raw/` は原則として不変の根拠、`wiki/`、`index.md`、`log.md` は通常編集対象という共通の運用前提を崩す場合は、`AGENTS.md` と各 command に理由を明示する。
- 通常運用で不要な作成者向け説明は、このディレクトリに置く。

## 標準構成

```text
src/qa_workflow_toolkit/assets/wiki/
  types/
    <wiki-type>/
      wiki_type.json
      AGENTS.md
      index.md
      log.md
      commands/
        convert.md
        ingest.md
        query.md
        lint.md
```

## 新規 wiki type 追加の流れ

1. wiki type の目的、対象入力、対象外、主要な知識構造、command の運用差分を定義する。
2. `src/qa_workflow_toolkit/assets/wiki/types/<wiki-type>/` を作成する。
3. `wiki_type.json` を作成し、ID、表示名、説明、version、sort order を定義する。
4. `AGENTS.md`、`index.md`、`log.md`、`commands/*.md` を作成する。
5. `qatool wiki init --type <wiki-type> --agent roocode --target <tmp> --yes` で配置結果を確認する。
6. Claude / Copilot / Codex の command 配置先も必要に応じて確認する。
7. `pytest` で registry / CLI / installer の期待値を確認する。wiki type 一覧や sort order の固定期待がある場合はテストを更新する。

詳細は [wiki_type_addition_guide.md](wiki_type_addition_guide.md) を参照する。

## 関連文書

- [wiki_type_addition_guide.md](wiki_type_addition_guide.md): 現行CLIに wiki type を追加する際の実装ポイント。
- [../skill-authoring/README.md](../skill-authoring/README.md): workflow asset 側の作成・再構成方針。
