# Verify CR-480 (raw copy)

Head: c01042578e1fa0248761c1286fa33c336de63794

Judged at c0104257 (full SHA above) unless a line says otherwise. Base 80d482fd.

## Claims

1. Real browser, after: the E3 check passes at the head.
   Command (worktree at head): `npm run visual:render` then `uv run --no-sync --group docs python work/verifier/dump_capture.py after-cases.json`
   Output (`work/verifier/after-capture.log`): `passed: block-editing/v55-raw-copy-light-900`, `{"status": "passed", "scenario_count": 1, ...}`, exit 0.
   `evidence/after-cases.json`: defaultPrevented per copy = [0,1,1,1,1,1,1,1,1,1,1,1,0]; case 0 is the copy before any source text (native, correct), case 12 the old-side edge (native, correct); text/plain of case 2 starts `Intro with **bold** and a [link with **strong** words](https://example.com/page) here.\n\n---\n\n| Name | Value |`; case 4 (frontmatter) `---\ntitle: Raw copy\ntags: [copy, markdown]\n---\n\n# Raw copy\n\nIntro`; text/html holds the rendered elements. The check itself asserts exact text/plain, no chrome, whole-page select-all (real Ctrl+A, Ctrl+C) equal to the fixture, side by side, native cases. PASS.
2. Real browser, before: the same check on the base fails and shows the old behaviour.
   Command: same, in a detached worktree of 80d482fd with the branch's `test/visual` files copied in. Output (`before-capture.log`): `cap 1`, 12 failures "...: the copy was left to the browser", "Select all then copy did not give the whole source exactly: {'taken': False, 'plain': '', 'html': ''}".
   `evidence/before-cases.json`: defaultPrevented all 0; `browserSelectionText` of the table case `Name\tValue\none\tfirst\ntwo\tsecond`: confirms the PR's "Before: cells separated by tabs, no `---`". PASS.
3. Unit tests fail on the base, pass at the head (constitution section 3).
   Base (`unit-before.log`): `tsc` exit 2 (`Cannot find module '../../../src/core/mapping/rawCopy'`, `rawCopyEdges`, `chromeMarks`, ...), then `node scripts/node-test.mjs unit "out/test/{core/mapping/rawCopy,core/protocol/hostToPage,page/runtimeRawCopy,session/previewSourceText}.test.js"`: `tests 21, pass 14, fail 7` (rawCopy.test.js, hostToPage, previewSourceText, runtimeRawCopy x3, session x1).
   Head (`unit-after.log`, `tsc -p .` exit 0): same command, `tests 39, pass 39, fail 0`; rawCopy.test.ts has the 19 tests the PR says (names listed in the log). PASS.
4. Real VS Code window, keyboard chord, at the head.
   Command: `STUDIO_REAL_INPUT_SCENARIO=raw-copy npm run test:integration -- --trusted-only` (`e4-raw-copy.log`, first line is the head SHA).
   Output: `STEP done: real-input (3228 ms)`, `Exit code:   0`. The scenario (`test/integration/realInput/rawCopy.ts`) asserts, after a real Ctrl+C with a sentinel, `readText()` equals the exact raw Markdown in reading mode, in edit mode, after Ctrl+A (whole document) and `**bold**` natively from a block editor textarea. PASS.
   Also CI at the head: run 45403873608 (workflow_dispatch heavy) `integration`, `stress`, `static`, `static-windows`, `visual`, `viewer-graph`, `report` success (gallery was still running when read: not part of this claim); PR checks run 45403877492 pass.
5. Gate pass: no `chantier gate` pass exists at c010425 (`ship` says off=['no long gate passed ...']); this claim needs none: the short checks were run directly (claims 1-4); `just check` and `just preflight` per the Driver's notes and `work/gates/check5.log`, `preflight.log` are not re-run by me and are not claimed here.
6. Review box: the PR body checkbox `Review` is unchecked and cites no SHA; the log has `r3 approved at e050a7ac, committed as c010425` and `r2 inspector approved at 80d482fd...`. Nothing is claimed by the body, so nothing to refute.
7. Evidence images: `evidence/after-selection-over-frontmatter.png` opened: shows the fixture, the frontmatter table, heading and "Intro" highlighted, the toolbar; no path, no user name. Clipboard JSON paths rewritten to `C:\Users\user\...`. Observation (not a claim of the PR): the copied text/html keeps the `data-sphinx-source-file` attribute with the local file path of the document.

## PR description (second pass, judged at c01042578e1fa0248761c1286fa33c336de63794)

Command: `gh pr view 498 --json body -q .body` diffed with `work/pr-body.md`: identical (one trailing blank line). `git diff --stat origin/main...HEAD`: 42 files; `gh pr view 498 --json headRefOid`: c01042578e1f.... `gh pr view 498 --json statusCheckRollup`: static, static-windows, visual, viewer-graph, report, checks SUCCESS (integration and stress SKIPPED on the PR run; the heavy run 45403873608 passed them, claim 4).

- Clean: renders (template sections, Mermaid flowchart, table). PASS.
- Consistent with the diff: Summary, Deliverables (before/after table matches `before-cases.json` and `after-cases.json`), Changes (protocol `previewSourceText` in hostToPage.ts, `rawCopy*` core modules, `chromeMarks.ts`, page handler, 1 StRS + 7 SwRS, glossary entry) match the 42 files. Impacts no longer lists roles; `{ref}` copied whole is in Changes. The `balanceRawCut` seam exists in `rawCopyEdges.ts`. PASS.
- Proofs name the SHA (c010425 in the Test plan items); Review cites c010425, the log's `r3 approved at e050a7ac, committed as c010425` matches. PASS.
- Known gaps and Autonomous decisions present and cover the unproved items of claim 4 and the stacked edge balancing. PASS.
- Images: none attached. Role names: none. PASS.

## Verdict

Behaviour proved at the head (claims 1-4); description passes.

VERIFIED
