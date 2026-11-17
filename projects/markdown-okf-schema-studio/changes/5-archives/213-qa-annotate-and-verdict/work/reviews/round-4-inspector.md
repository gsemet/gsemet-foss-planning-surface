# CR 213 — Inspector review, round 4

**Verdict: APPROVE.**

Scope checked: the uncommitted `git diff` in the wt-213 worktree on top of HEAD ed239750. Two
files changed, nothing else (`git status --short`):

- `.agents/skills/markdown-studio-exploratory-qa-claude/references/qa-bug-template.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scripts/qa.mjs`

## 1. Padding sentence (qa-bug-template.md, "How to annotate")

New text: "When the shot has `--annotate`, a `--clip SELECTOR` gets 34 px of padding instead of 12, so
a label fits outside the outline."

This matches the code:

- `qa.mjs:195`: `resolveClip(page, session, options.clip, options.annotate ? 34 : 12)`
- `qa.mjs:294–304`: `pad` is used only in the selector branch. Numeric `x,y,w,h` and `preview`
  clips ignore it, so saying `--clip SELECTOR` is accurate.

The paragraph is rewrapped. Added lines are 96, 99 and 59 chars, all ≤100. The round-3 140-char line
is gone.

## 2. `drawAnnotations` comment (qa.mjs)

New comment: labels are tried outside the outline above, then below, else inside its top-right
corner. The first spot inside `bounds` that touches no other frame or label wins. If none fits, the
label goes above, with a warning.

This matches the code:

- `spots` is ordered as follows:
  - above: `f.y - h - 2`
  - below: `f.y + f.h + 2`
  - top-right inside: `f.x + f.w - w - 4`, `f.y + 4`
- `spots.find(free)` takes the first spot that fits.
- `free` checks `bounds` and `hit` against the other frames and the labels already placed.
- The fallback is `spots[0]` (above) plus a warning.

"Strictly" is dropped, which was the round-3 nit.

Only comment lines changed: all four `-` and five `+` lines in qa.mjs start with `//`. The added
lines are 97, 100, 97 and 24 chars, all ≤100. `node --check scripts/qa.mjs`: OK.

## Round-3 finding

The required change (line 173 over 100 chars, and the misleading 34 px condition) is resolved. The
optional `drawAnnotations` wording nit is also resolved. The other round-3 nits were explicitly
optional and are left as they are, which is fine.
