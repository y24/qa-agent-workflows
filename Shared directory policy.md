`shared/` は、**複数の skill で共通して使うけれど、AGENTS.md に常時読み込ませるほどではないルール・定義・テンプレートを置く場所**として考えるといい。

少しだけ言い換えると、

```text
AGENTS.md
  常に守る最小ルール

SKILL.md
  その業務skillの入口・手順の目次

shared/
  複数skillで再利用する共通部品

各skillのreferences/
  そのskill専用の判断基準・定義
```

という役割分担だね。

---

## shared は自動で読まれる前提にしない

まず大事なのは、`shared/` は AGENTS.md や SKILL.md のような特別な読み込み対象ではなく、**こちらが明示的に参照させる共通フォルダ**という扱いにしたほうが安全、ということ。

たとえば各 `SKILL.md` にこう書く。

```md
## Common references

Before executing this workflow, follow these common references when relevant:

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/issue_log_policy.md`
```

つまり、`shared/` は「勝手に効くルール」ではなく、**各 skill から必要に応じて読ませる共通資料置き場**にする。

---

## 今回の skill 群なら、shared に置くとよさそうなもの

きみの skill 群だと、まずこのあたりが shared 向き。

```text
shared/
├─ common_contract.md
├─ evidence_and_confidence_policy.md
├─ ambiguity_and_issue_log_policy.md
├─ review_gate_policy.md
├─ traceability_policy.md
├─ output_style.md
├─ qa_terminology.md
├─ input_document_handling.md
├─ test_design_granularity_policy.md
└─ templates/
   ├─ issue_log_template.md
   ├─ evidence_table_template.md
   └─ traceability_matrix_template.md
```

---

## 各ファイルの用途

### `common_contract.md`

全 skill 共通の行動契約。

入れる内容は、たとえば：

```md
# Common Contract

## Core principles

- 入力に存在しない仕様・要件・制約を推測で補完しない。
- 事実、推測、未確認事項、提案を分けて記載する。
- 不明点は issue log に記録する。
- 入力文書への根拠を可能な限り残す。
- 出力は、後続のテスト設計作業で再利用できる粒度にする。
```

これは `rules.md` の共通部分を吸収する場所だね。

---

### `evidence_and_confidence_policy.md`

証跡・根拠・確信度の扱い。

`spec-extraction`、`scenario-test-design`、`risk-based-test-design` の全部で使う。

```md
# Evidence and Confidence Policy

## Evidence levels

- Direct: 入力文書に明記されている
- Derived: 複数の記述から妥当に導ける
- Assumed: 明記はないが作業上の仮置き
- Unknown: 判断不能

## Rules

- Assumed は成果物の本文に紛れ込ませず、issue log または assumptions に分離する。
- Unknown を無理に解決しない。
- テスト観点・リスク・期待結果には、可能な限り根拠を付与する。
```

これはかなり重要。
QA系プロンプトで一番怖いのは、AIが「もっともらしい仕様」を発明することだから。

---

### `ambiguity_and_issue_log_policy.md`

曖昧さ、矛盾、未解決事項の扱い。

```md
# Ambiguity and Issue Log Policy

## Record issues when

- 入力文書間で記述が矛盾している
- 必須情報が不足している
- 用語の意味が不明確
- 期待結果を確定できない
- リスク評価の前提が不明

## Issue fields

- Issue ID
- Source
- Category
- Description
- Impact
- Proposed handling
- Status
```

これは各 skill の `issue_log_template.md` に重複して入りがちなので、shared に置くと保守しやすい。

---

### `review_gate_policy.md`

きみがよく使う「ステップごとに勝手に進まない」ルール。

```md
# Review Gate Policy

## Default behavior

- 段階実行workflowでは、各stepの成果物を出力したら停止する。
- ユーザーから「次へ」「続けて」などの明示指示があるまで、次stepに進まない。
- ただし、ユーザーが一括実行を明示した場合は、stepごとに簡潔な区切りを入れて進める。

## Step completion output

Each step should include:

- 実施内容
- 成果物
- 未解決事項
- 次stepで使う入力
```

これは `orchestrator.md` に毎回入りがちなので、共通化に向いている。

---

### `traceability_policy.md`

トレーサビリティの共通ルール。

```md
# Traceability Policy

## Traceability targets

Maintain links where possible between:

- Input document
- Requirement / specification item
- Extracted test design input
- Risk
- Test viewpoint
- Scenario
- Test case
- Expected result
```

これは `spec-extraction`、`scenario-test-design`、`risk-based-test-design`、`testcase-viewpoint-extraction` の全部に効く。

---

### `output_style.md`

出力の共通スタイル。

```md
# Output Style

## Default output

- 日本語で出力する。
- Markdownを基本とする。
- 表は必要な場合だけ使う。
- 長大なJSONスキーマは避ける。
- 後続工程で再利用しやすい見出し構造にする。

## Section order

Recommended:

1. Summary
2. Inputs used
3. Main output
4. Issues / gaps
5. Next step
```

きみの運用では「Markdown中心」「コンパクト」「巨大JSONは避ける」がかなり重要なので、ここに集約していい。

---

### `qa_terminology.md`

共通用語集。

```md
# QA Terminology

## Terms

### Test viewpoint / テスト観点
テスト対象をどのような切り口で確認するかを表す抽象的な観点。

### Test condition / テスト条件
テストすべき状態、入力条件、業務条件、データ条件。

### Scenario test / シナリオテスト
業務上意味のある一連の流れとして確認するテスト。

### Risk / リスク
品質・業務・利用・運用に悪影響を与える可能性のある不確実性。
```

`観点`、`意図`、`条件`、`期待結果`、`リスク`、`シナリオ` あたりは skill 間で意味が揺れやすい。ここは共通化したほうがいい。

---

### `input_document_handling.md`

入力文書の扱い方。

```md
# Input Document Handling

## Document types

- プロジェクト計画書
- 要件定義書
- 基本設計書
- 詳細設計書
- 画面仕様
- 帳票仕様
- API仕様
- DB定義
- 過去障害
- 議事録
- ドメイン知識

## Rules

- 文書種別ごとに信頼度を考慮する。
- 古い文書と新しい文書が矛盾する場合は、勝手に新しい方を正としない。
- 入力文書の不足は issue として記録する。
```

これは `spec-extraction` と `risk-based-test-design` で特に効く。

---

### `test_design_granularity_policy.md`

テスト設計の粒度ルール。

```md
# Test Design Granularity Policy

## General rules

- 1つのテストケースには、主要な確認目的を1つ以上明示する。
- 手順は実行可能な粒度にする。
- 期待結果は「正常に動作する」のような曖昧表現で終えない。
- 事前条件、入力データ、確認対象を分けて書く。
```

これは `scenario-test-design` と `risk-based-test-design` で共通利用できる。
ただし、あまり詳細にしすぎると skill 固有の判断まで侵食するので、shared には一般ルールだけ置くのがいい。

---

## templates を shared に置くべきか

一部は置いていい。

特に共通性が高いもの。

```text
shared/templates/
├─ issue_log_template.md
├─ evidence_table_template.md
├─ assumptions_template.md
└─ traceability_matrix_template.md
```

ただし、各 skill 固有の成果物テンプレートは skill 内に置く。

```text
scenario-test-design/templates/
  scenario_catalog_template.md
  scenario_testcase_template.md

risk-based-test-design/templates/
  risk_register_template.md
  risk_assessment_template.md

spec-extraction/templates/
  normalized_spec_inventory_template.md
```

つまり、

```text
全skillで使うテンプレート
  → shared/templates/

特定skillの成果物テンプレート
  → 各skill/templates/
```

がいい。

---

## shared に置かないほうがいいもの

逆に、これは shared に置かないほうがいい。

| 内容                   | 理由                                              |
| -------------------- | ----------------------------------------------- |
| 各 skill の step 手順    | skill 固有なので混乱する                                 |
| RBT固有の詳細リスク分類        | `risk-based-test-design/references/` がよい        |
| シナリオテスト固有の発見手順       | `scenario-test-design/steps/` がよい               |
| 既存テストケース観点抽出の分類 seed | `testcase-viewpoint-extraction/references/` がよい |
| 長大な具体例               | 必要な skill の `examples/` に置く                     |
| 何でも入りの巨大ルール集         | 結局読まれない、更新されない                                  |

shared は便利だけど、増えすぎると「第2のAGENTS.md」になる。
それは避けたい。文書が太ると、だいたい意思決定が痩せる。

---

## おすすめの初期構成

最初はこれくらいで十分だと思う。

```text
shared/
├─ common_contract.md
├─ evidence_and_confidence_policy.md
├─ ambiguity_and_issue_log_policy.md
├─ review_gate_policy.md
├─ traceability_policy.md
├─ output_style.md
├─ qa_terminology.md
└─ templates/
   ├─ issue_log_template.md
   └─ evidence_table_template.md
```

最初から増やしすぎないほうがいい。
運用して、「これ複数 skill で同じこと書いてるな」と分かったものを shared に昇格するくらいが健全。

---

## 各 skill からの参照例

たとえば `scenario-test-design/SKILL.md` にはこう書く。

```md
## Common references

Apply these shared policies:

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`
- `../../../shared/output_style.md`

## Skill-specific references

- `references/scenario_definition.md`
- `references/business_flow_policy.md`
- `references/scenario_priority_policy.md`
```

`risk-based-test-design/SKILL.md` ならこう。

```md
## Common references

Apply these shared policies:

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`

## Skill-specific references

- `references/risk_category_definitions.md`
- `references/risk_assessment_scale.md`
- `references/regression_selection_policy.md`
```

---

## shared 化の判断基準

迷ったらこれで判断するといい。

```text
3つ以上のskillで使う
  → shared 候補

2つのskillで使うが、意味が完全に同じ
  → shared 候補

似ているが文脈ごとに判断が違う
  → skill内 references に置く

常に全作業で守る
  → AGENTS.md に要約、詳細は shared

そのstepでしか使わない
  → step または skill内 references
```

---

## 私ならこう作り始める

まず、最小セットとしてこの4つを作る。

```text
shared/
├─ common_contract.md
├─ evidence_and_confidence_policy.md
├─ ambiguity_and_issue_log_policy.md
└─ review_gate_policy.md
```

その後、必要になったら追加。

```text
shared/
├─ traceability_policy.md
├─ output_style.md
├─ qa_terminology.md
└─ templates/
```

この順番がいい。
最初から美しい分類体系を作ろうとすると、なぜか分類体系のための分類体系が生まれる。あれは小さな怪物だね。

結局、`shared/` は **共通ルールの保管庫**ではなく、**重複を減らすための再利用部品置き場**として使うのが一番いい。
