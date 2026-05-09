# run_step_prompt_template.md

# Step実行プロンプトテンプレート

## 1. 目的

このテンプレートは、AIエージェントにシナリオテスト設計プロンプト群の各stepを実行させるための共通プロンプトである。

各stepを実行する際は、このテンプレートを複製し、対象step、参照ファイル、入力文書、出力先を指定して使用する。

---

## 2. 実行対象step

以下のいずれかを指定する。

```text
Step 1: 入力文書の要点抽出
Step 2: 業務フロー・利用シーン整理
Step 3: シナリオ観点の抽出
Step 4: シナリオ候補の設計
Step 5: テストケース化・優先度付け
````

今回実行するstep:

```text
Step X: 
```

---

## 3. 参照ファイル

今回のstepでは、以下のファイルを参照すること。

### 3.1 共通ルール

```text
prompts/rules.md
prompts/orchestrator.md
```

### 3.2 対象stepのガイド

```text
prompts/step_guides/stepX_xxx_guide.md
```

### 3.3 出力テンプレート

```text
prompts/output_templates/XX_xxx_template.md
```

### 3.4 前stepまでの成果物

必要なもののみ指定する。

```text
outputs/01_input_summary.md
outputs/02_business_flows.md
outputs/03_scenario_viewpoints.md
outputs/04_scenario_candidates.md
```

### 3.5 入力文書

必要なもののみ指定する。

```text
input_docs/
  project_plan.md
  requirements.md
  screen_specs.md
  domain_knowledge.md
  past_defects.md
```

### 3.6 レビュー・確認事項

必要に応じて指定する。

```text
logs/review_comments.md
logs/issue_log.md
```

---

## 4. 出力先

今回のstepの成果物は、以下に出力すること。

```text
outputs/XX_xxx.md
```

---

## 5. 実行指示

上記の参照ファイルを読み、対象stepの成果物を作成すること。

作業時は、必ず以下を守る。

* `rules.md` を最上位ルールとして扱う
* `orchestrator.md` のstep進行ルールに従う
* 対象stepの `step*_guide.md` に従う
* 指定された `output_templates` の構成を優先する
* 原文にない情報を断定しない
* 推測が必要な場合は `推測` と明記する
* 不明点、矛盾、仕様不足は `確認事項` に分離する
* 重要な判断には根拠を付与する
* 各項目には、後続stepで参照しやすいIDを付与する
* 出力はMarkdown形式とする
* step完了後、次stepへ進まずレビュー待ちにする

---

## 6. 今回の追加指示

案件固有の追加指示がある場合は、ここに記載する。

```md
- 
- 
- 
```

---

## 7. 対象範囲

今回扱う対象範囲を記載する。

```md
- 対象システム:
- 対象機能:
- 対象業務:
- 対象リリース:
- 対象外:
```

対象範囲が入力文書から判断できない場合は、推測で補完せず確認事項にすること。

---

## 8. 重点観点

今回、特に重視する観点があれば記載する。

```md
- 業務影響が大きい領域:
- 仕様変更が大きい領域:
- 過去不具合が多い領域:
- 帳票・出力確認:
- 外部連携確認:
- 権限・ロール確認:
- 締め・取消・再実行:
```

未指定の場合は、入力文書と前step成果物に基づいて判断すること。
ただし、根拠のない重点化は行わないこと。

---

## 9. 出力時の注意

成果物の最後に、必ず以下を含めること。

```md
## 確認事項

| ID | 種別 | 内容 | 影響 | 関連箇所 | 状態 |
|---|---|---|---|---|---|
| Q-001 | 不明 / 矛盾 / 仕様不足 / 判断待ち / 対象外候補 |  |  |  | 未確認 |
```

```md
## 次stepへの引き継ぎ

- 
- 
- 
```

```md
## レビュー依頼

Step X の成果物を作成しました。

主な確認ポイント:
- 
- 
- 

確認事項:
- 
- 

次に進む場合は「Step X+1へ進んでください」と指示してください。
修正が必要な場合は、修正内容を指示してください。
```

Step 5の場合は、次stepへの進行指示ではなく、最終レビュー依頼とする。

---

## 10. 禁止事項

以下を禁止する。

* ユーザーの明示指示なしに次stepへ進むこと
* 対象stepの責務を超えた成果物を作成すること
* Step 1でテスト観点やテストケースを作ること
* Step 2で詳細なテスト手順や期待結果を作ること
* Step 3でシナリオ候補やテストケースを作ること
* Step 4で詳細なテストケースを作ること
* Step 5で仕様にない期待結果を断定すること
* 入力文書にない画面名、項目名、ステータス名、業務ルールを創作すること
* 一般論だけで観点やシナリオを大量生成すること
* 確認事項を本文に紛れ込ませること
* 巨大なJSONやYAMLで出力すること

---

## 11. 実行プロンプト例

### 11.1 Step 1実行例

```md
# 実行対象step

Step 1: 入力文書の要点抽出

# 参照ファイル

- prompts/rules.md
- prompts/orchestrator.md
- prompts/step_guides/step1_input_summary_guide.md
- prompts/output_templates/01_input_summary_template.md
- input_docs/project_plan.md
- input_docs/requirements.md
- input_docs/screen_specs.md
- input_docs/domain_knowledge.md
- input_docs/past_defects.md

# 出力先

- outputs/01_input_summary.md

# 指示

上記を参照し、Step 1の成果物を作成してください。

以下を守ってください。

- シナリオテスト設計に必要な情報だけを抽出してください
- テスト観点、シナリオ候補、テストケースは作成しないでください
- 原文にない情報を断定しないでください
- 不明点は確認事項に分離してください
- 完了後、次stepへ進まずレビュー待ちにしてください
```

---

### 11.2 Step 2実行例

```md
# 実行対象step

Step 2: 業務フロー・利用シーン整理

# 参照ファイル

- prompts/rules.md
- prompts/orchestrator.md
- prompts/step_guides/step2_business_flow_guide.md
- prompts/output_templates/02_business_flows_template.md
- outputs/01_input_summary.md
- logs/review_comments.md

# 出力先

- outputs/02_business_flows.md

# 指示

上記を参照し、Step 2の成果物を作成してください。

以下を守ってください。

- 業務目的単位でフローを整理してください
- 単機能確認一覧にしないでください
- 詳細なテスト手順や期待結果は作成しないでください
- 不明点は確認事項に分離してください
- 完了後、次stepへ進まずレビュー待ちにしてください
```

---

### 11.3 Step 3実行例

```md
# 実行対象step

Step 3: シナリオ観点の抽出

# 参照ファイル

- prompts/rules.md
- prompts/orchestrator.md
- prompts/step_guides/step3_scenario_viewpoint_guide.md
- prompts/output_templates/03_scenario_viewpoints_template.md
- outputs/01_input_summary.md
- outputs/02_business_flows.md
- logs/review_comments.md

# 出力先

- outputs/03_scenario_viewpoints.md

# 指示

上記を参照し、Step 3の成果物を作成してください。

以下を守ってください。

- 業務フローに紐づくシナリオ観点を抽出してください
- 一般論だけの観点を大量生成しないでください
- シナリオ候補やテストケースは作成しないでください
- 観点ごとに確認したいこと、重要な理由、根拠を記載してください
- 完了後、次stepへ進まずレビュー待ちにしてください
```

---

### 11.4 Step 4実行例

```md
# 実行対象step

Step 4: シナリオ候補の設計

# 参照ファイル

- prompts/rules.md
- prompts/orchestrator.md
- prompts/step_guides/step4_scenario_candidate_guide.md
- prompts/output_templates/04_scenario_candidates_template.md
- outputs/01_input_summary.md
- outputs/02_business_flows.md
- outputs/03_scenario_viewpoints.md
- logs/review_comments.md

# 出力先

- outputs/04_scenario_candidates.md

# 指示

上記を参照し、Step 4の成果物を作成してください。

以下を守ってください。

- シナリオ観点を業務上意味のあるシナリオ候補にまとめてください
- 詳細な操作手順や期待結果は作成しないでください
- 各シナリオに関連フロー、関連観点、優先度、採用判断を記載してください
- 対象外候補や保留は勝手に除外確定せず、レビュー対象にしてください
- 完了後、次stepへ進まずレビュー待ちにしてください
```

---

### 11.5 Step 5実行例

```md
# 実行対象step

Step 5: テストケース化・優先度付け

# 参照ファイル

- prompts/rules.md
- prompts/orchestrator.md
- prompts/step_guides/step5_testcase_detail_guide.md
- prompts/output_templates/05_test_cases_template.md
- outputs/01_input_summary.md
- outputs/02_business_flows.md
- outputs/03_scenario_viewpoints.md
- outputs/04_scenario_candidates.md
- logs/review_comments.md

# 出力先

- outputs/05_test_cases.md

# 指示

上記を参照し、Step 5の成果物を作成してください。

以下を守ってください。

- 採用対象のシナリオ候補を実行可能なテストケースにしてください
- 操作手順と期待結果を対応させて記載してください
- 期待結果は合否判定可能な表現にしてください
- 仕様にない画面項目、ボタン名、ステータス名、メッセージ文言を断定しないでください
- 不明点は確認事項に分離してください
- 最終レビュー観点を記載してください
```

---

## 12. 実行後の確認

AIエージェントは、成果物作成後に以下を自己確認すること。

| 確認項目                | 結果      |
| ------------------- | ------- |
| 対象stepの責務を超えていないか   | OK / NG |
| 原文にない情報を断定していないか    | OK / NG |
| 推測を推測として明記しているか     | OK / NG |
| 確認事項を分離しているか        | OK / NG |
| 根拠を記載しているか          | OK / NG |
| 次stepへの引き継ぎを記載しているか | OK / NG |
| レビュー待ちで停止しているか      | OK / NG |

NGがある場合は、成果物を修正してから提出すること。
