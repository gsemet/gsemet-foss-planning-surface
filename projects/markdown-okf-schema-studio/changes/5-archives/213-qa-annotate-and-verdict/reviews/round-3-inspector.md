# CR 213 — Inspector review, round 3 (final)

**Verdict: CHANGES REQUESTED (doc-only, about 2 minutes, no code, no reshoot).** The code and both
proofs are good, and every round-2 item and nit is done. One prose line breaks the 100-char gate,
and the same sentence misstates when the 34 px padding applies. If no further round is possible,
treat this as an open point the driver can fix while squashing. It is not a reason to block.

What I checked myself: the full `git diff HEAD` in the wt-213 worktree against c1399a18. Only
`.agents/skills/markdown-studio-exploratory-qa-claude/` changed: SKILL.md, charters.md,
scenario-format.md and scripts/qa.mjs are modified, and `bug-sheet-template.md -> qa-bug-template.md`
is a staged rename. `git status` shows nothing outside the skill. No `bug-sheet-template` reference
is left under `.agents` outside the archives. I opened both proof images.

## Gates (run by me)

- `node --check`: 8/8 `scripts/*.mjs` OK.
- Python: 4/4 files parse (`ast.parse`, so no `__pycache__` was created and none exists).
- `bash -n`: `setup-workspace.sh` and `q` OK.
- Scenarios: 22/22 parse as JSON.
- linkcheck.py: 18 links, 1 broken. It is the `…` placeholder at
  `references/harness-pitfalls.md:83`, which was already there and is not in this diff. The anchor
  `qa-bug-template.md#how-to-annotate` matches the `## How to annotate` heading.
- 100-char prose: **1 failure**, `references/qa-bug-template.md:173` (140 chars). All the other long
  added lines are tables, `FINDING` return lines, the alert link line or code.

Cleanup: `pgrep -fl msq-cr213` is empty and `/private/tmp/claude-502/cr213-driver/qa` does not exist.

## Round-2 items, verified

1. **Selector clip padding.** Fixed. `shot()` calls `resolveClip(..., options.annotate ? 34 : 12)`,
   and `resolveClip(page, session, clip, pad = 12)` uses it only for the selector branch. The new
   clip proof shows the red label above the outline, outside it and not cut off. The outline is
   about 830/1000 px of the image wide, which matches w=290 + 8 px of margin inside a 358 px clip
   (290 + 2 × 34). This is consistent with the printed box x=797 y=294 w=290 h=22.
2. **Nearby-text limit.** Documented in qa-bug-template.md, and in charters.md right after "Check
   the printed boxes and open the image once."
3. **Example is the proof command.** It is the same in qa-bug-template.md and charters.md: red
   `aside[data-okf-github-alert] ~ p` "Defect: lazy line leaves the Note", green `blockquote`
   "Works: quote keeps it". The full proof matches it.

The nits are all done:
- A bare `--annotate` throws `annotate: --annotate needs a selector or x,y,w,h`. A bare value is
  `true` in the list.
- An unknown `--color` warns and falls back to red.
- `--which` is clamped with `Math.min(..., visible.length - 1)`. With no visible preview the index
  is `-1`, which gives `undefined`, so the check is skipped safely.
- The wording now reads "outside their outline when there is room (above, then below), else inside".

## Done when (00-request.md), item by item

- [x] `q shot … --annotate … --note …` draws an outline at the selector's real position, proven on
  a real shot. Both proofs show correctly placed outlines in a clean state.
- [x] SKILL.md opens with the purpose. Sheets carry Verdict, Requirements and "Why this is wrong"
  (template line under the title, a section, charters.md method). The index has "Decisions for the
  owner".
- [x] `references/qa-bug-template.md` replaces `bug-sheet-template.md`, and every link is updated.
- [x] Syntax gates, scenario JSON and the relative-link check pass. The only broken link is the
  pre-existing placeholder.
- Parts 2 (items 1–7), 3 and 3b are present:
  - each proposal section has its own `Uncheck to disagree: [x]`;
  - there is a "No test: <reason>" block with its tick;
  - the balance rule is in the template and in SKILL.md;
  - the fix CR carries out only the ticked sections;
  - the owner's example is there, introduced with "Example, from another finding".

  "How to annotate" is in the template and in charters.md, and the overlay design choice is
  documented. There is no front matter, only the plain line under the title.

## Required change

1. **`references/qa-bug-template.md` lines 172–175 ("How to annotate").**
   - Line 173 is 140 chars.
   - "With `--clip SELECTOR` the clip gets 34 px of padding (12 px otherwise)" reads as if a
     selector clip always gets 34 px. The code uses 34 px only when the shot has `--annotate`.

   Rewrap and reword, for example:

   ```
   the note if it hides something that matters. When the shot has `--annotate`, a `--clip SELECTOR`
   gets 34 px of padding instead of 12, so a label fits outside the outline. An empty box is an
   error; a box outside the clip or the visible preview is a warning. `--which N` picks the
   preview, as for `q box`.
   ```

## Optional nits (fine to leave as they are)

- `scripts/qa.mjs`: the `drawAnnotations` comment still says "placed strictly outside their outline:
  above, below, inside the top-right corner". Drop "strictly", in the same way as the doc wording.
- An unknown colour is warned about only for CLI `--color` values. An object-form `{at, color}`
  with a typo turns red with no warning. This is harmless.
- `resolveClip` runs before `annotations()`. So with a bare `--annotate`, the error comes after the
  clip is resolved, with 34 px of padding. The shot is not taken, so this has no effect.
