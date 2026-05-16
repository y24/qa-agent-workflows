# Output Location Policy

## Default Output Root

ユーザーまたは作業対象リポジトリが出力先を指定している場合は、その指定を優先する。
指定がない場合、業務実行時の成果物は以下へ出力する。

```text
outputs/runs/<run_id>/
```

## Run ID

`run_id` は以下の形式を基本とする。

```text
YYYYMMDD-HHMMSS_<topic_slug>
```

- 日時は作業開始時点のローカル時刻を使う。
- `topic_slug` は英数字、ハイフン、アンダースコア中心で短く表す。
- 日本語や空白を含む案件名は、必要に応じて `_run_manifest.md` の Topic に記録する。

## Standard Run Layout

```text
outputs/runs/<run_id>/
  _run_manifest.md
  _input_inventory.md
  _issue_log.md
  <skill-name>/
  final/
  exports/
```

## Directory Roles

| Path | Role |
|---|---|
| `outputs/runs/<run_id>/_run_manifest.md` | run の目的、使用 skill、出力先、開始時刻などのメタ情報 |
| `outputs/runs/<run_id>/_input_inventory.md` | 入力文書、前段成果物、参照元の一覧 |
| `outputs/runs/<run_id>/_issue_log.md` | skill 横断の未解決事項、矛盾、不足、確認事項 |
| `outputs/runs/<run_id>/<skill-name>/` | skill ごとの中間成果物、Step 成果物、handoff |
| `outputs/runs/<run_id>/final/` | 人間が読む最終成果物 |
| `outputs/runs/<run_id>/exports/` | CSV、JSON、Excel 変換用などの機械処理向け成果物 |

## Rules

- `.agents/skills/` 配下に業務成果物を出力しない。
- `shared/` 配下に業務成果物を出力しない。
- `docs/` 配下に業務成果物を出力しない。
- 複数 skill をまたぐ作業では、同一 run ディレクトリ配下に skill 名ごとのサブディレクトリを作成する。
- skill ごとの中間成果物は `<skill-name>/` に置く。
- 次工程へ渡す要約が必要な場合は、対象 skill のディレクトリに `_handoff.md` を置く。
- 人間向けの最終成果物は `final/` に置く。
- CSV、JSON、Excel 変換用などの機械処理向け成果物は `exports/` に置く。
- 未解決事項は run 直下の `_issue_log.md` に集約するか、skill 別 issue log から参照する。

## Git Handling

通常の業務成果物を git 管理するかどうかは、ユーザー指定または対象プロジェクトの運用に従う。
指定がない場合は、機密情報や案件固有情報が含まれる可能性を前提に、コミット対象にする前に確認する。
