# Verify CR-304 (round 2)

Head: f11132b20f3f7872e5b5184a1259f93a489c0838

Base (before): faa47192defd011e38a669df019fbc4b3d33da25 (= origin/main = merge-base; detached worktree
`batch-22-CR-304-verify-base`, removed by the Driver's cleanup, not touched here).
Move judged: 7c96789..f11132b (clean rebase onto new main plus new commit f11132b). Claims are judged at
f11132b unless a line says `carried`.

How the browser checks ran: `uv run --script work/verifier/verify_board.py` (all checks, four sizes; I added
`memberW` to its group probe and moved the scratch to `scratchpad/run3`) and
`uv run --script work/verifier/verify_drag.py` (check 4, 2940). Both start two live boards (base worktree and
head worktree) over scratch copies of `docs/demo/` outside the repo, drive them with Playwright Chromium and stop
them by PID. Screenshots `evidence/{before,after}-<size>-<check>.png` were overwritten by this run.

## Claims

1. Panel closes on a view change (check 1) - PASS at f11132b (2560, 2940, 1400, 375).
   After: left bar to Home panel open false; "see the batch" false; Back false; dirty edit then left bar: dialog
   asked true, stay view=kanban, panel open true, edit kept true. Before at 1400: left bar true, see-batch true,
   Back true. Phone: no openable on Home (`c1_home_openables: 0`), so "see the batch" not run; bar tap by JS click
   (`covered_view_clicks_by_js`: home x6), as in round 1.
2. No horizontal scroll bar on hover (check 2) - PASS at f11132b (2560, 2940, 1400): 18 cards hovered,
   `c2_hovers_showing_hbar` 0 at each size, tilt 18/18.
3. Card width (check 3, the round-1 failure) - PASS at f11132b. `c3_pi_widths` after:
   - 1400: every card in inbox, P1, P2, P3, P4, 3-ready is 291 px (inbox column 331); P1 group members 291
     (frame 305), same as a loose card. P3 six cards in six rows (the column is 418 wide).
   - 2560 and 2940: all cards 320 px; group members 320 (frames 1304, 1632); P3 six cards in 2 rows; DOM order
     equals visual order; members inside the frame.
   - 375: all cards 262 px, group members 262; `.tri` swipe kept (overflow-x auto, scrollW 930 > clientW 351).
   Screenshots read: `after-1400-c3-triage.png` shows equal card widths in the three columns and in the
   group frames; `docs/web-board/triage-pc.png` (the new head's picture) shows the same.
4. Drag and drop (check 4) - PASS at f11132b (2940). `verify_drag.py` output `same_diffs: true`: an inbox
   card dropped on a P3 card (group dialog, `newgroup`) and the P1 group `checkout-polish` dragged by its handle
   to P2 give the same file changes before and after. (The `verify_board.py` c4 group drag, which grabs the
   first handle `api-hardening` in the inbox, timed out at 2940: the handle is covered at that point; the
   dedicated script, which targets the P1 group, passes and is the check.)
5. Frontmatter never shown (check 5) - PASS at f11132b (all sizes): Triage and Kanban show the card-0 and fm-p1
   paragraphs, `shows_raw_frontmatter` false; before at 1400 it is true on both. Home lists neither item in the
   demo (same as round 1).
6. Wide table in the panel (check 6) - PASS at f11132b: panel 1152 (2560), 1323 (2940), 680 (1400), 375;
   table right edge inside the panel (2523 <= 2546; 2903 <= 2926; 1363 <= 1386; 352 <= 375); page horizontal
   scroll false everywhere; before at 1400 the table ran out (1554 > 1386).
7. `description()` test - PASS at f11132b. `uv run --no-sync --project . pytest
   skills/chantier/scripts/cli/tests/test_board_description.py -q` gives `7 passed in 0.26s`. The new
   `empty-frontmatter` case (`"---\n---\nThe text.\n"` gives `The text.`) passes with the regex
   `\A﻿?---[ \t]*\n(?:.*?\n)?---[ \t]*(?:\n|\Z)`; the BOM case is now written `﻿` explicitly. Before
   (carried from 7c96789): on main's code 4 failed, 2 passed; the new case is a fresh frontmatter shape main
   does not handle, as main strips no frontmatter at all.
8. PR body `work/pr-body.md` against the diff at f11132b (`git diff --stat origin/main HEAD`: 10 files) - PASS
   apart from the two intended placeholders (`<sha7>` in the Test plan, picture "attached below once pushed").
   Beyond them: the Known gaps bullet "the full scenario run is not yet done at this head" is stale once CI is
   green (CI at f11132b: just scenario ubuntu-latest green per the brief); the Driver should tick or drop it.
   Summary, Deliverables, Changes and the 291/320 px numbers match the measured widths above.
9. Not run here: `just check`, `just scenario`, CI (the brief says green at f11132b); `just docs-screenshots`
   (the picture in the diff was read, not regenerated).

## Verdict

VERIFIED
