# T02 implementation — round 3

STATUS: DONE

## Summary
Round 3 fixes the single MAJOR finding of `reviews/T02-review-r2.md` (finding 1). The first mode
read in `setEditMode` now goes through `withCurrentFrame`, so a detached frame is retried instead of
failing. Nothing else in the function changed. The harness has no other edits this round. Proof (a)
lists every detach-sensitive call site and each one sits in an allowed context. Proof (b) ran the
gate twice, and both runs passed with all five `PASS real-input screenshot` lines. No `src/` file and
no test assertion changed. `previewEditing.test.ts` and the Follow-ups were not touched.

## Files changed
- `test/integration/realInput/harness.ts` — `setEditMode`: the first read at the top of the loop is
  now `const mode = await withCurrentFrame(page, (frame) => frame.locator("html").getAttribute("data-sphinx-preview-edit-mode"));`
  followed by `if (mode === wanted) return currentPreviewFrame(page);`. The rest of the function is
  unchanged.

## Files changed (earlier rounds, kept)
- `test/integration/realInput/harness.ts` (rounds 1–2), `test/integration/realInput.test.ts` (new),
  `test/integration/trusted-suite.ts` and `test/integration/review-index.ts` (registration).

## Tests written first (failing before the fix)
- None this round. The review asks for a robustness fix to the harness, not a new bug test. The
  detach error that round 2 saw in this read is recorded in `logs/T02-proof-s5-trusted.log:307`.

## Tests added or changed
- None.

## Existing assertions changed
- None.

## Verification
- Proof (a): `grep -nE "getAttribute|\.click\(|inputValue|evaluate"` over `harness.ts` and
  `realInput.test.ts`. Every hit is in an allowed context:
  - `harness.ts:116-118` `findCurrentFrame`: the document id, version and request id reads.
  - `harness.ts:154` `focusedCaret`: `frame.evaluate`. Its only caller is `realInput.test.ts:51`,
    inside the `waitFor` predicate of `waitForCaretAtEnd`.
  - `harness.ts:212` `setEditMode`: the mode read, now inside `withCurrentFrame`.
  - `harness.ts:215` `setEditMode`: the toggle click, inside `withCurrentFrame`.
  - `harness.ts:220` `setEditMode`: the mode read in the `waitFor` predicate.
  - `harness.ts:270`, `275`, `283` `createEvidence` / `capture`: called only through
    `captureAfter` (`realInput.test.ts:87`), which wraps it in `withCurrentFrame`.
  - `realInput.test.ts:95`, `99`, `126`, `150`, `174`, `203`: the clicks, inside `withCurrentFrame`.
  - `realInput.test.ts:112`, `161`: reads in `waitFor` predicates.
  - Not listed by the grep: `setEditMode`'s final `return currentPreviewFrame(page)` and the
    `findCurrentFrame` call inside the `waitFor` predicate. Neither reads a DOM attribute.
- Proof (b): `scripts/gate.sh T02-impl unit trusted` run twice, both PASS.
  - Run 1: compile, unit, trusted-build and trusted all PASS. Logs `logs/T02-r3-unit.log` and
    `logs/T02-r3a-trusted.log` (copies, taken before run 2 overwrote the `T02-impl-*` names).
  - Run 2: compile, unit, trusted-build and trusted all PASS. Logs `logs/T02-impl-unit.log` and
    `logs/T02-impl-trusted.log`. Unit: `tests 355` (the same count as T01 and round 2). Trusted:
    `PASS real-input screenshot` for `01-paragraph-blur-commit`, `02-ctrl-enter-commit`,
    `03-arrow-navigation`, `04-table-cell-enter` and `05-open-with-editor`.
- `git status` after the runs: only `test/integration/realInput.test.ts` and `realInput/harness.ts`
  (plus the registration files from earlier rounds) are changed. One `git status` taken after the
  second run listed an untracked `realInput/frontmatter-e2e-yNnrMy/` folder. A later `ls` of
  `realInput/` showed only `harness.ts`. I did not find the cause. `previewEditing.test.ts:210` makes
  `frontmatter-e2e-*` folders under `.artifacts`, and `run-tests.ts:106` cleans them, so this may be a
  transient folder from that test. It is not in the working tree now.

## Evidence for reviewers
- Logs: `logs/T02-r3-unit.log`, `logs/T02-r3a-trusted.log`, `logs/T02-impl-unit.log`,
  `logs/T02-impl-trusted.log`.
- Screenshot folder of the second run: `.artifacts/real-input-*` (latest `REAL-INPUT-LATEST.md`).

## Feedback addressed (rounds 2–3)
- Finding 1 (MAJOR, `setEditMode` first read not detach-tolerant): fixed as the review specifies.
  The first read goes through `withCurrentFrame`, so a detached frame is retried. The round-2 report
  said this read already used `withCurrentFrame`. That was wrong: the code did not do it until this
  round. The round-2 sentence in the report is now true.
- Proof (c): this report describes the code as it is now. `setEditMode` clicks up to three times.
  Each click goes through `withCurrentFrame`, and each wait for the mode is a `waitFor` predicate
  that reads through `findCurrentFrame`. The first mode read goes through `withCurrentFrame`.

## Open points / STOP reason
- Nothing blocking. The F1 and F2 follow-ups (`previewEditing.test.ts` theme loops, and the
  `realinput-*` fixture gitignore) are not addressed here, as the task asks.
- The gate ran twice with no failure. I did not run `trusted` a third time, so the stability
  evidence for this revision is two green runs.
