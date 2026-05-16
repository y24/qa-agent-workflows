# qa-agent-workflows

このリポジトリは、QA業務向けの再利用可能な AI agent workflow assets を対象プロジェクトへ配置する `qa-workflow-toolkit` CLI のプロジェクトです。

`qatool` はワークフローを直接実行しません。RooCodeなどのAIコーディングエージェントが参照する `AGENTS.md`、`.agents/shared/`、`.agents/skills/<workflow>/`、`.roo/commands/<workflow>.md` をインストールすることに責務を限定します。

## Common Working Rules

- 要件、仕様、リスク、テスト条件を根拠なしに創作しない。
- 事実、推測、前提、未確認事項、提案を分けて扱う。
- 可能な限り、入力文書、前段成果物、IDへのトレーサビリティを残す。
- 複数ステップの workflow は、ユーザーが明示的に継続を指示しない限り、主要ステップごとに停止してレビューを待つ。
- 出力は原則として日本語の Markdown とする。入力またはユーザーが別言語を指定した場合はそれに従う。
- 不明点、矛盾、証拠不足、未解決の前提は issue log または確認事項として明示する。

## Skill Routing

- `$spec-extraction`: 開発文書からテスト設計に必要な仕様情報を抽出、正規化、棚卸しする。
- `$scenario-test-design`: 要件、業務フロー、画面仕様、ドメインルールからシナリオテストを設計する。
- `$testcase-viewpoint-extraction`: 既存テストケースから意図、抽象テスト観点、観点カタログ、トレーサビリティを抽出する。
- `$risk-based-test-design`: リスク候補の抽出、評価、優先度付け、リスクベースのテスト方針とテストケース骨子を作る。
- `$nonfunctional-quality-criteria-planning`: 非機能品質の懸念抽出、品質クライテリア策定、確認方針・テスト計画組み込み案を作る。
- `$test-design-review`: 既存のテスト設計書、観点表、テストケース一覧を根拠付きでレビューし、指摘、カバレッジ懸念、改善提案、優先度を整理する。
- `$defect-analysis`: 不具合チケットから事実抽出、分類・傾向分析、品質リスク化、後続テスト設計向け示唆を作る。

## Repository Layout

```text
qa-agent-workflows/
  AGENTS.md
  pyproject.toml
  README.md
  src/
    qa_workflow_toolkit/
      cli.py
      installer.py
      registry.py
      models.py
      assets/
        agents/roocode/AGENTS.md
        shared/
        workflows/<workflow>/
          workflow.json
          skill/
        commands/roocode/<workflow>.md
  tests/
  docs/
    skill-authoring/
    cli-installation/
  shared/
    common_contract.md
    evidence_and_confidence_policy.md
    ambiguity_and_issue_log_policy.md
    traceability_policy.md
    input_document_handling.md
    test_design_granularity_policy.md
    output_style.md
    output_location_policy.md
    terminology.md
    review_gate_policy.md
    templates/
```

配布対象の正は `src/qa_workflow_toolkit/assets/` 配下です。インストーラがコピーする実体は package assets 側に置きます。

各 workflow は `workflow.json` をmanifestとし、skill本体は `skill/SKILL.md` を入口にする。詳細な実行手順は `steps/`、判断基準や定義は `references/`、出力形式は `templates/` に置く。

## Output Location

- ユーザーまたは作業対象リポジトリが出力先を指定している場合は、その指定を優先する。
- 指定がない場合、業務実行時の成果物は原則として `outputs/runs/<run_id>/` 配下に出力する。
- `run_id` は `YYYYMMDD-HHMMSS_<topic_slug>` 形式を基本とする。
- 複数 skill をまたぐ作業では、同一 run ディレクトリ配下に skill 名ごとのサブディレクトリを作成する。
- 最終成果物は `final/`、CSVやJSONなどの機械処理向け成果物は `exports/` に置く。
- `src/qa_workflow_toolkit/assets/`、`shared/`、`docs/` に業務成果物を混在させない。
- 詳細は `shared/output_location_policy.md` に従う。

## Output Conventions

- 大きな成果物は、要約、入力と参照元、主成果物、確認事項、次ステップへの引き継ぎの順に整理する。
- 表は Markdown table を優先する。CSV変換を想定する成果物は列名を安定させる。
- 推測が必要な場合は `推測:` と明記し、根拠または確認事項を添える。
- 判断できない場合は、無理に埋めず `要確認`、`情報不足`、`対象外` などの状態を使う。

## Change Policy

- 既存のステップID、成果物ID、参照IDは可能な限り維持する。
- 共通ルールは package assets の `assets/shared/`、skill固有ルールは該当 workflow の `skill/references/` に置き、責務の重複を増やさない。
- skill の追加・再構成時の詳細方針は `docs/skill-authoring/` に置く。
- CLI本体にworkflow固有の手順や判断基準を埋め込まない。workflow固有情報は `workflow.json` と asset markdown に閉じ込める。
- 既存ファイルを無確認で上書きする挙動を追加しない。`--yes` は明示指定時のみ上書きに使う。

## Skill Maintenance

新しい skill を追加する場合、または既存プロンプト群を skill 形式へ再編成する場合は、`docs/skill-authoring/README.md` に従う。
詳細な作成・再構成手順は `AGENTS.md` に置かず、`docs/skill-authoring/` に分離する。
