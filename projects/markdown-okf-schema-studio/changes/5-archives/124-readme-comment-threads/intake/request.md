# 124 — README presents comment threads

Type: docs · Priority: P2 · From backlog: `02-backlog/P2/readme-comment-threads`

## Intent (user)

# README: present comment threads as an original feature

User request (2026-10-26): the README must present comment threads as a distinctive feature:
comments anchored to a passage of a Markdown document, stored in a JSON file next to the
document (versioned with it, no server), with replies, resolve and delete. Present it as the
groundwork for future interactive multi-user capabilities.

- Add it to the differentiators of the README showcase, with a screenshot of an open thread
  (captured by the automatic screenshot scenarios, Cream theme).
- Explain where the comments live (the sidecar JSON) and where the author name comes from
  (the setting added by the comment-thread readability fix).
- Wait for the comment-thread readability fix to land, so the screenshot shows the readable version.

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Stacked above CR 110 (readability + author setting) so the screenshot shows the readable popup and the README can name the author setting.
- Screenshot produced by the automatic README screenshot scenarios (Cream theme), not by hand.
- Wording: comments anchored to a passage, stored in a JSON file next to the document and versioned with it, no server; replies, resolve, delete; groundwork for future multi-user collaboration (stated as a direction, no promise of dates).
