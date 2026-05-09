分量としては、**今の AGENTS.md はかなり良い範囲に収まっている**と思う。
ざっくり見ると 70〜90行程度なので、前に話した「120行以内を目標、200行以内を上限」という基準から見ても問題ない。

ただし、改善するならポイントはある。

**長すぎるというより、“常時読むべき内容”と“スキル保守時だけ読めばよい内容”が少し混ざっている**感じだね。

---

## 評価

### 良いところ

今の AGENTS.md はかなり整理されている。

特に良いのはこのあたり。

* QA業務向けプロジェクトであることが冒頭で分かる
* 共通ルールが簡潔
* Skill Routing が明確
* Repository Layout が一目で分かる
* `SKILL.md` / `steps/` / `references/` / `templates/` の責務が書かれている
* 推測禁止、トレーサビリティ、レビューゲートがちゃんと入っている

このままでも実用上は大きな問題はないと思う。

---

## 改善したほうがよさそうな点

### 1. `File Size Policy` は AGENTS.md から外してよい

ここは一番改善余地がある。

`File Size Policy` は、QA workflow を**実行するエージェント**が毎回知る必要は薄い。
これはどちらかというと、**skill を作る人・再編成する人向けの保守ルール**だね。

なので、ここは以下に移すのがよさそう。

```text
docs/skill-authoring/file_size_policy.md
```

AGENTS.md には、案内だけ残す。

```md
## Skill maintenance

新しい skill を追加する場合、または既存プロンプト群を skill 形式へ再編成する場合は、`docs/skill-authoring/README.md` に従う。
```

これで AGENTS.md が少し軽くなる。

---

### 2. `Change Policy` も一部は docs 側でよい

`Change Policy` の内容は悪くない。
でも、これも多くは「保守時のルール」だね。

AGENTS.md に残すなら、1〜2行くらいで十分。

```md
## Change Policy

- 業務別の詳細手順やファイルサイズ方針は `docs/skill-authoring/` に置く。
- 共通ルールは `shared/`、skill固有ルールは該当 skill の `references/` に置き、責務の重複を増やさない。
```

今の詳細版は `docs/skill-authoring/migration_checklist.md` や `skill_structure_standard.md` に移すのがよさそう。

---

### 3. `Output Conventions` は `shared/output_style.md` と重複しやすい

AGENTS.md に出力規約を書くのは悪くない。
ただ、`shared/output_style.md` があるなら、AGENTS.md には要約だけでよい。

たとえば今の内容はこう短縮できる。

```md
## Output Conventions

- 出力は原則として日本語の Markdown とする。
- 大きな成果物は、要約、入力と参照元、主成果物、確認事項、次ステップへの引き継ぎの順に整理する。
- 詳細な出力規約は `shared/output_style.md` に従う。
```

`推測:` や `要確認` の扱いは、`shared/evidence_and_confidence_policy.md` や `shared/ambiguity_and_issue_log_policy.md` に寄せてもいい。

---

## 私ならこう直す

常時読む AGENTS.md としては、これくらいまで絞る。

````md
# qa-agent-workflows

このリポジトリは、QA業務向けの再利用可能な AI agent workflow skills をまとめたプロジェクトです。

## Common Working Rules

- 要件、仕様、リスク、テスト条件を根拠なしに創作しない。
- 事実、推測、前提、未確認事項、提案を分けて扱う。
- 可能な限り、入力文書、前段成果物、IDへのトレーサビリティを残す。
- 複数ステップの workflow は、ユーザーが明示的に継続を指示しない限り、主要ステップごとに停止してレビューを待つ。
- 出力は原則として日本語の Markdown とする。入力またはユーザーが別言語を指定した場合はそれに従う。
- 不明点、矛盾、証拠不足、未解決の前提は issue log または確認事項として明示する。

## Skill Routing

- `$spec-extraction`: 開発文書からテスト設計に必要な仕様情報を抽出、正規化、棚卸しする。
- `$scenario-test-design`: 要件、業務フロー、画面仕様、ドメインルールからシナリオテストを設計する。
- `$testcase-viewpoint-extraction`: 既存テストケースから意図、抽象テスト観点、観点カタログ、トレーサビリティを抽出する。
- `$risk-based-test-design`: リスク候補の抽出、評価、優先度付け、リスクベースのテスト方針とテストケース骨子を作る。

## Repository Layout

```text
qa-agent-workflows/
  AGENTS.md
  docs/
    skill-authoring/
  shared/
  .agents/
    skills/
      spec-extraction/
      scenario-test-design/
      testcase-viewpoint-extraction/
      risk-based-test-design/
````

各 skill は `SKILL.md` を入口とし、詳細な実行手順は `steps/`、判断基準や定義は `references/`、出力形式は `templates/` に置く。

## Shared References

共通ポリシーは `shared/` に置く。各 skill は必要に応じて以下を参照する。

* `shared/common_contract.md`
* `shared/evidence_and_confidence_policy.md`
* `shared/ambiguity_and_issue_log_policy.md`
* `shared/traceability_policy.md`
* `shared/review_gate_policy.md`
* `shared/output_style.md`

## Output Conventions

* 大きな成果物は、要約、入力と参照元、主成果物、確認事項、次ステップへの引き継ぎの順に整理する。
* 表は Markdown table を優先する。CSV変換を想定する成果物は列名を安定させる。
* 推測や判断不能な内容は本文に紛れ込ませず、推測、要確認、情報不足、対象外などの状態を明示する。

## Skill Maintenance

新しい skill を追加する場合、または既存プロンプト群を skill 形式へ再編成する場合は、`docs/skill-authoring/README.md` に従う。

業務別の詳細手順を `AGENTS.md` に直接追加しない。

````

---

## 移動先のおすすめ

今の AGENTS.md から外した内容は、こう分けるとよい。

```text
docs/skill-authoring/
  README.md
  file_size_policy.md
  migration_checklist.md
  skill_structure_standard.md
````

対応関係はこう。

| 今の内容                     | 移動先                                                |
| ------------------------ | -------------------------------------------------- |
| `File Size Policy` 全体    | `docs/skill-authoring/file_size_policy.md`         |
| `Change Policy` の詳細      | `docs/skill-authoring/migration_checklist.md`      |
| `SKILL.md` の責務説明         | `docs/skill-authoring/skill_structure_standard.md` |
| `Repository Layout` の詳細版 | `docs/skill-authoring/README.md`                   |
| 常時守る最小ルール                | `AGENTS.md` に残す                                    |

---

## 最終判断

今の AGENTS.md は、**分量としては問題ない**。
ただ、今後 skill が増えていくなら、早めに以下だけやっておくときれい。

1. `File Size Policy` を `docs/skill-authoring/file_size_policy.md` に移す
2. `Change Policy` の詳細を `docs/skill-authoring/` に移す
3. AGENTS.md には「詳細は docs/skill-authoring を参照」とだけ残す
4. `shared/` の各ポリシーと AGENTS.md の重複を増やさない

今の状態は「悪い」ではなく、**これ以上増える前に分岐点を作っておくと安全**という感じ。
小さなうちに剪定しておくと、あとで文書の森に迷わずに済む。
