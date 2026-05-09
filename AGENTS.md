# qa-agent-workflows

このリポジトリは、QA業務向けの再利用可能な AI agent workflow skills をまとめたプロジェクトです。

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

## Repository Layout

```text
qa-agent-workflows/
  AGENTS.md
  shared/
    qa_common_contract.md
    evidence_and_confidence_policy.md
    terminology.md
    output_style.md
    review_gate_policy.md
  .agents/
    skills/
      spec-extraction/
      scenario-test-design/
      testcase-viewpoint-extraction/
      risk-based-test-design/
```

各 skill は `SKILL.md` を入口とし、詳細な実行手順は `steps/`、判断基準や定義は `references/`、出力形式は `templates/` に置く。

## Output Conventions

- 大きな成果物は、要約、入力と参照元、主成果物、確認事項、次ステップへの引き継ぎの順に整理する。
- 表は Markdown table を優先する。CSV変換を想定する成果物は列名を安定させる。
- 推測が必要な場合は `推測:` と明記し、根拠または確認事項を添える。
- 判断できない場合は、無理に埋めず `要確認`、`情報不足`、`対象外` などの状態を使う。

## Change Policy

- 既存のステップID、成果物ID、参照IDは可能な限り維持する。
- 既存プロンプト本文を更新する場合は、責務の重複を増やさない。共通ルールは `AGENTS.md` または `shared/`、skill固有ルールは該当 skill の `references/` に置く。
- `SKILL.md` は入口、目的、トリガー、入出力、workflow、参照ファイル一覧に限定し、巨大な実行マニュアルにしない。

### File Size Policy

- 1ファイルは「1回の作業で読ませても痛くない量」を目安にする。
- `AGENTS.md` は原則120行以内、最大200行を目安にし、業務別の詳細は `shared/` または各 skill 配下へ分離する。
- 各 skill の `SKILL.md` は原則200行以内、最大300行を目安にする。300行を超える場合は、詳細を `steps/`、`references/`、`templates/` へ分離する。
- 各 `steps/*.md` は原則180行以内、最大250行を目安にする。250行を超える場合は、判断基準・例・テンプレートを別ファイル化する。
- `references/*.md` が100行を超える場合は冒頭に目次を置き、300行を超える場合はテーマ別に分割する。
- `templates/*.md` はできるだけ100行以内にし、複数テンプレートを1ファイルに詰め込まない。
- `examples/*.md` は1ファイル1テーマを基本とし、良い例・悪い例・完成例が長い場合は分割する。
- `scripts/` は行数より責務の単位を優先し、1機能1スクリプトを目安にする。
- 同じルールを `AGENTS.md`、`SKILL.md`、`steps/` に重複記載しない。
