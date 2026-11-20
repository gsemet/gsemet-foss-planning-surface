# CR-351 verification (Verifier), round after the rebase

Head: 3d1c337b0efb9e21242e6c401a888afd1b66ede9

Pushed head = committed head: `git rev-parse HEAD` and `git ls-remote origin chantier/batch-06/cr-351-...`
both give `3d1c337b0efb9e21242e6c401a888afd1b66ede9`; `git status --short` empty.

Verdict: **VERIFIED** (Linux widths and verdicts are an explicit UNVERIFIED Known gap, accepted by the owner grant).

## Move: clean rebase d4a0089 -> 3d1c337, patch unchanged (VERIFIED at 3d1c337)

```text
git diff 768570c d4a0089 | git patch-id --verbatim  -> 6c14d3a149d88914d3637899a3786ba22a7d3416
git diff 412ca69 3d1c337 | git patch-id --verbatim  -> 6c14d3a149d88914d3637899a3786ba22a7d3416
git diff --stat 412ca69 3d1c337: test/page/pinnedFont.ts (56 +), test/page/tableBreakout.test.ts (26 +-), 2 files
```

The patch is the same, and its two files are the only ones the proofs exercised. The new base
(412ca69) brought CR-350 CI/gallery changes that these tests do not run. Code claims C1, C2, C6, C7
of the previous verify.md (Head d4a0089) are therefore carried.

- C1 pin helper as specified: carried from d4a0089: identical patch-id. At 3d1c337 `git diff 412ca69 3d1c337` shows `throw new Error(\`the pinned test font did not load: ...\`)` in `pinnedFont.ts`.
- C2 pinned widths `688s 688s 688s 688s 1068W 735W 748W 338s 537s 719W 894W 824W`, no-pin Segoe widths, bad-font failure (`work/verifier/matrix-r2.md`): carried from d4a0089: identical patch-id, same test file and helper.
- C6 case 11 old text stays in the column under the pin, new text breaks out: carried from d4a0089: identical patch-id.
- C7 comments rewritten: carried from d4a0089: identical patch-id.

## Hang observation (carried, and judged against the body) (VERIFIED at 3d1c337)

`grep -n -B3 -A3 "pinTestFonts(page)" test/page/tableBreakout.test.ts` at 3d1c337: line 178
`await pinTestFonts(page);` sits in `openPage` with no `try` and no `browser.close()` before the
`return { browser, page, close }` on line 180. So a throw leaves Chromium open, as the body's
Known gap says (observation `work/verifier/r2-bad-face.log`, carried from d4a0089).

## Long gate at 3d1c337 (VERIFIED)

`work/gates/20261120-090329.log`, first line:
`gate CR-351 branch chantier/batch-06/cr-351-change-specification-layout-tests-that-d head 3d1c337b0efb9e21242e6c401a888afd1b66ede9`;
last lines `ci-static: passed`, `result: pass at 3d1c337b0efb9e21242e6c401a888afd1b66ede9`.
`$CHANTIER log CR-351`: `driver gate result=pass head=3d1c337b... command=just preflight`.
`preflight` runs `ci-static`, which runs `just check` (previous verify.md C3; unit 4059 pass, 0 fail, 15 skipped, as the body says).

## CI at 3d1c337 (VERIFIED)

`gh pr checks 429`: `checks pass`, `report pass`, `static pass`, `static-windows pass`,
`visual pass`; `gallery`, `pages`, `tag-release`, `integration`, `release`, `release-check`,
`stress`, `toc-loop` skipping (PR rule). CI skips the breakout tests (no Chromium; previous verify.md C4), so it proves nothing about the pinned widths; the body says so.

## Linux widths and verdicts: UNVERIFIED (Known gap, accepted)

No Linux run exists (no CI job runs the browser tests, no Linux machine). The Chief of Staff
decided (owner grant, A-24, `$CHANTIER log CR-351` 08:01:50Z) that this stays an explicit
UNVERIFIED Known gap. It is a stated gap, not a claimed fact, so it does not fail the verdict.

## Review box (VERIFIED)

Body: `Review: approved at 3d1c337 (carried from d4a0089)`. `$CHANTIER log CR-351`, 06:49:52Z:
`r2 approved at 768570c0..., committed as d4a00894`, the `carried from` SHA, and the move
is a clean rebase with an identical patch-id.

## PR description at 3d1c337 (VERIFIED)

`gh pr view 429 --json body` against `work/pr-body.md`: `diff --strip-trailing-cr` differs only
by one trailing blank line, so the posted body equals the file.

- Clean: sections render (Summary, Deliverables with a code block and a table, Changes, Impacts, Blast radius, decisions, Known gaps, Test plan, Internal references); no images, so no username or home folder shown.
- Consistent with the diff: Summary, Deliverables and Changes describe the two-file diff (helper new; `openPage` pin; test 1 pin assertion; comments; case 11 text); `test/visual/themes.ts` and `src/` are not in `git diff --stat 412ca69 3d1c337`.
- Widths table equals the matrix (carried C2); case 11 numbers equal C6.
- Linux: Deliverables and Known gaps both mark it UNVERIFIED and no longer say CI passes or will confirm it (the earlier failure is fixed). The Known gaps lists the Linux gap and the hang when a pinned font fails to load (matches the code, above); no "None".
- Test plan SHAs: the changed-tests and Review marks cite 3d1c337 with `carried from d4a0089`, valid after a patch-id-identical rebase; local gates cite 3d1c337 (gate log above); the CI box cites 3d1c337 (checks above) and says the heavy dispatch was at d4a0089 (previous verify.md C5), and that the `static` jobs skip the breakout tests.
- No `STALE` mark; no role name outside Internal references.
- Known gaps vs `before-after.md`: no evidence pair uncaptured (no images involved).
