# orchestrator.md

# リスクベースドテスト設計 Orchestrator

## 1. 目的

このファイルは、リスクベースドテスト設計プロンプト群の実行順序と進行ルールを定義する。

各ステップの詳細な作業内容は、個別の step guide に従う。  
この orchestrator.md には、ステップ進行、入力・出力、停止条件、レビュー条件のみを記載する。

---

## 2. 全体フロー

リスクベースドテスト設計は、以下の5ステップで実施する。

| Step | 名称 | 主な目的 | 主な成果物 |
|---:|---|---|---|
| Step 1 | 入力文書整理・分析スコープ確定 | 入力文書を整理し、リスク抽出の対象範囲を明確にする | `01_input_scope_summary.md` |
| Step 2 | リスク候補抽出 | 入力情報からプロダクトリスク候補を根拠付きで抽出する | `02_risk_candidate_list.md` |
| Step 3 | リスク評価・優先順位付け | リスク候補を評価し、テスト設計上の優先度を決める | `03_risk_register.md` |
| Step 4 | リスクベースドテスト方針設計 | 優先リスクに対するテスト観点・テスト深度・技法を決める | `04_risk_based_test_strategy.md` |
| Step 5 | テストケース骨子・トレーサビリティ作成 | リスクと対応するテストケース骨子を整理する | `05_testcase_outline_and_traceability.md` |

---

## 3. 基本進行ルール

### 3.1 一度に複数ステップを実行しない

1回の実行では、原則として1ステップのみ実行する。

各ステップの成果物を出力したら、そこで停止する。  
ユーザーから明示的な指示があるまで、次のステップへ進んではならない。

許可される次ステップ指示の例:

```text
次へ
次をお願いします
Step 2に進んでください
この内容で続けてください
````

---

### 3.2 現在のステップに必要なファイルだけを参照する

コンテキスト肥大化を防ぐため、各ステップで参照するファイルを限定する。

|   Step | 参照するファイル                                                                                                  |
| -----: | --------------------------------------------------------------------------------------------------------- |
| Step 1 | `rules.md`, `step1_input_scope_guide.md`, 入力文書                                                            |
| Step 2 | `rules.md`, `step2_risk_extraction_guide.md`, `references/risk_taxonomy.md`, `01_input_scope_summary.md`  |
| Step 3 | `rules.md`, `step3_risk_assessment_guide.md`, `references/scoring_model.md`, `02_risk_candidate_list.md`  |
| Step 4 | `rules.md`, `step4_test_strategy_guide.md`, `references/test_technique_mapping.md`, `03_risk_register.md` |
| Step 5 | `rules.md`, `step5_testcase_outline_guide.md`, `04_risk_based_test_strategy.md`, `03_risk_register.md`    |

必要がある場合のみ、前段階の成果物を追加で参照してよい。
ただし、参照する場合は、なぜ必要かを簡潔に明示する。

---

### 3.3 各ステップの成果物を次ステップの入力にする

各ステップは、直前までの成果物を前提として実行する。

```text
入力文書
  → Step 1: 入力整理・スコープ確定
    → Step 2: リスク候補抽出
      → Step 3: リスク評価・優先順位付け
        → Step 4: テスト方針設計
          → Step 5: テストケース骨子・トレーサビリティ作成
```

前ステップの成果物に不明点・保留事項がある場合は、それを無視せず、次ステップで以下のいずれかとして扱う。

* 確認事項
* 仮説
* 制約
* 未解決リスク
* テスト対象外候補

---

## 4. ステップ別の実行定義

## Step 1: 入力文書整理・分析スコープ確定

### 目的

入力文書を読み取り、リスク抽出に使う情報を整理する。
このステップでは、リスク候補の詳細抽出や優先度評価は行わない。

### 入力

* プロジェクト計画書
* 要件定義書
* 基本設計書
* 画面仕様
* 外部IF仕様
* バッチ仕様
* 権限仕様
* 過去障害
* ドメイン知識
* その他、ユーザーが指定した資料

### 使用ガイド

* `rules.md`
* `step1_input_scope_guide.md`

### 出力

* `01_input_scope_summary.md`

### 停止条件

`01_input_scope_summary.md` を出力したら停止する。

---

## Step 2: リスク候補抽出

### 目的

Step 1 の成果物をもとに、テスト設計で扱うべきリスク候補を抽出する。

このステップでは、リスクの優先順位付けは行わない。
リスク候補を、根拠・発生条件・影響対象とともに整理する。

### 入力

* `01_input_scope_summary.md`
* 必要に応じて、入力文書の該当箇所

### 使用ガイド

* `rules.md`
* `step2_risk_extraction_guide.md`
* `references/risk_taxonomy.md`

### 出力

* `02_risk_candidate_list.md`

### 停止条件

`02_risk_candidate_list.md` を出力したら停止する。

---

## Step 3: リスク評価・優先順位付け

### 目的

Step 2 で抽出したリスク候補を評価し、テスト設計上の優先度を決める。

評価では、影響度、発生可能性、検出困難度、根拠信頼度を扱う。

### 入力

* `02_risk_candidate_list.md`
* 必要に応じて、`01_input_scope_summary.md`

### 使用ガイド

* `rules.md`
* `step3_risk_assessment_guide.md`
* `references/scoring_model.md`

### 出力

* `03_risk_register.md`

### 停止条件

`03_risk_register.md` を出力したら停止する。

---

## Step 4: リスクベースドテスト方針設計

### 目的

Step 3 で優先順位付けしたリスクに対して、テスト方針を設計する。

リスクごとに、確認すべきテスト観点、必要なテストデータ、推奨されるテスト技法、テスト深度を整理する。

### 入力

* `03_risk_register.md`
* 必要に応じて、`02_risk_candidate_list.md`

### 使用ガイド

* `rules.md`
* `step4_test_strategy_guide.md`
* `references/test_technique_mapping.md`

### 出力

* `04_risk_based_test_strategy.md`

### 停止条件

`04_risk_based_test_strategy.md` を出力したら停止する。

---

## Step 5: テストケース骨子・トレーサビリティ作成

### 目的

Step 4 のテスト方針をもとに、テストケース骨子を作成する。
あわせて、リスク、テスト観点、テストケースの対応関係を整理する。

このステップでは、詳細な操作手順までは作成しない。
詳細手順は、必要に応じて別工程で作成する。

### 入力

* `04_risk_based_test_strategy.md`
* `03_risk_register.md`

### 使用ガイド

* `rules.md`
* `step5_testcase_outline_guide.md`

### 出力

* `05_testcase_outline_and_traceability.md`

### 停止条件

`05_testcase_outline_and_traceability.md` を出力したら停止する。

---

## 5. 成果物一覧

最終的に、以下の成果物を作成する。

```text
01_input_scope_summary.md
02_risk_candidate_list.md
03_risk_register.md
04_risk_based_test_strategy.md
05_testcase_outline_and_traceability.md
```

補助的に、以下のファイルを使用する。

```text
rules.md
orchestrator.md
step1_input_scope_guide.md
step2_risk_extraction_guide.md
step3_risk_assessment_guide.md
step4_test_strategy_guide.md
step5_testcase_outline_guide.md

templates/input_scope_summary_template.md
templates/risk_candidate_list_template.md
templates/risk_register_template.md
templates/risk_based_test_strategy_template.md
templates/testcase_traceability_template.md

references/risk_taxonomy.md
references/scoring_model.md
references/test_technique_mapping.md
references/review_checklist.md

run_step_prompt_template.md
```

---

## 6. 実行時の応答形式

各ステップを実行するときは、以下の形式で応答する。

````markdown
# Step X: <ステップ名>

## 使用した入力

- <入力ファイルまたは入力文書>
- <前ステップ成果物>

## 成果物

```markdown
<成果物本文>
````

## 確認事項

* <ユーザーに確認すべき事項>

## 次に進む前のレビュー観点

* <レビューすべき観点>

````

ただし、成果物そのものが長い場合は、成果物本文を中心に出力し、説明は最小限にする。

---

## 7. レビュー待ちルール

各ステップの完了後、必ずユーザーのレビューを待つ。

次のような状態では、次ステップへ進んではならない。

- 成果物を出力した直後
- 確認事項が残っている
- ユーザーが修正指示を出している
- ユーザーがレビュー中である
- 前ステップの内容に重大な不整合がある

次ステップへ進んでよいのは、ユーザーが明示的に続行を指示した場合のみである。

---

## 8. 不明点・不足情報の扱い

不明点があっても、作業を完全に停止する必要はない。  
ただし、不明点を勝手に補完してはならない。

以下のように扱う。

| 状態 | 扱い |
|---|---|
| 軽微な不明点 | 確認事項に記録し、仮置きで進める |
| テスト設計に影響する不明点 | 未確定事項として明示する |
| リスク評価に影響する不明点 | 根拠信頼度を下げる |
| テスト対象範囲が不明 | 対象外・保留として分離する |
| 仕様判断が必要 | ユーザー確認事項にする |

---

## 9. コンテキスト圧縮ルール

各ステップでは、次の原則に従う。

- 入力文書の全文を再掲しない
- 前ステップの成果物を必要以上に引用しない
- 表は必要な列に絞る
- 長い説明よりも、次ステップで使える構造化情報を優先する
- 判断理由は簡潔に記載する
- 同じ内容を複数箇所に重複して書かない

---

## 10. 途中修正時の扱い

ユーザーが過去ステップの成果物に修正を指示した場合は、以下のように扱う。

1. 修正対象のステップを特定する
2. 修正内容を反映する
3. 影響を受ける後続成果物を明示する
4. 必要に応じて、後続ステップを再実行する

例:

```text
Step 2 のリスク候補が追加された場合、
Step 3 のリスク評価と Step 4 以降のテスト方針に影響する可能性がある。
````

---

## 11. 完了条件

本プロンプト群の完了条件は、以下である。

* 主要なリスクが根拠付きで抽出されている
* リスクに優先度が付与されている
* 優先リスクに対するテスト方針が定義されている
* リスク、テスト観点、テストケース骨子の対応関係が追跡可能である
* 未確認事項、未カバーリスク、対象外リスクが明示されている
* 詳細テスト設計へ進める状態になっている
