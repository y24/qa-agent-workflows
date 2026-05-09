# run_step_prompt_template.md

## 1. 目的

このテンプレートは、AIエージェントに特定のステップだけを実行させるために使用する。

目的は以下である。

- 実行対象ステップを明確にする
- 使用する guide / reference / template を限定する
- 入力ファイルと出力ファイルを明示する
- 次ステップへの自動進行を防ぐ
- 推測による補完を抑制する
- ユーザーレビューを前提に、段階的に成果物を作成する

---

## 2. 使い方

以下のテンプレートをコピーし、実行対象ステップに応じて項目を埋める。

このテンプレートを使用する場合、AIエージェントは指定されたステップのみを実行する。  
指定されていないステップや、後続ステップの成果物を作成してはならない。

---

## 3. 実行用テンプレート

```markdown
# 実行対象ステップ

- Step:
- ステップ名:
- 使用する step guide:
- 実行対象範囲:
- バッチ名:
- 入力ファイル:
  - 
- 参照ファイル:
  - rules.md
  - 
- 使用テンプレート:
  - 
- 出力ファイル:
  - 

---

# 実行指示

以下のルールに従って、指定されたステップのみを実行してください。

## 基本ルール

- `rules.md` に従うこと。
- 指定された step guide に従うこと。
- 指定された入力ファイルのみを主な根拠として使用すること。
- 指定された参照ファイルは、判断基準や出力形式の補助として使用すること。
- 入力に存在しない仕様、業務ルール、設計意図を確定事項として追加しないこと。
- 推定を行う場合は、必ず推定であることを明示すること。
- 推定度を `高` / `中` / `低` で記録すること。
- 推定を根拠に、さらに別の推定を重ねないこと。
- 不明点、曖昧点、矛盾、判断保留は issue として記録すること。
- 根拠となる TC ID を必ず維持すること。

## ステップ制御

- このステップのみを実行すること。
- 次のステップには進まないこと。
- 後続ステップの成果物を作成しないこと。
- 出力後はユーザーのレビューを待つこと。
- ユーザーから明示的な指示があるまで、次ステップを実行しないこと。

## 出力ルール

- 出力ファイル単位で Markdown 形式で出力すること。
- 指定された出力ファイル以外は作成しないこと。
- 表形式が指定されている場合は、Markdown table を使用すること。
- issue がない場合も、「記録すべき issue はありません」と明記すること。
- 成果物を過度に長文化しないこと。
- 後続ステップに必要な情報を優先して残すこと。

---

# 入力情報

ここに、実行対象となる入力ファイルの内容を貼り付ける。

## 入力ファイル1

```markdown
ここに入力ファイルの内容を貼り付ける
````

## 入力ファイル2

```markdown
ここに入力ファイルの内容を貼り付ける
```

---

# 参照情報

必要に応じて、参照ファイルの内容を貼り付ける。

## rules.md

```markdown
ここに rules.md の内容を貼り付ける
```

## step guide

```markdown
ここに対象 step guide の内容を貼り付ける
```

## reference

```markdown
ここに必要な reference の内容を貼り付ける
```

## template

```markdown
ここに必要な template の内容を貼り付ける
```

---

# 出力してほしい成果物

以下の成果物を出力してください。

*

---

# 追加指示

必要に応じて、今回だけの追加指示を記載する。

例:

* 対象は `取引先マスタ` 関連のテストケースに限定する。
* 推定度が `低` のものは、本文に含めず issue のみに記録する。
* 観点候補は1テストケースあたり最大3件までにする。
* バッチ名は `batch_01_customer_master` とする。

````

---

## 4. Step 01 実行例

```markdown
# 実行対象ステップ

- Step: Step 01
- ステップ名: 入力整理・テストケース正規化
- 使用する step guide: steps/step_01_input_normalization_guide.md
- 実行対象範囲: 入力されたテストケース全体
- バッチ名: なし
- 入力ファイル:
  - 元テストケース資料
- 参照ファイル:
  - rules.md
  - steps/step_01_input_normalization_guide.md
- 使用テンプレート:
  - templates/testcase_inventory_template.md
  - templates/issue_log_template.md
- 出力ファイル:
  - 01_testcase_inventory.md
  - 01_input_issues.md

---

# 実行指示

指定された入力テストケース資料を正規化してください。

このステップでは、テスト意図や観点候補は抽出しないでください。  
入力資料の情報を標準項目に整理し、不明点や曖昧点は issue として記録してください。

次の Step 02 には進まないでください。
````

---

## 5. Step 02 実行例

```markdown
# 実行対象ステップ

- Step: Step 02
- ステップ名: 意図・観点候補の抽出
- 使用する step guide: steps/step_02_intent_and_candidate_extraction_guide.md
- 実行対象範囲: 01_testcase_inventory.md に含まれる全TC
- バッチ名: なし
- 入力ファイル:
  - 01_testcase_inventory.md
  - 01_input_issues.md
- 参照ファイル:
  - rules.md
  - steps/step_02_intent_and_candidate_extraction_guide.md
  - references/definitions.md
  - references/ambiguity_policy.md
- 使用テンプレート:
  - templates/intent_and_candidate_template.md
  - templates/issue_log_template.md
- 出力ファイル:
  - 02_intent_and_viewpoint_candidates.md
  - 02_extraction_issues.md

---

# 実行指示

`01_testcase_inventory.md` の各テストケースから、主意図、副次意図、観点候補、根拠、推定度を抽出してください。

観点候補は元テストケースに近い粒度で記録し、抽象化しすぎないでください。  
抽象観点カタログや観点IDは作成しないでください。

次の Step 03 には進まないでください。
```

---

## 6. Step 03 実行例

```markdown
# 実行対象ステップ

- Step: Step 03
- ステップ名: 抽象観点カタログ化
- 使用する step guide: steps/step_03_viewpoint_cataloging_guide.md
- 実行対象範囲: 02_intent_and_viewpoint_candidates.md に含まれる全観点候補
- バッチ名: なし
- 入力ファイル:
  - 02_intent_and_viewpoint_candidates.md
  - 02_extraction_issues.md
- 参照ファイル:
  - rules.md
  - steps/step_03_viewpoint_cataloging_guide.md
  - references/definitions.md
  - references/abstraction_policy.md
  - references/viewpoint_category_seed.md
- 使用テンプレート:
  - templates/viewpoint_catalog_template.md
  - templates/issue_log_template.md
- 出力ファイル:
  - 03_viewpoint_catalog.md
  - 03_cataloging_issues.md

---

# 実行指示

`02_intent_and_viewpoint_candidates.md` の観点候補をもとに、抽象観点カタログを作成してください。

類似する観点候補は必要に応じて統合し、再利用可能な抽象観点にしてください。  
ただし、Step 02 に存在しない観点を新規追加しないでください。  
各抽象観点には、観点ID、カテゴリ、説明、元観点候補、根拠TC、抽象化レベル、抽象化理由を記録してください。

次の Step 04 には進まないでください。
```

---

## 7. Step 04 実行例

```markdown
# 実行対象ステップ

- Step: Step 04
- ステップ名: トレーサビリティ確認・最終化
- 使用する step guide: steps/step_04_traceability_and_finalization_guide.md
- 実行対象範囲: 全成果物
- バッチ名: なし
- 入力ファイル:
  - 01_testcase_inventory.md
  - 01_input_issues.md
  - 02_intent_and_viewpoint_candidates.md
  - 02_extraction_issues.md
  - 03_viewpoint_catalog.md
  - 03_cataloging_issues.md
- 参照ファイル:
  - rules.md
  - steps/step_04_traceability_and_finalization_guide.md
  - references/definitions.md
  - references/ambiguity_policy.md
- 使用テンプレート:
  - templates/traceability_matrix_template.md
  - templates/issue_log_template.md
- 出力ファイル:
  - 04_final_traceability_matrix.md
  - 04_final_issue_log.md
  - 04_final_summary.md

---

# 実行指示

これまでの成果物をもとに、テストケース、意図、観点候補、抽象観点の対応関係を確認し、最終成果物を作成してください。

このステップでは、新しい抽象観点を追加しないでください。  
根拠TCがない観点は最終成果物から除外し、issue として記録してください。  
推定度が低い内容は確定扱いせず、レビュー対象または issue として扱ってください。
```

---

## 8. バッチ処理時の実行例

大量のテストケースを分割して処理する場合は、バッチ名を明示する。

```markdown
# 実行対象ステップ

- Step: Step 02
- ステップ名: 意図・観点候補の抽出
- 使用する step guide: steps/step_02_intent_and_candidate_extraction_guide.md
- 実行対象範囲: 取引先マスタ関連のテストケース
- バッチ名: batch_01_customer_master
- 入力ファイル:
  - 01_testcase_inventory__batch_01_customer_master.md
  - 01_input_issues__batch_01_customer_master.md
- 参照ファイル:
  - rules.md
  - steps/step_02_intent_and_candidate_extraction_guide.md
  - references/definitions.md
  - references/ambiguity_policy.md
- 使用テンプレート:
  - templates/intent_and_candidate_template.md
  - templates/issue_log_template.md
- 出力ファイル:
  - 02_intent_and_viewpoint_candidates__batch_01_customer_master.md
  - 02_extraction_issues__batch_01_customer_master.md

---

# 実行指示

`batch_01_customer_master` の範囲のみを対象として、意図・観点候補を抽出してください。

他バッチのテストケースは参照しないでください。  
バッチ横断の統合は行わないでください。
```

---

## 9. 追加指示の書き方

追加指示を書く場合は、対象ステップのルールを上書きしすぎないようにする。

### 良い追加指示

```text
推定度が低いものは、本文には含めず issue のみに記録してください。
```

```text
観点候補は、1テストケースあたり最大3件を目安にしてください。
```

```text
今回は対象機能が取引先マスタであることが分かっているため、対象機能欄には取引先マスタと記録してください。
```

### 避ける追加指示

```text
一般的に不足している観点も追加してください。
```

```text
仕様上必要そうな観点を補ってください。
```

```text
曖昧なところは適当に補完してください。
```

```text
低推定度でもそれらしく確定扱いしてください。
```

こういう指示は、成果物を見た目だけ賢そうにする。
でも、あとで根拠をたどれなくなる。静かな事故だね。

---

## 10. 実行時の確認事項

AIエージェントに依頼する前に、以下を確認する。

```markdown
| 確認項目 | 確認結果 |
|---|---|
| 実行する Step が明記されているか |  |
| 入力ファイルが明記されているか |  |
| 出力ファイルが明記されているか |  |
| 使用する step guide が明記されているか |  |
| 必要な reference のみに絞られているか |  |
| 次ステップへ進まない指示が入っているか |  |
| 推測補完を禁止する指示が入っているか |  |
| issue 記録の指示が入っているか |  |
| バッチ処理の場合、バッチ名が明記されているか |  |
```

---

## 11. 禁止事項

このテンプレートを使う場合、AIエージェントに以下を指示してはならない。

* 複数ステップをまとめて実行させる
* 後続ステップの成果物を先に作らせる
* 入力にない仕様を補完させる
* 一般的な観点を自由に追加させる
* issue を省略させる
* 推定度を省略させる
* 根拠TCを省略させる
* レビュー前に最終化させる
