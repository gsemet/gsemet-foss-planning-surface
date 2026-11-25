# Before and after

Before: base `17b779d502b9633fd42dd275986067397db5c4aa`. After: head
`8c6845a50d411d894d83c7160e52e1306548330d`.

The extension has no visible change (`src/` is identical at both commits). The one visible change
is the editing page of the user docs, which gains the clip.

| Pair | Before (17b779d) | After (8c6845a) | What it shows |
| --- | --- | --- | --- |
| The "MyST rendering" bullet of `docs/user/editing.md` | `editing-page-before.png` | `editing-page-after.png` | Before: text only, no video element. After: the same text, then the renderings tour clip as a video (1280x720, 16 s), paused at 1.5 s on the Mermaid mark. |

The pictures come from the page's Markdown rendered by the head's renderer and the site's
clip-to-video step, in headless Chromium, light only, with a plain stylesheet: they are not the
published site's theme. Both were opened: no user name, home folder or local path in them.

## Reproduce

From the head worktree, after `just compile`, with a detached worktree of the base
(`GIT_LFS_SKIP_SMUDGE=1 git worktree add --detach <base-worktree> 17b779d5`):

```bash
node --import ./scripts/register-myst-patches.mjs <work>/verifier/shot.cjs <head-worktree> <base-worktree> <work>/verifier/evidence
```

Output at this head:

```text
before: renderings tour video elements = 0
before: video = null
after: renderings tour video elements = 1
after: video = {"width":1280,"height":720,"duration":16}
```

The base holds no version of the clip, so there is no before picture of the clip itself.
