# normalization_rules.md

# 正規化・統合ルール

## 目的

Raw抽出情報を、後続Stepで扱いやすい正規化仕様へ整理する。

## 基本方針

- 同一仕様、関連仕様、別仕様を区別する。
- 表記揺れや用語違いは候補として整理し、根拠なしに同義確定しない。
- 矛盾、不足、粒度不足、未確定、根拠弱を消さずに状態として残す。
- 正規化後も Raw ID と参照元を維持する。

## 正規化項目

| 項目 | 内容 |
|---|---|
| Spec ID | 正規化仕様ID |
| カテゴリ | 標準カテゴリ |
| 仕様内容 | 統合後の仕様要約 |
| 状態 | confirmed / ambiguous / conflicting / missing_detail / tentative / out_of_scope |
| 確度 | 高 / 中 / 低 |
| 参照Raw ID | 根拠となるRaw ID |
| 参照元 | Doc ID、章、節、項目 |

## 詳細参照

- 統合・分割・表記揺れ・矛盾の判断: `normalization_policy.md`
- 根拠と確度: `evidence_and_confidence_rules.md`
- 推測禁止: `anti_hallucination_rules.md`
