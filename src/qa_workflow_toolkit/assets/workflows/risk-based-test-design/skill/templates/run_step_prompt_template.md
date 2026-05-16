# templates/run_step_prompt_template.md

# Step実行プロンプトテンプレート

## 用途
特定Stepの実行、再実行、レビュー、最終整合性確認を依頼するときに使う最小テンプレート。

## Step実行依頼テンプレート

```text
目的: 指定Stepの成果物だけを作成する。

## 実行対象Step

- Step:
- 目的:

## 入力

- 入力文書または前Step成果物:

## 参照ファイル
- `rules.md`
- `orchestrator.md`
- `steps/<対象stepのguide>`
- `templates/<対象成果物template>`
- 必要な `references/`

## 実行指示
- 入力文書または前Step成果物に基づいて作成する。
- 根拠のない仕様、リスク、テスト条件を創作しない。
- 推測、仮説、確認事項は事実と分けて記載する。
- 対象Stepの成果物だけを作成する。
- 出力後は停止し、次Stepへ進まない。
```

## レビュー依頼テンプレート

```text
目的: 指定成果物をレビューし、次Stepへ進めるか判断する。

## レビュー対象

- Step:
- 成果物:

## 参照ファイル
- `references/review_checklist.md`
- `references/review_checklist_steps.md`
- 必要な前Step成果物

## 出力
- 総合判定: OK / 条件付きOK / 要修正
- 指摘一覧
- 修正が必要な事項
- 未解決事項
- 次Stepへ進む条件
```

## 再実行依頼テンプレート

```text
目的: 変更入力を反映して指定Stepを再実行する。

## 再実行対象

- Step:
- 修正理由:

## 変更された入力

-

## 実行時の注意
- 既存IDは可能な限り維持する。
- 変更影響を後続成果物へ引き継ぐ。
- 削除、統合、追加した項目は理由を記録する。
```

## 最終整合性確認依頼テンプレート

```text
目的: 全成果物の対応関係と残存リスクを確認する。

## レビュー対象
- `01_input_scope_summary.md`
- `02_risk_candidate_list.md`
- `03_risk_register.md`
- `04_risk_based_test_strategy.md`
- `05_testcase_outline_and_traceability.md`

## 確認観点
- 対象範囲、リスク、評価、テスト観点、テストケース骨子の対応が切れていないか
- P0/P1リスクの扱いが明確か
- 未カバー、対象外、残存リスクが説明されているか
```
