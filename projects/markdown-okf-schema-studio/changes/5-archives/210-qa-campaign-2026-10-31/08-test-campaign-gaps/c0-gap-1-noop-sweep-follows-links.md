# c0-gap-1 — noop-sweep.mjs follows links and then reports misleading "not found after re-render" errors

The sweep clicks the centre of each block. On a link-only block (see c0-1) the click navigates the
preview to another document; the remaining targets are then looked up in the wrong document and
reported as `not found after re-render (... the buffer did not change, so the mapping moved)`.
Seen on 15-road-ahead.md (105 cell errors, the glossary became the preview), 06-guidelines-governance.md
(79 block errors), 02-foundations.md `--from 60` (20 errors, preview jumped to chapter 10).
Also: tabs and the preview group are left changed, and `--limit` without `--from` did not bound a
`blocks` run (52 targets tried with `--limit 15`).
**Direction.** After each target check the preview H1/document URI; skip or Cmd-click-safe targets
whose centre is on an `a`; stop and report `NAVIGATED` instead of continuing.
Also observed once more: `vault/wiki/benchmarks/uber-ai-cost-6x-increase.md` block L51 (a wiki-link list
item) is "not found after re-render", reproduced twice, preview unchanged; not diagnosed.
