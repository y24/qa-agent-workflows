# extraction_category_definitions.md

# 抽出カテゴリ定義

## 目的

Step 2以降で抽出・正規化する仕様情報の標準カテゴリを定義する。

カテゴリは整理の補助であり、独自カテゴリを増やさず、主カテゴリを1つ選ぶ。迷う場合は関連カテゴリを備考に書く。

## カテゴリ一覧

| カテゴリ | 用途 |
|---|---|
| `feature` | 機能、ユースケース、処理目的 |
| `screen` | 画面、ページ、画面遷移 |
| `ui_item` | 入力項目、表示項目、ボタン、ラベル |
| `report` | 帳票、CSV、PDF、出力ファイル |
| `api` | API、外部IF、リクエスト、レスポンス |
| `batch` | バッチ、ジョブ、スケジュール処理 |
| `data` | データ、テーブル、マスタ、項目定義 |
| `business_rule` | 業務ルール、制約、業務判断 |
| `validation` | 入力チェック、妥当性確認 |
| `state_transition` | 状態、ステータス、遷移 |
| `condition_branch` | 条件分岐、判定ロジック |
| `calculation` | 計算、集計、丸め、式 |
| `permission` | 権限、ロール、認可 |
| `error_handling` | エラー、例外、リカバリ |
| `operation` | 操作、運用手順、手作業 |
| `non_functional` | 性能、可用性、互換性、セキュリティなど |
| `open_issue` | 未決事項、確認事項、仕様未確定 |

## 基本方針

- 原文の主旨に最も近い主カテゴリを1つ選ぶ。
- 推測で分類しない。分類不能な場合は `open_issue` または `要確認` とする。
- カテゴリ名は固定値を使う。
- 関連カテゴリは備考に書く。

## 詳細参照

- 各カテゴリの定義、該当情報、例、注意: `extraction_category_catalog.md`
- 判断に迷いやすいカテゴリの切り分け: `extraction_category_decision_policy.md`

## 使用するStep

| Step | 使用目的 |
|---|---|
| Step 2 | 生情報抽出時のカテゴリ付与 |
| Step 3 | 正規化後カテゴリの確認 |
| Step 4 | テスト設計インプットのカテゴリ別整理 |
