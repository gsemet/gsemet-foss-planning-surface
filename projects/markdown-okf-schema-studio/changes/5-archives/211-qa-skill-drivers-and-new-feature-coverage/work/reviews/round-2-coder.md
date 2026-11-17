Coder round 2: fixed Inspector r1 findings 1-11 and implemented item 6.
noop-sweep: in-page PICK_POINT (elementFromPoint closest a[href]); all points on links -> skipped; doc id via
html[data-sphinx-preview-document-id] (src/page/runtime.ts:93) compared 500 ms after click; back via
[data-sphinx-preview-back], poll 5 s, setEditMode(ctx,true). admon.md added. new-features: min(rev date, Date)-1 day,
warn at 200. coverage-map: Revision: line only when present. charters: NEWFEATURE line, replay window counted,
no-subagent fallback. use-cases E3/E4 repointed. setup-workspace vault rsync order fixed.
Item 6: bug-sheet-template Currently/Expected block + rules (q shot NAME --clip preview), reference-style image
placeholders; SKILL.md limit 2 JPEGs + triage copy; charters FINDING lines carry currently/expected paths.
Dry runs: coverage-map --campaign 210 -> Baseline b9118506; new-features --campaign 210 -> 1 row #228 (false
positive: #228 is in b9118506 as 6a2cb9d8, rebase-merged; its mergeCommit 9e551bff is not in the local clone).
