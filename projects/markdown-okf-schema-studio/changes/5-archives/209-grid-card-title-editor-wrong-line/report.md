# Report: CR 209

PR [#236](https://github.com/gsemet/markdown-okf-schema-studio/pull/236), merged by the user 2026-10-31 (merge commit b9118506); closes #229. Normal CI run 41180127608 green; no heavy (render-level change). Opus Inspector APPROVE in round 2.

- Card titles (`{grid-item-card}`, `{card}`) and the `:header:` / `:footer:` options are parsed as inline text (a leading "2." stays literal) and map to their own source line; `:link:` cards keep no mapping.
- Behaviour change: a click on any card title opens the title editor inside the card, on the directive line.
- New SwRS-MDOKFSTUDIO-BLOCK-258 (proposed); MYST-100 updated. 7 render tests (6 fail before the fix); visual checks v25/v26 tightened.
- Screenshots: branch `screenshots/cr209-grid-card-title`. Details: reports/report.md.
- Follow-ups in P3: card-in-blockquote-line-offset, block-258-done-e2e. #226 left to the owner.
