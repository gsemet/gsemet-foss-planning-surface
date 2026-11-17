# Final regression replay — summary

Date 2026-10-14. HEAD `8d1ee21` on `dev/gsemet-deep-ux-analysis`, extension tree clean. The
extension was compiled and bundled from source (`npm run compile`, `npm run bundle`; `q doctor`:
"bundle up to date"). A fresh QA workspace was built with `setup-workspace.sh --force` (no vault)
and cloned three times. Three fresh sessions mirror T40's batches: `r5a` (UX-01–11), `r5b`
(UX-12–21), `r5c` (UX-22–34). The observer ran in each session. Real mouse and keyboard input
only; no product, `book/` or `.agents/skills/` file was changed.

All 37 scenarios of [`../replay/scenarios/`](../replay/scenarios/) were run, in T40's order
(setup scenarios first; UX-04 run A and run B; UX-13 twice). UX-07 hover, UX-26 status page, UX-27
and UX-30 Explorer entry, UX-31 picker and UX-32 tab labels were also redone with driver calls, as
T40 did.

## Result

**0 regressions.** 30 IDs unchanged, 4 expected changes (UX-21, UX-27 label, UX-28, UX-30), all
traced to the commits since T40.

| ID | T40 status | Final status | Verdict |
| --- | --- | --- | --- |
| [UX-01](UX-01.md) | fixed | fixed | unchanged |
| [UX-02](UX-02.md) | fixed | fixed | unchanged |
| [UX-03](UX-03.md) | fixed | fixed | unchanged (same 401 artefact on webview creation) |
| [UX-04](UX-04.md) | fixed | fixed | unchanged |
| [UX-05](UX-05.md) | fixed | fixed | unchanged |
| [UX-06](UX-06.md) | fixed | fixed | unchanged (identical carets) |
| [UX-07](UX-07.md) | fixed | fixed | unchanged |
| [UX-08](UX-08.md) | fixed | fixed | unchanged |
| [UX-09](UX-09.md) | fixed | fixed | unchanged |
| [UX-10](UX-10.md) | fixed | fixed | unchanged |
| [UX-11](UX-11.md) | fixed | fixed | unchanged (0 px drift) |
| [UX-12](UX-12.md) | fixed | fixed | unchanged |
| [UX-13](UX-13.md) | fixed | fixed | unchanged (one transient host page error, not reproduced) |
| [UX-14](UX-14.md) | fixed | fixed | unchanged |
| [UX-15](UX-15.md) | fixed | fixed | unchanged |
| [UX-16](UX-16.md) | fixed | fixed | unchanged |
| [UX-17](UX-17.md) | fixed | fixed | unchanged |
| [UX-18](UX-18.md) | fixed | fixed | unchanged |
| [UX-19](UX-19.md) | fixed | fixed | unchanged |
| [UX-20](UX-20.md) | fixed | fixed | unchanged |
| [UX-21](UX-21.md) | fixed, with gaps | fixed, gaps closed | expected change (D-21, T41) |
| [UX-22](UX-22.md) | unchanged (frozen) | unchanged (frozen) | unchanged |
| [UX-23](UX-23.md) | fixed | fixed | unchanged |
| [UX-24](UX-24.md) | unchanged (frozen) | unchanged (frozen) | unchanged |
| [UX-25](UX-25.md) | fixed | fixed | unchanged (0 navigations) |
| [UX-26](UX-26.md) | fixed | fixed | unchanged |
| [UX-27](UX-27.md) | fixed | fixed | unchanged; Explorer label expected change (D-20, T42) |
| [UX-28](UX-28.md) | not fixed | partly fixed | expected change (D-10 T34, D-22 T43) |
| [UX-29](UX-29.md) | fixed | fixed | unchanged (0 px) |
| [UX-30](UX-30.md) | fixed | fixed | expected change (D-20, T42): one check now stale |
| [UX-31](UX-31.md) | fixed | fixed | unchanged |
| [UX-32](UX-32.md) | fixed | fixed | unchanged |
| [UX-33](UX-33.md) | fixed | fixed | unchanged |
| [UX-34](UX-34.md) | unchanged (frozen) | unchanged (frozen) | unchanged |

### Expected changes

- **UX-21 (D-21, T41 `50eab0f`).** a: a new field is written where the table shows it
(`depends_on` after `derived_by`, `approver` after `custom_key`); b: Enter saves a new custom
key, written `approver: Ann` without quotes; c: Escape with focus on the picker closes the field
editor (also seen at the end of UX-20). The T40 gaps are closed.
- **UX-27 / UX-30 (D-20, T42 `fabc1fa`).** The Explorer entry and the title-bar tooltip read
"Open Preview to Side (⌘K ⇧V)"; the palette still shows the category. The UX-30 scenario's
title-button check filters on `/Studio/` and now fails; the button exists and opens the preview.
The check needs the short title.
- **UX-28 (D-10 T34 `8d1ee21`, D-22 T43 `e26e836`).** See below.
- **Side effect of T30/T34, seen in UX-13:** table cell commits caused 0 webview navigations
(T40: bursts of 3 per commit).

## UX-28 measured independently

`book/chapters/02-foundations.md`, `UX-28-setup` then `UX-28-typing-navigations`, exactly as T40.

| Run | `incrementalUpdates` | Characters | Navigations |
| --- | --- | --- | --- |
| T40 at `50cd143` | (did not exist) | 32 | 26 (0.81 per character) |
| Final, run 1 | on (default) | 32 | **9** (0.28 per character) |
| Final, run 2 | on | 32 | **6** (0.19 per character) |
| Final, 10 characters at 60 ms and at 400 ms | on | 10 | **0** and **0** |
| Flicker probe | on | 21 | 0 (2095 samples: one scrollY, one height) |
| Kill switch | **off** | 10 | **6** |
| Kill switch | **off** | 32 | 18 |

- The preview no longer reloads for short bursts, and the kill switch restores reloads live.
- Continuous fast typing still reloads: the navigations start 0.8–1.25 s into the burst and stop
right after the last key. Code reading (not verified): a render that completes before the page
acknowledged the previous patch falls back to a full load (`src/extension.ts:929–940`). The
sheet's "Done when" ("typing never navigates the webview frame") is therefore not met.
- Screenshot right after typing, with the typed text visible:
`output/qa/markdown-studio-claude/runs/r5c/shots/UX-28-after-typing.jpg`, copied to
[`../../mr/images/07-typing-no-reload-after.jpg`](../../mr/images/07-typing-no-reload-after.jpg).
Its file name says "no reload", but the run it shows had 9 navigations.
- Filmstrip: 24 frames, no blank frame, no scroll jump
(`output/qa/markdown-studio-claude/runs/r5c/shots/UX-28-film-*.png`).

## Page and console errors

- `[pageerror] Found unexpected null`, once (r5b, 03:41:24.532, UX-13 run 1). It came during the
full load when the preview switched from `synth/tables.md` to `04-code-and-tables.md` (4 frame
navigations in 40 ms). It is thrown by VS Code's webview host
(`…/contrib/webview/browser/pre/index.html`, `assertIsDefined`) when a pending content frame is
replaced quickly. The UX-13 re-run went through the same switch and stayed clean. T40 saw the
same message once while typing (UX-28); no r5c typing run produced it.
- `Failed to load resource: 401` for a `vscode-resource` URL: twice in r5a, when a Studio webview
was created (03:36:16 Open With editor in UX-03; 03:39:31 side preview in UX-11-setup). This is
T40's side observation; no other session logged it.
- Extension host `DEP0040 punycode` deprecation warnings (ignored by the `errors` check).

## Notes and limits

- UX-04 run B and the UX-30 title-button check fail by construction (see their files); neither is
a product regression.
- Absolute geometry values (UX-09 heights, UX-11 scrollY, UX-15 client width) differ slightly
from T40 because of the preview width; the measured invariants are the same.
- Logs: `output/qa/markdown-studio-claude/runs/r5{a,b,c}/console.log`, scenario results under
`runs/r5{a,b,c}/scenarios/`. Clones `ws-r5a`, `ws-r5b`, `ws-r5c` are kept until review.
- All VS Code windows and observers were stopped by PID (`q stop`); afterwards no `msq-`,
`observe.mjs`, `qa.mjs` or `--extensionDevelopmentPath` process was running.

## Addendum: UX-28 at 7a21a2b

T34 round 3 (`7a21a2b`) chains the content patches. A re-run in session `r6` measured **0**
navigations in each of 3 runs of 32 characters, 0 in a run of 10 characters, and 16 with the
setting off. UX-28 is **fixed**; see [UX-28](UX-28.md).
