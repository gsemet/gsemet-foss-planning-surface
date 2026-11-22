# CR-442 scenario failures at be847cc: diagnosis

Reproduction: `just scenario` in the worktree. Log: work/gates/20261122-020805.log. Transcript:
scenario/results/scenario-20261122-020808-40260.md, with one `<unit>-github.md` per unit in the folder
next to it. Units red: stack (10 checks), gates (3), series-deps (10). Green: release, parallel,
direct, qa-driver, surface-board, gitlab.

No CLI bug found. Every failure is a scenario step that ships a CR the record places on another
CR's branch while its git branch is not on that branch, or a cascade of one. Line numbers are
scenario/run_scenario.py at be847cc. I changed no file and did not re-run after the proposed fixes.
Steps marked UNTESTED were never reached (their function aborted at the first failure).

Two kinds of cause:

- A. The new `push()` (l.861-870) rebases onto `pr_base`, else `start_on`, else main, while
  `driver_round` and `ship` still open the PR on `base or "main"` (l.873-885). A CR that `take`
  started on another CR's branch (`start_on`) is now pushed carrying that CR, but its PR opens on
  main: the old rail "on main and out of draft, carries CR-x" refuses `ship`. Fix: pass `base=`.
- B. A scenario "stack driver" that only retargets the forge (`forge_base`) then `ship`s: the branch
  still sits on main, so the new chain check refuses ("branch not based on CR-x's head"). Fix: rebase
  onto the branch below and push before that `ship` (helper at the end).

## series-deps

1. l.7709 `driver_round(w, b, "series_b.py", "B = 1\n")` (A: b has start_on = a's branch).
   Fix: add `base=w.cr(a)["branch"]` (as l.8548 does). This one line explains all five series
   failures: ship CR-102 exit 2 (its head carries CR-101, PR on main), handback "ready means a PR
   recorded", then the cascade of l.7712-7731 (`take` lease still held, "rebased on the default
   branch", "third starts on the second's branch", blocked question, `order add`).
2. early_conflict, l.7884-7886 (`hand_back(second, 2)`, helper l.7838-7843). In the stack batch the
   second is taken after the first is ready, so it starts on the first's branch. Its worktree
   writes `shared.py` N = 2 against the first's N = 1 and `push()` now rebases onto
   origin/<first branch>: add/add conflict (CalledProcessError, git rebase exit 1). Fix: give
   `hand_back` a filename parameter (`def hand_back(cr, value, name="shared.py")`, l.7838, used
   at l.7842) and call `hand_back(second, 2, "shared_second.py")` at l.7886. That case only checks
   that no merge-tree runs and no `conflict` ask is sent; a real conflict is not its point. The
   parallel case l.7852-7857 has no start_on: unchanged.

## stack

3. stack_batch, l.6659 `driver_round(w, four, "stack3.py", "N = 3\n")` (A: four's start_on is
   three's branch, checked at l.6643). Fix: add `base=w.cr(three)["branch"]`. Cascade: ship CR-104
   exit 2, handback CR-104 ready, then "stack_batch ran to the end" (AttributeError rstrip on a
   None PR). UNTESTED after l.6668: re-ships of four at l.6700, 6714, 6726 (four holds three's
   head: expected fine); l.6770-6771 `forge_base(two, main)` + `ship two` (two holds one's head
   after the restack() calls the CR already added at l.6598-6599: expected fine).
4. base_from_pr, l.6958-6976 (B): `driver_round` one and two on main, `stack`, then
   `forge_base(two -> one)` (l.6964) and `ship two` (l.6976) is refused. Fix: insert
   `rebase_onto(w, two, one)` just before l.6964, keeping the `forge_base` (l.6964) and the ship
   (l.6976). Do not use `restack()` here: it also ships, which would move the `ship` and the forge
   read counts of l.6965-6969. The rebase comes before `w.ready(two, link)` (l.6970); that call
   runs gate and verdict itself at the new head. "base_from_pr ran to the end" (IndexError) is the
   cascade.
5. ready_words_unplaced, checks 6, 7, 8 (l.8730-8751): no problem in the function itself. The fake
   forge keeps PR links across batches; base_from_pr aborted before its l.6979
   `forge_base(link, main)`, so PR #41 and #42 stayed on `chantier/batch-03/cr-101-base-one` (log:
   "waits on the branch ... (no CR of this batch)"). Fix 4 clears it. This function never calls
   `stack` and has no live start_on, so `chain_below` returns None: no new refusal there.
6. ready_words, l.9153-9155 (B): `driver_round` a, b, c on main, then `forge_base(b -> a)`,
   `forge_base(c -> b)`, then `ship b` (l.9162) is refused. Fix: replace l.9154-9155 by
   `restack(w, b, a)` then `restack(w, c, b)` (bottom up; they do forge_base and ship). The later
   ships of b (l.9162-9170) re-ship an unchanged head. UNTESTED after l.9162:
   - l.9213-9222 `ship c` on b's branch: fine once the fix above holds.
   - l.9309-9315 (check 11, forge puts the top PR on a): `driver_round` a, b, c on main, then
     `ship a`, `ship b` in the loop l.9311-9313 (b is stacked under a: refused) and `ship c`
     l.9315. Fix: after the driver rounds (l.9309-9310) add `rebase_onto(w, b, a)` then
     `rebase_onto(w, c, b)`. c's chain neighbour is b although its forge PR is on a: `ship` records
     the forge base a, the chain check reads the chain.
   - l.9336-9354 (check 9, release on the top): `on_branch(w, rel, top branch)` already puts the
     release on the top branch: expected fine.
   - l.9380-9396: parallel batch, no chain check: fine.

## gates

7. gate_carry_stack, l.6385-6396 (B variant): `under` is amended and force-pushed (l.6385-6386) but
   never shipped again, so its recorded head is stale; `over` is rebased onto the new tip and
   `ship over` (l.6396) is refused: "CR-106's branch moved since its last ship (28f4a98 ->
   d97121f): it ships first". That is the rail working as designed. Fix: after the force push at
   l.6386 add `w.chantier("ship", under, w.cr(under)["pr"])` (the stack driver restacks bottom up
   and ships each CR), before the fetch and rebase of `over` (l.6387). Then `ship over` holds the
   recorded head and records the `carry`; the check's `old`, `tip` and gate count comparisons are
   unchanged. The handback refusal ("worktree's head is not the head ship recorded") is the
   cascade.

## Helper to add (git only, no forge, no ship)

Next to `restack` (l.8292), and let `restack` call it for its first three lines:

    def rebase_onto(w: World, cr_id: str, under: str) -> None:
        """The stack driver's git part of a restack: rebase onto the CR under it, push with a lease."""
        c = w.cr(cr_id)
        wt = Path(c["worktree"])
        w.sh("git", "fetch", "--quiet", "origin", cwd=wt)
        w.sh("git", "rebase", "--quiet", f"origin/{w.cr(under)['branch']}", cwd=wt)
        w.sh("git", "push", "--quiet", "--force-with-lease", "-u", "origin", c["branch"], cwd=wt)

## Other sections

release, parallel, direct, qa-driver, surface-board, gitlab are green at be847cc (their series,
stacked and release ships start on main or already hold the CR below: `on_branch`, l.8548's
`base=`). After the edits rerun `just scenario`: the UNTESTED tails above (stack_batch after l.6668,
base_from_pr after l.6976, ready_words after l.9162, early_conflict after l.7886, series-deps after
l.7731) did not run in this build, so another refusal may show up there.
