# 112 — Edit toolbar: tooltips everywhere, rule icon, easier rule editing

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-missing-tooltips-editbar`

## Intent (user)

It seems like not all edition tool bar has a tooltip

![Tooltip](image.png)

And i would like to see the same slide effect than the tooltip on the main floating toolbar

---

Change the icon for the horizontal bar

![image-1.png](image-1.png)

should be `---` not like the "centered text"

---



Also, it is had to click on an horizontal bar to edit it, like if only its height is detectable to allow user to edit this line

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Every button of the block edit toolbar gets a tooltip, using the same component and slide-in animation as the main floating toolbar (reuse it, do not duplicate it).
- Horizontal-rule button: a `---`-style icon (codicon `horizontal-rule` if available, else a small inline SVG of a dashed line), not the centered-text icon.
- Horizontal rules get a taller invisible hit area (about 12px above and below) so a click edits them.
