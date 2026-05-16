# QA Workflow Toolkit

QA業務向けAI agent workflow assetsを、対象プロジェクトへ配置するインストーラCLIです。

`qatool` はワークフローを実行しません。RooCodeなどのAIコーディングエージェントが参照する `AGENTS.md`、`.agents/shared/`、`.agents/skills/`、`.roo/commands/` をコピーします。

## Installation

```bash
pip install -e .
```

## Commands

```bash
qatool
qatool list
qatool install
```

非対話で導入する例:

```bash
qatool install --workflow test-design --agent roocode --yes
qatool install --workflow scenario-test-design --agent roocode --yes
qatool install --workflow all --agent roocode --yes
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

RooCodeでは `/test-design docsフォルダの資料を参照してテスト設計を開始して` のように slash command を実行します。

既存ファイルがある場合、対話実行では上書き、スキップ、`AGENTS.md` の別名作成を選択できます。`--yes` 指定時は既存ファイルを上書きします。
