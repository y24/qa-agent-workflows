# QA Workflow Toolkit

```
   ___      _       _____ ___   ___  _     _  _____ _____
  / _ \    / \     |_   _/ _ \ / _ \| |   | |/ /_ _|_   _|
 | | | |  / _ \ _____| || | | | | | | |   | ' / | |  | |
 | |_| | / ___ \_____| || |_| | |_| | |___| . \ | |  | |
  \__\_\/_/   \_\    |_| \___/ \___/|_____|_|\_\___| |_|
```

QA業務向けAI agent workflow assetsを、カレントディレクトリへ配置するインストーラCLIです。

`qatool` 自身はワークフローを実行しません。RooCodeやClaudeなどのAIコーディングエージェントが参照する `AGENTS.md`、`.agents/shared/`、`.agents/skills/`、agent別のcommandsをカレントディレクトリに配置します。

---

## Installation

インストール:

```bash
pip install -e .
```

アンインストール:

```bash
pip uninstall qa-workflow-toolkit
```

---

## Commands Overview

`qatool` を実行すると、対話メニューから操作を選択できます。

```bash
qatool
```

各機能をコマンドで呼び出すこともできます。

```bash
qatool wiki init
qatool workflow list
qatool workflow install
qatool workflow update
qatool workflow uninstall
```

非対話で実行する場合は、以下のように対象 workflow、agent、上書き可否をオプションで指定します。

```bash
qatool wiki init --name research-notes --agent roocode --yes
qatool workflow install --workflow scenario-test-design --agent roocode --yes
qatool workflow install --workflow scenario-test-design --agent claude --yes
qatool workflow install --workflow all --agent roocode --yes
qatool workflow update --workflow all --yes
qatool workflow uninstall --workflow scenario-test-design --agent roocode --yes
```

主な共通オプション:

| オプション | 対象 | 説明 |
| --- | --- | --- |
| `--target`, `-t` | `wiki init`, `workflow install/update/uninstall` | 配置先プロジェクトのディレクトリ。省略時はカレントディレクトリ。 |
| `--agent`, `-a` | `wiki init`, `workflow install/uninstall` | commandの配置先agent。`roocode` または `claude`。 |
| `--yes`, `-y` | `wiki init`, `workflow install/update/uninstall` | 確認プロンプトを省略して実行します。install/updateでは既存の生成物を上書きします。 |
| `--workflow`, `-w` | `workflow install/update/uninstall` | 対象workflow ID。`all` を指定すると対象workflowをまとめて扱います。 |
| `--agents-md` / `--no-agents-md` | `workflow install/update` | `AGENTS.md` を作成・更新対象に含めるかを指定します。 |

---

## Workflow Commands

`workflow` コマンドは、QA業務向けの agent workflow assets をカレントディレクトリへ配置・更新・削除するためのコマンド群です。
導入される workflow は、AIコーディングエージェントがスラッシュコマンド経由で参照する `SKILL.md`、共通ポリシー、agent別commandファイルで構成されます。

### ワークフロー一覧表示

利用可能な workflow 一覧を表示します。
各 workflow のID、表示名、説明を確認できます。

```bash
qatool workflow list
```

### ワークフローのインストール

workflow assets をカレントディレクトリにインストールします。
インストール後、RooCodeやClaudeなどのagentでスラッシュコマンドを実行できるようになります。

```bash
qatool workflow install
```

主に配置されるもの:

| 配置先 | 役割 |
| --- | --- |
| `AGENTS.md` | 対象プロジェクトでagentが最初に読む共通指示。`--no-agents-md` で作成を省略できます。 |
| `.agents/shared/` | workflow横断で使う共通ルール、根拠・曖昧性・トレーサビリティなどのポリシー。 |
| `.agents/skills/<workflow>/` | workflow固有の `SKILL.md`、手順、判断基準、テンプレート。 |
| `.roo/commands/<workflow>.md` | RooCode用のスラッシュコマンド。 |
| `.claude/commands/<workflow>.md` | Claude用のスラッシュコマンド。 |
| `.qa-toolkit/workflows.json` | インストール済みworkflowとリポジトリ単位の設定を記録する状態ファイル。 |

対話実行では、対象 workflow、agent、`AGENTS.md` 作成有無、既存ファイルがある場合の扱いを選択できます。
既存ファイルがある場合、通常は上書き、スキップ、`AGENTS.md` の別名作成を選べます。

### ワークフローの更新

インストール済み workflow assets を、現在の package assets の内容で更新します。
本ツールを更新した後、対象プロジェクトへ新しい skill 定義や共通ルールを反映するために使います。

```bash
qatool workflow update
```

### ワークフローのアンインストール

インストール済み workflow assets をカレントディレクトリから削除します。

```bash
qatool workflow uninstall
```

### ワークフロー導入後の使い方

導入先のAIエージェントで、インストールしたワークフローの slash command を実行します。

```text
/scenario-test-design docsフォルダの資料を参照してシナリオテストを設計して
/risk-based-test-design 要件定義書と不具合傾向をもとにリスクベーステスト方針を作って
```

---

## Wiki Commands

`wiki` コマンドは、LLMが継続的に保守するMarkdown wikiの初期構成を作るためのコマンド群です。
現時点では `init` を提供しています。

### wikiの新規構築

LLMが保守するMarkdown wikiの初期状態を対象ディレクトリに作成します。

```bash
qatool wiki init
```

- 名称の入力: wikiの名前入を入力します。そのままEnterすると、対象ディレクトリ名をwiki名として使います。
- agent選択: スラッシュコマンド用の.mdファイルが選択したエージェントに応じたフォルダに配置されます。

作成される主なファイルとディレクトリ:

```text
target-project/
├─ AGENTS.md
├─ raw/
├─ wiki/
├─ .temp/
├─ index.md
├─ log.md
└─ <agent-command-dir>/
   ├─ ingest.md
   ├─ query.md
   ├─ lint.md
   └─ convert.md
```

### wiki構築後の使い方

導入先のagentで、スラッシュコマンド `/convert`、`/ingest`、`/query`、`/lint` を利用できます。

| command | 役割 |
| --- | --- |
| `/convert` | `.temp/` に置いた変換前ファイルを `markitdown` コマンドでMarkdown化し、`raw/` に配置します。 |
| `/ingest` | `raw/` のソースを読み、根拠を保ったまま `wiki/`、`index.md`、`log.md` に統合します。 |
| `/query` | `index.md` と `wiki/` の関連ページを優先して質問に回答し、根拠と未確認事項を示します。 |
| `/lint` | wikiの矛盾、根拠不足、索引漏れ、孤立ページ、古い記述、未解決事項を点検します。 |

