# CR-507 before and after

- Before: captured at base `4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e`; carried to the current base
  `f9dc2c630b852635e8bffcd0b00b42cc886b293c`: `test/site`, `images`, `scripts` and the package files, which draw the
  header, did not change between them.
- After: head `0592dde49824cc0bb9fab3dbca07b6c0aaef2f20`. Captured again there (`../recapture-0592dde/`,
  log `../h0592-capture.log`): all five files are byte-identical to the ones here, first taken at
  `6c5106e4589592002f828b6feb3d545a442591aa`. The Markdown renderer (`src/core/render/`) changed between those two
  heads, so the equality comes from the new capture, not from unchanged files.
- All captures: headless Chromium on the built site over `file://` (no address bar, no path),
  viewport 1280 wide. The site is light only (`color-scheme: light`), so there is no dark pair.
- No image shows a user name or a home folder.

## Pairs

| Before (4e4eeb4, carried to f9dc2c6) | After (0592dde) | What it shows |
| --- | --- | --- |
| `before-header.png` | `after-header.png` | The site header, taken on How we ship: five links before; six after, "How we test" between "How we ship" and "Gallery". |
| none: the page is not in the base site | `after-page-top.png` | The new page's top, down to the end of the diagram. |
| none | `after-table.png` | The table "Which test proves which requirement". |
| none | `after-not-enforced.png` | The section "What is not enforced yet". |
| none | `after-diagram-native.png` | The diagram `images/how-we-test/test-levels.svg` at its own size (1240 by 640). |

The base capture log says `docs/how-we-test.html: not in this site` (`../base-capture.log`).

## How to reproduce

`<W>` is the CR worktree, `<V>` is `work/verifier` of the CR folder.

After, in `<W>` at the head:

1. Back up `images/` files (the recipe rewrites tracked pictures).
2. `just site-from-run 45830014522` (reports of a green heavy run, then `just site-assemble`).
3. `node <V>/capture.mjs <W> out/site <V>/recapture-0592dde after`.
4. Copy the backed-up pictures back.

Before, in a detached worktree of the base:

1. Copy the head build's `out/reports/` into it, and `node_modules/mermaid/dist/mermaid.min.js`.
2. `npm run site` (log `../base-site.log`). The gallery step was not run there (its Python
   environment lacks PIL); it does not draw the header or the captured page.
3. `node <V>/capture.mjs <W> out/site <V>/evidence before` (log `../base-capture.log`).
