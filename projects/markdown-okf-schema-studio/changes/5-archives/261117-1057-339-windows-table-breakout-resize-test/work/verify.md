# Verify CR-339

Head: 390f6ed5e9e9c1ce5b85d4077b69934d29a5c539

Base: 68f36c384fc0fba1dca66fee8d835dcf59292e4e (origin/main, equal to the merge-base).

## Claim 1: fails at base, passes at head on Windows (judged at 390f6ed and 68f36c3)

Command (both worktrees): `npx tsc -p .` then `node scripts/node-test.mjs unit "out/test/page/tableBreakout.test.js"`.

- Base (detached worktree, node_modules junction): `pass 5 / fail 1`; `Auto measures a table again on a real resize while a cell is edited` failed with `AssertionError: light: the breakout follows the pane (705 then 727 px)`.
- Head: all 6 pass, including that test (635 ms); `ℹ pass 6 / fail 0`.

PROVED. Linux: CI run 44066835282 at 390f6ed, `gh pr checks 407`: static pass, static-windows pass, visual pass, report pass.

## Claim 2: only test/page/tableBreakout.test.ts changed (390f6ed)

`git diff --stat origin/main...HEAD`: `test/page/tableBreakout.test.ts | 6 ++++--` (1 file, 4 insertions, 2 deletions). PROVED.

## Claim 3: PR description (posted body equals work/pr-body.md except one blank line)

Matches the diff: 760 becomes 600, `<= 600`, a comment. Renders; no role names; Known gaps has the Linux item.
FAILED parts:
- Deliverables table gives widths for Verdana, Arial, Consolas (797, 722, 720, and 568 at 600 px). Only Segoe 705 then 727 at 760 is reproduced here (base run). The rest comes from the debugger's probe notes, not proof at this head; also "640 and 700 px also pass". Mark them UNVERIFIED in Known gaps or narrow them.
- Test plan says "`just format`, `just check-limits check-markers`: pass" at no head: the only gate log (work/gates/20261117-112644.log) is `just preflight` at a18fc89f, not 390f6ed, and covers none of those commands. No gate pass at the head.

Evidence: no visual change, no screenshots (Impacts: "No visual change"). Base worktree removed.

NOT VERIFIED

## Description pass at 390f6ed5e9e9c1ce5b85d4077b69934d29a5c539

Head: 390f6ed5e9e9c1ce5b85d4077b69934d29a5c539

- Description read with `gh pr view 407 --json body`; diff `git diff origin/main...HEAD`: one file, test/page/tableBreakout.test.ts, 760 to 600 and `<= 600`; Changes matches, nothing unmentioned.
- Font claims: 705 then 727 reproduced in the base run above; Verdana/Arial/Consolas widths and the 640/700 px passes are marked UNVERIFIED in Deliverables and listed in Known gaps. Checked.
- Local gates line: `git range-diff origin/main...a18fc89f origin/main...HEAD` shows `1: a18fc89f = 1: 390f6ed5` (patch unchanged by the rebase), so the preflight pass at a18fc89 (gates/20261117-112644.log, first line names CR-339 and a18fc89f) is correctly carried. tsc and the 6 of 6 test run at head: proven above.
- CI at 390f6ed: `gh pr checks 407`: static, static-windows, visual, checks, report pass (head oid 390f6ed).
- Known gaps lists the Linux gap and the unverified fonts. No STALE mark. Review box unchecked, not claimed.
- Verdict: VERIFIED
