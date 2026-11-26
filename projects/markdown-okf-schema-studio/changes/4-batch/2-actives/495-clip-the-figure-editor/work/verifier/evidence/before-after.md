# Before / after, CR-495

Before: base c3c3a57ed16874bf56f5834ef6d789443e842fbb (head of the CR-494 branch).
After: head cae819b958dff6138d9b5dee1638a487234a5d79.

Both sides are read from git objects in the CR worktree, no second checkout. The diff changes no
`src/` file, so the pair is the docs text and the committed file list, not a UI screenshot of the
extension.

## 1. Clip line in the user docs

Reproduce: `git show <sha>:docs/user/editing.md | grep -c clips/figure-editor`
and `git diff c3c3a57e cae819b9 -- docs/user/editing.md`

Before (c3c3a57): `0` matching lines.

After (cae819b): line 181, in the palette bullet after "Escape keeps the figure as inserted.":

    ![In edit mode, Edit figure over a figure opens one form: the caption is retyped, Width set to 40%, Align to Right and Name to fig-harbour-light; Apply writes the new option lines under the kept alt line, and Ctrl+Enter / ⌘Enter shows the smaller figure floating right of the text](../demo-video/clips/figure-editor/figure-editor.gif)

## 2. Clip folder

Reproduce: `git ls-tree --name-only <sha> docs/demo-video/clips/figure-editor/`

Before (c3c3a57): no entry.

After (cae819b): `check.json`, `clip.md`, `contact-sheet.png`, `figure-editor.gif`,
`figure-editor.mp4`, `figure-editor.webm`, `first-last.png`, `frames/`, `poster.png`,
`scenario.mjs`, `stage/`.
