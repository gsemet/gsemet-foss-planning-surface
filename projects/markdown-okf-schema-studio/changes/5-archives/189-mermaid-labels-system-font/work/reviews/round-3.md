# CR 189 — Round 3 review (inspector, picture proof)

**Verdict: APPROVE**

## Scope checked

- Worktree `markdown-okf-schema-studio-wt-178` at `b545be4f` (fix(preview): measure and draw Mermaid
  labels with one pinned font). `git status --porcelain --untracked-files=all` shows exactly one entry:
  `M images/readme/myst-diagrams-and-figure.png`. `git diff origin/main --stat -- images/` lists only
  that file. No other `images/readme/` changes.
- The working-tree image is byte-identical to `/private/tmp/claude-502/cr189-driver/after-heavy.png`
  (720x549 PNG), from heavy CI run 40794782167.

## Before (origin/main)

The provided `before-main.png` copy is a Git LFS pointer, not a PNG (oid `7090743…`, 56477 bytes).
I smudged the real image from `HEAD` with `git lfs smudge` and inspected it. It shows the bug:
the edge labels are clipped on the right ("Yes" shows as "Yes" cut off, "No" as "Nc"), and the node
label "Hold and inspect" is cut to "Hold and inspe".

## After (heavy CI capture)

- "Yes", "No" are fully rendered, with their background boxes enclosing the text.
- "Hold and inspect" wraps to two lines ("Hold and" / "inspect") inside its node and is fully visible.
- "Review telemetry", "Ready?" and "Dispatch fleet" are whole and centred in their shapes.
- Second diagram (Plan → Dispatch → Observe → Correct cycle) is intact. All four nodes, arrows and
  labels are present. Because the first diagram is now about 22 px taller (two-line node), it sits
  lower, but its panel stays fully inside the 720x549 frame. "Diagram source" disclosure is intact.

## Notes (non-blocking)

- The driver's `before-main.png` was saved as an LFS pointer. Future picture proofs should smudge
  the image (`git show <ref>:<path> | git lfs smudge`) before handing it over.
- The second diagram's panel now ends close to the bottom edge of the capture (a few px of margin).
  It is acceptable but leaves little room if the first diagram grows again.
