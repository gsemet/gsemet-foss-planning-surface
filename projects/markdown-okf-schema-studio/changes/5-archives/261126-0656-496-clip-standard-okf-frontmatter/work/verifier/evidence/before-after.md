# Before and after, CR-496 (okf-frontmatter clip)

Before: base `cae819b958dff6138d9b5dee1638a487234a5d79`. After: head `d386ff61a3d5a2cda0cb54130a5ffea5600a3793`.

## Pair 1: the OKF user page and the clip folder

- Before: `git ls-tree -r --name-only cae819b9 docs/demo-video/clips/okf-frontmatter` lists 0 files;
  `git grep -c "okf-frontmatter.gif" cae819b9 -- docs/user/okf.md` finds nothing (exit 1).
- After: `git diff cae819b9 d386ff61 -- docs/user/okf.md` adds one image line for
  `../demo-video/clips/okf-frontmatter/okf-frontmatter.gif`; the folder holds 16 tracked files.
- Shows: the page gains the clip. No extension screen changes (no `src/` file in the diff), so no
  before screenshot exists.

## Images

No new capture for this move. The images in the CR folder's `evidence/` (captured at 39d3eb3) are
frames of the clip folder, whose git tree is the same object (`e2f7baed`) at 39d3eb3 and d386ff6.
