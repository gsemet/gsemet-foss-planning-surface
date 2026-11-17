# Answers

The owner gave the behaviour above and went to bed: no further question is possible tonight.

Autonomous decisions, to list in the PR body under "Autonomous decisions":

- Applies to every comment editor: a new comment, a reply, an edit of a comment.
- Near the bottom of the window the editor opens above its text, or moves up, so it is entirely visible.
- The editor stays attached to its text when the page scrolls, even if that takes it off screen; the draft
  is never lost by scrolling.
- Escape and a click outside act the same way, wherever the focus is. No draft or an unchanged one: the
  editor closes. A changed draft: a small question in the editor itself, "Discard" or "Keep editing";
  `window.confirm` is not available in a webview. The Keep editing answer leaves it open with its text.
