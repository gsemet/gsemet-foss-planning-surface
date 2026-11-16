# CR-110 verification

Head: c3d18c3633372c7e6f018049e87389e361e50ad0 (`git rev-parse HEAD` in the worktree).

## Claims

1. Heartbeat 30m on Claude, in `foreman.md` and the README table; Copilot `/every 4m` unchanged.
   Command: `git diff origin/main...HEAD -- README.md skills`. Output: README row "55 minutes" became
   "30 minutes"; `foreman.md` "every `55m`" became "every `30m`"; the Copilot row is untouched.
2. `foreman.md` ends the `/loop` (`stop: true`) right after `land` and on a wake with no Driver run and no
   order undone (30 minutes); a blocked stack or batch counts; the heartbeat goes on while a Driver runs;
   restart on an order's line or `ping`; Copilot case. Seen in the same diff, all present.
3. `driver.md` CI: 3 hours on one head, then `handback <cr> blocked infra: CI still running after 3 hours`,
   with a longer limit from the project's rules. Present. `foreman.md`: a `pong` proves life, not movement;
   3 hours with nothing new gets `stop`. Present.
4. `chief-of-staff.md`: Copilot delete/re-arm at idle; "Recovery" says a stale heartbeat counts only while a
   CR is `working`. Present.
5. `SILENT_MINUTES` 20 to 40 in `hooks/register.tsx`; the test moves from heartbeat 09:30 / "30 min" to
   09:10 / "50 min" against the 10:00 clock (above 40), and the 09:55 case stays below. Read in the diff.
6. CLI unchanged: `git diff --stat` lists only README.md, hooks (2 files) and 3 reference cards.
7. Done when, grep: `grep` does not exist on this Windows shell. Command run instead:
   `Select-String -Path README.md,skills\chantier\references\*.md -Pattern "55"`. Output: no match
   (count 0). It names no heartbeat.
8. `just check`: run in the worktree, output `26 passed in 4.09s`.
9. `just scenario`: not re-run. Read `work/gates/20261106-071847.log`:
   - `github: 172/172 checks passed in 166.6 s`
   - `gitlab: 172/172 checks passed in 166.4 s`
   The transcripts are under the worktree's `scenario/results/`. The log is by the Driver, and I did not tie
   it to c3d18c3 beyond the caller's statement.

## Not proven by execution

`hooks/register.test.tsx` needs the host and `just check` does not run it. I could not run it. Its edit
is checked by reading only. This does not change my word: the change is two constants and a threshold
that read consistent, but it stays a claim without a run.

## Word

VERIFIED (claims 1 to 9 hold; the register test is unrun, as said above).

Cosmetic, not blocking: the new "Recovery" sentence in `chief-of-staff.md` runs past the wrap width.
