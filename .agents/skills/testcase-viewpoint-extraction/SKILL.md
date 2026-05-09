---
name: testcase-viewpoint-extraction
description: Use when extracting test intent, abstract test viewpoints, viewpoint catalogs, and traceability from existing test cases. Do not use to generate new tests from requirements alone.
---

# テストケース観点抽出 skill

## 目的

既存テストケースを分析し、各ケースの意図と再利用可能なQA観点を抽出する。抽出結果は、根拠を追跡できる観点カタログとして整理する。

## 入力

- 既存のテストケース一覧、テスト手順、期待結果、テスト管理ツールのエクスポート
- 関連する画面仕様や要件がある場合は、その資料

## 出力

- `01_testcase_inventory.md`
- `01_input_issues.md`
- `02_intent_and_viewpoint_candidates.md`
- `02_extraction_issues.md`
- `03_viewpoint_catalog.md`
- `03_cataloging_issues.md`
- `04_final_traceability_matrix.md`
- `04_final_issue_log.md`
- `04_final_summary.md`

## ワークフロー

1. 入力の正規化とテストケースインベントリ作成
2. 意図と観点候補の抽出
3. 抽象化された観点カタログの作成
4. トレーサビリティ確認と最終化

ユーザーが明示的に継続を指示しない限り、各ステップ完了後に停止し、レビューを待つ。

## 参照ファイル

- 共通ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- 定義と判断基準: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 観点は既存テストケースから抽出し、無関係な要件から新規生成しない。
- 確信度の低い解釈は issue log またはレビュー事項に残す。
- 根拠が不足する観点は、レビュー対象として明示しない限り最終成果物に含めない。
