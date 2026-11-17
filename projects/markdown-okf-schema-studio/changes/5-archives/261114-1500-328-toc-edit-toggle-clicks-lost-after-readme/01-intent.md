# The edit toggle loses its clicks in the toc step, after readme-html

Found by CR-326 (the flaky real-window integration steps of the v1.9.0 cycle). Not fixed there.

## What fails

The `toc` real-window step (`scenarioToc`, `test/integration/tocWindow.ts`) fails with
`Edit mode did not switch to on: the toggle missed 3 clicks`. The page is rendered, the toggle is on
top at its own centre (`hitIsToggle: true`), the click count stays 0, no page error: the real mouse
events never reach the content page. The webview host frame (`index.html`) reports `hasFocus=false`,
active element `body`.

## Evidence

| Run | Where | Result |
|-----|-------|--------|
| 43532691444, attempt 1 | `main` push `1191fb6c`, integration | failed, `toc` right after `readme-html` |
| 43577748076 | branch heavy, head `dc7e7f25`, integration, 2600x1440 screen | failed, `toc` right after `readme-html`, click point (1283,99) x3 |
| 43579225181 | branch toc-loop 40 rounds, each round runs `readme-html` then `toc`, 2600x1440 screen, head `c78c309e` | rounds 4 and 9 failed, 38 clean |
| 43579222581 | branch heavy and stress 60 rounds, head `c78c309e` | green (the integration `toc` passed this time) |
| 43576431799, toc-loop 40 rounds without `readme-html` | head `17454607` | green |

Facts:

- The Xvfb screen size is NOT the cause: the failure happens on a 2600x1440 screen with the click
  point (1283,99) far inside it. The 1280x1024 default was a wrong lead (it is still raised to 2600
  wide by CR-326, because it was a real mismatch with the 1400 px emulated viewports).
- `toc` right after `readme-html` fails about 5% of the time (2 of 40); `toc` alone, or in the
  stress rounds (60 passes), did not fail in the runs above.
- At the failing round the VS Code window is `focused: true, active: true`, the workbench document
  has focus, and the content page's trace shows `page blur  active=body pageFocus=false` at 497 ms:
  the content page lost the focus around the first click. The workbench focus moves show the
  usual `window-blur / window-focus active body` pairs before the webview takes the focus.
- CR-326 added before the first click: `page.bringToFront()`, a wait for the window focused and no
  pending group unlock focus command. It did not remove the failure (round 4 and 9 above).

## Guess (not proven)

The workbench moves the focus to `body` and back to the webview around the preview opening
(group focus or unlock commands), and a real click during that window does not reach the
content page. It may be the same mechanism as the block editor closing right after a click
(palette, alert-dropdown; run 43416264245, 43536948441), but nothing proves a link. It may be a
VS Code behaviour a real user can hit (a click right after the preview opens is lost); that is
unknown.

## To do

Reproduce with `gh workflow run ci.yml --ref <branch> -f toc_loop=40` (each round runs `readme-html`
then `toc`), then read the failing round's `workbench focus at the failing step` and the page
trace. Candidates: what `readme-html` leaves behind (a group, a tab, a focus command), and which
VS Code focus command lands late. SwRS to check: SwRS-MDOKFSTUDIO-BLOCK-047 (commit on leave).

## 2026-11-14: seen on another step

On the v1.9.1 version push (ci.yml run 43590898224, main 5a61b0c9, attempt 1) integration failed
on `myst-blocks`, the step after `toc` (toc and readme-html passed): "Edit mode did not switch to
on: the toggle missed 3 clicks", all three clicks at (1283,99), hostFrame hasFocus=false
active=body. The bug is not specific to `toc`: any edit-toggle click after a preview opens may be
lost. Relayed by the Foreman.
