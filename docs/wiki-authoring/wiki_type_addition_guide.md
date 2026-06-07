# Wiki Type Addition Guide

この文書は、現行の `qa-workflow-toolkit` CLI に新しい wiki type を追加する際の実装ポイントをまとめる。
CLI は wiki を運用せず、対象リポジトリへ wiki 用の `AGENTS.md`、初期ファイル、agent command を配置することだけを責務とする。

## 追加するファイル

新規 wiki type の正は package asset 側に置く。

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

`src/qa_workflow_toolkit/assets/wiki/types/basic/` は汎用的な LLM wiki の標準 type である。
新規 type は `basic` をコピーして始めてもよいが、目的が違う箇所だけを変え、汎用 type との不要な差分を増やさない。

## `wiki_type.json`

`wiki_type.json` は `qatool wiki init` の type 選択肢になる。
必須項目は `src/qa_workflow_toolkit/models.py` の `WikiTypeManifest.from_dict` と揃える。

最小例:

```json
{
  "id": "project-docs",
  "display_name": "Project Docs",
  "description": "プロジェクト文書を継続的に整理するwikiを構築する。",
  "version": "1.0.0",
  "sort_order": 200,
  "default": false
}
```

注意点:

- `id` は kebab-case にする。
- `display_name` は対話選択に出る短い名前にする。
- `description` は type の目的と Basic との差分が分かる一文にする。
- `sort_order` は `qatool wiki init` の対話選択順を決める。未指定 type は指定済み type の後ろに ID 順で並ぶ。
- `default` は原則として既存の `basic` だけを `true` にする。複数 type が `default: true` の場合は sort order が先のものが使われる。

## Template Asset

`AGENTS.md`、`index.md`、`log.md`、`commands/*.md` は `qatool wiki init` / `wiki update` で配置される。
テンプレートでは以下の placeholder を使える。

| placeholder | 内容 |
|---|---|
| `[[wiki_name]]` | `--name` または対象ディレクトリ名から解決した wiki 名。 |
| `[[wiki_type]]` | `wiki_type.json` の `id`。 |

`AGENTS.md` には以下の metadata コメントを含める。

```md
<!-- generated-by: qa-workflow-toolkit -->
<!-- wiki-name: [[wiki_name]] -->
<!-- wiki-type: [[wiki_type]] -->
```

## Command Asset

`commands/*.md` は agent ごとの command ディレクトリへ配置される。
RooCode では `.roo/commands/<command>.md`、Claude では `.claude/commands/<command>.md`、GitHub Copilot では `.github/prompts/<command>.prompt.md`、Codex では `.codex/prompts/<command>.md` に配置される。

既存 command の役割:

| command | 役割 |
|---|---|
| `convert` | `.temp/` の変換前ファイルを `raw/` 向け Markdown に変換する。 |
| `ingest` | `raw/` のソースを読み、`wiki/`、`index.md`、`log.md` に統合する。 |
| `query` | `index.md` と `wiki/` を根拠に質問へ回答する。 |
| `lint` | wiki の矛盾、索引漏れ、根拠不足、更新漏れを点検する。 |

新規 type で command の意味を変える場合は、`AGENTS.md` と command 本文の両方で一貫させる。
CLI 側の `WIKI_OPERATIONS` を変更しない限り、追加 command は自動では配置されない。

## CLI 挙動で意識する点

- `wiki init` は type、wiki 名、agent から install plan を作る。
- `--yes` かつ `--type` 省略時は `default: true` の wiki type を使う。
- `wiki update` は `.qatool/metadata.json` に記録された `wiki_type` を使って `AGENTS.md` と command を更新する。
- `wiki update` は `wiki/`、`raw/`、`index.md`、`log.md` を運用データとして扱い、上書きしない。
- `change-agent` は記録済みの `wiki_type` を維持したまま command 配置先だけを変更する。
- agent ごとの command 配置先は `src/qa_workflow_toolkit/agents.py` で定義される。

## 確認手順

一時ディレクトリを使って、少なくとも以下を確認する。

```powershell
qatool wiki init --type <wiki-type> --name tmp-wiki --agent roocode --target work/tmp-wiki-<wiki-type>-roocode --yes
qatool wiki init --type <wiki-type> --name tmp-wiki --agent claude --target work/tmp-wiki-<wiki-type>-claude --yes
qatool wiki init --type <wiki-type> --name tmp-wiki --agent copilot --target work/tmp-wiki-<wiki-type>-copilot --yes
qatool wiki init --type <wiki-type> --name tmp-wiki --agent codex --target work/tmp-wiki-<wiki-type>-codex --yes
qatool wiki update --target work/tmp-wiki-<wiki-type>-roocode --yes
pytest
```

確認観点:

- 対話実行の `Select wiki type` に ID、表示名、説明が出る。
- `--type <wiki-type>` で対象 type の asset が使われる。
- `AGENTS.md` に `wiki-name` と `wiki-type` metadata が出る。
- `.qatool/metadata.json` に `wiki_type` が記録される。
- RooCode の command が `.roo/commands/` に配置される。
- Claude の command が `.claude/commands/` に配置される。
- GitHub Copilot の prompt file が `.github/prompts/*.prompt.md` に配置される。
- Codex の custom prompt が `.codex/prompts/` に配置される。
- `wiki update` が command の差分を更新し、`index.md` と `log.md` を上書きしない。

## テスト更新

新規 wiki type を追加した場合、固定期待を持つテストの更新が必要になることがある。

- `tests/test_registry.py`: wiki type 一覧、sort order、manifest の期待値。
- `tests/test_cli.py`: `wiki init` の type 選択、metadata、update の出力。
- `tests/test_installer.py`: agent 別 command 配置の挙動。

CLI の仕組みを変えずに wiki type を追加するだけなら、既存テストへ必要最小限の期待値追加に留める。

## レビュー前チェック

- [ ] wiki type 固有の手順や判断基準を CLI 本体に追加していない。
- [ ] package asset 側に正を置いている。
- [ ] `wiki_type.json` の ID、表示名、説明が目的を正しく表している。
- [ ] `wiki_type.json` とディレクトリ名が一致している。
- [ ] `AGENTS.md`、`index.md`、`log.md`、`commands/*.md` が存在する。
- [ ] `AGENTS.md` に `generated-by`、`wiki-name`、`wiki-type` metadata がある。
- [ ] command と `AGENTS.md` の運用方針が矛盾していない。
- [ ] `raw/`、`wiki/`、`index.md`、`log.md` の責務が明確である。
- [ ] roocode / claude / copilot / codex の init 結果を確認した。
- [ ] `wiki update` が運用データを上書きしないことを確認した。
- [ ] `pytest` を実行した。
