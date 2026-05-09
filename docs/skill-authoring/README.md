# Skill Authoring Guide

このディレクトリは、新しい skill を追加する場合、または既存のプロンプト群を skill 形式へ再編成する場合の保守方針をまとめる。
通常の QA 実行時に必ず読む運用ルールではなく、skill を作成・分割・レビューする人または agent が参照する文書である。

## 文書の位置づけ

| 配置先 | 役割 |
|---|---|
| `AGENTS.md` | リポジトリ全体の常時適用ルール。詳細な skill 作成手順は置かない。 |
| `docs/skill-authoring/` | skill の追加、再構成、レビューに関する保守者向け方針。 |
| `shared/` | 複数 skill が実行時に参照する共通ポリシー、用語、出力ルール。 |
| `.agents/skills/<skill-name>/` | 実際に呼び出される skill 本体。 |

## 基本原則

- `SKILL.md` は入口に限定し、巨大な実行マニュアルにしない。
- 実行手順は `steps/`、判断基準や定義は `references/`、成果物形式は `templates/` に分離する。
- 分割は行数だけで決めず、業務上の責務単位で行う。
- `part1`、`part2` のような番号だけの分割は避け、ファイル名から目的が分かるようにする。
- 共通ルールを `AGENTS.md`、`SKILL.md`、`steps/` に重複記載しない。
- 既存のステップ ID、成果物 ID、参照 ID は可能な限り維持する。
- 通常実行時に不要な作成者向け説明は、このディレクトリに置く。

## 標準構成

```text
.agents/skills/<skill-name>/
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

## 作成・再構成の流れ

1. skill の目的、対象入力、対象外、主要成果物を定義する。
2. 既存文書またはプロンプトを、入口、手順、判断基準、テンプレート、例に分類する。
3. ファイルサイズ方針に従い、責務単位で分割する。
4. `SKILL.md` から必要なファイルだけを参照できるようにリンクを整理する。
5. トレーサビリティ、レビューゲート、確認事項の扱いが失われていないか確認する。
6. 移行チェックリストで、重複、リンク切れ、巨大ファイル化を確認する。

## 関連文書

- [skill_structure_standard.md](skill_structure_standard.md): skill 配下の標準ファイル構成。
- [file_size_policy.md](file_size_policy.md): ファイル種別ごとの目安行数と分割基準。
- [naming_conventions.md](naming_conventions.md): skill 名、steps、references、templates の命名規則。
- [migration_checklist.md](migration_checklist.md): 既存プロンプト群を skill へ移行する際のチェックリスト。
- [skill_review_checklist.md](skill_review_checklist.md): 追加・再構成後のレビュー観点。
