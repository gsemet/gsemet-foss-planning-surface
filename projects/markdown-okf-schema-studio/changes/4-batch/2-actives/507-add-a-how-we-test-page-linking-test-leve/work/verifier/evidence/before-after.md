# CR-507 before and after

- Before: base `4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e` (branch of CR-514, below this CR).
- After: head `6c5106e4589592002f828b6feb3d545a442591aa`.
- All captures: headless Chromium on the built site over `file://` (no address bar, no path),
  viewport 1280 wide. The site is light only (`color-scheme: light`), so there is no dark pair.
- Each image was opened: none shows a user name or a home folder.

## Pairs

| Before (4e4eeb4) | After (6c5106e) | What it shows |
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
3. `node <V>/capture.mjs <W> out/site <V>/evidence after` (log `../head-capture.log`).
4. Copy the backed-up pictures back.

Before, in a detached worktree of the base:

1. Copy the head build's `out/reports/` into it, and `node_modules/mermaid/dist/mermaid.min.js`.
2. `npm run site` (log `../base-site.log`). The gallery step was not run there (its Python
   environment lacks PIL); it does not draw the header or the captured page.
3. `node <V>/capture.mjs <W> out/site <V>/evidence before` (log `../base-capture.log`).
