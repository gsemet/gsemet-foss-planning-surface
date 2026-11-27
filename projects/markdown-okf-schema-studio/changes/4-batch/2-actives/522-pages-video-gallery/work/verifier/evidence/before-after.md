# Before and after

- Before: `6b1dd90d176a9ed4a2139e2cf71e11eb02e9fc03` (origin/main, the merge base), on a detached
  worktree at `<worktree>/out/base-522`, removed afterwards.
- After: `8541bedf7295b79a55d110b9b2117d18b1cda551` (the pushed head).

How: `npm run site` in each tree, then `node work/verifier/before_after.cjs <worktree> <tree>
before|after <this folder>`. The README sections are rendered from each tree's `README.md` with
markdown-it (not GitHub's own rendering), each GIF as an image. The site is cream only, so there is
no light and dark pair. Every picture below was opened and looked at: none shows the user name or the
home folder (`~/.claude/workflows/` is text of the demo page itself, in the Edit MyST pictures).

| Before | After | What it shows |
| --- | --- | --- |
| `before-site-header.png` | `after-site-header.png` | Six header links, then seven with Videos between Gallery and Requirements |
| `before-readme-raw-markdown.png` | `after-readme-raw-markdown.png` | "Highest respect for the raw Markdown": no picture, then the table drag GIF |
| `before-readme-edit-myst.png` | `after-readme-edit-myst.png` | "Edit MyST visually": three pictures (editing still, Cream and Dark pair), then the same three with the slash menu grid and figure editor GIFs after the editing still |
| `before-readme-diff.png` | `after-readme-diff.png` | "See what changed since the last commit": the change marks still, then the side-by-side diff GIF |
| `before-readme-radio.png` | `after-readme-radio.png` | "Decide in the page: choices in your plans": the Cream and Dark stills, then the radio buttons GIF |
| none: `videos.html` did not exist at the base (404) | `after-videos-page-top.png`, `after-videos-page.png` | The Videos page: posters, nothing playing, no video file requested |

A GIF in an after picture is caught at one frame.
