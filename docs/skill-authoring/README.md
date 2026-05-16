# Workflow Asset Authoring Guide

このディレクトリは、`qa-workflow-toolkit` に新しい workflow asset を追加する場合、または既存 workflow の skill / command / shared asset を再構成する場合の保守方針をまとめる。
通常の QA 実行時に必ず読む運用ルールではなく、workflow asset を作成・分割・レビューする人または agent が参照する文書である。

## 文書の位置づけ

| 配置先 | 役割 |
|---|---|
| `AGENTS.md` | リポジトリ全体の常時適用ルール。詳細な skill 作成手順は置かない。 |
| `docs/skill-authoring/` | workflow asset の追加、再構成、レビューに関する保守者向け方針。 |
| `src/qa_workflow_toolkit/assets/workflow/` | CLI が配布する workflow asset の正。 |
| `src/qa_workflow_toolkit/assets/workflow/shared/` | 複数 workflow が実行時に参照する共通ポリシー、用語、出力ルール。 |
| `src/qa_workflow_toolkit/assets/workflow/workflows/<workflow>/workflow.json` | CLI が workflow を列挙・インストールするための manifest。 |
| `src/qa_workflow_toolkit/assets/workflow/workflows/<workflow>/skill/` | インストール後に `.agents/skills/<workflow>/` へ配置される skill 本体。 |
| `src/qa_workflow_toolkit/assets/workflow/commands/<workflow>.md` | agent 別 command ディレクトリへ配置される command。 |

## 基本原則

- `SKILL.md` は入口に限定し、巨大な実行マニュアルにしない。
- 実行手順は `steps/`、判断基準や定義は `references/`、成果物形式は `templates/` に分離する。
- 分割は行数だけで決めず、業務上の責務単位で行う。
- `part1`、`part2` のような番号だけの分割は避け、ファイル名から目的が分かるようにする。
- 共通ルールを `AGENTS.md`、`SKILL.md`、`steps/` に重複記載しない。共通化する場合は package asset 側の `assets/workflow/shared/` に置く。
- 既存のステップ ID、成果物 ID、参照 ID は可能な限り維持する。
- 実行成果物の出力先は `assets/workflow/shared/output_location_policy.md` を参照し、skill 本体や共通ポリシー配下に混在させない。
- 通常実行時に不要な作成者向け説明は、このディレクトリに置く。
- CLI 本体に workflow 固有の手順や判断基準を埋め込まない。workflow 固有情報は `workflow.json` と asset markdown に閉じ込める。

## 標準構成

```text
src/qa_workflow_toolkit/assets/workflow/
  shared/
  commands/
    <workflow>.md
  workflows/
    <workflow>/
      workflow.json
      skill/
        SKILL.md
        orchestrator.md
        rules.md
        steps/
          step_01_<purpose>_guide.md
          step_02_<purpose>_guide.md
        references/
          <topic>_policy.md
          <topic>_catalog.md
        templates/
          <artifact>_template.md
        examples/
          <theme>_example.md
```

`examples/` は必要な場合だけ作成する。通常の実行で毎回読む必要がない具体例、良い例・悪い例、完成例を置く。

## 新規 workflow 追加の流れ

1. workflow の目的、対象入力、対象外、主要成果物、command 名を定義する。
2. `src/qa_workflow_toolkit/assets/workflow/workflows/<workflow>/skill/` に skill 本体を作成する。
3. `src/qa_workflow_toolkit/assets/workflow/commands/<workflow>.md` に command を作成する。
4. `src/qa_workflow_toolkit/assets/workflow/workflows/<workflow>/workflow.json` を作成し、install source / target を定義する。
5. `qatool workflow list` で workflow が表示されることを確認する。
6. 一時ディレクトリへ `qatool workflow install --workflow <workflow> --agent roocode --target <tmp> --yes` を実行し、配置結果を確認する。
7. `qatool workflow install --workflow <workflow> --agent claude --target <tmp> --yes` で command が `.claude/commands/` に入ることも確認する。
8. `pytest` で registry / installer / CLI の期待値を確認する。sort order や workflow 数の固定期待がある場合はテストを更新する。

詳細は [workflow_addition_guide.md](workflow_addition_guide.md) を参照する。

## 関連文書

- [workflow_addition_guide.md](workflow_addition_guide.md): 現行CLIに workflow を追加する際の実装ポイント。
- [skill_structure_standard.md](skill_structure_standard.md): skill 配下の標準ファイル構成。
- [file_size_policy.md](file_size_policy.md): ファイル種別ごとの目安行数と分割基準。
- [naming_conventions.md](naming_conventions.md): skill 名、steps、references、templates の命名規則。
- [migration_checklist.md](migration_checklist.md): 既存プロンプト群を skill へ移行する際のチェックリスト。
- [skill_review_checklist.md](skill_review_checklist.md): 追加・再構成後のレビュー観点。
