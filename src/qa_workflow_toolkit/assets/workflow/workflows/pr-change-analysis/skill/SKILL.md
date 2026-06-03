---
name: pr-change-analysis
description: Use when a QA engineer gives one or more Azure DevOps Pull Request URLs and wants to understand what changed and what to test. The skill fetches PR metadata, code diffs, descriptions, and review comments via the Azure DevOps MCP, then produces a QA-readable diff report per PR and an analysis report of risks and test viewpoints (especially nonfunctional). For multiple PRs it also produces a cross-PR summary. Do not use when the user wants to author code, create or merge a PR, or only needs a line-by-line code review rather than test impact analysis.
---

# PR変更分析 skill

## 目的

普段コードの詳細を読まないQAエンジニアが、Azure DevOpsのPull Requestで「何がどう変わったか」を理解し、テストの影響範囲・リスク・観点を設計できるようにする。

コード差分だけでなく、Description、レビューコメント、リンクされた作業項目も読み、QAが読める言葉に翻訳する。リスクと、特に非機能のテスト観点を導く。

## 入力

- Azure DevOps Pull Request の URL（1件以上、複数可）
- 任意: 着目してほしい機能・品質特性、対象環境、過去不具合や懸念点
- 任意: テスト設計のスコープや目的（リリース判定、回帰範囲の見極め等）

Azure DevOps の情報取得は Azure DevOps MCP（`repo_*` / `wit_*` ツール）が利用可能である前提とする。取得手順とツール名は `references/azure_devops_mcp_usage.md` に従う。

## 出力

- `00_collection_plan.md`（対象PR一覧・取得項目・前提）
- PRごと: `<pr-slug>/diff_report.md`（差分レポート）
- PRごと: `<pr-slug>/analysis_report.md`（分析レポート: リスク＋テスト観点）
- `summary.md`（複数PR時の横断サマリ）
- `issue_log.md`（取得失敗・情報不足・確認事項）

## ワークフロー

1. 対象PR特定・情報収集スコープ整理
2. 全PRの変更内容理解・差分レポート作成
3. PRごとのリスク・テスト観点分析（リスクと観点を統合）
4. 横断サマリ作成（PRが複数のときのみ）

Step 1からStep 2（全PRの差分レポート作成）までは一気に進めてよい。差分レポートをすべて出力したら停止し、レビューを待つ。Step 3、Step 4の前後では、ユーザーが明示的に継続を指示しない限り停止する。

## 参照ファイル

- 共通方針:
  - `../../shared/common_contract.md`
  - `../../shared/evidence_and_confidence_policy.md`
  - `../../shared/ambiguity_and_issue_log_policy.md`
  - `../../shared/review_gate_policy.md`
  - `../../shared/traceability_policy.md`
  - `../../shared/output_style.md`
  - `../../shared/output_location_policy.md`
  - `../../shared/input_document_handling.md`
  - `../../shared/test_design_granularity_policy.md`
- skill固有ルール: `rules.md`
- 実行順序と停止条件: `orchestrator.md`
- ステップ別手順: `steps/`
- MCP取得手順・変更種別・非機能観点・翻訳方針: `references/`
- 出力テンプレート: `templates/`

## ガードレール

- 差分、Description、レビューコメント、作業項目に実在する内容だけを事実として扱う。コードに書かれていない挙動・意図・原因を創作しない。
- 取得できなかった情報（権限不足、差分が大きすぎる、バイナリ等）は埋めず、カバー範囲を明示して `issue_log.md` に記録する。
- リスク・テスト観点には、根拠となる変更（ファイル、差分箇所、コメントID、作業項目ID）または前Step成果物IDを残す。
- 非機能観点（性能、可用性、セキュリティ、互換性、運用性、移行・ロールバック等）を必ず一度走査する。該当なしと判断した場合はその根拠を残す。
- PR内容は機密の可能性があるため、成果物をコミット対象にする前に確認する（出力先方針に従う）。
