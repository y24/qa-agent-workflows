# Step 4: テスト種別ごとのテスト観点策定

## 目的

選定されたテスト種別ごとに、詳細テスト設計へ引き継ぐためのテスト観点を策定する。

## 入力

- `03_test_type_strategy.md`
- `02_system_test_coverage_analysis.md`
- `references/viewpoint_traceability_policy.md`
- `templates/test_viewpoint_policy_template.md`

## 手順

1. 計画対象または計画候補の Test Type ID ごとに、必要な観点を `VP-001` 形式で定義する。
2. 各 Viewpoint ID に、確認目的、対象、主品質特性、副品質特性、関連 Coverage、根拠 Source Fact を紐づける。
3. 詳細設計担当者への引き継ぎとして、必要な詳細化事項、確認すべき未確定条件を記録する。
4. 根拠が弱い観点は `計画候補・要確認` とし、最終計画で確定扱いにしない。
5. 重複する観点は統合し、統合理由を記録する。

## 観点粒度

- 良い粒度: 「管理者ロールと一般利用者ロールで参照・更新可能範囲が仕様どおり分離されること」
- 詳細すぎる粒度: 「ユーザーAでログインし、ボタンXを押して、エラーコードYを確認する」
- 根拠不足の粒度: 「セキュリティを十分に確認する」

## 禁止事項

- 詳細テストケースを作らない。
- 入力にない期待値や閾値を作らない。
- 根拠のない非機能観点を追加しない。

## 出力

`04_test_viewpoint_policy.md`

## 完了条件

- 各 Viewpoint ID が Test Type ID、Coverage ID、Source Fact ID へ追跡できる。
- 詳細テスト設計へ渡す方針と未確認事項が明確である。
- 最終付属資料を作れるだけのトレーサビリティが揃っている。
