# orchestrator.md

# シナリオテスト設計プロンプト群 オーケストレーター

## 1. 目的

このファイルは、AIエージェントがシナリオテスト設計を段階的に進めるための進行管理ルールを定義する。

AIエージェントは、本ファイルと `rules.md`、各step guideを参照し、以下の5stepで成果物を作成する。

1. Step 1: 入力文書の要点抽出
2. Step 2: 業務フロー・利用シーン整理
3. Step 3: シナリオ観点の抽出
4. Step 4: シナリオ候補の設計
5. Step 5: テストケース化・優先度付け

各stepの完了後は、必ずユーザーレビュー待ちとする。  
ユーザーから明示的に次stepへ進む指示があるまで、次のstepに進んではならない。

---

## 2. 参照ファイル

AIエージェントは、作業時に以下のファイルを参照する。

```text
prompts/
  rules.md
  orchestrator.md
  step_guides/
    step1_input_summary_guide.md
    step2_business_flow_guide.md
    step3_scenario_viewpoint_guide.md
    step4_scenario_candidate_guide.md
    step5_testcase_detail_guide.md
  templates/
    run_step_prompt_template.md
    review_comment_template.md
    issue_log_template.md
  output_templates/
    01_input_summary_template.md
    02_business_flows_template.md
    03_scenario_viewpoints_template.md
    04_scenario_candidates_template.md
    05_test_cases_template.md
````

案件ごとの入力・出力は、原則として以下のように配置する。

```text
input_docs/
  project_plan.md
  requirements.md
  screen_specs.md
  domain_knowledge.md
  past_defects.md

outputs/
  01_input_summary.md
  02_business_flows.md
  03_scenario_viewpoints.md
  04_scenario_candidates.md
  05_test_cases.md

logs/
  issue_log.md
  review_comments.md
```

---

## 3. 共通実行ルール

すべてのstepで、以下を守る。

1. `rules.md` を最上位ルールとして扱う
2. 対象stepの `step*_guide.md` を参照する
3. 指定された入力ファイルのみを優先的に読む
4. 原文にない情報を断定しない
5. 推測は `推測` と明記する
6. 不明点は `確認事項` に分離する
7. 各stepの成果物に、次stepへの引き継ぎを記載する
8. step完了後、勝手に次stepへ進まない

---

## 4. Step全体フロー

```text
input_docs/
  ↓
Step 1: 入力文書の要点抽出
  ↓ outputs/01_input_summary.md
Step 2: 業務フロー・利用シーン整理
  ↓ outputs/02_business_flows.md
Step 3: シナリオ観点の抽出
  ↓ outputs/03_scenario_viewpoints.md
Step 4: シナリオ候補の設計
  ↓ outputs/04_scenario_candidates.md
Step 5: テストケース化・優先度付け
  ↓ outputs/05_test_cases.md
```

---

# 5. 各stepの定義

## 5.1 Step 1: 入力文書の要点抽出

### 目的

シナリオテスト設計に必要な情報を、入力文書から抽出・整理する。

### 主な入力

```text
input_docs/
  project_plan.md
  requirements.md
  screen_specs.md
  domain_knowledge.md
  past_defects.md
```

実際のファイル名は案件により異なってよい。
ただし、AIエージェントは参照した文書名を成果物に記録する。

### 参照するプロンプト

```text
rules.md
orchestrator.md
step_guides/step1_input_summary_guide.md
output_templates/01_input_summary_template.md
```

### 出力

```text
outputs/01_input_summary.md
```

### 主な出力内容

* システム概要
* 業務目的
* 対象ユーザー・ロール
* 主要機能
* 入力・出力
* 画面・帳票・外部連携
* 業務ルール
* 制約・前提
* 例外・エラー条件
* 未確定事項・確認事項

### 禁止事項

* テスト観点を作成しない
* シナリオ候補を作成しない
* テストケースを作成しない
* 文書にない業務ルールを補完しない

### 完了条件

* シナリオ設計に必要な要点が整理されている
* 不明点が確認事項として分離されている
* 参照元文書が記録されている
* 次stepへの引き継ぎが記載されている
* ユーザーレビュー待ちになっている

---

## 5.2 Step 2: 業務フロー・利用シーン整理

### 目的

Step 1の要点抽出結果をもとに、ユーザーが業務上どのような流れでシステムを利用するかを整理する。

### 主な入力

```text
outputs/01_input_summary.md
input_docs/ のうち必要な範囲
```

### 参照するプロンプト

```text
rules.md
orchestrator.md
step_guides/step2_business_flow_guide.md
output_templates/02_business_flows_template.md
```

### 出力

```text
outputs/02_business_flows.md
```

### 主な出力内容

* 業務フロー一覧
* 利用シーン一覧
* フロー詳細
* 主要な分岐
* 前提条件
* 関連機能・関連画面
* 関連データ
* 後続業務・出力
* 確認事項

### 禁止事項

* 詳細なテスト手順を作成しない
* 期待結果を詳細化しすぎない
* 単機能の確認項目一覧にしない
* 根拠のない業務フローを創作しない

### 完了条件

* 主要な業務フローがID付きで整理されている
* 各フローの目的、利用者、前提、流れが分かる
* 分岐や例外が分かる範囲で整理されている
* 不明点が確認事項として分離されている
* 次stepへの引き継ぎが記載されている
* ユーザーレビュー待ちになっている

---

## 5.3 Step 3: シナリオ観点の抽出

### 目的

Step 2で整理した業務フロー・利用シーンをもとに、シナリオテストで確認すべき観点を抽出する。

### 主な入力

```text
outputs/01_input_summary.md
outputs/02_business_flows.md
input_docs/ のうち必要な範囲
```

### 参照するプロンプト

```text
rules.md
orchestrator.md
step_guides/step3_scenario_viewpoint_guide.md
output_templates/03_scenario_viewpoints_template.md
```

### 出力

```text
outputs/03_scenario_viewpoints.md
```

### 主な出力内容

* シナリオ観点一覧
* 観点の目的
* 関連する業務フロー
* 関連するリスク
* 確認したいこと
* 優先度の仮判断
* 根拠
* 確認事項

### 禁止事項

* テストケースを作成しない
* 詳細な操作手順を作成しない
* 観点を一般論だけで大量列挙しない
* 業務フローと無関係な観点を作らない

### 完了条件

* 業務フローに紐づいた観点が整理されている
* 観点ごとに確認目的とリスクが分かる
* 根拠または関連フローが明記されている
* 不明点が確認事項として分離されている
* 次stepへの引き継ぎが記載されている
* ユーザーレビュー待ちになっている

---

## 5.4 Step 4: シナリオ候補の設計

### 目的

Step 3で抽出したシナリオ観点をもとに、実施候補となるシナリオテストを設計する。

### 主な入力

```text
outputs/01_input_summary.md
outputs/02_business_flows.md
outputs/03_scenario_viewpoints.md
input_docs/ のうち必要な範囲
```

### 参照するプロンプト

```text
rules.md
orchestrator.md
step_guides/step4_scenario_candidate_guide.md
output_templates/04_scenario_candidates_template.md
```

### 出力

```text
outputs/04_scenario_candidates.md
```

### 主な出力内容

* シナリオ候補一覧
* シナリオ目的
* 対象ユーザー・ロール
* 前提条件
* 利用データ概要
* 操作の大まかな流れ
* 確認ポイント
* 関連フロー
* 関連観点
* 優先度
* 採用・保留・対象外の判断材料
* 確認事項

### 禁止事項

* 詳細なテストケースにしない
* 画面操作を細かく補完しすぎない
* 未レビューの観点を確定扱いしない
* 類似シナリオを大量に重複作成しない

### 完了条件

* シナリオ候補がID付きで整理されている
* 各シナリオの目的と確認ポイントが分かる
* 関連する観点・業務フローが追跡できる
* 優先度とその理由が記載されている
* 不明点が確認事項として分離されている
* 次stepへの引き継ぎが記載されている
* ユーザーレビュー待ちになっている

---

## 5.5 Step 5: テストケース化・優先度付け

### 目的

レビュー済みのシナリオ候補を、実行可能なテストケースに落とし込む。

### 主な入力

```text
outputs/01_input_summary.md
outputs/02_business_flows.md
outputs/03_scenario_viewpoints.md
outputs/04_scenario_candidates.md
input_docs/ のうち必要な範囲
logs/review_comments.md
```

### 参照するプロンプト

```text
rules.md
orchestrator.md
step_guides/step5_testcase_detail_guide.md
output_templates/05_test_cases_template.md
```

### 出力

```text
outputs/05_test_cases.md
```

### 主な出力内容

* テストケース一覧
* テスト目的
* 対応シナリオ
* 前提条件
* テストデータ
* 操作手順
* 期待結果
* 確認ポイント
* 優先度
* 実行区分
* 関連要件・関連観点
* 確認事項

### 禁止事項

* 仕様にない詳細操作を断定しない
* 期待結果を曖昧にしない
* 1ケースに複数の目的を詰め込みすぎない
* レビュー前のシナリオ候補を無条件に採用しない
* 根拠のないテストデータを作り込まない

### 完了条件

* 実行可能なテストケースになっている
* 合否判定可能な期待結果がある
* シナリオ、観点、業務フローとの対応が追跡できる
* 優先度と理由が整理されている
* 不明点が確認事項として分離されている
* 最終成果物としてレビュー可能な状態になっている

---

# 6. レビュー待ち制御

各stepの最後には、以下の形式でレビュー待ち状態を明示する。

```md
## レビュー依頼

Step X の成果物を作成しました。

主な確認ポイント:
- ...
- ...
- ...

確認事項:
- ...
- ...

次に進む場合は「Step X+1へ進んでください」と指示してください。
修正が必要な場合は、修正内容を指示してください。
```

AIエージェントは、このレビュー依頼を出した後、次stepの成果物を作成してはならない。

---

# 7. 手戻り時の制御

ユーザーから修正指示があった場合、AIエージェントは以下の順で対応する。

1. 修正対象のstepを特定する
2. 修正対象の成果物を更新する
3. 影響範囲を確認する
4. 後続stepに影響がある場合は明記する
5. 必要に応じて確認事項を更新する
6. 再度レビュー待ちにする

## 7.1 後続成果物がまだ存在しない場合

対象stepの成果物のみを更新する。

## 7.2 後続成果物が存在する場合

以下をユーザーに提示する。

```md
## 影響範囲

今回の修正により、以下の後続成果物に影響する可能性があります。

- outputs/03_scenario_viewpoints.md
- outputs/04_scenario_candidates.md
- outputs/05_test_cases.md

必要に応じて、該当stepから再実行してください。
```

AIエージェントは、ユーザーの明示指示なしに後続成果物を勝手に再生成してはならない。

---

# 8. 差分更新ルール

既存成果物を更新する場合、可能な限り既存IDを維持する。

## 8.1 IDを維持するケース

* 説明文の修正
* 根拠の追記
* 優先度の変更
* 確認事項の追記
* 表現の整理

## 8.2 IDを変更または追加するケース

* 項目を分割する
* 新しい業務フローを追加する
* 新しい観点を追加する
* 新しいシナリオ候補を追加する
* 新しいテストケースを追加する

## 8.3 IDを削除するケース

削除する場合は、可能であれば削除理由を記録する。

```md
## 削除・統合履歴

| 旧ID | 処理 | 理由 | 統合先 |
|---|---|---|---|
| SV-003 | 統合 | SV-001と内容が重複 | SV-001 |
```

---

# 9. 確認事項ログの扱い

各stepで発生した確認事項は、成果物内に記載する。
必要に応じて `logs/issue_log.md` に集約する。

確認事項の推奨形式:

```md
| ID | 種別 | 内容 | 影響 | 関連箇所 | 状態 |
|---|---|---|---|---|---|
| Q-001 | 不明 | 承認後のデータ反映タイミングが不明 | シナリオ設計・期待結果に影響 | requirements.md > 承認機能 | 未確認 |
```

状態は以下を使う。

| 状態  | 意味             |
| --- | -------------- |
| 未確認 | まだ回答がない        |
| 確認中 | ユーザーまたは関係者に確認中 |
| 解決  | 確認済み           |
| 保留  | 今回は判断しない       |
| 対象外 | 今回のテスト設計対象外    |

---

# 10. 入力文書の扱い

## 10.1 入力文書をすべて信用しすぎない

入力文書間に矛盾がある場合は、勝手に解釈して統合しない。
矛盾として記録する。

```md
| ID | 種別 | 内容 | 関連文書 | 影響 |
|---|---|---|---|---|
| Q-005 | 矛盾 | 要件定義書では承認必須、画面仕様では承認操作の記載なし | requirements.md / screen_specs.md | 業務フロー・シナリオ候補に影響 |
```

## 10.2 優先順位が指定されている場合

ユーザーまたはプロジェクトで文書の優先順位が指定されている場合は、それに従う。

例:

1. ユーザーの明示指示
2. 最新の要件定義書
3. 画面仕様
4. 業務仕様
5. 過去資料

優先順位が不明な場合は、矛盾を確認事項にする。

---

# 11. 出力粒度の制御

## 11.1 詳細化しすぎないstep

以下のstepでは、詳細化しすぎない。

| Step   | 詳細化しない内容          |
| ------ | ----------------- |
| Step 1 | テスト観点、シナリオ、テストケース |
| Step 2 | 詳細操作手順、期待結果       |
| Step 3 | テスト手順、テストデータ詳細    |
| Step 4 | 実行手順、詳細期待結果       |

## 11.2 詳細化するstep

Step 5では、テスト実行可能な粒度まで詳細化する。

ただし、仕様上不明な部分は `要確認` とする。
AIエージェントが想像で埋めてはならない。

---

# 12. 優先度付けの制御

優先度は、Step 3以降で扱う。

| Step   | 優先度の扱い            |
| ------ | ----------------- |
| Step 1 | 原則扱わない            |
| Step 2 | 業務重要度が分かる場合のみ補足   |
| Step 3 | 観点単位で仮優先度を設定      |
| Step 4 | シナリオ候補単位で優先度を設定   |
| Step 5 | テストケース単位で最終優先度を設定 |

優先度を付ける場合は、必ず理由を記載する。

---

# 13. 実行時プロンプトの基本形

各stepの実行時は、原則として `templates/run_step_prompt_template.md` を使用する。

最小形式:

```md
# 実行対象step

Step X: ○○

# 参照ファイル

- prompts/rules.md
- prompts/orchestrator.md
- prompts/step_guides/stepX_xxx_guide.md
- outputs/前step成果物.md
- input_docs/必要な入力文書.md

# 指示

上記を参照し、Step X の成果物を作成してください。

以下を守ってください。

- 原文にない情報を断定しない
- 推測は推測と明記する
- 不明点は確認事項に分離する
- 完了後、次stepへ進まずレビュー待ちにする
```

---

# 14. 成果物の命名規則

成果物は、step番号を先頭に付ける。

```text
01_input_summary.md
02_business_flows.md
03_scenario_viewpoints.md
04_scenario_candidates.md
05_test_cases.md
```

必要に応じて、レビュー版や修正版を作成してよい。

```text
01_input_summary_v2.md
04_scenario_candidates_reviewed.md
05_test_cases_final.md
```

ただし、同一案件内で命名規則が乱れないようにする。

---

# 15. 最終成果物

最終成果物は `outputs/05_test_cases.md` とする。

必要に応じて、以下を追加で作成してよい。

```text
outputs/traceability_matrix.md
outputs/testcase_export.csv
outputs/scenario_summary.md
outputs/open_questions.md
```

ただし、これらは標準必須成果物ではない。
ユーザーから求められた場合、または案件上必要な場合のみ作成する。

---

# 16. エージェントの完了メッセージ

各step完了時は、簡潔に以下を伝える。

```md
Step X の成果物を作成しました。

作成物:
- outputs/XX_xxx.md

主な内容:
- ...
- ...
- ...

確認事項:
- ...

次に進む場合は、Step X+1 へ進むよう指示してください。
```
