Head: e33fb594c13db75ffeb3f7df9ca10718839210dd

Claims (all judged at e33fb594):

1. A board started by hand keeps serving after a registered seat moves; a `--seat` board keeps its rule.
   Command: `just scenario --unit surface-board` in the worktree. Output: `ok surface-board (github): 219/219 checks, 246.0 s`.
   The transcript ticks "when the seat moves the board stops by itself, exit 0", "the board whose seats are gone stops by itself, with no request of ours" and "a board started by hand registers a session's seat and keeps serving when that session goes". Log: work/verifier-scenario.log. The code diff (seats.py `follows`, command.py `Seats(projects, follows=bool(args.seat))`) matches spec section 1.
2. Docs match the specification and `board/autosync_api.py` wording: `git diff <base>...HEAD -- docs` shows the web-board.md changes (starting, When it stops, By hand) and the planning-modes.md changes (The board item, new "With no agent" section). Note: the rewrapped lines in web-board.md are long (cosmetic).
3. PR description (posted body equals work/pr-body.md, via `gh pr view 339 --json body`): Summary, Deliverables and Changes match the diff; Known gaps names the surface follow-up. The `<sha7>` placeholders sit in the Test plan checklist, which the CLI fills. No images.
   Note: scenario/README.md has no bullet about this step (grep finds none), so no change there.
4. Review box: `$CHANTIER log CR-376` holds "r3 approved at 059b2dba, committed as e33fb594".

VERIFIED

## Description-only pass (PR 339, head e33fb594c13db75ffeb3f7df9ca10718839210dd)

Head: e33fb594c13db75ffeb3f7df9ca10718839210dd

- Description as posted (`gh pr view 339 --json body,headRefOid`, headRefOid = e33fb594...): renders (sections, table, fold), no images, Known gaps lists the one follow-up, Test plan names e33fb59 or carries from 059b2db with reason. Judged at e33fb594.
- Review box `approved at e33fb59`: `chantier log 376` note "r3 approved at 059b2dba, committed as e33fb594" proves it.
- Code claims carried from the VERIFIED judgment at e33fb594 (unchanged head).

VERIFIED
