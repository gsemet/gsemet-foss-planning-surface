# CR-464 diagnosis: diff-preview-scroll D1 times out on main

Status: failure point and shape PROVEN from logs; the exact mechanism is NOT proven (three
candidates, one ranked first). No local repro: the worktree has no `node_modules`, and the real-window
suite needs `just dev` plus a full integration run. A diagnostics-first heavy run is the proof step
(see "Proof plan"). Nothing was guessed into a fix: the fix below is valid whichever candidate holds.

## Reproduction

- CI only so far: `gh workflow run ci.yml --ref <branch> -f heavy=true` (job `integration`, xvfb
  2600x1440, VS Code 1.147.0 `286f582d`), or locally `npm run test:integration` (one real window).
- Not reproducible from `just check` / simulated tests: D1 only exists in the real window.

## Evidence (runs)

Logs saved under `work/scratch/` (run1.log = 44957381296, run2.log = 44958907144,
run3-attempt1.log = 44951690958 attempt 1); artifacts under `work/scratch/artifacts-<run id>/int/`.

| run | code | diff-preview-scroll | note |
|---|---|---|---|
| 44949474643 (CR-460 heavy, 42d01082) | earlier CR-460 tree | done, 4899 ms | green |
| 44951690958 attempt 1 (39f2419d) | = main tree | not reached | red elsewhere: `TIMEOUT: locator.count did not return within 10000 ms` (unrelated flake, a different step) |
| 44951690958 attempt 2 (39f2419d) | = main tree | done, 5059 ms | green on re-run |
| 44957381296 (push main 58b4c302) | main | FAILED, 21535 ms | "Timed out waiting for the inline diff's editor to scroll." |
| 44958907144 (heavy of PR #474, CR-463) | main + CR-463 | FAILED, 21602 ms | same message |

What the logs prove:
1. The failing wait is `scrollEditorTo(real, 100, "the inline diff's editor to scroll")`, D1, line 69 of
   the test (stack: `scrollEditorTo` <- `withLayout` <- `run`). It is the editor's OWN visible range
   that never reached line 95; the preview-follow wait (line 70) is never reached.
2. 21.5 s = about 1.5 s of setup + the 20 s budget of that wait. So everything before it passed
   quickly and deterministically in both failures: side preview of a.md ready, the diff is the active
   tab, an editor of `a.md` with scheme `file` exists in `visibleTextEditors`. A healthy step
   (D1 + both D2 layouts) takes about 5 s in total.
3. Same VS Code build, same code (39f2419d is the main tree): green once, red twice. So it is a
   race (bimodal), not a deterministic regression, and not a CR-463 effect. The preceding step
   (`diff-preview`, 8.4 and 9.1 s vs 9.1 and 9.5 s in green) shows no difference.
4. No hang dump exists for this failure (only `post-step/ps.txt`): the failure is a plain
   `waitFor` timeout inside the step budget, so no window state, tab list, editor list or
   preview state was recorded. This is the diagnostics gap (ci.guidelines.md rule 12).

What the logs do NOT prove: whether `real` was a live editor of the inline diff, and what the
editor's visible range, or the host's scroll sync, did during the 20 s.

## Candidate causes (code paths that produce "editor never reaches line 95")

D1 differs from the neighbouring green T1 (`diffPreview.test.ts`, inline layout, same
sequence) in exactly one way: T1 scrolls with the `cursorBottom` COMMAND, which acts on the
live active editor; D1 scrolls with `editor.revealRange` on a `TextEditor` OBJECT it picked once from
`visibleTextEditors` (`diffPreviewScroll.test.ts` lines 65-69), with no check that it is the diff's
editor, and without awaiting or observing the reveal (`revealRange` returns void).

- C1 (ranked first): a stale or wrong editor object. Before `openDiff` the group holds the plain
  editor E0 of `a.md` (same `file:` URI as the diff's modified side). `openDiff` returns once the
  diff is the active tab and `activeTextEditor !== undefined`; both are satisfied by E0 while the
  tab model (`onDidChangeTabs`) and the editors delta (`onDidChangeVisibleTextEditors`) are two
  separate ext-host channels. The next wait ("an editor of a.md, scheme file") is satisfied by E0
  too. `revealRange` on an editor the main thread has already disposed rejects
  (`TextEditor(id) not found`) as an unobserved promise, E0's `visibleRanges` stays frozen, and the
  wait times out at 20 s with nothing in the log. Consistent with: instant pass or full timeout,
  nothing in between; green runs are the ones where the delta won the race. Not proven (no editor
  identity logged).
- C2: the host scrolls the editor back. `revealFromPage` -> `revealEditorLine`
  (`src/session/features/scrollSync.ts`) turns any `previewScroll` the page reports into
  `editor.revealLine` on the real file's visible editor. Opening the diff makes the host re-point the
  preview (`followActiveDiff` -> `onActiveDocumentChanged`); a page scroll report of line ~1 landing
  after the test's reveal would put the editor back at the top. Less likely: the test's wait polls
  every 25 ms and would usually catch the transient scroll, and T1 has the same exposure and passes.
- C3: `revealRange` sent to the inline diff's modified editor before its layout/diff computation
  gave it a viewport: ignored, no later event. Also compatible, also unprovable from the log.

No candidate points to a product bug of the inline layout (the host code only reads
`visibleRanges`; T1 inline scrolls and follows). C2 would be a product-side race in scroll sync;
it is the only candidate that would need a product fix, and the diagnostics below will show it.

## Fix (proposal, root-cause independent, no sleep, no retry, no raised timeout)

In `test/integration/diffPreviewScroll.test.ts` (and, since D2 has the same shape, its
`editorsOfScheme(SCHEME)` loop):

1. Deterministic readiness signal for the editor identity. Capture
   `const before = new Set(vscode.window.visibleTextEditors)` before `openDiff`; after it, wait for
   an editor of `a.md` (scheme `file`) that is NOT in `before` and is in the active group's
   diff tab (`tabGroups` active tab is the `TabInputTextDiff`). That is the live diff editor; E0
   can no longer be chosen (kills C1, and is harmless if C1 is not the cause).
2. Scroll with an awaited, observable call: the built-in `revealLine` command
   (`{ lineNumber: 100, at: "top" }`: a scroll with no cursor move, acts on the active editor and
   returns a thenable, so a rejection fails the test with its own error) instead of the fire-and-
   forget `revealRange`, after asserting the active editor is the picked one.
   If a TextEditor is kept, `await` nothing is possible, so the command is the way.
3. Diagnostics in the failure message of `scrollEditorTo` and of the follow wait (rule 12): at
   timeout, throw with: every visible editor (scheme, fsPath, viewColumn, `visibleRanges`,
   whether it is the picked one, whether it existed before the diff), the active editor, the tab
   groups (input kind, active), the layout setting, and the preview's
   `lastSourceScrollLine`/`lastRevealedSourceLine`/phase. A failure then names C1 (the picked editor
   is not in visibleTextEditors or pre-existed), C2 (range moved then returned: also record the
   max `firstVisibleLine` seen during the wait) or C3 (range never moved, editor live).
4. Only if the diagnostics show C2: product fix in `scrollSync.ts` (a previewScroll report that is
   not an echo of the host's own sync, or that comes before the page has scrolled on user input,
   must not move the editor), with a unit test in `test/host`, an SwRS touch (LIFE-100/108) and
   `just requirements-update`.
5. No skip: D1 stays a required step.

## Proof plan

1. Land the diagnostics + identity fix (steps 1-3) on the CR branch; `just check` and
   `just preflight` as far as Windows allows.
2. Make D1/D2 a stress scenario: `diff-preview-scroll` is not in `STRESS_SCENARIOS_BY_HOST`
   (`test/shared/stressPlan.ts`; the list is the key list of the real-input suite's stress table in
   `test/integration/realInput/run.ts`, checked at start, with the budget guards of
   `test/build/hangWatchdog.test.ts` and `test/build/stressPlan.test.ts`). Add it there with a comment
   citing runs 44957381296 and 44958907144, so the fix is proven by repetition rather than by one
   green run.
3. Heavy CI: `gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=60
   -f stress_scenarios=diff-preview-scroll` (about 2 scenario runs per round: well under the 220
   limit) plus at least three consecutive green normal heavy runs. If any round fails, the new
   failure message decides between C1, C2, C3; a theory the failure contradicts is dropped.
4. Separate note for the Driver: run 44951690958 attempt 1 failed at a different step
   (`locator.count` 10 s timeout in a frame call). It is a second flake, outside CR-464's scope;
   file it if it reappears.
