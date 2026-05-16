# extraction_category_decision_policy.md

# 抽出カテゴリ判断ポリシー

## 迷いやすい切り分け

| 迷う組み合わせ | 判断 |
|---|---|
| `business_rule` / `validation` | 業務判断や禁止事項が中心なら `business_rule`。入力値の妥当性確認が中心なら `validation`。 |
| `ui_item` / `validation` | 項目の存在や表示仕様なら `ui_item`。項目値の制約なら `validation`。 |
| `condition_branch` / `business_rule` | 処理切替の条件なら `condition_branch`。業務上の制約なら `business_rule`。 |
| `condition_branch` / `calculation` | 分岐条件が中心なら `condition_branch`。算出式や集計が中心なら `calculation`。 |
| `state_transition` / `business_rule` | 状態の変化や遷移可否なら `state_transition`。状態に基づく業務制約なら `business_rule`。 |
| `permission` / `business_rule` | ロールや認可が中心なら `permission`。業務統制上のルールが中心なら `business_rule`。 |
| `error_handling` / `validation` | 入力拒否なら `validation`。処理失敗後の扱いなら `error_handling`。 |
| `api` / `error_handling` | IF仕様そのものなら `api`。失敗時処理が中心なら `error_handling`。 |
| `batch` / `operation` | システム処理なら `batch`。人の運用手順なら `operation`。 |
| `data` / `calculation` | データ項目や構造なら `data`。算出や集計なら `calculation`。 |

## 簡易フロー

1. 画面・項目・帳票・API・バッチなどの対象物かを確認する。
2. 入力制約、状態、条件分岐、計算、権限、エラーなどの振る舞いかを確認する。
3. 業務ルールか、システム処理か、人の運用かを確認する。
4. 未確定、矛盾、確認事項なら `open_issue` を検討する。
5. 複数カテゴリにまたがる場合は主目的に最も近いカテゴリを選び、関連カテゴリを備考に書く。

## 禁止事項

- 独自カテゴリを増やす
- 一般論でカテゴリを補完する
- 根拠のない関連カテゴリを付ける
- 分類作業のために原文の意味を変える
