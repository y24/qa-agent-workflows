# run_step_prompt_template.md

# Step実行プロンプトテンプレート

## Step実行依頼

```text
目的: 指定Stepの成果物だけを作成する。

## 実行対象Step
- Step:
- 目的:

## 入力
- 入力ファイルまたは前Step成果物:

## 参照ファイル
- `rules.md`
- `orchestrator.md`
- `steps/<対象stepのguide>`
- `templates/<対象成果物template>`
- 必要な `references/`

## 実行指示
- 既存テストケースを根拠にする。
- 推定、低確度、曖昧さは明示する。
- 対象Stepの成果物だけを作成する。
- 出力後は停止し、次Stepへ進まない。
```

## レビュー依頼

```text
目的: 指定成果物をレビューし、次Stepへ進めるか判断する。

## レビュー対象
- Step:
- 成果物:

## 出力
- 総合判定: OK / 条件付きOK / 要修正
- 指摘一覧
- 未解決Issue
- 次Stepへ進む条件
```
