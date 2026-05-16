# QA Workflow Toolkit

```
   ___      _       _____ ___   ___  _     _  _____ _____
  / _ \    / \     |_   _/ _ \ / _ \| |   | |/ /_ _|_   _|
 | | | |  / _ \ _____| || | | | | | | |   | ' / | |  | |
 | |_| | / ___ \_____| || |_| | |_| | |___| . \ | |  | |
  \__\_\/_/   \_\    |_| \___/ \___/|_____|_|\_\___| |_|
```

QA業務向けAI agent workflow assetsを、対象プロジェクトへ配置するインストーラCLIです。

`qatool` 自身はワークフローを実行しません。RooCodeなどのAIコーディングエージェントが参照する `AGENTS.md`、`.agents/shared/`、`.agents/skills/`、`.roo/commands/` をカレントディレクトリに配置します。

## Installation

```bash
pip install -e .
```

## Commands

```bash
qatool
qatool workflow list
qatool workflow install
qatool workflow update
qatool workflow uninstall
```

非対話で導入する例:

```bash
qatool workflow install --workflow scenario-test-design --agent roocode --yes
qatool workflow install --workflow all --agent roocode --yes
qatool workflow update --workflow all --agent roocode --yes
qatool workflow uninstall --workflow scenario-test-design --agent roocode --yes
```

## Installed Layout

```text
target-project/
├─ AGENTS.md
├─ .agents/
│  ├─ shared/
│  └─ skills/
└─ .roo/
   └─ commands/
```

RooCodeでは `/scenario-test-design docsフォルダの資料を参照してシナリオテストを設計して` のように slash command を実行します。

既存ファイルがある場合、対話実行では上書き、スキップ、`AGENTS.md` の別名作成を選択できます。`--yes` 指定時は既存ファイルを上書きします。

`workflow update` はインストール時に `.qa-toolkit/workflows.json` へ保存したworkflow名、agent種別、`AGENTS.md` 作成有無を参照し、インストール済みworkflowを現在のpackage assetsで更新します。更新対象のうち差分がない項目はplanに表示せず、差分がある項目だけをまとめて上書きします。

`workflow uninstall` はpackage assetsと完全一致するworkflow固有の `.agents/skills/<workflow>/` と `.roo/commands/<workflow>.md` を削除します。手動編集済みのファイルは削除せず、`--workflow all` の場合のみ共有ファイルも削除候補にします。
