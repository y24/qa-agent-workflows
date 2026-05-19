# Step 5: 戦略計画書と付属資料の最終化

## 目的

Step 1からStep 4の成果物を統合し、システムテスト計画書の戦略部分と付属資料を作成する。

## 入力

- `01_input_scope_summary.md`
- `02_system_test_coverage_analysis.md`
- `03_test_type_strategy.md`
- `04_test_viewpoint_policy.md`
- `templates/system_test_strategy_plan_template.md`
- `templates/quality_characteristic_matrix_template.md`
- `templates/viewpoint_traceability_template.md`

## 手順

1. 戦略計画書に、目的、対象、対象外、入力と根拠、非機能カバレッジ、テスト種別方針、観点方針、未確認事項、次工程への引き継ぎをまとめる。
2. スケジュール、体制、工数、担当者割当が混入していないか確認する。
3. 具体的なテストケース、手順、入力値、期待結果が混入していないか確認する。
4. ISO/IEC 25010品質特性ごとのマトリクスを作成し、該当する Viewpoint ID を記載する。
5. Viewpoint IDごとのトレーサビリティ付属資料を作成する。
6. 根拠不足、要確認、対象外が最終成果物から消えていないか確認する。

## 出力

- `05_system_test_strategy_plan.md`
- `appendix_quality_characteristic_matrix.md`
- `appendix_viewpoint_traceability.md`

## 完了条件

- テスト設計担当者が各テスト種別を詳細化できる方針になっている。
- 各観点の根拠と品質特性が追跡できる。
- 入力にない内容が推測で補完されていない。
- この workflow の対象外情報が含まれていない。
