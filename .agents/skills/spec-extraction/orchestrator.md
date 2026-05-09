# orchestrator.md

# Spec Extraction Orchestrator

## 役割

`$spec-extraction` の5Stepを順番に実行し、開発文書からテスト設計に使える仕様インプットを根拠付きで作成する。

ユーザーが明示的に継続を指示しない限り、各Stepの出力後に停止してレビューを待つ。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | ドキュメント棚卸し | 入力文書 | `document_inventory.md` | `steps/step1_document_inventory_guide.md` | `templates/document_inventory_template.md` |
| 2 | 事実情報の抽出 | Step 1成果物、入力文書 | `raw_extraction.md` | `steps/step2_raw_extraction_guide.md` | `templates/raw_extraction_template.md` |
| 3 | 正規化・統合 | Step 2成果物 | `normalized_spec_inventory.md` | `steps/step3_normalization_guide.md` | `templates/normalized_spec_inventory_template.md` |
| 4 | テスト設計インプット化 | Step 3成果物 | `test_design_input_catalog.md` | `steps/step4_test_design_input_guide.md` | `templates/test_design_input_catalog_template.md` |
| 5 | ギャップレビュー | Step 1-4成果物 | `gap_and_review_report.md` | `steps/step5_gap_review_guide.md` | `templates/gap_and_review_report_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 入力文書、前Step成果物、ユーザー指定を根拠にする。
- 入力にない仕様、期待結果、テスト条件を事実として創作しない。
- 推測、仮説、確認事項、未確定事項を明示する。
- 未処理範囲を隠さない。

## 共通参照

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`
- `../../../shared/output_style.md`
- `../../../shared/output_location_policy.md`
- `../../../shared/input_document_handling.md`

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 1 | `rules.md`, `steps/step1_document_inventory_guide.md`, `templates/document_inventory_template.md` | `references/document_inventory_policy.md`, `references/evidence_and_confidence_rules.md` |
| 2 | `rules.md`, `steps/step2_raw_extraction_guide.md`, `templates/raw_extraction_template.md` | `references/extraction_category_definitions.md`, `references/extraction_category_catalog.md`, `references/evidence_and_confidence_rules.md`, `references/anti_hallucination_rules.md` |
| 3 | `rules.md`, `steps/step3_normalization_guide.md`, `templates/normalized_spec_inventory_template.md` | `references/normalization_rules.md`, `references/normalization_policy.md`, `references/evidence_and_confidence_rules.md` |
| 4 | `rules.md`, `steps/step4_test_design_input_guide.md`, `templates/test_design_input_catalog_template.md` | `references/test_design_input_policy.md`, `references/anti_hallucination_rules.md` |
| 5 | `rules.md`, `steps/step5_gap_review_guide.md`, `templates/gap_and_review_report_template.md` | `references/gap_review_policy.md`, `references/anti_hallucination_rules.md` |

## 応答形式

```markdown
# Step X: <ステップ名>

## 入力
- 

## 実行結果
<対象Stepの成果物>

## 未処理・要確認
- 

## 完了判定
- 完了 / 一部完了 / 要追加入力
```

## 途中修正

- 既存IDは可能な限り維持する。
- 削除、統合、追加、分割の理由を記録する。
- 後続成果物がある場合は、影響範囲と再実行が必要なStepを明示する。

## 最終完了条件

- `Doc ID -> Raw ID -> Spec ID -> TDI ID -> Gap ID` の追跡ができる。
- 未確認、矛盾、不足、未処理範囲が途中で消えていない。
- 後続テスト設計で断定してはいけない事項が明示されている。
