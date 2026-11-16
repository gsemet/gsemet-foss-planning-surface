# Verify CR-184 gate-proof-cli-fixes

Head: 1f269b21c140a0c1e1fe40cafee983b7ca1c5fce (pushed head of PR 121; worktree clean)

Method: I ran the worktree's CLI (skills/chantier/scripts/cli/chantier.py of the worktree, via the
scenario's World, which resolves SKILL from the worktree) in a temporary scratch repo with a fake
forge, never in the main checkout. I drove only the steps `gate_proof` and `restore_cr`
(script: scratchpad run184.py, imports scenario/run_scenario.py). Result: 20 passed, 0 failed.

Long gate, cited and not rerun: work/gates/20261111-225414.log: `just check` 45 passed;
`just scenario` github 558/558 and gitlab 558/558, at 1f269b2 (log written by the older
main-checkout CLI, so it has no header line: expected). I did not rerun the suite.

Claims, each judged at 1f269b21c140a0c1e1fe40cafee983b7ca1c5fce:

1. Gate log first line = `gate CR-n branch ... <40-char HEAD>`, event holds the same SHA, last line
   `result: pass`: proved (check 1 of gate_proof).
2. core.abbrev 12: gate, ship, verdict, handback ready succeed, CR head is 40 chars: proved.
3. `gate` on a modified or untracked file exits 2, runs nothing ("a gate binds to a commit, commit
   first"; event count unchanged): proved.
4. A gate command that commits: exit 4, "head moved", no pass at either head: proved.
5. `handback ready` exit 2 with the named cause for a commit after ship ("the worktree is at ee86f98,
   not at 1e1a3d5"), a dirty tree, a head not pushed ("origin/... is not pushed"), and a gate passed
   only at an earlier head ("no long gate passed at <40-char sha>"); with `--no-gate` the first three
   still refuse: proved (6 refusals asserted).
6. Short-head events and record from before the change still reach `handback ready`: proved.
7. spent_usd >= budget_usd: `round` exits 5 "budget spent: $2.00 of $1.0; only the user raises it",
   round count unchanged, nothing logged; the budget message wins when the limit is reached too;
   gate, ship, note, verdict, handback still work; within budget the round-limit refusal keeps
   its own message; with no budget, round unchanged: proved. (Cosmetic: "$1.0" vs "$2.00" format.)
8. `restore 6-trash/<stamp>-<slug>` gives `1-inbox/<slug>` with files, STATUS.md updated; a former
   batch CR loses its number and keeps `formerly CR-n of batch-m`; a plain `2026-plan` keeps its
   number: proved.
9. A name clash exits 2 with nothing moved, `--slug` resolves it; an item of `5-archives` is refused
   ("restore takes a folder directly under 6-trash"): proved.
10. Restored cancelled CR of a paused batch: stays cancelled, one-line note on branch, worktree and
    PR; `close` without `--yes` still runs: proved.
11. A number taken off a restored folder is never reused (restored.json): proved.
12. Cards consistent: diff touches driver, foreman, concepts, worker, griller, chief-of-staff, rails
    docstring and the `round` help; no agents/ file changed (`git diff --stat origin/main`): judged
    by reading the stat and the PR body; not re-read line by line.
13. PR description (gh pr view 121 at headRefOid 1f269b2): clean, sections and fold render in
    Markdown; Summary, Deliverables and Changes match the diff (commands.py, rails.py, state.py,
    status.py, cli.py, cards, scenario steps); gate numbers (558/558 each) match the gate log. The
    `Verified at <sha7>` box is for the Driver to fill after this verdict; the "Review: approved at
    1f269b2" line rests on the review notes, which I did not re-judge.

VERIFIED
