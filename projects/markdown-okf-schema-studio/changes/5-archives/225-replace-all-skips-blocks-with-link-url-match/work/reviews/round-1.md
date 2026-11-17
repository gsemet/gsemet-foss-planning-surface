# Review round 1 — CR 225 (Replace all skips blocks with a link URL match)

Verdict: CHANGES REQUESTED

Reviewed: the uncommitted change in `markdown-okf-schema-studio-wt-225` on top of origin/main 0b4ede78
(src, tests, requirements), against the owner-approved behaviour note (choices A–D).
`just unit`: 3330 pass, 0 fail. Visual, integration and real-window tests not run (per brief).

## What holds

- The dry run never edits: `handleFindReplace` returns before `this.apply` when `dryRun === true`;
  read-only and open-edit refusals still come first (covered by the new session test).
- The real replace path is unchanged: without `dryRun`, a refused plan still answers
  `FIND_REPLACE_NOTHING`, the edits are applied as before.
- Correlation: the dry run goes through `hostRequests.ask` with its own `editId`, so its answer
  cannot settle the real replace's callback. It does not set `busy`, and the timer drops itself
  while a replace is in flight.
- Staleness: `search`, option toggles, refresh, row close and bar close all bump the generation
  and reset `hostSkipped`; stale and refused answers are ignored. The sum is right: the page sends
  only mapped matches, so page-unmapped + host-skipped does not double count; the "refused" dry
  run answers `skipped = items.length` (all mapped items). The real replace note does not add
  `hostSkipped`.
- The changed assertion in `test/core/edits/findReplace.test.ts` keeps its intent ("a match that
  does not map one-to-one is skipped and counted"): `The Studio` against `The **Studio**` has no
  source occurrence, so it is skipped.
- New tests fail on the previous code (checked by reasoning): the link-target test would plan 3
  of 4 (source count 3 vs 2 for line 5-6); the findBar tests expect a dry-run request that HEAD
  never sends; the validator test rejects `dryRun: "true"` that HEAD accepted; the session dry-run
  test asserts `applied` is empty where HEAD applies.
- Hidden-span edge cases checked with the built planner (scratch script): escaped `\[a](x)` stays
  visible, a link spanning lines and a title spanning lines are hidden correctly, `- [ ] (x)` is not
  a link, nested image-in-link works, a fenced block is treated as one code span by the scanner
  (links inside fences stay counted), unknown constructs (HTML `<a href>`) still skip.
- Requirements: TOOLBAR-012 and StRS TOOLBAR-003 are `draft`, new TOOLBAR-131 is `proposed`; no
  approved requirement edited. Markers present at code and tests. Log entry present.
- File sizes: findBar.ts 668, findReplace.ts 186, sourceEdits.ts 507 (< 800).

## Findings

1. **blocker** — `test/integration/findInPreview.test.ts:308-316`. The real-window scenario
   (also run by the `stress` CI job as `find-in-preview`) uses a SOURCE with
   `[studio link](https://example.com/studio)` (line 56) and expects Replace all to change only
   "and the studio keeps" and "the studio table cell"; its comment says "math, link target and the
   like are skipped". With this change the link label is now replaced
   (`[atelier link](https://example.com/studio)`), so `assert.equal(notes.getText(), replaced)`
   fails. Fix: add `.replace("[studio link]", "[atelier link]")` to `replaced`, update the comment
   (math is still skipped, so the note assertion `cannot be replaced from the preview` still
   holds), and say in the commit/PR why the assertion changed (constitution §3). Consider also
   asserting the target URL is kept.

2. **minor** — `src/core/edits/findReplace.ts:85` and `:95-98`. `REFERENCE_DEFINITION` is applied
   to the whole block text without regard to code: a `[label]: dest` line inside a fenced or
   indented code block is visible on the page but hidden by the planner. Usually this turns a
   previously replaceable match into a skip (regression for Markdown examples in code blocks, e.g.
   searching `https` in a fenced `[ref]: https://...` line), but combined with a fence info string
   equal to the query it produces a WRONG edit. Reproduced: source
   "```foo\n[x]: foo\n```\n", item (1-3, "foo", occurrence 0 of 1) — the page shows one `foo`; the
   planner hides the visible one and replaces the info string, giving "```PIN\n[x]: foo\n```".
   (Before the change: 2 source occurrences vs 1 → skipped, safe.) Fix: collect the code ranges the
   scanner already detects (backtick runs, which cover fences) and drop reference-definition spans
   that overlap them; also do not treat a line indented by 4+ spaces (outside a list/quote) as a
   definition, or at least restrict the prefix to `[ ]{0,3}` after the `>` markers. Add a test with
   a fenced `[x]: needle` line.

3. **minor** — `test/visual/capture_find_checks.py:57-70`. The check reads `sent[0]` of all
   `previewFindReplace` messages as the Replace all request. The toggle click now schedules a dry
   run 150 ms later; if the Playwright steps between the toggle click and the Replace all click take
   longer than that, the dry run is sent first (with `replacement: ""` when it fires before the
   input event), and the "replace request is malformed" check fails. Timing-dependent, unlikely
   locally, possible on a slow CI runner. Fix: filter `item.type === 'previewFindReplace' &&
   !item.dryRun` when reading `sent`.

4. **minor** — `src/page/modules/findBar.ts:575-578` (replace input handler). When the replacement
   is longer than `MAX_FIND_REPLACEMENT`, `scheduleDryRun` sends nothing; shortening the replacement
   does not reschedule, so the note keeps the page's count until the next search. Fix (optional):
   call `scheduleDryRun()` from the replace input handler only when the previous dry run was dropped
   for the length reason, or ignore the replacement length for the dry run (counts do not depend on
   the replacement; truncate it or send `""`). The latter also makes the request smaller.

5. **nit (no action required)** — `src/core/edits/findReplace.ts:117-125`. The opener stack does not
   follow CommonMark's "no link inside a link" rule: in `[a [b](c) d](e)` the outer `(e)` is shown
   as text but hidden by the planner. Result is a skip (count mismatch), never a wrong edit on its
   own; acceptable as a heuristic, maybe worth a one-line comment.
