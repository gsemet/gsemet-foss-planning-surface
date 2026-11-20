# CR-351, matrix probe, round 2 (Verifier)

Head: d4a00894f923617c3152d6067ec9491a59a3ac79

Committed head, not pushed. Windows 11, Node v24.22.2, headless Chromium of playwright-core.
Worktree clean at the start and at the end (`git status --short`: empty). First matrix of this CR:
nothing carried.

Build: `npx tsc -p .` (exit 0) in the worktree before the runs.

Probe: `work/scratch/fontProbe.test.ts`. `diff test/page/tableBreakout.test.ts <probe>` shows only
the `PROBE` prints, the case 11 minimum print, `if (!process.env.NO_PIN)` before
`await pinTestFonts(page)`, and test 5's old comment: the cases and assertions are the committed ones.
Run as in `work/coder/r1.md`: copied to `test/page/zzFontProbe.ts`, `npx tsc -p .` (exit 0),
copy deleted, run, then `out/test/page/zzFontProbe.js(.map)` deleted (`ls out/test/page | grep -ci probe`: 0).

## W-pin (Windows, pinned): HELD at d4a0089

Command: `node --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js`

```text
✔ Auto keeps a table in the column when its minimum widths fit and breaks it out when they do not
✔ Auto breaks a table out when a cell holds content that cannot shrink
✔ Auto keeps the breakout of a table while a cell is edited, in every cell it moves to
✔ Auto keeps a table that fits the column in the column while a cell is edited
✔ Auto measures a table again on a real resize while a cell is edited
✔ Auto gives the column width to a table edited as source, or holding another editor field
✔ an editor opened on a paragraph does not measure the tables again; one opened on a table does
ℹ tests 7  ℹ pass 7  ℹ fail 0
```

(The file has seven tests; tests 1 to 6 of the matrix are among them, all pass.)

Widths, command `node --import ./scripts/register-myst-patches.mjs --test out/test/page/zzFontProbe.js`:

```text
PROBE pinned light cases 688s 688s 688s 688s 1068W 735W 748W 338s 537s 719W 894W 824W
PROBE pinned light case11-minimum 734 [115,58,76,75,219,191]
PROBE pinned dark cases 688s 688s 688s 688s 1068W 735W 748W 338s 537s 719W 894W 824W
PROBE pinned dark case11-minimum 734 [115,58,76,75,219,191]
PROBE pinned light cases 1068W 972W 1068W
PROBE pinned dark cases 1068W 972W 1068W
PROBE pinned light tick-open 719
PROBE pinned dark tick-open 719
ℹ tests 7  ℹ pass 7  ℹ fail 0
```

Matches `work/coder/r2.md` to the pixel: twelve cases, case 11 894 W with a 734 px minimum
(46 px over 688, A-22), test 2 1068/972/1068, tick matrix 719 px (the value in test 5's comment).
All twelve verdicts match `CASES`.

## W-nopin (Windows, pin removed in the probe only): HELD at d4a0089

Command: `NO_PIN=1 node --import ./scripts/register-myst-patches.mjs --test out/test/page/zzFontProbe.js`

```text
PROBE segoe light cases 688s 688s 688s 688s 1068W 775W 773W 341s 537s 705W 932W 863W
PROBE segoe light case11-minimum 759 [111,57,83,76,228,205]
✖ Auto keeps a table in the column when its minimum widths fit and breaks it out when they do not
PROBE segoe light cases 1068W 1010W 1068W
PROBE segoe dark cases 1068W 1010W 1068W
PROBE segoe light tick-open 705
PROBE segoe dark tick-open 705
ℹ tests 7  ℹ pass 6  ℹ fail 1
AssertionError [ERR_ASSERTION]: light: the page draws in the pinned fonts (cell -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI", system-ui, sans-serif, code "SF Mono", Menlo, Consolas, monospace, loaded true)
```

Segoe UI / Consolas widths, tick matrix 705 px, as in `work/coder/r2.md`; the twelve verdicts
still match `CASES` (case 11 932 W). The one failure is the pin assertion, as expected.

## Pin holds (test 1 assertion): HELD at d4a0089

With the pin, test 1 passes (W-pin run above), so the assertion
`first(cell) === "Studio Test Sans" && first(code) === "Studio Test Mono" && loaded` holds in both
themes. Without the pin it fails on its first theme with the Segoe UI / Consolas families (W-nopin
output above): the assertion catches a lost pin.

Observation: the `loaded` part is true without the pin too (`loaded true` in the W-nopin message):
`document.fonts.check` returns true when no face of that family is in the set. The family checks
alone carry the assertion; not a cell failure (the specification asks for exactly this check).

## Missing font: HELD at d4a0089 (throw), with a finding

Temporary runs on the compiled helper only (`out/test/page/pinnedFont.js`, backed up first,
restored by copy and `npx tsc -p .`; `cmp` with the backup: same; no source touched, nothing
committed). Raw logs: `work/verifier/r2-missing-font.log`, `work/verifier/r2-bad-face.log`.

1. Wrong path (`KaTeX_SansSerif-Bold.woff2` -> `KaTeX_SansSerif-Missing.woff2`). Command:
   `STUDIO_TABLE_THEME=light timeout 120 node --import ./scripts/register-myst-patches.mjs --test --test-force-exit --test-name-pattern="minimum widths fit" out/test/page/tableBreakout.test.js`
   (exit 1):

   ```text
   ℹ pass 0  ℹ fail 1
   Error: ENOENT: no such file or directory, open '<worktree>\node_modules\katex\dist\fonts\KaTeX_SansSerif-Missing.woff2'
   ```

2. A file that is not a font (`../katex.min.css`), same command (exit 1):

   ```text
   ℹ pass 0  ℹ fail 1
   Error: the pinned test font did not load: ../katex.min.css (error) from <worktree>\node_modules\katex\dist\fonts
   ```

Both name the file; no fallback to the platform's font.

Finding (for the Driver): the same wrong-path run without `--test-force-exit` (the project's
runner, `scripts/node-test.mjs`, passes no such flag and no timeout) did not exit: it was still
running after more than 5 minutes with no result printed (background task, output only the `grep`
line of the edit). `openPage` launches Chromium, then `pinTestFonts` throws before `openPage`
returns the `close`, so the browser is never closed and the test process stays alive. A missing
font would hang `just check` / CI until their timeout rather than fail at once. The specification's
claim (throws with the file name) holds; closing the browser when the pin throws (a `try` around
`pinTestFonts` in `openPage`) would make it fail fast. My attempt to stop the hung child by its PID
(`Stop-Process -Id 29532 -Confirm:$false`) was refused: "Permission for this action was denied by
the Claude Code auto mode classifier. Reason: [Destructive or Unwanted Actions]." The background
task ends with this session.

## L-pin (Linux): not judged: CI later

## Cleanup

`git status --short` in the worktree: empty at d4a00894. `out/test/page`: no probe file; the
compiled helper equals the HEAD build. Scratch holds only the Coder's `fontProbe.test.ts`.
