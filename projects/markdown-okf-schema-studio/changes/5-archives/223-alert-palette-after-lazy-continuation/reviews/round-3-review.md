# Round 3 review: alert palette after a lazy continuation line

Verdict: **APPROVE**

I reviewed the worktree `markdown-okf-schema-studio-wt-223`: uncommitted changes on top of
`origin/main` 0b4ede78. The first round-3 Inspector was cut off before its verdict. Before I
started, I checked that `src/core/render/mystGithubAlerts.ts` and
`src/page/modules/blockEditActions.ts` are the round-3 versions. They import `lazyLineAsText` and
`blockQuoteAround` from `src/core/syntax/blockQuoteRange.ts`, and that file defines
`MYST_BLOCK_BREAK` and `EMPTY_LIST_ITEM`. Nothing was reverted.

I swapped one worktree file once to prove that the new tests fail on the round-2 code, then put it
back. The checksum of `git diff` plus the three untracked files was `90a1de99…` before and after.
I ran `npm run compile` after the restore. My probes and outputs are in
`/private/tmp/claude-502/cr223-driver/inspector3b/`.

## Round-2 findings: status

1. **Blocking, a lazy `+++` crashed `renderMyst`: fixed.**
   - `lazyLineAsText` (`src/core/syntax/blockQuoteRange.ts:54`, `:101-104`) now escapes a leading
     `+++`.
   - These inputs all render and match `gh api markdown -f mode=gfm` (`cmp3b.txt`):
     - `+++`, `+++ {"a": 1}`, and `+++` indented by 2, 3, 4 spaces or a tab;
     - `++++`, `+++x` and `+++ b`;
     - a lazy `+++` right after the head, after a quoted list and after a nested quote;
     - a CRLF document, an alert indented one space, and an alert inside a `:::{grid-item-card}`.
   - The alert body text shows `+++`, never `\+++`.
   - The 3 new `GITHUB_CASES` rows (`test/core/render/alertLazyContinuation.test.ts:104-107`) fail
     on the round-2 `blockQuoteRange.ts` with `TypeError: Cannot read properties of undefined
     (reading 'length')`. That run had 48 tests: 45 passed and 3 failed (`r2run.txt`). All 48 pass
     on round 3.
2. **The GFM-009 wording on MyST-only syntax: fixed.** The boundary scenario
   (`SwRS-MDOKFSTUDIO-GFM-009.md:48-52`) now says that a lazy line never makes a MyST block break.
   It also says that `% c`, `(lbl)=`, `[^1]: n` and `$$` keep their MyST meaning inside the
   admonition, where GitHub shows text. The log entry says the same.
3. **The build snapshot path (`sourceTransforms.ts`): out of scope**, as agreed. It is still a
   follow-up item.
4. **Readability nits: fixed.** `EMPTY_LIST_ITEM` is named and documented (`:51-52`). The second
   HTML start test has its comment (`:134-135`).
5. **One test per row: fixed.** Each `GITHUB_CASES` row is its own `test()` with
   `@tests_req SwRS-MDOKFSTUDIO-GFM-009` (`:110-116`).

## Non-blocking

1. **These `+++` crashes also happen on `origin/main`; this CR does not cause them.**
   - `- +++\n` with no alert at all throws the same `TypeError`.
   - So do `> [!NOTE]\n> a\n- +++\n` (the list item after the alert) and a quoted
     `> [!NOTE]\n> a\n> +++\n`.
   - This is the MyST `+++` inside a container crash that round 2 already noted. It belongs in the
     planned backlog item and does not block this CR.
2. **Known differences from GitHub that this CR did not introduce.** These cases are unchanged
   from `origin/main` and are not regressions:
   - We render alerts in list items and titled alerts (`> [!TIP] T`); GitHub does not.
   - After a blank line, `+++` is a MyST block break.
   - `+ ++` is MyST's own parse.

## Regression hunt

- **Normal alerts with no lazy lines:** I rendered the 21 inputs of round 2's `norm.json` with the
  round-3 build. The HTML is byte-identical to the `origin/main` output
  (`inspector2/norm-orig.txt`, same base commit 0b4ede78), saved as `norm-r3.txt`.
- **The whole diff:** the round-3 changes against round 2 touch only these:
  - the `+++` escape;
  - the named `EMPTY_LIST_ITEM` regex and the added comment;
  - the 3 new test rows and the per-row tests;
  - the GFM-009, PALETTE-115 and log wording.
- **The palette** shares `blockQuoteEnd`, so the caret on a lazy `+++` line is in the alert, as the
  render shows it.
- **Requirements:**
  - GFM-009 and PALETTE-115 stay `proposed`.
  - The index line is regenerated.
  - The `implemented_in_files` and `tested_in_files` lists and the `@implements_req` and
    `@tests_req` markers are present.
  - GFM-037 and the approved requirements are untouched.

## Gate results

- `just check`: exit 0 (`check.txt`).
  - Boundaries (314 modules), limits (905 files) and settings pass.
  - Unit 3377/3377 and security 71/71 pass, and pytest has 153 passed.
  - okfreq reports 1072 requirements, 0 errors and 21 warnings.
  - The `HANG DUMP written` lines come from the CR 173 hang-dump tests, which expect them; round 2
    had them too.
  - No flakes, although another worktree (wt-227) was running its unit tests at the same time.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings. These are the existing broken cross-link warnings,
  such as BLOCK-069, GFM-016 and PALETTE-092.
- Targeted run of the 3 changed or new test files: 73/73 pass.
