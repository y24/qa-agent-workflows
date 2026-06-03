# Azure DevOps MCP 取得手順

Azure DevOpsからのPull Request情報の取得は、Azure DevOps MCP（https://github.com/microsoft/azure-devops-mcp）が利用可能である前提とする。
このファイルでは、本ワークフローで使うツールとパラメータ、URLの分解規則、取得レシピを定義する。

## ツール名の注意

ここに記すのはMCPサーバが登録する正規のツール名（例: `repo_get_pull_request_by_id`）である。
実際の呼び出し名は、エージェント側でMCPサーバ名の接頭辞が付く場合がある（例: `mcp__azure-devops__repo_get_pull_request_by_id`、`mcp_ado_repo_get_pull_request_by_id` など）。
環境に存在するツール一覧を確認し、同じ末尾名のツールを使う。組織（organization）は通常MCPサーバ側の設定で固定されるため、パラメータでは `project` / `repositoryId` / `pullRequestId` を指定する。

## PR URL の分解規則

代表的なAzure DevOpsのPR URL形式:

```text
https://dev.azure.com/{organization}/{project}/_git/{repository}/pullrequest/{pullRequestId}
https://{organization}.visualstudio.com/{project}/_git/{repository}/pullrequest/{pullRequestId}
```

- `{project}` を `project`、`{repository}` を `repositoryId`、`{pullRequestId}` を `pullRequestId` に対応させる。
- `repositoryId` にはリポジトリ名を指定できる（GUIDが必要な場合は名前で解決してから使う）。
- `{project}` や `{repository}` にURLエンコード（`%20` 等）が含まれる場合はデコードする。
- 形式に当てはまらない、または値が欠けるURLは推測で補わず、確認事項にする。

## 使用ツールと主なパラメータ

| 用途 | ツール名 | 主なパラメータ |
|---|---|---|
| PRメタ情報の取得 | `repo_get_pull_request_by_id` | `repositoryId`(必須), `pullRequestId`(必須), `project`, `includeWorkItemRefs`, `includeLabels`, `includeChangedFiles` |
| 変更ファイル/差分の取得 | `repo_get_pull_request_changes` | `repositoryId`(必須), `pullRequestId`(必須), `iterationId`, `project`, `top`, `skip`, `compareTo`, `includeDiffs`, `includeLineContent` |
| コメントスレッド一覧 | `repo_list_pull_request_threads` | `repositoryId`(必須), `pullRequestId`(必須), `project`, `iteration`, `top`, `skip`, `status` |
| スレッド内コメント取得 | `repo_list_pull_request_thread_comments` | `repositoryId`(必須), `pullRequestId`(必須), `threadId`(必須), `project`, `top`, `skip` |
| 作業項目の一括取得 | `wit_get_work_items_batch_by_ids` | `ids`(必須), `project`, `fields` |
| 作業項目の個別取得 | `wit_get_work_item` | `id`(必須), `project`, `fields`, `expand` |
| （補助）PR一覧・特定 | `repo_list_pull_requests_by_repo_or_project` | `repositoryId`, `project`, `status`, `top`, `skip` ほか |

パラメータ名はMCPのバージョンで変わりうる。存在するパラメータのみを使い、不明なものは指定しない。

## 取得レシピ（PR 1件あたり）

1. **メタ情報**: `repo_get_pull_request_by_id` を `includeWorkItemRefs: true`、`includeLabels: true`、`includeChangedFiles: true` で呼び、タイトル、Description、source/targetブランチ、状態、作成者、ラベル、リンク作業項目参照、変更ファイル概要を得る。
2. **差分**: `repo_get_pull_request_changes` を呼ぶ。まず差分なし（`includeDiffs` 省略または false）で変更ファイル規模を把握し、必要なファイルについて `includeDiffs: true`（必要なら `includeLineContent: true`）で内容を取得する。件数が多い場合は `top` / `skip` でページングする。
3. **コメント**: `repo_list_pull_request_threads` でスレッド一覧を取得し、内容が要約に不足する場合は各 `threadId` について `repo_list_pull_request_thread_comments` で本文を取得する。システム生成スレッド（投票・ステータス変更等）と人手のレビューコメントを区別する。
4. **作業項目**: メタ情報のリンク参照から作業項目IDを集め、`wit_get_work_items_batch_by_ids` でまとめて取得する。ユーザーストーリー/バグの内容を変更意図の根拠にする。

## 取得時の原則

- 大きなPRは差分を一度に全取得せず、変更ファイル一覧→重要ファイルの差分、の順で段階取得する。
- 取得上限・ページング・権限不足で読めなかった範囲は、レポートの「カバー範囲」に明記し、`issue_log.md` に残す。
- バイナリ、生成物、ロックファイル、フォーマット専用変更は、差分本文の精読より変更種別の判定を優先する。
- 取得した値はそのまま根拠として引用できるよう、ファイル名・スレッドID・コメントID・作業項目IDを保持する。
- 取得失敗時は推測で補わず、再取得方針か確認事項として記録する。
