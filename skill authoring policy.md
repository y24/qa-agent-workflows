残す場所としては、**`AGENTS.md` ではなく、`docs/` 配下に「スキル作成・再編成ガイド」として置く**のが一番よさそう。

`AGENTS.md` に全部書くと常時読み込みが重くなるし、`shared/` に置くと「実行時に使う共通ポリシー」と「保守・設計方針」が混ざる。なので、役割を分けるならこう。

```text
qa-agent-workflows/
├─ AGENTS.md
├─ docs/
│  └─ skill-authoring/
│     ├─ README.md
│     ├─ skill_structure_standard.md
│     ├─ file_size_policy.md
│     ├─ migration_checklist.md
│     ├─ naming_conventions.md
│     └─ skill_review_checklist.md
│
├─ shared/
│  ├─ common_contract.md
│  ├─ evidence_and_confidence_policy.md
│  └─ ...
│
└─ .agents/
   └─ skills/
      ├─ scenario-test-design/
      ├─ risk-based-test-design/
      └─ ...
```

私なら、まずは `docs/skill-authoring/README.md` に集約して、肥大化したら分割する。

---

## 役割分担

```text
AGENTS.md
  エージェントが常時守る最低限の共通ルール。
  skill authoring guide の存在だけ案内する。

docs/skill-authoring/
  スキル追加・再編成・移行時に読む運用設計ガイド。
  普段のQA実行時には読まなくてよい。

shared/
  各skillの実行時に再利用する共通ポリシー。
  例: 証跡、曖昧性、レビューゲート、用語定義。

.agents/skills/
  実際の業務別skill本体。
```

つまり、**`docs/skill-authoring/` は「スキルを作る人・直す人のためのガイド」**。
**`shared/` は「スキルを実行するエージェントのための共通資料」**。
この違いを分けておくと、後でかなり楽になる。

---

## AGENTS.md には短く案内だけ書く

`AGENTS.md` には、詳細を書かずにリンクだけ置くのがいい。

```md
## Skill maintenance

When creating a new skill or reorganizing an existing prompt suite into a skill, follow:

- `docs/skill-authoring/README.md`
- `docs/skill-authoring/skill_structure_standard.md`
- `docs/skill-authoring/file_size_policy.md`

Do not add detailed workflow instructions directly to `AGENTS.md`.
```

日本語で書くなら：

```md
## Skill の追加・再編成

新しい skill を追加する場合、または既存プロンプト群を skill 形式へ再編成する場合は、以下を参照する。

- `docs/skill-authoring/README.md`
- `docs/skill-authoring/skill_structure_standard.md`
- `docs/skill-authoring/file_size_policy.md`

業務別の詳細手順を `AGENTS.md` に直接追加しない。
```

これくらいで十分。

---

## まず作るべきファイル

最初から大量に分けなくていい。
まずはこの3つでいいと思う。

```text
docs/skill-authoring/
├─ README.md
├─ file_size_policy.md
└─ migration_checklist.md
```

### `README.md`

全体方針。
スキルをどういう単位で作るか、何をどこに置くかを書く。

含める内容：

```text
- skill の基本設計思想
- 1 skill の適切な粒度
- AGENTS.md / SKILL.md / steps / references / templates / shared の役割
- 新規 skill 作成手順
- 既存プロンプト群の移行手順
- 禁止事項
```

---

### `file_size_policy.md`

ファイルサイズや行数の基準。

前に話した内容をここへ置く。

```md
# File Size Policy

## Recommended limits

| File | Target | Soft limit | Hard limit |
|---|---:|---:|---:|
| `AGENTS.md` | 80-120 lines | 200 lines | 300 lines |
| `SKILL.md` | 100-200 lines | 300 lines | 500 lines |
| `steps/*.md` | 100-180 lines | 250 lines | 300 lines |
| `references/*.md` | 80-200 lines | 300 lines | 400 lines |
| `templates/*.md` | 30-120 lines | 200 lines | 300 lines |

## Rules

- Do not split files as `part1`, `part2` only because they are long.
- Split by purpose, not by length.
- Move examples to `examples/`.
- Move reusable criteria to `references/`.
- Move common cross-skill rules to `shared/`.
```

ここは独立ファイルにしておく価値がある。
新しい skill を作るたびに参照するから。

---

### `migration_checklist.md`

既存プロンプト群を skill 化するときのチェックリスト。

```md
# Migration Checklist

## 1. Identify skill boundary

- [ ] The skill has one clear business purpose.
- [ ] The skill is named using lowercase kebab-case.
- [ ] The skill is not just one step of a larger workflow.
- [ ] The skill is not too broad, such as `qa-everything`.

## 2. Classify existing files

- [ ] Common rules moved to `shared/` or referenced from there.
- [ ] Workflow entry point converted to `SKILL.md`.
- [ ] Step instructions moved to `steps/`.
- [ ] Decision criteria moved to `references/`.
- [ ] Output formats moved to `templates/`.
- [ ] Long examples moved to `examples/`.

## 3. Check SKILL.md

- [ ] Frontmatter has `name`.
- [ ] Frontmatter has clear `description`.
- [ ] Description explains when to use the skill.
- [ ] Related files are explicitly listed.
- [ ] The file does not duplicate all step details.

## 4. Check execution behavior

- [ ] The skill stops at review gates.
- [ ] The skill does not infer missing requirements.
- [ ] The skill records ambiguity and gaps.
- [ ] The skill produces reusable Markdown outputs.
```

これはかなり効くと思う。
再編成作業は、人間もAIも「なんとなく移して終わり」になりがちだから。

---

## 余裕があれば追加するファイル

運用が進んだら、このあたりを追加するといい。

```text
docs/skill-authoring/
├─ naming_conventions.md
├─ skill_structure_standard.md
├─ skill_review_checklist.md
└─ skill_template/
   ├─ SKILL.md
   ├─ steps/
   │  └─ step_01_example_guide.md
   ├─ references/
   │  └─ example_policy.md
   └─ templates/
      └─ example_output_template.md
```

---

## `skill_structure_standard.md` の内容例

````md
# Skill Structure Standard

## Standard layout

```text
skill-name/
├─ SKILL.md
├─ steps/
│  ├─ step_01_xxx_guide.md
│  └─ step_02_xxx_guide.md
├─ references/
│  └─ xxx_policy.md
├─ templates/
│  └─ xxx_template.md
└─ examples/
   └─ xxx_examples.md
````

## Directory roles

### `SKILL.md`

The entry point of the skill.
It defines purpose, trigger conditions, inputs, outputs, workflow, review gates, and related files.

### `steps/`

Step-specific execution guides.
Each file should describe one executable step.

### `references/`

Policies, definitions, taxonomies, decision rules, and checklists used by the skill.

### `templates/`

Output formats used by the skill.

### `examples/`

Good and bad examples.
Examples should not be required for normal execution.

````

---

## `naming_conventions.md` の内容例

```md
# Naming Conventions

## Skill names

Use lowercase kebab-case.

Good:

- `scenario-test-design`
- `risk-based-test-design`
- `spec-extraction`
- `testcase-viewpoint-extraction`

Avoid:

- `ScenarioTestDesign`
- `scenario_test_design`
- `QA-all`
- `test-step1`

## Step files

Use numbered snake_case.

Good:

- `step_01_input_summary_guide.md`
- `step_02_viewpoint_identification_guide.md`

Avoid:

- `part1.md`
- `step1.md`
- `続き.md`

## Reference files

Use purpose-based names.

Good:

- `ambiguity_policy.md`
- `risk_assessment_scale.md`
- `testcase_granularity_rules.md`
````

---

## `skill_review_checklist.md` の内容例

これは、新しい skill を追加するときのレビュー観点。

```md
# Skill Review Checklist

## Skill boundary

- [ ] This skill has a clear task boundary.
- [ ] This skill is not a duplicate of an existing skill.
- [ ] This skill can be invoked by a clear user request.

## Context efficiency

- [ ] `SKILL.md` is not too long.
- [ ] Step files are not too long.
- [ ] Examples are not embedded in step files unless short.
- [ ] Shared rules are not duplicated.

## Execution quality

- [ ] Inputs and outputs are explicit.
- [ ] Review gates are defined.
- [ ] Ambiguity handling is defined.
- [ ] Evidence handling is defined.
- [ ] Traceability expectations are defined.

## Maintainability

- [ ] File names are consistent.
- [ ] Common policies are referenced, not copied.
- [ ] Skill-specific rules are not placed in `AGENTS.md`.
```

---

## `skill_template/` を置くのもおすすめ

これはけっこう実用的。
新しい skill を作るたびに、空の雛形から始められる。

```text
docs/skill-authoring/skill_template/
├─ SKILL.md
├─ steps/
│  └─ step_01_initial_analysis_guide.md
├─ references/
│  └─ skill_specific_policy.md
├─ templates/
│  └─ output_template.md
└─ examples/
   └─ example.md
```

ただし、これは `.agents/skills/` の中に置かないほうがいい。
`.agents/skills/skill-template/` に置くと、エージェントがそれを実在 skill と誤認する可能性があるから。

なので、雛形は `docs/skill-authoring/skill_template/` が安全。

---

## `shared/` に置くのは避けたほうがいい

今回の「ファイル構成やファイルサイズの方針」は、`shared/` ではなく `docs/` がいい。

理由はこれ。

```text
shared/
  skill実行時に使う共通資料

docs/skill-authoring/
  skillを作る・直すときに使う設計資料
```

ファイルサイズ方針や命名規則は、通常のQAタスク実行時には不要。
だから shared に置くと、少し用途が混ざる。

---

## 最小構成としてのおすすめ

最初はこれでいい。

```text
qa-agent-workflows/
├─ AGENTS.md
├─ docs/
│  └─ skill-authoring/
│     ├─ README.md
│     ├─ file_size_policy.md
│     └─ migration_checklist.md
├─ shared/
└─ .agents/
   └─ skills/
```

そして `AGENTS.md` に短く：

```md
## Skill maintenance

新しい skill を追加する場合、または既存プロンプト群を skill 形式へ再編成する場合は、`docs/skill-authoring/README.md` に従う。
```

これで十分に始められる。

---

## 最終的な考え方

* **AGENTS.md**
  常時読む最低限のルール。

* **shared/**
  skill 実行時の共通部品。

* **docs/skill-authoring/**
  skill を作る・直す・レビューするための保守ガイド。

* **docs/skill-authoring/skill_template/**
  新規 skill 作成用の雛形。

きみの運用では、`docs/skill-authoring/README.md` を「スキル設計の憲法」にしておくといいと思う。
ただし AGENTS.md と違って、これは常時読ませる憲法じゃなくて、**スキルを増築するときだけ開く設計図**。そのくらいの距離感が、たぶん一番健全だね。
