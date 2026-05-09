# orchestrator.md

## 1. 目的

このファイルは、既存テストケースから以下を段階的に抽出する作業全体を制御する。

- テストケースの正規化
- 各テストケースのテスト意図の抽出
- テスト観点候補の抽出
- 抽象化されたテスト観点カタログの作成
- テストケース、意図、観点のトレーサビリティ確認
- 最終成果物の作成

このファイルでは、作業順序、入力・出力、レビューゲート、再実行方針を定義する。  
個別ステップの詳細な作業手順は `steps/` 配下の各 guide に従う。

---

## 2. 全体ステップ

本プロンプト群では、以下の4ステップで作業を進める。

```text
Step 01: 入力整理・テストケース正規化
Step 02: 意図・観点候補の抽出
Step 03: 抽象観点カタログ化
Step 04: トレーサビリティ確認・最終化
````

各ステップは、ユーザーから明示的に指示された場合のみ実行する。
1回の実行では、原則として1ステップのみ実行する。

---

## 3. ステップ概要

### Step 01: 入力整理・テストケース正規化

#### 目的

入力されたテストケース資料を、後続ステップで扱いやすい標準形式へ整える。

#### 主な作業

* 入力資料の構造確認
* 対象範囲の確認
* テストケースIDの確認または仮ID付与
* テストケース情報の正規化
* 欠落・曖昧・矛盾の記録

#### 主な入力

* 元テストケース資料
* 画面仕様、機能仕様、補足資料がある場合はその範囲
* ユーザーからの対象範囲指定

#### 参照ファイル

```text
rules.md
steps/step_01_input_normalization_guide.md
templates/testcase_inventory_template.md
templates/issue_log_template.md
```

#### 出力

```text
01_testcase_inventory.md
01_input_issues.md
```

#### 完了条件

* 解析対象のテストケースが一覧化されている
* 各テストケースにIDがある
* 前提条件、操作/入力、期待結果が可能な範囲で整理されている
* 欠落や曖昧さが issue として記録されている

---

### Step 02: 意図・観点候補の抽出

#### 目的

正規化されたテストケースから、各テストケースの意図とテスト観点候補を抽出する。

#### 主な作業

* 各テストケースの主意図を抽出する
* 必要に応じて副次意図を抽出する
* テスト観点候補を抽出する
* 根拠となるテストケース記述を明示する
* 推定度を付与する
* 推定が弱いもの、不明点を issue として記録する

#### 主な入力

```text
01_testcase_inventory.md
01_input_issues.md
```

#### 参照ファイル

```text
rules.md
steps/step_02_intent_and_candidate_extraction_guide.md
references/definitions.md
references/ambiguity_policy.md
templates/intent_and_candidate_template.md
templates/issue_log_template.md
```

#### 出力

```text
02_intent_and_viewpoint_candidates.md
02_extraction_issues.md
```

#### 完了条件

* 各テストケースに主意図が付与されている
* 必要に応じて副次意図が記録されている
* 各テストケースに観点候補が紐づいている
* 意図・観点候補の根拠が記録されている
* 推定度が付与されている
* 根拠が弱い内容が issue として記録されている

---

### Step 03: 抽象観点カタログ化

#### 目的

Step 02 で抽出した観点候補を統合・抽象化し、再利用可能なテスト観点カタログを作成する。

#### 主な作業

* 類似する観点候補を統合する
* 個別機能に依存しすぎた表現を一般化する
* 抽象化しすぎた観点名を避ける
* 観点IDを付与する
* カテゴリを付与する
* 根拠テストケースを紐づける
* 抽象化理由を記録する

#### 主な入力

```text
02_intent_and_viewpoint_candidates.md
02_extraction_issues.md
```

#### 参照ファイル

```text
rules.md
steps/step_03_viewpoint_cataloging_guide.md
references/definitions.md
references/abstraction_policy.md
references/viewpoint_category_seed.md
templates/viewpoint_catalog_template.md
templates/issue_log_template.md
```

#### 出力

```text
03_viewpoint_catalog.md
03_cataloging_issues.md
```

#### 完了条件

* 各抽象観点に観点IDが付与されている
* 各抽象観点にカテゴリが付与されている
* 各抽象観点に1件以上の根拠テストケースがある
* 抽象化理由が説明されている
* 根拠の弱い観点や分類困難な観点が issue として記録されている

---

### Step 04: トレーサビリティ確認・最終化

#### 目的

テストケース、テスト意図、観点候補、抽象観点の対応関係を確認し、最終成果物として整理する。

#### 主な作業

* 各テストケースに意図があるか確認する
* 各テストケースに観点が紐づいているか確認する
* 各抽象観点に根拠テストケースがあるか確認する
* 根拠のない観点を最終成果物から除外する
* 推定度が低い内容をレビュー対象にする
* issue を統合・整理する
* 最終成果物を作成する

#### 主な入力

```text
01_testcase_inventory.md
01_input_issues.md
02_intent_and_viewpoint_candidates.md
02_extraction_issues.md
03_viewpoint_catalog.md
03_cataloging_issues.md
```

#### 参照ファイル

```text
rules.md
steps/step_04_traceability_and_finalization_guide.md
references/definitions.md
references/ambiguity_policy.md
templates/traceability_matrix_template.md
templates/issue_log_template.md
```

#### 出力

```text
04_final_traceability_matrix.md
04_final_issue_log.md
04_final_summary.md
```

#### 完了条件

* テストケース、意図、観点の対応関係が追跡できる
* 根拠のない抽象観点が最終成果物に含まれていない
* issue が重複整理されている
* 最終的な注意点、制約、レビュー推奨箇所が明示されている

---

## 4. 実行順序

原則として、以下の順序で実行する。

```text
Step 01
  ↓
Step 02
  ↓
Step 03
  ↓
Step 04
```

後続ステップは、前ステップの成果物を入力として使用する。

ただし、ユーザーが明示的に指示した場合は、特定ステップのみ再実行してよい。

---

## 5. レビューゲート

レビューゲートは、原則として2箇所に置く。

```text
Gate 1: Step 01 完了後
Gate 2: Step 03 完了後
```

### Gate 1: 入力整理レビュー

#### 対象成果物

```text
01_testcase_inventory.md
01_input_issues.md
```

#### 確認観点

* 解析対象のテストケースが正しいか
* 除外すべき行や資料が混ざっていないか
* テストケースIDの扱いが妥当か
* 操作/入力、期待結果、前提条件の列解釈が妥当か
* 仮IDを付与したケースが妥当か
* 欠落・曖昧さの記録が妥当か

#### レビュー後の分岐

* 問題なし: Step 02 へ進む
* 修正あり: Step 01 を修正してから Step 02 へ進む
* 対象範囲変更: Step 01 を再実行する

---

### Gate 2: 観点カタログレビュー

#### 対象成果物

```text
02_intent_and_viewpoint_candidates.md
02_extraction_issues.md
03_viewpoint_catalog.md
03_cataloging_issues.md
```

#### 確認観点

* テスト意図が元テストケースから読み取れるか
* 推定が過剰ではないか
* 観点候補の粒度が細かすぎないか
* 抽象観点が抽象化されすぎていないか
* 抽象観点が個別機能に依存しすぎていないか
* 観点カテゴリが妥当か
* 根拠TCの紐づけが妥当か
* レビューが必要な issue が明確か

#### レビュー後の分岐

* 問題なし: Step 04 へ進む
* 意図抽出に問題あり: Step 02 を修正または再実行する
* 観点抽象化に問題あり: Step 03 を修正または再実行する
* 入力解釈に問題あり: Step 01 へ戻る

---

## 6. 再実行ルール

### 6.1 Step 01 を再実行した場合

Step 01 の出力が変わった場合、原則として Step 02 以降も再実行する。

理由:

* テストケースID
* 対象範囲
* 操作/入力
* 期待結果
* 前提条件

これらが変わると、意図や観点の根拠が変わるため。

---

### 6.2 Step 02 を再実行した場合

Step 02 の出力が変わった場合、原則として Step 03 以降も再実行する。

理由:

* 観点候補が変わる
* 推定度が変わる
* 抽象観点の根拠が変わる

---

### 6.3 Step 03 を再実行した場合

Step 03 の出力が変わった場合、Step 04 は再実行する。

理由:

* 観点ID
* 観点名
* カテゴリ
* 根拠TC

これらが変わると、トレーサビリティ表が変わるため。

---

### 6.4 部分修正の場合

ユーザーが特定テストケース、特定観点、特定カテゴリのみの修正を指示した場合は、対象範囲を限定して修正してよい。

ただし、影響範囲を必ず記録する。

記録例:

```markdown
## 修正影響

- 修正対象: TC-014
- 影響する成果物:
  - 02_intent_and_viewpoint_candidates.md
  - 03_viewpoint_catalog.md
  - 04_final_traceability_matrix.md
- 備考:
  - VP-INPUT-002 の根拠TCが変更される可能性あり
```

---

## 7. 大量テストケースの処理方針

### 7.1 分割基準

テストケース数が多い場合、以下の優先順位でバッチ分割する。

1. 機能単位
2. 画面単位
3. 業務フロー単位
4. テスト種別単位
5. テストケースID範囲

### 7.2 バッチ名

バッチ名は以下の形式にする。

```text
batch_{連番}_{対象}
```

例:

```text
batch_01_customer_master
batch_02_journal_entry
batch_03_report_output
```

### 7.3 バッチ別成果物

バッチ分割した場合、成果物名にバッチ名を付ける。

例:

```text
01_testcase_inventory__batch_01_customer_master.md
02_intent_and_viewpoint_candidates__batch_01_customer_master.md
03_viewpoint_catalog__batch_01_customer_master.md
```

### 7.4 統合作業

複数バッチを処理した場合、Step 03 または Step 04 で統合作業を行う。

統合作業では以下を確認する。

* 類似観点の重複
* 観点IDの重複
* カテゴリ名の揺れ
* 抽象化レベルのばらつき
* 同一観点に対する表現差
* 根拠TCの統合漏れ

必要に応じて、統合版成果物を作成する。

```text
03_viewpoint_catalog__merged.md
04_final_traceability_matrix__merged.md
04_final_issue_log__merged.md
```

---

## 8. 成果物一覧

### 8.1 中間成果物

```text
01_testcase_inventory.md
01_input_issues.md
02_intent_and_viewpoint_candidates.md
02_extraction_issues.md
03_viewpoint_catalog.md
03_cataloging_issues.md
```

### 8.2 最終成果物

```text
04_final_traceability_matrix.md
04_final_issue_log.md
04_final_summary.md
```

### 8.3 任意成果物

必要に応じて、以下を作成してよい。

```text
03_viewpoint_catalog__merged.md
04_final_traceability_matrix__merged.md
04_final_issue_log__merged.md
```

---

## 9. 各成果物の位置づけ

### 01_testcase_inventory.md

元テストケースを正規化した一覧。
後続ステップの基礎資料として使用する。

### 01_input_issues.md

入力資料の曖昧さ、不足、ID欠落、対象範囲上の問題を記録する。

### 02_intent_and_viewpoint_candidates.md

各テストケースの意図と観点候補を記録する。
抽象化前の主要成果物。

### 02_extraction_issues.md

意図抽出や観点候補抽出時に発見した問題を記録する。

### 03_viewpoint_catalog.md

観点候補を抽象化・統合したテスト観点カタログ。
再利用可能な観点一覧として扱う。

### 03_cataloging_issues.md

観点統合、抽象化、カテゴリ分類時に発見した問題を記録する。

### 04_final_traceability_matrix.md

テストケース、意図、抽象観点の対応関係を示す最終トレーサビリティ表。

### 04_final_issue_log.md

全ステップの issue を統合・整理した最終 issue 一覧。

### 04_final_summary.md

抽出結果全体の要約、主要観点、注意点、レビュー推奨事項をまとめる。

---

## 10. 実行時の基本プロンプト構造

各ステップを実行するときは、原則として `templates/run_step_prompt_template.md` を使用する。

実行時には以下を明示する。

```text
- 実行するステップ
- 使用する step guide
- 入力ファイル
- 参照ファイル
- 出力ファイル
- 対象範囲
- 特記事項
```

例:

```markdown
# 実行対象ステップ

- Step: Step 02 意図・観点候補の抽出
- 使用するガイド: steps/step_02_intent_and_candidate_extraction_guide.md
- 入力ファイル:
  - 01_testcase_inventory.md
  - 01_input_issues.md
- 参照ファイル:
  - rules.md
  - references/definitions.md
  - references/ambiguity_policy.md
  - templates/intent_and_candidate_template.md
  - templates/issue_log_template.md
- 出力ファイル:
  - 02_intent_and_viewpoint_candidates.md
  - 02_extraction_issues.md

# 実行指示

指定されたステップのみを実行する。
次ステップには進まない。
```

---

## 11. 判断に迷った場合の扱い

AIエージェントが判断に迷った場合は、以下の優先順位に従う。

1. `rules.md` の禁止事項を優先する
2. 元テストケースの記述を優先する
3. step guide の具体的な手順に従う
4. reference の基準に従う
5. それでも判断できない場合は issue として記録する

判断に迷った内容を、推測で補完して成果物に混ぜてはならない。

---

## 12. ユーザー確認が必要なケース

以下の場合は、成果物内にレビュー要否を明示する。

* 推定度が低い意図を抽出した
* 観点候補の根拠が弱い
* 抽象観点のカテゴリ分類が難しい
* 同じテストケースから複数の主意図が読み取れる
* 期待結果が曖昧で、意図が確定できない
* 元テストケースの記述に矛盾がある
* 観点の抽象化レベルに迷いがある
* 根拠TCが少なく、観点として独立させるべきか判断が難しい

レビュー要否は、可能であれば表の列として明示する。

例:

```markdown
| TC ID | 主意図 | 観点候補 | 推定度 | レビュー要否 | 理由 |
|---|---|---|---|---|---|
| TC-008 | 登録内容が正しく表示されることを確認する | 登録後反映 | 中 | 要 | 期待結果の「正しく」が具体化されていない |
```

---

## 13. 最終化時の除外基準

Step 04 では、以下に該当する内容を最終成果物から除外するか、issue として扱う。

* 根拠TCが存在しない抽象観点
* 推定度が低く、根拠が弱い意図
* 入力テストケースと対応しない一般論の観点
* カテゴリ名だけで具体性のない観点
* 抽象化しすぎて確認条件や期待動作が失われた観点
* 重複しており、他観点に統合可能な観点

除外した場合は、理由を `04_final_issue_log.md` に記録する。

---

## 14. 最終成果物の品質確認

Step 04 の完了前に、以下を確認する。

```markdown
| 確認項目 | 判定 |
|---|---|
| すべての対象テストケースに意図が付与されているか |  |
| 各意図に根拠TCがあるか |  |
| 各抽象観点に根拠TCがあるか |  |
| 根拠のない観点が混入していないか |  |
| 推定度が低い内容が確定扱いされていないか |  |
| issue が統合されているか |  |
| 観点名が抽象的すぎないか |  |
| 観点名が個別機能に依存しすぎていないか |  |
| テストケース、意図、観点の対応関係が追跡できるか |  |
```

---

## 15. 完了条件

全体作業は、以下を満たしたとき完了とする。

* `04_final_traceability_matrix.md` が作成されている
* `04_final_issue_log.md` が作成されている
* `04_final_summary.md` が作成されている
* 各抽象観点に根拠TCがある
* 推定度が低い内容がレビュー対象として分離されている
* 入力テストケースと抽出結果の対応が追跡できる
* ユーザーが最終成果物として利用可能な状態になっている

---

## 16. 重要な制約

このプロンプト群は、既存テストケースをもとに意図と観点を抽出するためのものである。

したがって、以下は主目的ではない。

* 新規テストケースの大量生成
* 仕様書に基づく網羅的なテスト設計
* 不足観点の自由な洗い出し
* 一般的なテスト観点一覧の作成
* テストケースの自動修正

不足観点や改善提案を出す場合も、元テストケースから読み取れる範囲に限定する。
