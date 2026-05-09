# orchestrator.md

# シナリオテスト設計 Orchestrator

## 目的

`$scenario-test-design` の5Stepを順番に実行し、入力サマリ、業務フロー、シナリオ観点、シナリオ候補、テストケースを段階的につなぐ。

ユーザーが明示的に継続を指示しない限り、各Stepの出力後に停止してレビューを待つ。

## 全体フロー

| Step | 目的 | 主入力 | 主出力 | Guide | Template |
|---|---|---|---|---|---|
| 1 | 入力文書の要点抽出 | 入力文書 | `01_input_summary.md` | `steps/step1_input_summary_guide.md` | `templates/01_input_summary_template.md` |
| 2 | 業務フロー・利用シーン整理 | Step 1成果物 | `02_business_flows.md` | `steps/step2_business_flow_guide.md` | `templates/02_business_flows_template.md` |
| 3 | シナリオ観点抽出 | Step 2成果物 | `03_scenario_viewpoints.md` | `steps/step3_scenario_viewpoint_guide.md` | `templates/03_scenario_viewpoints_template.md` |
| 4 | シナリオ候補設計 | Step 3成果物 | `04_scenario_candidates.md` | `steps/step4_scenario_candidate_guide.md` | `templates/04_scenario_candidates_template.md` |
| 5 | テストケース化・優先度付け | Step 4成果物 | `05_test_cases.md` | `steps/step5_testcase_detail_guide.md` | `templates/05_test_cases_template.md` |

## 基本進行ルール

- 現在のStepに必要なファイルだけを参照する。
- 前Step成果物を主入力にし、元文書の再参照は根拠確認に必要な範囲へ限定する。
- 入力文書にない仕様、業務ルール、画面操作、期待結果を事実として創作しない。
- 推測、仮説、確認事項、未確定事項を明示する。
- 各Step完了後、ユーザーから明示的な続行指示があるまで次Stepへ進まない。

## 共通参照

- `../../../shared/common_contract.md`
- `../../../shared/evidence_and_confidence_policy.md`
- `../../../shared/ambiguity_and_issue_log_policy.md`
- `../../../shared/review_gate_policy.md`
- `../../../shared/traceability_policy.md`
- `../../../shared/output_style.md`
- `../../../shared/test_design_granularity_policy.md`

## Step別参照

| Step | 必須参照 | 必要時参照 |
|---|---|---|
| 1 | `rules.md`, `steps/step1_input_summary_guide.md`, `templates/01_input_summary_template.md` | `references/input_summary_policy.md` |
| 2 | `rules.md`, `steps/step2_business_flow_guide.md`, `templates/02_business_flows_template.md` | `references/business_flow_policy.md` |
| 3 | `rules.md`, `steps/step3_scenario_viewpoint_guide.md`, `templates/03_scenario_viewpoints_template.md` | `references/scenario_viewpoint_policy.md` |
| 4 | `rules.md`, `steps/step4_scenario_candidate_guide.md`, `templates/04_scenario_candidates_template.md` | `references/scenario_candidate_policy.md` |
| 5 | `rules.md`, `steps/step5_testcase_detail_guide.md`, `templates/05_test_cases_template.md` | `references/testcase_detail_policy.md`, `references/review_policy.md` |

## 応答形式

```markdown
# Step X: <ステップ名>

## 使用した入力
- 

## 成果物
<対象Stepの成果物>

## 確認事項
- 

## 次stepへの引き継ぎ
- 
```

## レビューと手戻り

- レビューは `references/review_policy.md` を使う。
- 再実行時は既存IDを可能な限り維持する。
- 追加、削除、統合、分割した項目は理由を記録する。
- 後続成果物が存在する場合は、影響範囲と再実行が必要なStepを明示する。

## 最終成果物

- `01_input_summary.md`
- `02_business_flows.md`
- `03_scenario_viewpoints.md`
- `04_scenario_candidates.md`
- `05_test_cases.md`

## 完了条件

- `Flow ID -> Viewpoint ID -> Scenario ID -> TC ID` の対応が追跡できる。
- 未確認事項、対象外、未カバー、保留が途中で消えていない。
- テストケースが詳細テスト設計または実行準備に渡せる粒度になっている。
