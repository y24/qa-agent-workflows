# Evidence And Confidence Policy

## Evidence Types

- `direct`: 入力資料または前段成果物に明記されている。
- `derived`: 明記された情報から自然に導ける。
- `inferred`: 推測を含む。必ず `推測` として示す。
- `unknown`: 判断に必要な情報がない。

## Confidence Labels

- `high`: 直接根拠があり、解釈の余地が小さい。
- `medium`: 根拠はあるが、前提や解釈が一部含まれる。
- `low`: 根拠が弱い、または複数解釈があり得る。

## Handling Rules

- `inferred` と `low` の成果物は、レビュー対象または確認事項に含める。
- `unknown` を仕様として補完しない。
- 複数資料が矛盾する場合は、片方を採用せず、矛盾として記録する。
