# Step 3: テスト種別の選定と戦略整理

## 目的

Coverage をもとに、システムテストで計画すべき複数のテスト種別を根拠付きで選定し、各テスト種別の目的、対象、扱う品質特性、未確認事項を整理する。

## 入力

- `02_system_test_coverage_analysis.md`
- `references/test_type_catalog.md`
- `references/iso25010_quality_characteristics.md`
- `templates/test_type_strategy_template.md`

## 手順

1. Coverage ID をテスト種別候補へ対応づける。
2. 各テスト種別を `計画対象`、`計画候補・要確認`、`対象外`、`根拠不足` に分類する。
3. `計画対象` と `計画候補・要確認` には `TT-001` 形式の Test Type ID を付与する。
4. 各 Test Type ID について、目的、対象、主品質特性、関連 Coverage、根拠、未確認事項を記録する。
5. 対象外または根拠不足のテスト種別は、理由を短く残す。

## 禁止事項

- catalog にある全テスト種別を採用しない。
- テスト種別名だけで戦略を終えない。
- 詳細なテスト手順、テストデータ、期待結果を作らない。
- 根拠不足のテスト種別を計画対象へ混ぜない。

## 出力

`03_test_type_strategy.md`

## 完了条件

- 計画対象のテスト種別が、Coverage ID と根拠へ紐づいている。
- 複数テスト種別の役割分担が説明できる。
- 次Stepでテスト観点へ落とせる粒度になっている。
