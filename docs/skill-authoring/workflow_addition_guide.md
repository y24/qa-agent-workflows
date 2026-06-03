# Workflow Addition Guide

この文書は、現行の `qa-workflow-toolkit` CLI に新しい QA workflow を追加する際の実装ポイントをまとめる。
CLI は workflow を実行せず、対象リポジトリへ agent workflow asset を配置することだけを責務とする。

## 追加するファイル

新規 workflow の正は package asset 側に置く。

```text
src/qa_workflow_toolkit/assets/workflow/
  commands/
    <workflow>.md
  workflows/
    <workflow>/
      workflow.json
      skill/
        SKILL.md
        orchestrator.md
        rules.md
        steps/
        references/
        templates/
```

`src/qa_workflow_toolkit/assets/workflow/shared/` は全 workflow 共通 asset の正である。
新規 workflow 固有の判断基準やテンプレートを shared に置かない。

## `workflow.json`

`workflow.json` は `qatool workflow list`、`install`、`update`、`uninstall` の入口になる。
必須項目は `src/qa_workflow_toolkit/models.py` の `WorkflowManifest.from_dict` と揃える。

最小例:

```json
{
  "id": "example-workflow",
  "display_name": "例示ワークフロー",
  "description": "入力資料から例示用の成果物を作る",
  "version": "0.1.0",
  "sort_order": 800,
  "skill_name": "example-workflow",
  "command_name": "example-workflow",
  "default_agent": "roocode",
  "supported_agents": ["roocode", "claude", "copilot", "codex"],
  "install": {
    "agents_md": true,
    "shared": {"source": "shared", "target": ".agents/shared"},
    "skill": {"source": "workflows/example-workflow/skill", "target": ".agents/skills/example-workflow"},
    "command": {"source": "commands/example-workflow.md", "target": ".roo/commands/example-workflow.md"}
  },
  "post_install_message": "/example-workflow <入力資料>"
}
```

注意点:

- `id`、`skill_name`、`command_name` は原則として同じ kebab-case にする。
- `sort_order` は `qatool workflow list` の表示順を決める。未指定の workflow は指定済み workflow の後ろに ID 順で並ぶ。
- `supported_agents` を省略すると、コード上の全対応 agent が対象になる。明示した方が意図を追いやすい。
- `install.command.target` は現状の install 処理では agent ごとの command 先に置き換えられるため、実質的な source 定義として扱う。ただし既存 manifest と同じ形で `.roo/commands/<workflow>.md` を書く。
- `install.shared.source` は通常 `shared`、`install.shared.target` は通常 `.agents/shared` にする。
- `install.skill.source` は `workflows/<workflow>/skill`、`install.skill.target` は `.agents/skills/<workflow>` にする。
- `post_install_message` はインストール後に表示する最短の使用例にする。

## Command Asset

`src/qa_workflow_toolkit/assets/workflow/commands/<workflow>.md` は agent の command から skill を起動するための薄い入口にする。
RooCode では `.roo/commands/<workflow>.md`、Claude では `.claude/commands/<workflow>.md`、GitHub Copilot では `.github/prompts/<workflow>.prompt.md`、Codex では `.codex/prompts/<workflow>.md` に配置される。

command には以下を含める。

- 呼び出す skill 名。
- 入力資料の渡し方。
- workflow の最初のステップで止まり、レビュー待ちする必要がある場合の指示。
- 成果物の出力先は shared の output policy に従うこと。

詳細な業務手順、判断基準、テンプレート本文は command に置かず、skill 配下へ置く。

## Skill Asset

skill 本体は `workflows/<workflow>/skill/` に置く。
インストール後は対象リポジトリの `.agents/skills/<workflow>/` になるため、skill 内の相対リンクはこの配置を前提に確認する。

標準構成:

```text
skill/
  SKILL.md
  orchestrator.md
  rules.md
  steps/
  references/
  templates/
```

`SKILL.md` は入口、`orchestrator.md` は進行制御、`rules.md` は skill 固有ルールに絞る。
共通ルールを参照する場合は、インストール後の相対位置で `../../shared/<file>.md` を参照するのが基本になる。

## Shared Asset の扱い

`assets/workflow/shared/` は全 workflow へ同じ内容が配布される。
shared を変更すると既存 workflow の `install` / `update` / `uninstall` に影響するため、次を確認する。

- 複数 workflow に本当に共通する内容か。
- 既存 workflow の参照リンクが壊れないか。
- 既存の用語、ID、出力ポリシーと矛盾しないか。
- 対象リポジトリでユーザー変更された shared は `uninstall` 時に削除されず、`update --yes` では上書きされることを説明できるか。

## CLI 挙動で意識する点

- `install` は `AGENTS.md`、shared、skill、command を計画し、既存ファイルがある場合は interactive では上書き / skip を確認する。
- `--yes` 付きの `install` は既存 asset を上書きする。ただし source と target が一致する場合は `no change` 扱いになる。
- `--no-agents-md` を指定すると `AGENTS.md` は配置しない。
- `update` はインストール済み metadata を使い、差分のある asset を上書きする。
- `uninstall` は package asset と完全一致するものだけ削除する。ユーザーが変更した asset は skipped になる。
- 複数 workflow が残っている場合、shared と `AGENTS.md` は最後の workflow を消すまで残る。
- agent ごとの command 配置先は `src/qa_workflow_toolkit/agents.py` で定義される。

## 確認手順

一時ディレクトリを使って、少なくとも以下を確認する。

```powershell
qatool workflow list
qatool workflow install --workflow <workflow> --agent roocode --target work/tmp-<workflow>-roocode --yes
qatool workflow install --workflow <workflow> --agent claude --target work/tmp-<workflow>-claude --yes
qatool workflow install --workflow <workflow> --agent copilot --target work/tmp-<workflow>-copilot --yes
qatool workflow install --workflow <workflow> --agent codex --target work/tmp-<workflow>-codex --yes
qatool workflow update --workflow <workflow> --target work/tmp-<workflow>-roocode --yes
qatool workflow uninstall --workflow <workflow> --target work/tmp-<workflow>-roocode --yes
pytest
```

確認観点:

- `workflow list` に ID、表示名、説明が出る。
- RooCode の command が `.roo/commands/<workflow>.md` に配置される。
- Claude の command が `.claude/commands/<workflow>.md` に配置される。
- GitHub Copilot の prompt file が `.github/prompts/<workflow>.prompt.md` に配置される。
- Codex の custom prompt が `.codex/prompts/<workflow>.md` に配置される。
- skill が `.agents/skills/<workflow>/SKILL.md` として配置される。
- shared が `.agents/shared/` に配置される。
- `.qa-toolkit/workflows.json` に workflow metadata が記録される。
- 2回目の install で一致 asset が `no change` になる。
- uninstall で変更済み asset が削除されない。

## テスト更新

新規 workflow を追加した場合、固定期待を持つテストの更新が必要になることがある。

- `tests/test_registry.py`: workflow 一覧、sort order、manifest の期待値。
- `tests/test_installer.py`: install plan、agent 別 command 配置、uninstall の挙動。
- `tests/test_cli.py`: `workflow list` 表示、install / update / uninstall の出力。

CLI の仕組みを変えずに workflow を追加するだけなら、既存テストへ必要最小限の期待値追加に留める。

## レビュー前チェック

- [ ] workflow 固有の手順や判断基準を CLI 本体に追加していない。
- [ ] package asset 側に正を置いている。
- [ ] `workflow.json` の source が実在する。
- [ ] command、skill、shared の責務が分かれている。
- [ ] skill 内の shared 参照がインストール後の相対位置で成立する。
- [ ] 出力先ポリシーが `assets/workflow/shared/output_location_policy.md` と矛盾していない。
- [ ] `qatool workflow list`、roocode install、claude install、pytest を確認した。
