# Clicking the body of a GitHub alert opens the whole alert in the block editor

Decision (user, 2026-10-28): align GitHub alerts with BLOCK-014. A click in the body of a
`> [!NOTE]` / `[!TIP]` / `[!IMPORTANT]` / `[!WARNING]` / `[!CAUTION]` alert opens the whole alert,
from the marker line to the last quoted line, the same way an admonition opens its whole directive.
Today only the clicked paragraph opens (seen in the user's report for the alert line-shift hotfix,
PR #185).

Order: after 1.0.0, after the CI tagging hotfix and the P1 integration hang.

Needs:
- BLOCK-014 (or the GFM SwRS, GFM-009) updated to cover alerts (SwRS are not approval-locked; do
  not touch the locked StRS list).
- A unit test on the opened block range.
- Care with the alert line map added by PR #185: an alert whose body has several paragraphs, two
  consecutive alerts, an alert inside a list item.
