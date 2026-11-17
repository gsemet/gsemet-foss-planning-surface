# 050 — preview-warning-and-pasted-image

From the follow-ups of CR 043 (real VS Code tests): two product issues seen in captures.

## Decisions (user grill, 2026-10-23)

1. MyST `conf.py` warnings (missing extension, unsupported syntax…): today only in Problems and as
   an editor squiggle; the preview keeps them in a visually hidden status region when rendering
   succeeds (`[data-sphinx-preview-status="success"]`). Show a discreet banner at the top of the
   preview: warning icon, short text, a link/button that opens the Problems view; closable, and
   stays closed for that document for the session (reappears when the warning set changes).
   Stylesheet only, readable in light/dark/cream/current-theme, accessible (role=status, focusable
   close button), does not cover the floating toolbar or shift the scroll-sync anchor.
2. Pasted image: (a) pasting an image inserts it as its own paragraph (blank line before and after
   when needed, like GitHub/Obsidian), never glued at the end of a text line; (b) an inline image
   inside a paragraph (`Text. ![x](x.png) more`) renders in the text flow at its position, not
   above the paragraph. Check how figures/standalone images are mapped (CR 007/T7 work) so block
   images keep their figure behaviour.
3. Tests: unit (paste insertion text, banner state), visual scenarios (banner light+dark, closed
   state; inline image in a paragraph; pasted image paragraph), and the existing real-window
   image-paste capture updated if its expectation changes (assertion intent kept).
4. Branch `changes-requests/050-preview-warning-and-pasted-image`, screenshots on
   `changes-requests/050-preview-warning-and-pasted-image-assets`.
5. Speed: Opus everywhere, reviewer on the round diff, ready when `checks` is green. Rounds: 3.
   PR written for an external reader.
