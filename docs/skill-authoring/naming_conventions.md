# Naming Conventions

この文書は、skill とその構成ファイルの命名規則を定義する。
名前は、通常実行時に必要なファイルをすばやく判断できることを優先する。

## skill 名

- 小文字の kebab-case を使う。
- 業務目的が分かる名前にする。
- 技術的な実装方式ではなく、QA 業務上の用途を表す。

例:

```text
spec-extraction
scenario-test-design
testcase-viewpoint-extraction
risk-based-test-design
```

## steps

形式:

```text
step_<number>_<purpose>_guide.md
```

ルール:

- `<number>` は2桁にする。
- `<purpose>` はそのステップの成果または作業を表す。
- `guide` は実行手順であることを示す。
- 既存のステップ ID がある場合は、可能な限り維持する。

例:

```text
step_01_input_review_guide.md
step_02_normalization_guide.md
step_03_review_pack_guide.md
```

## references

形式:

```text
<topic>_<kind>.md
```

主な `<kind>`:

| 種別 | 用途 |
|---|---|
| `policy` | 方針、判断ルール、制約。 |
| `catalog` | 分類、観点、リスク、パターンの一覧。 |
| `criteria` | 評価基準、判定条件。 |
| `taxonomy` | 階層分類や概念整理。 |
| `glossary` | 用語定義。 |

例:

```text
risk_scoring_policy.md
scenario_pattern_catalog.md
evidence_classification_criteria.md
```

## templates

形式:

```text
<artifact>_template.md
```

例:

```text
spec_inventory_template.md
scenario_test_outline_template.md
risk_assessment_template.md
```

複数成果物を1ファイルにまとめる場合は、短い補助テンプレートに限る。
主要成果物は原則として1ファイル1テンプレートにする。

## examples

形式:

```text
<theme>_example.md
```

良い例・悪い例・完成例を分ける場合:

```text
<theme>_good_example.md
<theme>_bad_example.md
<theme>_complete_example.md
```

## 避ける名前

- `part1.md`、`part2.md`
- `misc.md`
- `notes.md`
- `prompt.md`
- `new.md`
- `old.md`
- `final.md`
- `copy.md`

一時的な名前で作成した場合でも、作業完了前に目的が分かる名前へ変更する。
