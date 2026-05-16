# QA Terminology

## Core Terms

| 用語 | 意味 |
|---|---|
| テスト観点 | テスト対象をどのような切り口で確認するかを表す抽象的な観点 |
| テスト条件 | テストすべき状態、入力条件、業務条件、データ条件 |
| シナリオテスト | 業務上意味のある一連の流れとして確認するテスト |
| リスク | 品質、業務、利用、運用に悪影響を与える可能性のある不確実性 |
| 根拠 | 入力文書、前段成果物、ユーザー指定など、判断のもとになる情報 |
| 推測 | 入力から可能性は考えられるが、明記されていない解釈 |
| issue | 不足、曖昧さ、矛盾、証拠不足、判断待ちとして追跡すべき事項 |

## Common IDs

| 対象 | 推奨ID |
|---|---|
| Document | `DOC-001` |
| Extracted fact | `EXT-001` |
| Normalized specification | `SPEC-001` |
| Test design input | `TDI-001` |
| Business flow | `BF-001` |
| Use scene | `US-001` |
| Scenario viewpoint | `SV-001` |
| Scenario candidate | `SC-001` |
| Risk | `R-001` |
| Test case | `TC-001` |
| Issue / question | `Q-001` |
| Viewpoint | `VP-001` |

## Common Status

| 状態 | 意味 |
|---|---|
| `confirmed` | 根拠があり確定扱いできる |
| `to_be_confirmed` | 確認が必要 |
| `missing` | 必要情報が存在しない |
| `contradiction` | 入力間または成果物間に矛盾がある |
| `out_of_scope` | 今回の対象外 |
| `deferred` | 後続工程で扱う |

## Priority Labels

- `P0`: 必須。重大な業務影響や致命的なリスクに関わる。
- `P1`: 高優先。通常のテスト範囲で必ず確認したい。
- `P2`: 中優先。条件付きで確認したい。
- `P3`: 低優先。余力があれば確認する。
