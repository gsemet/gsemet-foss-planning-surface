# Before / after

Before: f11132b (base, detached worktree, removed). After: f3af2c07e6dfbd3199071df20874862e335e9a22
(retaken at this head; the closed-button pictures at 1400 now show the count line wrapped).
Reproduce: `uv run --script work/verifier/drive.py <checkout> <out> <tag>` (a scratch copy of
`docs/demo/` as the surface, shop-api with a long `repo:`, mobile-app with none; a scratch in-project
folder). The scratch folders are deleted at the end. The pictures show the temporary folder's path.

| Pair | Shows |
| --- | --- |
| `{before,after}-surface-pc-en-closed.png`, `-pc-fr-closed.png` | button closed, overview, 1400x860 |
| `{before,after}-surface-pc-en-menu.png`, `-pc-fr-menu.png` | menu open, 1400x860 |
| `{before,after}-surface-phone-{en,fr}-{closed,menu}.png` | the same at 375x812 |
| `{before,after}-solo-{pc,phone}-en-closed.png` | in-project board, no picker, no change |
| `{before,after}-measures.json` | texts, titles (hover), widths |
