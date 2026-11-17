# Behaviour note — the Comments button hides every review mark

## Today
With the toolbar Comments button off ("Show comments", aria-pressed=false) only the inline gray and
thread chips go away. The highlighted quotes (`mark[data-okf-comment-thread]`), the dotted underline
of resolved threads, the badges and the "Orphaned comments" box stay, and a click or Enter on a
highlight (or a click on a badge or orphan entry) still opens the thread popover.
The setting `preview.showComments=false` has the same gap.

## After (proposal)
While comments are hidden (button off, or setting false), every review mark goes: chips, highlight
colour and underline (the quoted text stays as plain text), badges and the "Orphaned comments" box.
A former highlight is plain text: no pointer cursor, not in the Tab order, a click or Enter opens no
popover and acts like a click on plain text (reveal the source line; in edit mode, edit the block).
Pressing the button again brings everything back.

## Requirements touched
- SwRS-MDOKFSTUDIO-REVIEW-152 (proposed): widened from chips to every review mark; title and scenarios.
- SwRS-MDOKFSTUDIO-REVIEW-021 (proposed): "A highlight, badge or orphan entry opens the thread
  popover" gets the exception "while comments are shown".
- StRS-MDOKFSTUDIO-REVIEW-012 / REVIEW-001 (approved): not edited.

## Choices left open (with proposals)
1. Click on a hidden highlight: plain-text click (reveal / edit block) rather than a swallowed no-op.
2. Keyboard: hidden highlights leave the Tab order (tabindex/role removed or -1) and come back on show.
3. A popover open when the reader presses Hide: it closes.
4. Setting `preview.showComments=false` hides every mark too (same rule as the button).
5. The text-selection Comment button (compose new thread, REVIEW-038) stays available while hidden
   (out of scope); a new thread created while hidden stays hidden until Show.
6. The "badge after" block (a static 14 px line) disappears, so a few pixels of layout move; the
   existing layout callback keeps the reading line.

## Shots
- /private/tmp/claude-502/cr224-driver/shots/before-comments-off-light.png
- /private/tmp/claude-502/cr224-driver/shots/before-comments-off-dark.png
- /private/tmp/claude-502/cr224-driver/shots/before-hidden-highlight-click-light.png
- Owner mockup: backlog-item/evidence/expected.jpg

## Owner answer (2026-10-31)
APPROVED as proposed, choices 1–7 (relayed by the Foreman).
