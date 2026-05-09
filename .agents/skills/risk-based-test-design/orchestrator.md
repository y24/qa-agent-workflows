# orchestrator.md

# リスクベースドテスト設計 Orchestrator

## 目的

`$risk-based-test-design` の5Stepを順番に実行し、各Stepの成果物を後続Stepの入力としてつなぐ。

複数Stepをユーザーが明示しない限り、一度に進めない。各Stepの出力後はレビュー待ちで停止する。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 入力文書整理・分析スコープ確定 | 入力文書 | `01_input_scope_summary.md` | `steps/step1_input_scope_guide.md` | `templates/input_scope_summary_template.md` |
| 2 | リスク候補抽出 | Step 1成果物 | `02_risk_candidate_list.md` | `steps/step2_risk_extraction_guide.md` | `templates/risk_candidate_list_template.md` |
| 3 | リスク評価・優先順位付け | Step 2成果物 | `03_risk_register.md` | `steps/step3_risk_assessment_guide.md` | `templates/risk_register_template.md` |
| 4 | リスクベースドテスト方針設計 | Step 3成果物 | `04_risk_based_test_strategy.md` | `steps/step4_test_strategy_guide.md` | `templates/risk_based_test_strategy_template.md` |
| 5 | テストケース骨子・トレーサビリティ作成 | Step 4成果物 | `05_testcase_outline_and_traceability.md` | `steps/step5_testcase_outline_guide.md` | `templates/testcase_traceability_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 前Step成果物を主入力にし、元文書の再参照は根拠確認に必要な範囲へ限定する。
- 入力文書にない仕様、リスク、テスト条件を事実として創作しない。
- 推測、仮説、確認事項、未確定事項は明示する。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 1 | `rules.md`, `steps/step1_input_scope_guide.md`, `templates/input_scope_summary_template.md` | `references/input_scope_policy.md`, `references/risk_taxonomy.md` |
| 2 | `rules.md`, `steps/step2_risk_extraction_guide.md`, `templates/risk_candidate_list_template.md` | `references/risk_taxonomy.md`, `references/risk_taxonomy_catalog.md`, `references/risk_extraction_policy.md` |
| 3 | `rules.md`, `steps/step3_risk_assessment_guide.md`, `templates/risk_register_template.md` | `references/scoring_model.md`, `references/risk_assessment_policy.md`, `references/risk_assessment_examples.md` |
| 4 | `rules.md`, `steps/step4_test_strategy_guide.md`, `templates/risk_based_test_strategy_template.md` | `references/test_technique_mapping.md`, `references/test_technique_catalog.md`, `references/test_strategy_policy.md` |
| 5 | `rules.md`, `steps/step5_testcase_outline_guide.md`, `templates/testcase_traceability_template.md` | `references/testcase_outline_policy.md`, `references/review_checklist.md` |

## 応答形式

```markdown
# Step X: <ステップ名>

## 使用した入力

- 

## 成果物

<対象Stepの成果物>

## 確認事項

- 

## 次に進む前のレビュー観点

- 
```

## レビューと再実行

- レビューは `references/review_checklist.md` と `references/review_checklist_steps.md` を使う。
- レビュー結果の記録形式と次Stepへ進む条件は `references/review_result_policy.md` を使う。
- 再実行時は既存IDを可能な限り維持し、追加、削除、統合、分割の理由を記録する。
- 後続成果物が存在する場合は、影響範囲を明示し、必要な再実行Stepを提案する。

## 完了条件

- Step 1からStep 5までの成果物が作成されている。
- `Risk ID -> Viewpoint ID -> TC ID` の対応が追跡できる。
- P0/P1リスクの扱い、未カバーリスク、対象外、残存リスクが説明されている。
- 未確認事項が途中で消えず、最終成果物に引き継がれている。
