# テスト設計 総合入口 Orchestrator

## Step 0: 共通方針の確認

作業開始前に、`SKILL.md` に列挙されたshared policyを確認する。
読めないファイルがある場合は、推測で進めず、不足ファイルとしてユーザーに報告する。

## Step 1: 入力と目的の棚卸し

- 入力文書、既存成果物、ユーザー依頼を整理する。
- 事実、推測、未確認事項を分ける。
- 依頼が不明確な場合は、進め方の選択肢と確認事項を提示する。

## Step 2: 使用skillの選択

`SKILL.md` の skill選択表に従い、使用する個別skillを選ぶ。
複数skillが必要な場合は、実行順序と各Stepの停止位置を提示する。

## Step 3: 個別skillへの移行

選択した `.agents/skills/<workflow>/SKILL.md` と `orchestrator.md` に従う。
ユーザーが明示的に継続を指示しない限り、次の主要Stepへ進まない。
