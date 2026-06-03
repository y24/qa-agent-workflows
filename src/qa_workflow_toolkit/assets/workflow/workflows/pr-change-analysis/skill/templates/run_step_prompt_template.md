# Run Step Prompt Template

```markdown
$pr-change-analysis の Step <番号> を実行してください。

## 対象

- 対象Pull RequestのURL（複数可）:
- テスト設計の目的・スコープ:
- 着目してほしい機能・品質特性:
- 対象環境:

## 入力

- <PR URL群、または前Step成果物>

## 出力先

- <指定がなければ shared/output_location_policy.md に従う>

## 注意事項

- 差分・Description・コメント・作業項目にない挙動、意図、原因を創作しない。
- 事実、推測、確認事項を分ける。
- 取得できなかった範囲はカバー範囲と issue_log.md に明示する。
- リスク・観点には根拠（変更箇所・コメントID・作業項目ID）または前StepのIDを残す。
- 非機能観点を一巡する。
- Step完了後（Step 2の全差分レポート、Step 3、Step 4）はレビュー待ちで停止する。
```
