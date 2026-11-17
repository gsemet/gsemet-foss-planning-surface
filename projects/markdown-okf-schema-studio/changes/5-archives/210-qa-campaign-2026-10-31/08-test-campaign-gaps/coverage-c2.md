# Coverage note — C2 review comment threads

Window c2, fixture `synth/rev.md` + `rev.comments.json` (ws-c2, copy of the pattern in assets/synth/review-threads.*), side preview, ~35 driver calls, 1 shot opened.

Exercised, all PASS except c2-1:
- Highlights from the sidecar (open, resolved dimmed); popover content; Resolve (immediate sidecar write), Reply, Escape and outside click close, one popover at a time.
- Create a thread: drag-select in preview, Add a comment button, Cmd+Enter; sidecar gets line, quote, author.
- Source editor: insert paragraph above, save: marks stay, sidecar lines shifted (+2). Never written before save.
- Edit inside the quote (source and inline editor): mark replaced by a badge; undo x3 brings the mark back with no sidecar change.
- Delete the anchored block: thread goes to "Orphaned comments", kept in the sidecar; orphan opens its popover.
- External rewrite (blocks moved, three paragraphs added, anchored paragraph triplicated): marks follow the text, duplicate resolved to the copy nearest the old line; sidecar lines correct after the next save.
- Resolve and reply while the buffer is dirty: sidecar written at once with disk-consistent lines, no error.
- Comments toggle: see c2-1.

Observed, not reported: editing 2 characters inside a 12-character quote (inline editor) demotes the thread to a badge at once
instead of a fuzzy re-anchor; the doc says live edits only shift lines, so this follows the design.

NOT covered: Delete (Yes/No) buttons, Reopen, deleting the last thread, Cmd+Alt+M shortcut, multi-block selection, invalid sidecar JSON
"never overwritten", renaming the document, edit-mode (pencil) while a popover is open, Escape on the compose box, fixtures-visual threads, vault notes, book chapters.
Harness notes: the Comments button lives in the toolbar chevron menu at the default narrow preview width (box 0x0 until the menu is open);
`Meta+Home` inside the inline textarea did not jump to the start (use `Meta+ArrowUp`).
