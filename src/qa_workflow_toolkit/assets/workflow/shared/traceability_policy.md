# Traceability Policy

## Purpose

入力、抽出情報、リスク、観点、シナリオ、テストケースの対応を追跡可能にするための共通方針を定義する。

## Traceability Targets

可能な範囲で、以下の対応を維持する。

- 入力文書、章、節、ページ、画面名、API名、機能名
- 前段成果物のID
- 抽出事実、正規化仕様、テスト設計インプット
- リスク、評価理由、テスト観点
- 業務フロー、利用シーン、シナリオ候補
- テストケース、期待結果、未カバー項目

## Minimum Rules

- 各主要成果物には、根拠または前段IDを付与する。
- 根拠がない項目は確定扱いにしない。
- 対応関係が切れた場合は issue log に記録する。
- ID変更、統合、分割、削除を行った場合は理由と影響先を残す。

## Recommended Matrices

| Workflow | Recommended Trace |
|---|---|
| `$spec-extraction` | `Doc ID -> Raw ID -> Spec ID -> TDI ID -> Gap ID` |
| `$scenario-test-design` | `Flow ID -> Viewpoint ID -> Scenario ID -> TC ID` |
| `$testcase-viewpoint-extraction` | `TC ID -> Intent ID -> Candidate ID -> Viewpoint ID` |
| `$risk-based-test-design` | `Risk ID -> Viewpoint ID -> TC ID` |
