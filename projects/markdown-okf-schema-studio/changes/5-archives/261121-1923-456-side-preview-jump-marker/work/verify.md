# Verify CR-456 (show the target-line arrow in the side preview on a jump)

Head: 7517dfd17699de1c122287a97082b04e756fed14

Verdict: VERIFIED (the declared and the added gaps below are marked UNVERIFIED; none failed).

Gate pass: `work/gates/20261121-193415.log`, first line `gate CR-456 branch chantier/batch-07/cr-456-show-the-target-line-arrow-in-the-side-p head 7517dfd17699de1c122287a97082b04e756fed14`, last line `result: pass at 7517dfd17699de1c122287a97082b04e756fed14` (`just preflight`, static stage on Windows).

All commands ran in the worktree at 7517dfd (`git status --short` clean, `git rev-parse HEAD` is the head above).

## Claims (each judged at 7517dfd)

1. Jump signal rules (spec 4.1 table, 6.2): `test/core/navigation/jumpSignal.test.ts` passes: a command change with one selection in an eligible `.md` is a jump at the 1-based line; keyboard, mouse and no-kind never; several selections, an expected Studio selection and a non-Markdown target never; a diff side jumps to the real file on either side.
   Command: `npm run compile`, then `node scripts/node-test.mjs unit "out/test/{core/navigation/jumpSignal,core/protocol/hostToPage,host/editorJumps,host/studioSelections,host/openAtLine,page/runtimeLineMarker,session/toolbarReq.requirements,session/diagReq.plantuml.requirements,site/e2eGroups}.test.js"`.
   Output (`work/verifier/unit-focused.log`): `tests 113, pass 112, fail 0, skipped 1` (the skip is the Windows symlink test). Lines 1-4 are the four jumpSignal tests, all passing.
2. Protocol: `previewRevealLine` accepts `scroll` absent, `"reading-line"` and `"if-off-screen"` and refuses another value; `previewLineMarkerClear` is accepted with the render envelope only. Same log, lines 8-10 pass.
3. Host `StudioSelections` and `editorJumps`: an expected selection is taken once by URI and line and expires after the window; only a command change with one selection is a jump; a diff side maps to the real file; the activation sends a jump to the following side preview only and "Open as Text" sends none; `openAtLine.test.ts` still passes. Same log, lines 14-18 and 30-31 pass.
4. Page: `reveal(line, "if-off-screen")` draws and leaves the page where it is when the line is on screen, scrolls to the reading line when off screen; absent scroll behaves as before; a folded section unfolds; `previewLineMarkerClear` removes the marker; the CR-445 marker tests are unchanged. Same log, lines 32-54 pass.
5. Session (memory host): a jump is posted to the following side preview only, never to a Studio tab; a jump before the switch waits for the page of that document; the switch drops another document's pending line and the old marker; anchor on asks `if-off-screen` and keeps the anchor, off takes it; a text-editor edit of the marked document clears once, a page-applied edit or a scroll does not, another document's edit keeps it; links and Back/Next in the following side preview request the target line, from a Studio tab or inside the same document they do not; a path link to the same file with a fragment marks, a plain anchor does not; a line past 5 s is dropped and a hidden page waits for its ready. Same log, lines 94-109 pass (`test/session/toolbarReq.requirements.test.ts`).
6. The Studio tab paths of LIFE-181 and the rest of the unit suite are unchanged: `npm run test:unit`, output (`work/verifier/unit-full.log`): `tests 4664, pass 4648, fail 0, skipped 16`, exit 0.
7. Requirements: `just requirements-lint` exit 0, last line `use case diagrams: 94 StRS checked, all parse (Mermaid 12.2.0)` (`work/verifier/requirements-lint.log`). New SwRS LIFE-186 to 191 and the updated LIFE-178/181/184/185 and StRS LIFE-023 are in the diff (`git diff --stat origin/main..HEAD`: 53 files).
8. Visual scenario (spec 6.4): `npm run visual:render` and `uv run --no-sync --group docs python test/visual/capture.py --scenario lifecycle-sync/v13-line-marker-jump-if-off-screen-light-900`; output `passed: lifecycle-sync/v13-line-marker-jump-if-off-screen-light-900` and `{"status": "passed", "scenario_count": 1, "screenshot_count": 1}` (`work/verifier/visual.log`). Capture `work/verifier/evidence/after-v13-jump-if-off-screen-light-900.png`, looked at: arrow and light band on the third source line of the wrapped paragraph, page still at the top, no path or username on screen. Light only; the spec asked for light and dark (narrowed in the PR body).
9. Real window (CI, Linux, head 7517dfd, run 44937061899): `gh run view 44937061899 --json headSha,jobs` gives `headSha 7517dfd17699de1c122287a97082b04e756fed14`; jobs `integration`, `stress`, `static`, `static-windows`, `visual`, `viewer-graph`, `checks`, `report` are `success`; `gallery` was still running (re-run). The `integration` job log (`gh run view 44937061899 --job <integration id> --log`, kept under `work/scratch/integration-job.log`, not published) shows `STEP start: side-preview-jump` ... `STEP done: side-preview-jump (8191 ms)` and `Extension host test runner exit code: 0`. The test `test/integration/sidePreviewJump.test.ts` asserts: J2 a `vscode.open` with a selection at line 40 marks line 40 of doc.md and the text editor is at line 40; J4 `cursorDown` keeps the marker, a text-editor edit removes it, a switch removes it and it does not return; J3 a jump to `other.md` line 55 switches the side preview and marks line 55 of other.md; J5 a diff-side jump is recorded on the real file and the marker takes the last jump's line (log: `J5 diff selection records: [{"uri":".../doc.md","firstLine":24,"kind":"command","target":"diff-side","jump":{"uri":".../doc.md","line":25}}]`); J7 a jump to doc.md line 30 keeps the text editor, opens no Studio tab, the side preview switches and marks line 30. J1 printed: `vscode.open with a selection (a search click): command/1/jump`; `cursorDown`, `cursorBottom`, `selectAll`, API selection and Go Back: `no selection change`.
   Narrowing: the marker is read from the host (`getActivePreviewForTests().markedLine`), not from the webview's `.sphinx-preview-line-marker`; the page's drawing is proved by claims 4 and 8.

## UNVERIFIED (declared by the Driver, and added)

- UNVERIFIED: J6 (anchor off, caret mark on, Studio tab beside the editor, hidden preview inside and past 5 s) is manual only, not run.
- UNVERIFIED: J1 to J5 and J7 never run locally, only in heavy CI (claim 9).
- UNVERIFIED: same-document path links with a line or fragment mark the target line, plain anchors do not (a session test, claim 5; not driven in a real window).
- UNVERIFIED: J5 asserts only that the last jump on the real file wins, so the marker can end on line 1.
- UNVERIFIED: Go to Symbol, F3, F8, Quick Open `:line`, Go to Line, Problems, terminal link and Ctrl+click are not driven in a real window (reached by `vscode.open` with a selection in J2, J3, J7).
- UNVERIFIED: the round-2 session tests never ran against a build without the feature.
- UNVERIFIED: a Studio selection on the same URI and line within 1 second is taken as Studio's own (stated in the SwRS and docs; unit-tested as `take` once, not driven live).
- UNVERIFIED (added): "arrow keys, a click, Page Down and typing never mark" in a real window: in CI `cursorDown`, `cursorBottom`, `selectAll` and an API selection produced no selection change at all, so J1 does not exercise them; only the unit tests of `jumpSignal` and `editorJumps` (claims 1 and 3) prove it. Go Back marks nothing in the real window (`no selection change`), against the PR Summary's earlier wording (narrowed in `work/pr-body.md`); VSCodeVim `j`/`k` is not confirmed to mark (the API selection recorded none), so the earlier Known gap saying they mark is not proved either.
- UNVERIFIED (added): no dark capture of v13 (spec 6.4), and no before image of a real search click.

## PR description (draft #468, as posted on the forge)

Not judged as a pass: the Driver rewrites it. Seen with `gh pr view 468`: it carries the earlier text, so it still says J1 to J7 "are not run" and "Before and after screenshots of a real search click ... are added to the evidence" (none was captured), and it has no Review box. `work/pr-body.md` was narrowed only for the UNVERIFIED items above; the Driver must fix the Impacts paragraph and add the Review box before the description is judged.

## Evidence files

- `work/verifier/unit-focused.log`, `work/verifier/unit-full.log`, `work/verifier/visual.log`, `work/verifier/requirements-lint.log`
- `work/verifier/evidence/after-v13-jump-if-off-screen-light-900.png`, `work/verifier/evidence/before-after.md`
