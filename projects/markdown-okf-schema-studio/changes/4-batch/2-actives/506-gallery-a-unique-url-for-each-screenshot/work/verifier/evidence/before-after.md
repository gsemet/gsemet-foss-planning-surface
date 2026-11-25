# CR-506 before and after

- Before (base, origin/main): `4a47151e8d055b7f096b69b1fca2d9bf9636f863`
- After (pushed head): `c715355c203d92df18200011749d1a73cead0ad9`
- Data: the same reports artifact for both builds, `studio-reports-attempt-1` of CI run
  `45476952370` (latest green heavy run of main, at `63ef752bba38647ac0f95fa166855ec6e5970293`;
  610 screenshots).
- All files were opened and looked at: legible, no username and no home folder path.
- A headless page has no address bar: the yellow strip at the bottom is added by the capture
  script and prints `location.href`. Port 8764 serves the base site, port 8765 the head site.

## Pairs

| Before | After | What it shows |
| --- | --- | --- |
| `before-viewer-next.png` | `after-viewer-next.png` | Same card opened, then Next (24 of 610). Before: the address stays `gallery.html`. After: `gallery.html#block-editing/r02-mod-enter-commit`. |
| `before-unknown-id.png` | `after-unknown-id.png` | Direct load of `gallery.html#nope/r99-gone`. Before: the grid, nothing said. After: the notice above the grid, no viewer. |
| `before-grid-1280.png` | `after-grid-1280.png` | The grid at 1280 px, no fragment: unchanged (identical bytes). |
| `before-grid-390.png` | `after-grid-390.png` | The grid at 390 px, no fragment: unchanged (identical bytes). |

## After only

The base page reads no fragment, so these have no distinct before (it shows the grid, as
`before-unknown-id.png` does).

| File | Direct load of |
| --- | --- |
| `after-viewer-visual.png` | `gallery.html#block-editing/v08-insert-point-hover-light-900` (123 of 610) |
| `after-viewer-step.png` | `gallery.html#block-editing/v08-insert-point-hover-light-900--hover` (122 of 610) |
| `after-viewer-registry.png` | `gallery.html#block-editing/r01-paragraph-blur-commit` (23 of 610) |

## Suggested for the PR's Impacts

`before-viewer-next.png` with `after-viewer-next.png`, and `before-unknown-id.png` with
`after-unknown-id.png`.

## Reproduce

`<worktree>` is the CR worktree, `<folder>` the CR folder.

1. `git -C <worktree> worktree add --detach <worktree>/out/base 4a47151e8d055b7f096b69b1fca2d9bf9636f863`
2. `gh run download 45476952370 -n studio-reports-attempt-1 -D <folder>/work/scratch/artifacts-45476952370`,
   then copy its content into `<worktree>/out/reports` and `<worktree>/out/base/out/reports`.
3. Head: `just site-assemble` (it rewrites tracked files under `images/`; restore them with
   `git checkout -- images`). Base: the okfreq requirements report, `npm run compile`,
   `npm run site` (the base build also needed `node_modules/mermaid/dist/mermaid.min.js`, copied
   from the head worktree).
4. `node <folder>/work/verifier/probe-real-site.mjs <worktree> <worktree>/out/base <folder>/work/verifier/evidence`
