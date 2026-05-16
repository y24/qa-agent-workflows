# Ambiguity And Issue Log Policy

## Purpose

曖昧さ、矛盾、証拠不足、未解決の前提を隠さず扱うための共通方針を定義する。

## Record Issues When

- 入力文書間、または前段成果物との間で記述が矛盾している。
- 必須情報、前提条件、期待結果、データ条件が不足している。
- 用語の意味、スコープ、優先度、状態が不明確である。
- 複数の解釈が成立し、どれを採用すべきか判断できない。
- 根拠が弱く、成果物へ確定情報として入れるにはレビューが必要である。
- 対象外、保留、未カバー、残存リスクとして明示すべき事項がある。

## Issue Categories

| Category | Meaning |
|---|---|
| `missing` | 必要情報が不足している |
| `ambiguity` | 複数解釈または曖昧な記述がある |
| `conflict` | 入力間または成果物間に矛盾がある |
| `weak_evidence` | 根拠が弱い、または間接的である |
| `scope` | 対象範囲、対象外、保留に関する論点 |
| `traceability` | IDや根拠の対応関係が切れている |
| `decision_needed` | ユーザーまたは関係者の判断が必要 |

## Issue Fields

issue log には、必要に応じて以下を含める。

- Issue ID
- Category
- Status
- Related ID
- Source
- Description
- Impact
- Priority
- Proposed handling
- Owner or reviewer

## Handling Rules

- issue を消して成果物を整えない。解決済みまたは対象外にした場合も判断理由を残す。
- 未確認事項を仕様として補完しない。
- 矛盾は独自判断で片方を採用せず、採用根拠がない限り `conflict` として扱う。
- 低確信度の推測は、主成果物ではなく確認事項、前提、または issue log に分離する。
