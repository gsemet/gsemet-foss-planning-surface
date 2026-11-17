# CR 208, round 1, Inspector review

Worktree: `markdown-okf-schema-studio-wt-208`, uncommitted diff against `origin/main`
(5 files: `src/session/features/comments.ts`, the new tests in
`test/session/reviewReqComments.requirements.test.ts`, REVIEW-012, the index and `tiers/log.md`).

Verdict: **NOT PROVEN.** The change itself is correct and safe hardening. But the round's main
claim, that a swallowed non-ENOENT read error caused the dumped failure, is not the likely cause.
The evidence points to an ENOENT window that main already closed.

## 1. Root cause: a more likely path exists, and main has already fixed it

The dump that shows the cause is `/private/tmp/claude-502/top-heavy2-stress.log`, line 3244
(heavy 40811480230). The `reports/stress-b71fac7c.log` in this folder predates the diagnostics
and has no "re-apply" trace. The dump shows:

- Resolve was clicked at 2589 ms, and the page traced `re-apply without threads` at 2602 ms
  (13 ms later).
- A reply was saved just before: mousedown at 2307 ms, and the sidecar ends with `comments: 2`.
- Host `commentPosts` went from 2 to 4, and the last post holds the resolved thread. No reload,
  no content patch.

In `apply()` (`src/page/modules/commentThreads.ts:486`) this trace fires only when the page gets
an empty `threads` list. The page's parser does not reduce valid threads to zero, so the host
posted `[]` and then posted the resolved thread.

On the code that ran (the run started at 03:20Z on 2026-10-29), `rename(..., {overwrite:true})` in
`src/host-vscode/vscodeHost.ts` went through `vscode.workspace.fs.rename`. VS Code's file service
deletes the target before it moves the file. So during every comment write the sidecar briefly
did not exist. The likely sequence:

1. The watcher event of the reply write, debounced by 150 ms, lands around 2450–2600 ms.
2. That post runs `stat` inside the delete-then-move window of the Resolve write and gets
   ENOENT. `readSidecar` returns `undefined`, and because `shown` is true the host posts `[]`.
   The page closes the popover. This is post 3.
3. `writeComment`'s own post after the rename posts the resolved thread. This is post 4.
4. The watcher events of the Resolve write hit the hash and serialized skip, so they post
   nothing.

That sequence matches exactly two posts, with the empty one first. Commit **5f0f3be0** ("fix(review):
replacing the comments file no longer deletes it first", authored at 03:41Z, one minute after
this failure at 03:40:47Z) closed the window. It is on `origin/main`, with
`test/host-vscode/fileRename.test.ts`.

**The round's fix does not cover this path.** The error is ENOENT, so `isFileNotFound` is true
and the new code still posts `[]`. The EBUSY theory has no evidence in the dump. On Linux CI, a
plain `stat`/`readFile` of a regular file does not return EBUSY. The theory is plausible on
Windows (EPERM/EBUSY during a replace) or with VS Code `Unavailable`, which makes it useful
hardening, not the cause.

On #202: I agree with the Coder that it did not widen the race. #202 only moved where `textHash`
is recorded. The empty list comes from the read result, not from the hash logic.

## 2. Tests

- I compiled and ran `out/test/session/reviewReqComments.requirements.test.js`: 15/15 pass.
- To check the unchanged code, I copied `out/` to a scratch folder and patched the compiled
  `comments.js` back to the old behaviour (`catch` returns `undefined`, no UNREADABLE return).
  "a read of the comments file that fails after a Resolve…" then fails with
  `AssertionError: no post lists zero threads`. The other 14 pass, including the deletion test.
  The test does fail before the fix.
- It is a real host-level replay: `handleResolve` posts the resolved thread, then two posts
  follow, the first with a failed read. The assertion is not weakened: no post may list zero
  threads, and the last post is still `t1` resolved.
- It is a host-side proxy, not a page-level check that the popover stays open. It relies on
  `apply()` closing the popover only on an empty list. I accept that, but say so.
- It injects EBUSY, which is not what the dump shows. A replay of the dumped failure would
  inject ENOENT from `stat` during the Resolve write. The fix does not handle that case, and
  main already prevents it at the rename level.

## 3. Fix correctness and regressions

- Real deletion still clears the threads: ENOENT gives `undefined`, which posts `[]`. The new
  test covers it and passes.
- The UNREADABLE return happens before `textHash` and `posted` are recorded, so the next good
  read is not skipped. Correct.
- Minor behaviour change: a file that stays unreadable (EACCES, or the sidecar path is a
  directory, EISDIR) used to clear the threads. Now the page keeps the stale threads until a
  later read succeeds. The new refusal scenario covers this ("denied"), so it is acceptable.
- No retry is scheduled after a failed read. "the next successful read is posted as usual"
  therefore depends on a later watcher event or render. Example: after a page reload,
  `posted` is reset; if that read fails, the page shows no threads until something else
  triggers a post. Old and new code behave the same here, so this is not a regression.
  Optional: one bounded retry.

## 4. SwRS

- REVIEW-012 is SwRS, `req_lifecycle: proposed`, with no `approved_by`. The guideline says
  "proposed: implemented, in force, not frozen. Change it with the code". Adding a refusal
  scenario to the same behaviour follows "one SwRS = one observable behaviour with all its
  scenarios". Editing it instead of creating a new requirement is acceptable. No locked StRS
  was touched.
- The index line was updated to match the description. `just requirements-lint` passes:
  0 index, projection or coverage changes, and only the existing PALETTE-264 W2 warnings.
- `tiers/log.md` overclaims: "Before, any read error counted as 'no comments file' and closed
  the popover of a just-resolved thread" reads as the proven cause of the flake. It is not.

## 5. Markers

- `@tests_req SwRS-MDOKFSTUDIO-REVIEW-012` is beside each new test.
- `readSidecar` keeps `@implements_req REVIEW-004` (size stub), and `post()` keeps
  `@implements_req REVIEW-012`. Markers conform.

## Required changes

1. **Correct the root-cause claim** in the round report, the PR body and `tiers/log.md`.
   - The dumped failure (40811480230) matches the ENOENT window of VS Code's delete-then-move
     rename, which 5f0f3be0 fixed on main after that run.
   - This CR's change is hardening for read failures other than a missing file; it would not
     have prevented the dumped failure.
   - Reword the log line to say a failed read *could* close the popover; do not state it as
     the cause.
2. **Answer the CR's open questions with this analysis:**
   - #202 did not widen the race.
   - The likely cause is fixed by 5f0f3be0.
   - Proof that the flake is gone has to come from heavy `stress` runs on main after 5f0f3be0
     (Foreman/driver: list the heavy runs since 5f0f3be0 and whether `review-threads` failed).
     Without that, the CR stays "cause likely fixed elsewhere, not proven".
3. **Optional, recommended:** add a host-level test that injects ENOENT on `stat` of the sidecar
   while the Resolve write runs, documenting why the single-step replace matters. It should
   fail if the replace went back to delete-then-move. If that is not practical in the session
   fake, cite `test/host-vscode/fileRename.test.ts` as the guard in REVIEW-012 verification
   instead.
4. **Optional:** the test name and log could mention "busy/denied" rather than suggesting this is
   the Resolve flake.

No code change is required to the comments.ts hunk itself; it is correct.
