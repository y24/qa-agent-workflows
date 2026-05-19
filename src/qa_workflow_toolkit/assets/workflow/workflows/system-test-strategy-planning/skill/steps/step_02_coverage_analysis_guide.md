# Step 2: システムテストで扱うべきカバレッジ候補の抽出

## 目的

Step 1の入力スコープをもとに、システムテストで確認すべき対象、品質特性、非機能カバレッジ候補を抽出する。

## 入力

- `01_input_scope_summary.md`
- 元文書の根拠確認に必要な範囲
- `references/iso25010_quality_characteristics.md`
- `templates/system_test_coverage_analysis_template.md`

## 手順

1. 入力文書上の要求、制約、利用条件、運用条件、外部IF、品質要求を `SF-001` 形式の Source Fact として整理する。
2. Source Fact から、システムテストで扱うべき Coverage を `CV-001` 形式で抽出する。
3. 各 Coverage に主品質特性と副品質特性を対応づける。
4. 非機能カバレッジは、根拠があるものだけを候補にする。
5. 条件不足、根拠不足、対象外を分けて記録する。

## 判断基準

- 明示要求がある場合は、Coverage にできる。
- 要求ではないが制約や利用条件が明記されている場合は、Coverage 候補にできる。
- 入力から必要性を説明できない場合は、Coverage にしない。

## 禁止事項

- ISO/IEC 25010の全特性を埋めるために観点を作らない。
- 性能、セキュリティ、信頼性などの一般論を根拠にしない。
- 目標値や閾値を仮置きしない。

## 出力

`02_system_test_coverage_analysis.md`

## 完了条件

- Coverage IDごとに根拠 Source Fact が追跡できる。
- 非機能カバレッジの対象と未確定事項が明確である。
- 次Stepでテスト種別を選定できる粒度になっている。
