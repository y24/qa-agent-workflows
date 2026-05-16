# Output Style

## Default Style

- 日本語で簡潔に書く。
- Markdownを基本とし、表が有効な箇所は Markdown table を使う。
- 長い説明より、ID、短い説明、根拠、状態を優先する。
- 同じ内容を複数箇所に重複して書かない。
- CSV変換を想定する表は、列名を安定させる。
- 入力またはユーザーが別言語を指定した場合は、その指定に従う。

## Recommended Structure

```md
# 成果物名

## 1. 概要

## 2. 入力と参照元

## 3. 主成果物

## 4. 確認事項

## 5. 次ステップへの引き継ぎ
```

## Prohibited Style

- 根拠のない断定
- 未確認事項の黙殺
- 仕様の空想補完
- 巨大なJSONやYAMLを既定出力にすること
- レビュー待ちを無視した自動継続

## Shared Templates

- `templates/issue_log_template.md`
- `templates/evidence_table_template.md`
- `templates/traceability_matrix_template.md`

## Related Policies

- `output_location_policy.md`
