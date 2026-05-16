# QA Workflow Toolkit

```
   ___      _       _____ ___   ___  _     _  _____ _____
  / _ \    / \     |_   _/ _ \ / _ \| |   | |/ /_ _|_   _|
 | | | |  / _ \ _____| || | | | | | | |   | ' / | |  | |
 | |_| | / ___ \_____| || |_| | |_| | |___| . \ | |  | |
  \__\_\/_/   \_\    |_| \___/ \___/|_____|_|\_\___| |_|
```

QA業務向けAI agent workflow assetsを、対象プロジェクトへ配置するインストーラCLIです。

`qatool` 自身はワークフローを実行しません。RooCodeやClaudeなどのAIコーディングエージェントが参照する `AGENTS.md`、`.agents/shared/`、`.agents/skills/`、agent別のcommandsをカレントディレクトリに配置します。

## Installation

```bash
pip install -e .
```

## Commands

```bash
qatool
qatool wiki init
qatool workflow list
qatool workflow install
qatool workflow update
qatool workflow uninstall
```

非対話で導入する例:

```bash
qatool wiki init --name research-notes --agent roocode --yes
qatool workflow install --workflow scenario-test-design --agent roocode --yes
qatool workflow install --workflow scenario-test-design --agent claude --yes
qatool workflow install --workflow all --agent roocode --yes
qatool workflow update --workflow all --agent roocode --yes
qatool workflow uninstall --workflow scenario-test-design --agent roocode --yes
```

## LLM Wiki Init

`qatool wiki init` は、LLMが保守するMarkdown wikiの初期状態をカレントディレクトリに作成します。
対話実行ではwiki名を入力します。未入力のままEnterすると、対象ディレクトリ名を使います。
agent選択は `roocode` と `claude` に対応しています。commandの配置先は `roocode` では `.roo/commands/`、`claude` では `.claude/commands/` です。

作成される主なファイルとディレクトリ:

```text
target-project/
├─ AGENTS.md
├─ raw/
├─ wiki/
├─ .temp/
├─ index.md
├─ log.md
├─ .agents/
│  └─ skills/
│     ├─ ingest/
│     ├─ query/
│     ├─ lint/
│     └─ convert/
└─ <agent-command-dir>/
   └─ commands/
      ├─ ingest.md
      ├─ query.md
      ├─ lint.md
      └─ convert.md
```

導入先のagentでは `/convert`、`/ingest`、`/query`、`/lint` を利用できます。
`/convert` は `.temp/` に置いた変換前ファイルを `markitdown` コマンドでMarkdown化し、`raw/` に配置するためのcommandです。

## Installed Layout

```text
target-project/
├─ AGENTS.md
├─ .agents/
│  ├─ shared/
│  └─ skills/
└─ <agent-command-dir>/
   └─ commands/
```

導入先のagentでは `/scenario-test-design docsフォルダの資料を参照してシナリオテストを設計して` のように slash command を実行します。

既存ファイルがある場合、対話実行では上書き、スキップ、`AGENTS.md` の別名作成を選択できます。`--yes` 指定時は既存ファイルを上書きします。

`workflow install` は対象リポジトリの `.qa-toolkit/workflows.json` に保存済みの agent 種別と `AGENTS.md` 作成有無を、次回以降の install で既定値として再利用します。これらは workflow ごとではなく、リポジトリ単位の共通設定として保存します。

`workflow update` はインストール時に `.qa-toolkit/workflows.json` へ保存した workflow 名、リポジトリ単位の agent 種別、`AGENTS.md` 作成有無を参照し、インストール済みworkflowを現在のpackage assetsで更新します。更新対象のうち差分がない項目はplanに表示せず、差分がある項目だけをまとめて上書きします。

`workflow uninstall` はpackage assetsと完全一致するworkflow固有の `.agents/skills/<workflow>/` と agent別commandファイルを削除します。手動編集済みのファイルは削除せず、`--workflow all` の場合のみ共有ファイルも削除候補にします。

workflow一覧の表示順は、各 `src/qa_workflow_toolkit/assets/workflow/workflows/<workflow>/workflow.json` の `sort_order` で制御します。未指定のworkflowは、`sort_order` 指定済みworkflowの後ろにID順で表示されます。
