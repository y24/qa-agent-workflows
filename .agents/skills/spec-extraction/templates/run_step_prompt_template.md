# run_step_prompt_template.md

## 1. このテンプレートの目的

このテンプレートは、AIエージェントに対して、指定したStepを実行させるための実行用プロンプトである。

このプロンプトは、以下の目的で使用する。

- `rules.md` と `orchestrator.md` に従って処理させる
- 指定したStepのみを実行させる
- 必要な入力成果物を明示する
- 処理対象範囲を限定する
- 推測・補完・先回りを防ぐ
- Step完了後に停止させる

---

## 2. 使用方法

このテンプレートの `<...>` 部分を、実行する内容に合わせて置き換える。

AIエージェントには、このプロンプトとあわせて、必要なファイルを渡す。

必ず渡すファイル:

- `rules.md`
- `orchestrator.md`
- 実行対象Stepの `step_guide`
- 必要な `helpers`
- 必要な `templates`
- 前Stepまでの成果物
- 対象ドキュメント本文または対象範囲

---

# 実行プロンプト

以下のプロンプト群に従って、指定されたStepを実行してください。

## 1. 参照する共通ファイル

必ず以下を参照してください。

- `rules.md`
- `orchestrator.md`

必要に応じて、以下の補助ファイルも参照してください。

- `helpers/extraction_category_definitions.md`
- `helpers/evidence_and_confidence_rules.md`
- `helpers/normalization_rules.md`
- `helpers/anti_hallucination_rules.md`

---

## 2. 実行するStep

今回実行するStepは以下です。

| 項目 | 内容 |
|---|---|
| 実行Step | `<Step番号>` |
| Step名 | `<Step名>` |
| 使用するStep Guide | `<step_guides/xxx.md>` |
| 使用するテンプレート | `<templates/xxx_template.md>` |
| 作成する成果物 | `<成果物ファイル名>` |

---

## 3. 実行ルール

以下を厳守してください。

- 指定されたStepのみを実行する
- 前後のStepを勝手に実行しない
- 成果物作成後は停止する
- ユーザー確認なしに次Stepへ進まない
- ドキュメントに明記されていない仕様を推測しない
- 不明点は不明として記録する
- 矛盾は矛盾として記録し、解消しない
- 不足情報を補完しない
- テストケースは作成しない
- 参照元IDを維持する
- 出力はMarkdown形式とする

---

## 4. 入力ファイル

今回使用する入力は以下です。

| 入力 | ファイル名・内容 | 備考 |
|---|---|---|
| 共通ルール | `rules.md` | 必須 |
| 進行管理 | `orchestrator.md` | 必須 |
| Step Guide | `<step_guides/xxx.md>` | 必須 |
| テンプレート | `<templates/xxx_template.md>` | 必須 |
| 補助ファイル | `<helpers/xxx.md>` | 必要に応じて |
| 前Step成果物 | `<前Stepの成果物>` | 必要に応じて |
| 入力ドキュメント | `<対象ドキュメント名または本文>` | 必要に応じて |
| ユーザー補足 | `<補足情報>` | ある場合のみ |

---

## 5. 処理対象範囲

今回処理する範囲は以下です。

| 項目 | 内容 |
|---|---|
| 対象DOC-ID | `<DOC-IDまたは不明>` |
| 対象ドキュメント | `<ドキュメント名>` |
| 対象章・節・ページ | `<対象範囲>` |
| 対象機能・領域 | `<対象機能・領域>` |
| 対象カテゴリ | `<対象カテゴリ>` |
| 対象ID範囲 | `<EXT-ID / SPEC-ID / TDI-ID など>` |
| 除外範囲 | `<除外する範囲>` |
| 未処理として残す範囲 | `<未処理範囲>` |

対象範囲が不明な場合は、推測せず `不明` または `要確認` と記録してください。

---

## 6. 出力形式

以下の構成で出力してください。

```md
# Step <番号>: <Step名>

## 入力

- 使用したファイル
- 使用した成果物
- 対象範囲
- 未提供の情報

## 実行結果

<指定されたテンプレートに従って成果物を出力>

## 未処理・要確認

- 未処理範囲
- 不明点
- 矛盾
- 不足
- 次Stepへ引き継ぐ事項

## 完了判定

- [ ] 指定された成果物が作成されている
- [ ] 必要なIDが付与されている
- [ ] 参照元が記録されている
- [ ] 推測による補完がない
- [ ] 矛盾を勝手に解消していない
- [ ] テストケースを作成していない
- [ ] 次Stepへ進まず停止している
````

チェックボックスは、実際の結果に応じて `[x]` または `[ ]` を使用してください。

---

## 7. Step別の実行指定例

### 7.1 Step 1を実行する場合

```md
以下のプロンプト群に従って、Step 1「ドキュメント棚卸し」を実行してください。

参照するファイル:
- rules.md
- orchestrator.md
- step_guides/step1_document_inventory_guide.md
- templates/document_inventory_template.md
- helpers/evidence_and_confidence_rules.md
- helpers/anti_hallucination_rules.md

作成する成果物:
- document_inventory.md

入力:
<開発ドキュメント一覧、ファイル名一覧、フォルダ構成、ユーザー補足など>

実行ルール:
- ドキュメント本文の詳細抽出は行わない
- 仕様内容を推測しない
- 各ドキュメントにDOC-IDを付与する
- 種別、対象領域、優先度、Step 2で読む範囲を整理する
- 完了後は停止し、Step 2へ進まない
```

---

### 7.2 Step 2を実行する場合

```md
以下のプロンプト群に従って、Step 2「事実情報の抽出」を実行してください。

参照するファイル:
- rules.md
- orchestrator.md
- step_guides/step2_raw_extraction_guide.md
- templates/raw_extraction_template.md
- helpers/extraction_category_definitions.md
- helpers/evidence_and_confidence_rules.md
- helpers/anti_hallucination_rules.md

作成する成果物:
- raw_extraction.md

入力:
- document_inventory.md
- 対象ドキュメント本文
- 対象範囲

対象範囲:
<今回抽出するDOC-ID、章、節、ページ、行、表など>

実行ルール:
- 原文に書かれている事実だけを抽出する
- 複数資料の統合は行わない
- 仕様の正誤判断は行わない
- 不足情報を補完しない
- テスト観点化しない
- テストケースを作成しない
- 各抽出情報にEXT-ID、DOC-ID、原文位置、カテゴリ、確度を付与する
- 完了後は停止し、Step 3へ進まない
```

---

### 7.3 Step 3を実行する場合

```md
以下のプロンプト群に従って、Step 3「正規化・統合」を実行してください。

参照するファイル:
- rules.md
- orchestrator.md
- step_guides/step3_normalization_guide.md
- templates/normalized_spec_inventory_template.md
- helpers/extraction_category_definitions.md
- helpers/evidence_and_confidence_rules.md
- helpers/normalization_rules.md
- helpers/anti_hallucination_rules.md

作成する成果物:
- normalized_spec_inventory.md

入力:
- document_inventory.md
- raw_extraction.md

対象範囲:
<今回正規化するEXT-ID範囲、カテゴリ、機能、対象領域など>

実行ルール:
- 抽出情報を仕様単位に整理する
- 同一仕様・同義表現・補完関係にある情報は統合してよい
- 統合時は参照EXT-IDをすべて残す
- 矛盾はcontradictionとして記録し、解消しない
- 不足情報はmissingまたはinsufficient_detailとして記録し、補完しない
- 未確定事項はto_be_confirmedとして扱う
- テスト観点化しない
- テストケースを作成しない
- 完了後は停止し、Step 4へ進まない
```

---

### 7.4 Step 4を実行する場合

```md
以下のプロンプト群に従って、Step 4「テスト設計インプット化」を実行してください。

参照するファイル:
- rules.md
- orchestrator.md
- step_guides/step4_test_design_input_guide.md
- templates/test_design_input_catalog_template.md
- helpers/extraction_category_definitions.md
- helpers/evidence_and_confidence_rules.md
- helpers/normalization_rules.md
- helpers/anti_hallucination_rules.md

作成する成果物:
- test_design_input_catalog.md

入力:
- normalized_spec_inventory.md
- 必要に応じて document_inventory.md
- 必要に応じて raw_extraction.md

対象範囲:
<今回テスト設計インプット化するSPEC-ID範囲、カテゴリ、機能、対象領域など>

実行ルール:
- 正規化仕様をテスト設計の材料に変換する
- テスト対象、確認すべき仕様、テスト観点、必要条件、入力データ観点、期待結果の種類を整理する
- 具体的なテストケースは作成しない
- 操作手順は作成しない
- 具体的なテストデータ値を網羅展開しない
- 期待結果は推測で断定しない
- 未確定・矛盾・不足のある仕様は注意付きで扱う
- 各項目にTDI-IDと参照SPEC-IDを付与する
- 完了後は停止し、Step 5へ進まない
```

---

### 7.5 Step 5を実行する場合

```md
以下のプロンプト群に従って、Step 5「不明点・矛盾・不足のレビュー」を実行してください。

参照するファイル:
- rules.md
- orchestrator.md
- step_guides/step5_gap_review_guide.md
- templates/gap_and_review_report_template.md
- helpers/evidence_and_confidence_rules.md
- helpers/normalization_rules.md
- helpers/anti_hallucination_rules.md
- 必要に応じて helpers/extraction_category_definitions.md

作成する成果物:
- gap_and_review_report.md

入力:
- document_inventory.md
- raw_extraction.md
- normalized_spec_inventory.md
- test_design_input_catalog.md

対象範囲:
<今回レビューするDOC-ID / EXT-ID / SPEC-ID / TDI-ID範囲、機能、対象領域など>

実行ルール:
- 不明点、矛盾、不足、粒度不足、未確定事項を整理する
- ギャップごとにGAP-IDを付与する
- テスト設計への影響を記録する
- 推奨対応と優先度を記録する
- 矛盾を勝手に解消しない
- 不足情報を推測で補完しない
- 仕様の正解を独断で決めない
- テストケースを作成しない
- 完了後は停止する
```

---

## 8. 入力不足時の扱い

入力が不足している場合でも、可能な範囲で処理してください。

ただし、不足情報は必ず明示してください。

記載例:

```md
## 入力不足

| 不足している入力 | 影響 | 対応 |
|---|---|---|
| document_inventory.md | DOC-IDや資料優先度を参照できない | 入力範囲内で仮IDを付与し、要確認として扱う |
| 原文位置情報 | 参照元の追跡性が弱くなる | 原文位置を「位置不明」として記録し、確度を下げる |
| 正本資料の情報 | 仕様判断上の優先度を判断できない | 優先度をUnknownとして扱う |
```

入力不足を理由に、推測で補完してはいけません。

---

## 9. 出力時の禁止事項

以下を禁止します。

* 指定されたStep以外を実行する
* ユーザー確認なしに次Stepへ進む
* 原文にない仕様を作る
* 曖昧な表現を断定に変える
* 不足情報を自然な仕様で補う
* 矛盾を勝手に解消する
* 参照元IDを省略する
* 根拠の弱い情報を確定仕様として扱う
* 未確定事項を確定仕様に変える
* テストケースを作成する
* 具体的な期待結果を推測する
* エラーメッセージを作る
* テストデータを具体値で網羅展開する

---

## 10. 出力後の停止ルール

成果物を出力したら、そこで停止してください。

最後に以下のように記載してください。

```text
<Step名>の成果物を作成しました。
内容を確認し、問題なければ次のStepを指示してください。
```

次Stepの成果物を続けて作成してはいけません。

---

## 11. 実行時チェックリスト

出力前に、以下を確認してください。

| 確認項目              | 判定          |
| ----------------- | ----------- |
| 指定されたStepのみ実行している | `<OK / NG>` |
| 対象範囲を超えて処理していない   | `<OK / NG>` |
| 参照元IDを記録している      | `<OK / NG>` |
| 不明点を不明として扱っている    | `<OK / NG>` |
| 推測による仕様補完がない      | `<OK / NG>` |
| 矛盾を勝手に解消していない     | `<OK / NG>` |
| テストケースを作成していない    | `<OK / NG>` |
| 次Stepへ進まず停止している   | `<OK / NG>` |
