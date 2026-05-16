# Skill Review Checklist

新規 workflow 追加後、または既存 skill の再構成後に使うレビュー観点。
レビューでは、内容の網羅性だけでなく、通常実行時に読みやすい構成になっているかを確認する。

## CLI Asset

- [ ] 配布対象の正が `src/qa_workflow_toolkit/assets/workflow/` 配下にある。
- [ ] `workflow.json` が必須項目を持ち、source / target が実在する asset と一致している。
- [ ] `command_name` と `commands/<workflow>.md` が一致している。
- [ ] `sort_order` が既存 workflow の表示順と矛盾していない。
- [ ] `post_install_message` が最短の使用例になっている。

## 入口

- [ ] `SKILL.md` は目的、起動条件、対象外、入力、成果物、workflow 概要に絞られている。
- [ ] 詳細な手順、長い判断基準、テンプレート本文、大量の例が `SKILL.md` に残っていない。
- [ ] 参照ファイル一覧から、必要な情報へ辿れる。
- [ ] 起動条件が他 skill と過度に重複していない。

## Workflow

- [ ] `orchestrator.md` でステップ順序が明確になっている。
- [ ] ユーザー確認を待つ位置が明確になっている。
- [ ] 入力不足、矛盾、対象外がある場合の扱いが明確になっている。
- [ ] 各ステップの成果物が次ステップへ引き継がれる。
- [ ] 実行成果物の出力先が `assets/workflow/shared/output_location_policy.md` に従っている。

## 手順

- [ ] 各 `steps/*.md` は1ステップ1責務になっている。
- [ ] 手順と判断基準が過度に混在していない。
- [ ] そのステップで不要な背景説明が少ない。
- [ ] 成果物 ID や参照 ID を維持する指示が残っている。

## 判断基準

- [ ] 判断基準、分類、カタログは `references/` に集約されている。
- [ ] `references/*.md` が100行を超える場合は目次がある。
- [ ] 共通ルールは `assets/workflow/shared/` に置かれ、skill 固有ルールと混ざっていない。
- [ ] 推測、前提、未確認事項、提案の扱いが明確である。

## テンプレート

- [ ] 主要成果物ごとにテンプレートが分かれている。
- [ ] 表の列名が安定している。
- [ ] CSV 変換を想定する成果物で列名が揺れていない。
- [ ] テンプレート内に長い業務説明や判断基準が混入していない。

## サイズ

- [ ] `SKILL.md` は原則200行以内、最大300行目安に収まっている。
- [ ] `steps/*.md` は原則180行以内、最大250行目安に収まっている。
- [ ] `references/*.md` は300行を超えていない。
- [ ] `templates/*.md` はできるだけ100行以内に収まっている。
- [ ] 行数内でも、責務が混在するファイルを残していない。

## リンクと整合性

- [ ] `SKILL.md`、`orchestrator.md`、`steps/` からの参照リンクが切れていない。
- [ ] 実行時に参照する共通ポリシー一覧に `output_location_policy.md` が含まれている。
- [ ] 旧ファイル名への参照が残っていない。
- [ ] 同じルールを複数ファイルに重複記載していない。
- [ ] 削除・移動した内容の代替参照先が明確である。

## CLI 確認

- [ ] `qatool workflow list` で対象 workflow が表示される。
- [ ] roocode install で `.roo/commands/<workflow>.md` に command が配置される。
- [ ] claude install で `.claude/commands/<workflow>.md` に command が配置される。
- [ ] 2回目の install で一致 asset が `no change` になる。
- [ ] `update` と `uninstall` の挙動を説明できる。
- [ ] `pytest` が通る。
