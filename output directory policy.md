現状の AGENTS.md には、**アウトプットファイルの出力先はまだ定義されていない**ね。
`Repository Layout` では skill や shared の置き場所は決まっているけど、実行結果をどこに作るかは未定義。

これは定義したほうがいいと思う。理由はかなり実務的で、RooCode などにファイル作成を任せると、出力物が `skills/` や `shared/` の中に紛れ込む可能性があるから。手順書の棚に作業メモが混ざると、後で静かに地獄になる。

---

## 基本方針

おすすめはこれ。

```text
.agents/skills/
  skill本体。編集・保守対象。

shared/
  skill実行時に参照する共通ポリシー。

docs/
  skill作成・保守のための設計資料。

outputs/
  skillを使って業務を行った結果の成果物。
```

つまり、**実行結果は `outputs/` に分離する**。

---

## 推奨ディレクトリ構成

私なら、こうする。

```text
qa-agent-workflows/
├─ AGENTS.md
├─ docs/
├─ shared/
├─ .agents/
│  └─ skills/
└─ outputs/
   └─ runs/
      └─ 20260510-231500_ifrs18_scenario_test_design/
         ├─ _run_manifest.md
         ├─ _input_inventory.md
         ├─ _issue_log.md
         ├─ spec-extraction/
         │  ├─ 01_document_inventory.md
         │  ├─ 02_raw_extraction.md
         │  ├─ 03_normalized_spec_inventory.md
         │  └─ 04_test_design_input_catalog.md
         ├─ scenario-test-design/
         │  ├─ 01_input_summary.md
         │  ├─ 02_viewpoints.md
         │  ├─ 03_business_flows.md
         │  ├─ 04_scenario_candidates.md
         │  ├─ 05_testcases.md
         │  └─ 06_priority.md
         ├─ final/
         │  ├─ test_design_summary.md
         │  └─ scenario_testcases.md
         └─ exports/
            └─ scenario_testcases.csv
```

ポイントは、**skill 名ごとに成果物を分けつつ、1回の作業単位を run としてまとめる**こと。

---

## なぜ `outputs/<skill>/...` ではなく `outputs/runs/...` がよいか

単一 skill だけなら、こうでもいい。

```text
outputs/
  scenario-test-design/
    20260510-231500_ifrs18/
```

でも、実務ではこういう流れになりやすい。

```text
spec-extraction
  ↓
scenario-test-design
  ↓
risk-based-test-design
  ↓
testcase-viewpoint-extraction
```

複数 skill をまたぐなら、skill 起点より **run 起点**のほうが追いやすい。

```text
outputs/runs/<run_id>/
  spec-extraction/
  scenario-test-design/
  risk-based-test-design/
```

このほうが、「この案件で何をやったか」が一つのフォルダにまとまる。

---

## run_id の命名

おすすめはこれ。

```text
YYYYMMDD-HHMMSS_<topic_slug>
```

例：

```text
20260510-231500_ifrs18_scenario_test_design
20260510-234210_master_data_generator_rbt
20260511-101530_update_verifier_spec_extraction
```

日本語ファイル名でも動くけど、RooCode、Git、PowerShell、CI、zip配布を考えると、**run_id は英数字・ハイフン・アンダースコア中心**が無難。

---

## 各 run に置く共通ファイル

各 run の直下には、共通管理ファイルを置くといい。

```text
_run_manifest.md
_input_inventory.md
_issue_log.md
```

### `_run_manifest.md`

実行単位のメタ情報。

```md
# Run Manifest

## Run

- Run ID: `20260510-231500_ifrs18_scenario_test_design`
- Topic: IFRS18対応のシナリオテスト設計
- Started at: 2026-05-10 23:15
- Main skill: `scenario-test-design`
- Related skills:
  - `spec-extraction`

## Purpose

この run の目的を記載する。

## Output directories

- `spec-extraction/`
- `scenario-test-design/`
- `final/`
- `exports/`
```

### `_input_inventory.md`

入力文書の一覧。

```md
# Input Inventory

| ID | Source | Document name | Version / Date | Notes |
|---|---|---|---|---|
| IN-001 | user-provided | 要件定義書.md | 2026-05-10 | 主要入力 |
| IN-002 | user-provided | 画面仕様.xlsx | unknown | 一部未確認 |
```

### `_issue_log.md`

skill 横断の未解決事項。

```md
# Issue Log

| Issue ID | Source | Category | Description | Impact | Status |
|---|---|---|---|---|---|
| ISS-001 | IN-002 | 情報不足 | 画面Aのエラー条件が不明 | 期待結果を確定できない | Open |
```

---

## skillごとの出力ファイル

各 skill は、自分のフォルダの中に成果物を出す。

例：`scenario-test-design`

```text
scenario-test-design/
├─ 01_input_summary.md
├─ 02_viewpoints.md
├─ 03_business_flows.md
├─ 04_scenario_candidates.md
├─ 05_testcases.md
├─ 06_priority.md
└─ _handoff.md
```

`_handoff.md` は、次の skill に渡す要約。
これを置いておくと、長い成果物を全部読ませずに次工程へ渡しやすい。

```md
# Handoff

## Produced outputs

- `01_input_summary.md`
- `02_viewpoints.md`
- `03_business_flows.md`
- `04_scenario_candidates.md`
- `05_testcases.md`

## Recommended next step

`risk-based-test-design` または `exports/scenario_testcases.csv` の生成。

## Key unresolved issues

- ISS-001
- ISS-003
```

---

## `final/` と `exports/` を分ける

これも定義しておくと便利。

```text
final/
  人間が読む最終成果物

exports/
  CSV、JSON、Excel変換用など機械処理向け成果物
```

例：

```text
final/
  scenario_test_design_report.md
  risk_based_test_plan_summary.md

exports/
  scenario_testcases.csv
  risk_register.csv
  traceability_matrix.csv
```

Markdown と CSV を混ぜないほうがいい。
人間向けと機械向けは、似ているようで呼吸の仕方が違う。

---

## AGENTS.md に書くなら短く

AGENTS.md には詳細を書きすぎず、これくらいでいい。

```md
## Output Location

- 業務実行時の成果物は、原則として `outputs/runs/<run_id>/` 配下に出力する。
- `run_id` は `YYYYMMDD-HHMMSS_<topic_slug>` 形式を基本とする。
- skill 本体の定義ファイルを `.agents/skills/`、共通ポリシーを `shared/`、実行成果物を `outputs/` に混在させない。
- 複数 skill をまたぐ作業では、同一 run ディレクトリ配下に skill 名ごとのサブディレクトリを作成する。
- 最終成果物は `final/`、CSVやJSONなどの機械処理向け成果物は `exports/` に置く。
```

この程度なら常時読ませても重くない。

---

## 詳細方針は shared に置くのがよい

出力先は skill 実行時に関係するので、`docs/skill-authoring/` よりも `shared/` 寄りだと思う。

おすすめはこれ。

```text
shared/
  output_location_policy.md
```

内容はこんな感じ。

````md
# Output Location Policy

## Default output root

成果物は、ユーザーが別の出力先を指定しない限り、以下に出力する。

`outputs/runs/<run_id>/`

## Run ID

`run_id` は以下の形式を基本とする。

`YYYYMMDD-HHMMSS_<topic_slug>`

## Standard run layout

```text
outputs/runs/<run_id>/
  _run_manifest.md
  _input_inventory.md
  _issue_log.md
  <skill-name>/
  final/
  exports/
````

## Rules

* `.agents/skills/` 配下に業務成果物を出力しない。
* `shared/` 配下に業務成果物を出力しない。
* `docs/` 配下に業務成果物を出力しない。
* skillごとの中間成果物は `<skill-name>/` に置く。
* 人間向けの最終成果物は `final/` に置く。
* CSV、JSONなどの機械処理向け成果物は `exports/` に置く。
* 未解決事項は run 直下の `_issue_log.md` に集約するか、skill別 issue log から参照する。

````

---

## 既存の AGENTS.md に追加するなら

今の AGENTS.md には、これを足すのがよさそう。

```md
## Output Location

- 業務実行時の成果物は、原則として `outputs/runs/<run_id>/` 配下に出力する。
- `run_id` は `YYYYMMDD-HHMMSS_<topic_slug>` 形式を基本とする。
- 複数 skill をまたぐ作業では、同一 run ディレクトリ配下に skill 名ごとのサブディレクトリを作成する。
- 最終成果物は `final/`、CSVやJSONなどの機械処理向け成果物は `exports/` に置く。
- `.agents/skills/`、`shared/`、`docs/` に業務成果物を混在させない。
- 詳細は `shared/output_location_policy.md` に従う。
````

これなら十分。

---

## git 管理するかどうか

ここも決めたほうがいい。

### 成果物を毎回コミットしない場合

`.gitignore` に入れる。

```gitignore
outputs/runs/
```

ただし、サンプル成果物だけ残したいなら：

```gitignore
outputs/runs/*
!outputs/runs/.gitkeep
!outputs/examples/
```

### 成果物も履歴管理したい場合

コミット対象にしてよい。
ただし、案件情報や機密情報を含みやすいので注意。

私なら、初期方針はこうする。

```text
- 通常の業務成果物は git 管理しない
- サンプル成果物だけ `outputs/examples/` に置く
- 本番案件の成果物は、案件リポジトリや指定フォルダに出力する
```

---

## もう一つの選択肢：プロンプト管理repoには成果物を置かない

これはけっこう重要。

`qa-agent-workflows` が **skill群を管理するためのリポジトリ**なら、実業務のアウトプットをここに置かない運用もあり。

その場合は：

```text
qa-agent-workflows/
  skill定義だけ

target-project/
  outputs/runs/<run_id>/
```

つまり、skill はライブラリ、成果物は案件側に置く。

この場合、AGENTS.md にはこう書く。

```md
- ユーザーまたは作業対象リポジトリが出力先を指定している場合は、その出力先を優先する。
- 指定がない場合のみ、現在の workspace の `outputs/runs/<run_id>/` に出力する。
```

これが一番安全かもしれない。

---

## 私の推奨

きみの用途なら、最終的にこう定義するのがよいと思う。

```text
原則:
  成果物は `outputs/runs/<run_id>/` に置く。

ただし:
  対象プロジェクト側に指定された成果物ディレクトリがある場合はそちらを優先する。

禁止:
  `.agents/skills/`
  `shared/`
  `docs/`
  に業務成果物を置かない。

構成:
  run直下に manifest / input inventory / issue log
  skill別フォルダに中間成果物
  final/ に人間向け最終成果物
  exports/ にCSV/JSON等
```

AGENTS.md には短く書く。
詳細は `shared/output_location_policy.md` に置く。

この形なら、RooCode で作業しても出力先が安定するし、skill 本体と業務成果物が混ざらない。あとから「この成果物、手順書なのか実行結果なのか分からない」という、地味に嫌な霧も出にくくなる。
