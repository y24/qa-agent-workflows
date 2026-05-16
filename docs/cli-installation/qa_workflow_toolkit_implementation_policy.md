# qa-workflow-toolkit 実装方針

## 1. 目的

`qa-workflow-toolkit` は、QA業務向けのAIエージェントワークフロー群を、対象プロジェクトへ簡単に導入するためのCLIツールである。

Pythonパッケージとして提供し、利用者は以下のようにインストールして使用する。

```bash
pip install -e .
qatool
qatool workflow install
```

`qatool` は、ワークフローそのものを直接実行するツールではない。

主な役割は、RooCodeなどのAIコーディングエージェントが参照できるように、以下のアセットを対象フォルダへ配置することである。

- `AGENTS.md`
- `.agents/shared/`
- `.agents/skills/<workflow>/`
- `.roo/commands/<workflow>.md`

導入後、利用者はRooCode上で `/scenario-test-design` などの slash command を実行し、各QAワークフローを開始する。

---

## 2. 基本方針

### 2.1 CLIはインストーラに徹する

`qatool` は、QAワークフローの中身を解釈・実行しない。

CLIの責務は以下に限定する。

- 利用可能なワークフロー一覧を読み込む
- 利用者にワークフローを選択させる
- 利用者に対象エージェントを選択させる
- 必要なファイルを対象プロジェクトへコピーする
- 既存ファイルとの衝突を確認する
- インストール結果と利用方法を表示する

ワークフロー固有の手順、ルール、成果物、ステップ構成は、すべてアセット側に閉じ込める。

### 2.2 ワークフロー固有知識をCLIに埋め込まない

CLI本体に `scenario-test-design` や `risk-based-test-design` などの個別ワークフロー前提の分岐を書かない。

ワークフローの情報は `workflow.json` に定義し、CLIはそれを読み込んで動作する。

これにより、将来的にワークフローを追加する場合も、基本的にはアセットフォルダとmanifestを追加するだけで対応できるようにする。

### 2.3 共通方針は `.agents/shared/` に集約する

全ワークフロー共通のポリシー、用語、出力ルール、レビューゲート方針などは `.agents/shared/` に配置する。

個別ワークフローのskillからは、相対パスで `.agents/shared/` 配下の共通ファイルを参照する。

```text
.agents/
├─ shared/
└─ skills/
```

この構成により、共通資産がAIエージェント用であることを明確にしつつ、各skillからも参照しやすくする。

### 2.4 slash commandは薄い入口にする

RooCodeの slash command には、長大なワークフロー手順を書かない。

slash command は、対象skillを呼び出すための入口として使う。

実際のルール、進行制御、ステップ定義、出力テンプレートは `.agents/skills/<workflow>/` 配下に置く。

---

## 3. インストール後のディレクトリ構成

`qatool workflow install` 実行後、対象プロジェクトには以下のような構成を作成する。

```text
target-project/
├─ AGENTS.md
├─ .agents/
│  ├─ shared/
│  │  ├─ common_contract.md
│  │  ├─ evidence_and_confidence_policy.md
│  │  ├─ ambiguity_and_issue_log_policy.md
│  │  ├─ traceability_policy.md
│  │  ├─ review_gate_policy.md
│  │  ├─ output_location_policy.md
│  │  └─ terminology.md
│  └─ skills/
│     └─ scenario-test-design/
│        ├─ SKILL.md
│        ├─ rules.md
│        ├─ orchestrator.md
│        ├─ steps/
│        ├─ templates/
│        └─ references/
└─ .roo/
   └─ commands/
      └─ scenario-test-design.md
```

複数ワークフローを導入した場合は、`.agents/skills/` と `.roo/commands/` に対象ワークフロー分のファイルを追加する。

```text
.agents/
├─ shared/
└─ skills/
   ├─ scenario-test-design/
   ├─ risk-based-test-design/
   └─ defect-analysis/

.roo/
└─ commands/
   ├─ scenario-test-design.md
   ├─ risk-based-test-design.md
   └─ defect-analysis.md
```

---

## 4. パッケージ側の推奨ディレクトリ構成

`qa-workflow-toolkit` 側は以下の構成とする。

```text
qa-workflow-toolkit/
├─ pyproject.toml
├─ README.md
├─ src/
│  └─ qa_workflow_toolkit/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ cli.py
│     ├─ console.py
│     ├─ installer.py
│     ├─ registry.py
│     ├─ models.py
│     ├─ paths.py
│     └─ assets/
│        └─ workflow/
│           ├─ agents/
│           │  └─ roocode/
│           │     └─ AGENTS.md
│           ├─ shared/
│           │  ├─ common_contract.md
│           │  ├─ evidence_and_confidence_policy.md
│           │  ├─ ambiguity_and_issue_log_policy.md
│           │  ├─ traceability_policy.md
│           │  ├─ review_gate_policy.md
│           │  ├─ output_location_policy.md
│           │  └─ terminology.md
│           ├─ workflows/
│           │  ├─ scenario-test-design/
│           │  └─ risk-based-test-design/
│           └─ commands/
│              └─ roocode/
│                 ├─ scenario-test-design.md
│                 └─ risk-based-test-design.md
└─ tests/
   ├─ test_cli.py
   ├─ test_registry.py
   └─ test_installer.py
```

### 4.1 `src/` レイアウトを使う理由

Pythonパッケージとしての動作確認と、ローカルファイルを偶然参照して動いてしまう事故を減らすため、`src/` レイアウトを採用する。

### 4.2 アセットの読み込み

CLI実行時は、`importlib.resources` を使って `assets/` 配下のファイルを読み込み、対象プロジェクトへコピーする。

これにより、パッケージインストール後もアセットファイルを安定して参照できるようにする。

---

## 5. 技術スタック

### 5.1 CLIフレームワーク

`Typer` を使用する。

理由:

- サブコマンドを追加しやすい
- 型ヒントとの相性がよい
- 将来的に `list`、`update`、`doctor`、`uninstall` などを追加しやすい

### 5.2 表示

`Rich` を使用する。

理由:

- ロゴ、バージョン、表形式のワークフロー一覧を見やすく表示できる
- エラーや警告を色分けしやすい
- CLIツールとしての体験がよくなる

### 5.3 対話UI

`questionary` を使用する。

理由:

- 矢印キー選択、Yes/No確認、選択式プロンプトを実装しやすい
- `qatool workflow install` の対話式操作に合っている

### 5.4 テスト

`pytest` を使用する。

主なテスト対象:

- workflow manifest の読み込み
- ワークフロー一覧表示
- インストール計画生成
- ファイルコピー
- 既存ファイル衝突時の処理
- `AGENTS.md` の上書き・別名作成・スキップ処理

---

## 6. `pyproject.toml` 方針

`pip install -e .` で `qatool` コマンドが使えるようにするため、`[project.scripts]` を定義する。

```toml
[project]
name = "qa-workflow-toolkit"
version = "0.1.0"
description = "CLI installer for QA agent workflows"
requires-python = ">=3.11"
dependencies = [
  "typer>=0.12",
  "rich>=13",
  "questionary>=2"
]

[project.scripts]
qatool = "qa_workflow_toolkit.cli:main"

[tool.setuptools.package-data]
qa_workflow_toolkit = ["assets/**/*"]
```

初期段階では開発用に `pip install -e .` を前提とする。

将来的に配布する場合は、通常の wheel 配布や社内パッケージリポジトリへの公開を検討する。

---

## 7. コマンド設計

## 7.1 初期対応コマンド

MVPでは以下のコマンドを実装する。

```bash
qatool
qatool workflow list
qatool workflow install
```

### `qatool`

引数なしで実行した場合、以下を表示する。

- ロゴ
- バージョン
- 概要
- 利用可能な主要コマンド
- 簡単な使用例

表示例:

```text
QA Workflow Toolkit 0.1.0

Usage:
  qatool workflow install    Install QA workflow assets into current folder
  qatool workflow list       Show available workflows

Examples:
  qatool workflow install
```

### `qatool workflow list`

利用可能なワークフロー一覧を表示する。

表示項目:

- ワークフローID
- 表示名
- 説明
- 対応エージェント

### `qatool workflow install`

対話式でワークフローを対象プロジェクトへインストールする。

処理内容:

1. ロゴとバージョンを表示
2. workflow registry を読み込む
3. ワークフロー一覧を表示
4. 利用者にワークフローを選択させる
5. 利用者にエージェントを選択させる
6. インストール計画を生成する
7. 既存ファイルとの衝突を確認する
8. ファイルをコピーする
9. インストール結果を表示する
10. RooCode上での使用例を表示する

---

## 8. 将来追加を想定するコマンド

初期実装では対応しないが、将来的に以下のコマンドを追加できる設計にしておく。

```bash
qatool workflow update
qatool workflow uninstall
qatool doctor
qatool init
qatool workflow list --installed
```

### `qatool workflow update`

既存インストール済みワークフローを更新する。

### `qatool workflow uninstall`

インストール済みワークフローを削除する。

ただし、手動編集されたファイルを削除するリスクがあるため、実装は慎重に行う。

### `qatool doctor`

対象プロジェクトの配置状態を検査する。

確認例:

- `.agents/shared/` が存在するか
- `.agents/skills/<workflow>/SKILL.md` が存在するか
- `.roo/commands/<workflow>.md` が存在するか
- `AGENTS.md` が存在するか
- 参照パスが壊れていないか

### `qatool workflow list --installed`

現在のプロジェクトに導入済みのワークフローを表示する。

---

## 9. workflow manifest設計

各ワークフローには `workflow.json` を持たせる。

例:

```json
{
  "id": "scenario-test-design",
  "display_name": "シナリオテスト設計",
  "description": "要件、業務フロー、画面仕様、ドメインルールからシナリオテストを設計する",
  "version": "0.1.0",
  "skill_name": "scenario-test-design",
  "command_name": "scenario-test-design",
  "supported_agents": ["roocode", "claude"],
  "default_agent": "roocode",
  "install": {
    "agents_md": true,
    "shared": {
      "source": "shared",
      "target": ".agents/shared"
    },
    "skill": {
      "source": "workflows/scenario-test-design/skill",
      "target": ".agents/skills/scenario-test-design"
    },
    "command": {
      "source": "commands/scenario-test-design.md",
      "target": ".roo/commands/scenario-test-design.md"
    }
  },
  "post_install_message": "/scenario-test-design <入力資料>"
}
```

### 9.1 manifestに持たせる情報

- ワークフローID
- 表示名
- 説明
- バージョン
- skill名
- command名
- 対応エージェント
- コピー元
- コピー先
- インストール後メッセージ

### 9.2 manifestで持たせない情報

以下はmanifestに持たせない。

- ワークフローの詳細手順
- ステップごとのプロンプト本文
- 出力テンプレート本文
- QA判断基準の本文

これらはskill配下のMarkdownファイルとして管理する。

---

## 10. インストール処理の詳細

### 10.1 インストール計画

`qatool workflow install` は、実際にコピーする前にインストール計画を生成する。

インストール計画には以下を含める。

- コピー元パス
- コピー先パス
- 種別
  - `agents_md`
  - `shared`
  - `skill`
  - `command`
- 既存ファイル有無
- 衝突時の処理方針

### 10.2 コピー対象

選択されたワークフローに対して、以下をコピーする。

```text
assets/workflow/agents/roocode/AGENTS.md
  → AGENTS.md

assets/workflow/shared/**
  → .agents/shared/**

assets/workflow/workflows/<workflow>/skill/**
  → .agents/skills/<workflow>/**

assets/workflow/commands/<workflow>.md
  → .roo/commands/<workflow>.md
```

### 10.3 共有ファイルの扱い

`.agents/shared/` は複数ワークフローで共有する。

そのため、複数ワークフローを導入しても同じファイルを重複コピーしない。

既存の `.agents/shared/` がある場合は、ファイル単位で衝突を確認する。

MVPでは、単純化のため `.agents/shared/` 全体を上書き確認の対象としてもよい。

---

## 11. 既存ファイルとの衝突処理

### 11.1 `AGENTS.md`

対象フォルダに `AGENTS.md` が存在する場合、以下を選択させる。

```text
Yes      上書きする
Rename   AGENTS_1.md のような別名で作成する
No       作成しない
```

別名作成時は、既存ファイルと衝突しないファイル名を自動採番する。

例:

```text
AGENTS_1.md
AGENTS_2.md
AGENTS_3.md
```

### 11.2 slash command

`.roo/commands/<workflow>.md` が存在する場合、上書きするか確認する。

MVPでは以下の選択肢でよい。

```text
Overwrite  上書きする
Skip       作成しない
```

### 11.3 skill

`.agents/skills/<workflow>/` が存在する場合、上書きするか確認する。

MVPでは以下の選択肢でよい。

```text
Overwrite  上書きする
Skip       作成しない
```

### 11.4 shared

`.agents/shared/` が存在する場合、上書きするか確認する。

MVPでは以下の選択肢でよい。

```text
Overwrite  上書きする
Skip       既存のsharedを維持する
```

将来的には、ファイル単位の差分確認や更新確認に拡張する。

---

## 12. 生成ファイルマーカー

`qatool` が生成するファイルには、可能な範囲で生成元マーカーを付与する。

例:

```md
<!-- generated-by: qa-workflow-toolkit -->
<!-- workflow-id: scenario-test-design -->
<!-- toolkit-version: 0.1.0 -->
```

このマーカーは将来的に以下の用途で使用する。

- `qatool workflow update` 時の安全な上書き判断
- `qatool workflow uninstall` 時の削除対象判断
- `qatool doctor` 時の状態確認

ただし、RooCodeが読むプロンプト本文に悪影響が出ない位置に置く。

---

## 13. skill側の共通ファイル参照ルール

各skillは、共通方針として `.agents/shared/` 配下のファイルを参照する。

`SKILL.md` から見た相対パスは以下になる。

```text
.agents/skills/scenario-test-design/SKILL.md
  → ../../shared/common_contract.md
```

`SKILL.md` には、以下のように明示的に記載する。

```md
## 共通方針

このskillを実行する前に、以下の共通方針を確認する。

- `../../shared/common_contract.md`
- `../../shared/evidence_and_confidence_policy.md`
- `../../shared/ambiguity_and_issue_log_policy.md`
- `../../shared/traceability_policy.md`
- `../../shared/review_gate_policy.md`
- `../../shared/output_location_policy.md`
- `../../shared/terminology.md`
```

また、`orchestrator.md` の冒頭にも Step 0 として共通方針確認を入れる。

```md
## Step 0: 共通方針の確認

作業開始前に、SKILL.mdに列挙されたshared policyを確認する。
読めないファイルがある場合は、推測で進めず、不足ファイルとしてユーザーに報告する。
```

---

## 14. slash command設計

Slash command は選択したagentのcommandsディレクトリに配置する。

例: `.roo/commands/scenario-test-design.md`

```md
---
description: テスト設計ワークフローを開始する
argument-hint: <入力資料フォルダまたは対象ドキュメント>
---

# Scenario Test Design Workflow

Use the `scenario-test-design` skill.

User request:
{{arguments}}

Follow the workflow described in the skill.
Do not proceed to the next major step until the user explicitly approves.
```

slash command には、以下を記載する。

- どのskillを使うか
- ユーザー引数をどう扱うか
- 勝手に次ステップへ進まないこと
- 必要なら成果物の出力先方針に従うこと

slash command には、以下を書かない。

- 長大なステップ手順
- 共通ポリシー全文
- 出力テンプレート全文
- 判断基準全文

---

## 15. AGENTS.md設計

`AGENTS.md` は、対象プロジェクトにおけるAIエージェント全体の基本ルールを定義する。

ただし、常時読まれる可能性があるため、内容は短く保つ。

`AGENTS.md` には以下を記載する。

- このプロジェクトでAIエージェントが従う基本方針
- 詳細ルールは `.agents/shared/` と `.agents/skills/` を参照すること
- 事実・推測・未確認事項を分けること
- 根拠のない仕様やテスト観点を創作しないこと
- 成果物は指定された出力先に保存すること
- ワークフローはユーザーの承認なしに次ステップへ進めないこと

長大な手順や個別ワークフローの内容は `AGENTS.md` に書かない。

---

## 16. MVPスコープ

初期実装の対象は以下とする。

### 16.1 対象エージェント

- RooCodeのみ

### 16.2 対象ワークフロー

- `scenario-test-design` のみ

ただし、構造としては複数ワークフロー追加に耐えられるようにする。

### 16.3 対応コマンド

```bash
qatool
qatool workflow list
qatool workflow install
```

### 16.4 インストール対象

```text
AGENTS.md
.agents/shared/**
.agents/skills/scenario-test-design/**
.roo/commands/scenario-test-design.md
```

### 16.5 衝突処理

- `AGENTS.md`: 上書き / 別名作成 / スキップ
- `.agents/shared/`: 上書き / スキップ
- `.agents/skills/<workflow>/`: 上書き / スキップ
- `.roo/commands/<workflow>.md`: 上書き / スキップ

---

## 17. 実装ステップ

### Step 1: パッケージ骨格を作成する

作成対象:

- `pyproject.toml`
- `src/qa_workflow_toolkit/__init__.py`
- `src/qa_workflow_toolkit/__main__.py`
- `src/qa_workflow_toolkit/cli.py`

この時点で、`pip install -e .` 後に `qatool` が実行できることを確認する。

### Step 2: 基本表示を実装する

`qatool` 実行時に以下を表示する。

- ロゴ
- バージョン
- 簡単な説明
- 使用可能コマンド

### Step 3: workflow registryを実装する

作成対象:

- `registry.py`
- `models.py`

実装内容:

- `assets/workflow/workflows/*/workflow.json` を読み込む
- manifestを検証する
- ワークフロー一覧を返す

### Step 4: `qatool workflow list` を実装する

ワークフロー一覧をRichのtableで表示する。

### Step 5: インストール計画生成を実装する

作成対象:

- `installer.py`
- `paths.py`

実装内容:

- 選択されたworkflowとagentからコピー対象を決定する
- コピー元・コピー先の一覧を生成する
- 既存ファイルの有無を確認する

### Step 6: `qatool workflow install` の対話UIを実装する

実装内容:

- workflow選択
- agent選択
- 既存ファイル衝突時の確認
- インストール実行
- 結果表示

### Step 7: scenario-test-designアセットを移植する

既存のQAプロンプト・ワークフロー資産から、`scenario-test-design` をMVP対象として移植する。

移植先:

```text
assets/workflow/workflows/scenario-test-design/skill/
assets/workflow/commands/scenario-test-design.md
assets/workflow/shared/
assets/workflow/agents/roocode/AGENTS.md
```

既存アセット内の参照パスを修正する。

```text
変更前:
../../../shared/...

変更後:
../../shared/...
```

### Step 8: pytestで動作確認する

主なテスト:

- `qatool` が起動する
- `qatool workflow list` がworkflowを表示する
- manifestを読み込める
- install planを生成できる
- 一時ディレクトリにファイルをコピーできる
- `AGENTS.md` 既存時に別名作成できる
- `.agents/shared/` が正しい場所に作成される
- `.agents/skills/scenario-test-design/SKILL.md` が作成される
- `.roo/commands/scenario-test-design.md` が作成される

### Step 9: RooCode上で手動確認する

確認内容:

- `/scenario-test-design` がRooCodeで認識される
- slash commandから `scenario-test-design` skill を使う流れになる
- skillが `.agents/shared/` の共通方針を参照できる
- ユーザー承認なしに次ステップへ進まない
- 出力先ルールに従って成果物を保存しようとする

---

## 18. テスト方針

### 18.1 単体テスト

対象:

- manifest読み込み
- manifest validation
- install plan生成
- 別名ファイル名生成
- コピー処理
- 衝突判定

### 18.2 CLIテスト

対象:

- `qatool`
- `qatool workflow list`
- `qatool workflow install --workflow scenario-test-design --agent roocode --yes` のような非対話実行

MVPでは対話UIの完全自動テストは無理に行わず、内部ロジックを単体テストし、CLIは最小限の起動確認に留める。

### 18.3 手動テスト

対象:

- 実際のRooCode上でslash commandが認識されるか
- skill参照が機能するか
- プロンプトの進行制御が意図通りか

---

## 19. 将来拡張方針

### 19.1 複数ワークフロー対応

MVP後、以下を追加する。

- scenario-test-design
- risk-based-test-design
- quality-criteria-design
- test-design-review
- testcase-viewpoint-extraction
- defect-analysis
- spec-extraction

### 19.2 複数エージェント対応

初期はRooCodeのみとする。

将来的には、他エージェント向けのコマンド配置やskill配置に対応できるよう、agent adapterを導入する。

例:

```text
AgentAdapter
├─ RooCodeAdapter
├─ ClaudeCodeAdapter
└─ CursorAdapter
```

ただし、MVPでは過剰設計を避け、RooCode用処理を中心に実装する。

### 19.3 更新管理

将来的に `qatool workflow update` を追加する。

そのために、生成ファイルマーカーやインストール状態ファイルの導入を検討する。

例:

```text
.agents/qatool.lock.json
```

lockファイルには以下を記録する。

- toolkit version
- installed workflows
- installed timestamp
- installed files
- source manifest version

MVPでは必須ではない。

---

## 20. 実装上の注意点

### 20.1 破壊的操作を避ける

既存ファイルを無言で上書きしない。

特に以下は慎重に扱う。

- `AGENTS.md`
- `.agents/shared/`
- `.agents/skills/<workflow>/`
- `.roo/commands/<workflow>.md`

### 20.2 パスは `pathlib.Path` で扱う

Windows環境での利用を想定しつつ、可能な範囲でOS非依存にする。

パス結合には文字列連結を使わず、`pathlib.Path` を使う。

### 20.3 アセットとコードを分離する

CLIコード内にMarkdown本文を埋め込まない。

すべてのプロンプト、テンプレート、共通方針は `assets/` 配下の実ファイルとして管理する。

### 20.4 READMEを整備する

READMEには以下を書く。

- ツールの目的
- インストール方法
- 基本コマンド
- `qatool workflow install` の使い方
- インストール後のディレクトリ構成
- RooCodeでの実行例
- 既存ファイルがある場合の挙動

---

## 21. 最終的なMVP完了条件

MVPは、以下を満たした時点で完了とする。

1. `pip install -e .` で `qatool` コマンドが使える
2. `qatool` でロゴ、バージョン、使い方が表示される
3. `qatool workflow list` で `scenario-test-design` が表示される
4. `qatool workflow install` で対話的に `scenario-test-design` を選択できる
5. `AGENTS.md` が配置される
6. `.agents/shared/` が配置される
7. `.agents/skills/scenario-test-design/` が配置される
8. `.roo/commands/scenario-test-design.md` が配置される
9. 既存 `AGENTS.md` に対して上書き・別名作成・スキップを選べる
10. RooCode上で `/scenario-test-design` が利用できる
11. `/scenario-test-design docsフォルダの資料を参照してシナリオテストを設計して` のような指示で、scenario-test-design skillのワークフローを開始できる

---

## 22. まとめ

`qa-workflow-toolkit` は、QAプロンプト・ワークフロー群をCLIで対象プロジェクトに導入するためのツールとして設計する。

初期段階では、RooCode向けに以下を配置する。

```text
AGENTS.md
.agents/shared/**
.agents/skills/<workflow>/**
.roo/commands/<workflow>.md
```

共通方針は `.agents/shared/` に集約し、個別ワークフローは `.agents/skills/<workflow>/` に配置する。

Slash commandは選択したagentのcommandsディレクトリに置き、skillを呼び出す薄い入口として扱う。

この構成により、既存のQAワークフロー資産を活かしつつ、将来的なワークフロー追加や他エージェント対応にも拡張しやすいCLIツールにできる。
