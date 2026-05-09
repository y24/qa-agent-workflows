意味はあるけど、**「長いから part1 / part2 に切る」だけなら、あまり意味はない**と思う。
むしろ、AIエージェントがどこを読めばいいか迷ったり、片方だけ読んで不完全に実行したりするリスクが増える。

大事なのは、**分割単位が“見出し”ではなく“用途”になっていること**だね。

---

## 結論

おすすめはこの考え方。

```text
悪い分割:
step_05_testcase_detail_part1.md
step_05_testcase_detail_part2.md
step_05_testcase_detail_part3.md

良い分割:
step_05_testcase_detail.md
references/testcase_granularity_rules.md
references/expected_result_policy.md
examples/testcase_detail_examples.md
templates/testcase_detail_template.md
```

つまり、**step 本体は短く保ち、重い説明・判断基準・例・テンプレートを外に出す**ほうがいい。

---

## part1 / part2 分割があまり効かない理由

たとえば、こういう分割はあまりよくない。

```text
step_05_part1.md
  - 目的
  - 入力
  - 前半の手順

step_05_part2.md
  - 後半の手順
  - チェック観点
  - 出力形式
```

この場合、エージェントは結局 **part1 と part2 の両方を読まないと正しく実行できない**。
つまり、コンテキスト削減になっていない。

さらに悪いことに、part2 を読み落とすと、品質チェックや出力条件が抜ける。
人間の手順書でも「続きは別紙2」みたいな構成は、だいたい事故の匂いがする。AIもそこそこ事故る。

---

## 分割に意味があるケース

意味があるのは、次のような場合。

### 1. 片方だけ読めば作業できる

```text
step_05_testcase_detail.md
references/testcase_granularity_rules.md
```

通常は `step_05_testcase_detail.md` だけ読む。
テストケース粒度に迷ったときだけ `references/testcase_granularity_rules.md` を読む。

これは意味がある。
必要時だけ読むから、コンテキストを節約できる。

---

### 2. サブステップとして独立している

たとえば `step_05_testcase_detail` が長すぎるなら、part1 / part2 ではなく、こう分ける。

```text
steps/
  step_05a_testcase_skeleton_guide.md
  step_05b_test_steps_and_expected_results_guide.md
  step_05c_testcase_review_and_refinement_guide.md
```

この場合は、それぞれが独立した作業単位になる。

```text
05a: テストケースの骨子を作る
05b: 手順・期待結果を具体化する
05c: 粒度・重複・証跡をレビューする
```

これは意味がある。
なぜなら、**各ファイルが「別の作業」を担当している**から。

---

### 3. オプション処理を切り出している

たとえば、通常のテストケース作成と CSV エクスポートは別にしてよい。

```text
steps/
  step_05_testcase_detail_guide.md
  step_06_priority_guide.md
  step_07_csv_export_guide.md
```

あるいは、詳細化の中でも optional なものは外に出す。

```text
references/
  abnormal_case_expansion_policy.md
  regression_candidate_selection_policy.md
  nonfunctional_viewpoint_addon.md
```

毎回使わないものを外に出すなら、ちゃんと意味がある。

---

## 分割の判断基準

私はこう判断するのがいいと思う。

```text
そのファイル単体で、明確な目的・入力・出力があるか？
  Yes → 分割してよい

別ファイルを必ず読まないと作業できないか？
  Yes → 分割の意味は薄い

通常時は読まなくてよい詳細か？
  Yes → references / examples / templates に切り出す

ユーザー確認を挟める作業単位か？
  Yes → substep に分割してよい
```

---

## 避けたい命名

`part1`、`part2` はできれば避けたほうがいい。

理由は、名前から中身が分からないから。

```text
避けたい:
step_05_part1.md
step_05_part2.md

良い:
step_05a_testcase_skeleton.md
step_05b_expected_results.md
step_05c_quality_review.md
```

AIにとっても、人間にとっても、**ファイル名がルーティング情報になる**。
`part2` は「2番目」ということしか伝えない。やや沈黙が深すぎる名前だね。

---

## おすすめの構成パターン

長い step は、こうするのが一番扱いやすい。

```text
steps/
  step_05_testcase_detail_guide.md

references/
  testcase_granularity_rules.md
  expected_result_policy.md
  precondition_and_testdata_policy.md
  traceability_policy.md

templates/
  testcase_detail_template.md
  issue_log_template.md

examples/
  testcase_detail_good_bad_examples.md
```

`step_05_testcase_detail_guide.md` の中では、こう書く。

```md
# Step 05: Test Case Detail

## Purpose
シナリオ候補を、実行可能なテストケースへ詳細化する。

## Inputs
- シナリオ候補一覧
- テスト観点
- 業務フロー
- 優先度の前提情報

## Outputs
- 詳細テストケース一覧
- 未解決事項
- トレーサビリティ情報

## Procedure
1. 各シナリオ候補をテストケース単位へ分解する。
2. 前提条件、テストデータ、操作、期待結果を具体化する。
3. 粒度が粗すぎる・細かすぎるケースを調整する。
4. 曖昧な仕様は推測せず、issue log に記録する。
5. 出力前に品質チェックを行う。

## Read When Needed
- 粒度判断に迷う場合: `references/testcase_granularity_rules.md`
- 期待結果の書き方に迷う場合: `references/expected_result_policy.md`
- 出力形式が必要な場合: `templates/testcase_detail_template.md`
- 記述例が必要な場合: `examples/testcase_detail_good_bad_examples.md`
```

これなら、通常時は step 本体だけ読める。
迷ったときだけ追加で読む。
これが、コンテキスト節約としてはかなり効く。

---

## 目安

長い step に対する判断は、こうでいいと思う。

| 状態             | 対応                                      |
| -------------- | --------------------------------------- |
| 150行以内         | そのままでよい                                 |
| 180〜250行       | 冗長な説明・例を外出し                             |
| 250行超          | references / templates / examples に切り出す |
| 300行超          | substep 化を検討                            |
| 1ファイルを読むだけでは重い | step 自体を分割する                            |

---

## まとめ

`part1 / part2` のような分割は、**読む量を減らせる場合だけ意味がある**。
でも、実際には両方読まないと実行できないことが多いので、あまりおすすめしない。

よりよい方針はこれ。

```text
step guide:
  実行に必要な最小手順

references:
  判断基準・分類・ポリシー

templates:
  出力形式

examples:
  具体例

substeps:
  本当に作業単位が分かれる場合だけ
```

だから、長い step を見出しごとに機械的に割るより、**「毎回読むもの」と「必要なときだけ読むもの」に分ける**のがいい。
コンテキストを守るという意味では、たぶんこれが一番効く。
