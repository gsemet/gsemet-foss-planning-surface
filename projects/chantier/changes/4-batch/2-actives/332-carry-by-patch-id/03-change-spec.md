---
type: cr-change-spec
description: The carry of a long gate pass and a verdict over a rebase compares the exact patch-ids of the CR's own commits, and is recorded when the moved head is shipped, the restack included.
---

# Change Specification: the carry compares patch-ids and is recorded at the restack

## Goal

In batch-23 the CLI refused to carry a pass over a rebase whose patch-id was identical (CR-316:
`handback refused: verdict does not carry (CLI says rebase changed patch though git patch-id
identical)`). That cost a second long gate and a second Verifier for nothing. Six CRs also ended the
batch with no verdict at their final heads. The stack driver restacked them after their hand-back,
and nothing recorded that their pass and verdict carried to the new heads.

The user's decisions (`02-answers.md`):

- carry-Q7, "as filed": the verdict carry compares the patch-id, not the diff text, and the carry
  is recorded at the restack.
- carry-Q8: the exact patch-id, `git patch-id --verbatim` (git 2.39 or later). An older git is
  refused with its reason. A rebase that changes only whitespace does not carry.
- carry-Q9: the CR's own commits are the commits above the base it was judged on. That base is
  recorded with the gate pass and the verdict. A change in the CR below does not break the carry
  when this CR's own commits did not change.
- carry-Q10: a resolved conflict (a `conflict-resolver` ran) still gets a new long gate and a
  Verifier, even with equal patch-ids. The cards keep that rule, and the carry holds only for a
  rebase with no conflict.
- carry-Q11: the one-time cost is accepted. CRs judged before this CR merges have no recorded base,
  so they get a new long gate and Verifier at their next move. This PR's Known gaps names it.
  take-base-nearest-pr's "a clean move costs no gate" holds from the batch after this merge.
- batch-Q8: the CR joins the next batch, with the other retro points of batch-23 and the four board
  CRs of 2026-11-17. The batch's make-up is the Chief of Staff's to set; this CR does not set it.

## Why the current check refused CR-316

`carry_check` (`skills/chantier/scripts/cli/src/chantier/commands/crs.py`) replays the judged head
`g`'s commits onto the base with `git merge-tree --write-tree --merge-base <merge-base(g, base)>
<base> <g>`. It asks for the head's exact tree, and for as many commits in `merge-base(g, base)..g`
as in `base..head`. CR-316 was started on CR-311's branch and moved onto CR-315's. Two things
went wrong:

- `merge-base(g, base)..g` held commits that were not CR-316's (CR-311's, under SHAs the new base
  does not have);
- `handback` takes `base` from `stack_base(record, c, repo)` without `planned`, so the base it
  compares against is the branch the CR started on (`stacks.py:155-156`), not the one it was moved
  onto.

So the count or the tree differed, although CR-316's own patch did not change. The method measures
a range, not the CR's own commits. Q9's recorded base defines those commits. The new head's base
is the branch it was moved onto.

`git cherry` is not used: it matches commits by the default `git patch-id`, which ignores whitespace
and line numbers, and Q8 asks for the exact one. The judged side's own commits come from the base
recorded at judgment (Q9), so no patch-equivalent commits need filtering.

## What changes

### 1. The bases (`commands/gate.py`, `commands/gate_run.py`, `commands/delivery.py`; `stacks.py` read-only)

**One rule (settled by the Chief of Staff, `02-answers.md`): a head's base is the branch the head
actually sits on.** Three candidates are tried, read in the CR's worktree:

- the start base, `stack_base(record, c, repo)`;
- the PR's base as `ship` last read it, `c.pr_base`, when set;
- the planned place, `stack_base(record, c, repo, planned=True)`.

For each candidate whose remote tip `<remote>/<branch>` is an ancestor of the head (`git
merge-base --is-ancestor <tip> <head>`), the base is that tip's SHA. When several are ancestors,
the base is the one nearest the head: the tip that every other ancestor tip is itself an ancestor
of. When no candidate's tip is an ancestor of the head, no base is recorded.

`c.pr_base` alone is not enough: only `ship` writes it (`delivery.py:170-172`). In a restack the
stack driver runs `ship` before `forge-stack rebuild` retargets the PRs (`driver.md:843-849`,
878-881), so a gate or a verdict run in that window would record the old base. The rule above
finds the base from git, whatever the forge or the record last said.

The same rule gives the base in both places:

- **At judgment.** Every `gate` event and every `verdict` event gains `base: <full SHA>`. "Every
  `gate` event" means each of them: the `pass` and `fail` events of a stopped run
  (`gate.py:143-150`), its `stopped` event (`gate.py:151`), the results and the `moved` event of a
  finished run (`gate.py:174`, `176`), and `gate_run.py:108`. The base is read once per invocation,
  at the gate's start, at `g.start`, and written on every event of that run. A verdict's base is
  read at `verdict` (`delivery.py:62`). With no base found, the event carries no `base` key and is
  still logged as now.
- **At `ship`, for the moved head.** After a rebase onto its planned place, that place's tip is
  an ancestor of the head and the nearest one, so the rule finds it. The stale forge base the PR
  still shows before `rebuild` changes nothing. The `carry` event records this base (§4).

### 2. The carry check: exact patch-ids of the CR's own commits (`commands/crs.py`)

`carry_check` takes the judged head with its recorded base, and the new head with its base from
§1. It returns None when the pass or verdict at the judged head carries, else the reason, which
goes in the existing `does not carry: <why>` clause. It uses one method, git's exact patch-id,
and no other.

- The CR's own commits are `<g's recorded base>..g` at the judged head `g`, and
  `<the new head's base (§1)>..head` at the new head. Both are listed oldest first
  (`git rev-list --reverse`).
- Each own commit's patch-id is `git patch-id --verbatim` of that commit's diff. One pipe for a
  range is fine: `git log --reverse -p --no-merges --format="commit %H" <range>` into `git patch-id
  --verbatim`. Git computes it; the CLI never compares diff text.
- The pass or verdict at `g` carries when both lists of patch-ids are equal, in order.
- The reasons, one line each:
  - `git <v> is older than 2.39: no patch-id --verbatim to prove it`. `PATCH_ID_GIT = (2, 39)`
    replaces `MERGE_TREE_GIT`; `git_version` stays;
  - `the pass at <g7> recorded no base: run the long gate again`, or `the verdict VERIFIED at
    <v7> recorded no base: verify again`. This covers an event from before this change, which is
    the one-time cost of Q11, and an event whose base git could not resolve. Nothing is guessed,
    because chantier takes no fallback;
  - `the rebase changed the patch`: the lists differ (a commit added, dropped, edited, squashed or
    reordered, or a whitespace-only change);
  - `a merge commit in <g7>'s commits` or `a merge commit in <head7>'s commits` (`git rev-list
    --merges` over that side's own range): a merge commit has no patch-id, so nothing is proved;
  - `the rebase resolved a conflict` (§3);
  - `<ref> cannot be read`, when git cannot resolve a ref. It is raised as the `ChantierError`
    that `facts.py` already catches, and `ship` catches it too (§4).
- Removed with the old method: `_replay`, the `merge-tree` call and `MERGE_TREE_GIT`. The
  Foreman's own `git merge-tree` conflict check (`foreman.md`, the early conflict check) is
  unrelated and unchanged.
- Following Q9, a change below the CR does not break the carry when the CR's own commits are
  unchanged. Examples: a lower CR rewritten into the new base, the CR moved onto a different CR's
  branch (CR-316), or a dropped CR's commits removed with `rebase --onto`.

### 3. A rebase that resolved a conflict never carries (Q10): `ship --conflict`

The CLI cannot see in git that a rebase had a conflict, so the one who resolved it says so, under
one general rule. **Any `ship` after a rebase during which a conflict was resolved takes
`--conflict`.** This holds whoever resolved it (a `conflict-resolver`, or the Driver itself) and
whoever runs the `ship` (a CR's Driver, the stack driver, the release Driver). It covers a rebase
for any reason: a `rebase:` note, `stacked on`, a mode switch, a restack, an insertion, a drop. The
`ship` event records `conflict: true`.

A `ship --conflict` voids every judged head and every carry recorded before it, for both the gate
and the verdict:

- `last_gate_pass` and `last_verdict_head` (§5) consider only the `gate`, `verdict` and `carry`
  events after the CR's last `ship` event with `conflict: true`;
- `carry_at` returns None at that head and at any head before it.

Only a long gate pass and a `VERIFIED` verdict at a head shipped after the conflict can carry
later. A later clean restack therefore never carries a pass or a verdict from before the conflict.
`handback_refusals` and `_carried_lines` give the reason `the rebase resolved a conflict` when the
last judged head they would carry from comes before such a `ship`.

The `declare` help text for `ship` names the flag. Shipping the same head again without the flag
clears nothing: the first `conflict: true` at a head stands.

### 4. The carry is recorded when the moved head is shipped (`commands/delivery.py`, `ship`)

A Driver runs `ship` after its own rebase, and the stack driver runs it for every CR it moves
("Recording a restack", step 3 of "After a partial merge"). The carry is recorded there. A CR that
the stack driver restacks after its hand-back therefore keeps a proven pass and verdict at its
final head, with no new hand-back.

At `ship`, once the head is read, for the long gate and for the verdict separately:

- **Nothing more** when the head has its own (`gate_passed(events, head)`; `last_verdict(events,
  head) == "VERIFIED"`) or a `carry` already recorded at it (`carry_at`, §5).
- **Otherwise**, when the CR has a judged head (`last_gate_pass`, `last_verdict_head`, §5) and this
  `ship` has no `--conflict`, `ship` runs `carry_check` from that judged head and its recorded base
  to this head and its base (§1).
- **A ref that cannot be read** (the `ChantierError`) is caught. `ship` then logs no carry and
  prints `off: the pass at <g7> does not carry: <ref> cannot be read` (and the verdict's line). The
  PR link, the head, the base and the draft flag are still recorded and the `ship` event is still
  logged, as now.
- **When at least one carries**, `ship` logs one `carry` event for the CR, after the `ship` event,
  in the same `RenderedBatch`. Its keys:
  - `head`: the full head;
  - `base`: the full SHA of the new head's base (§1);
  - `gate_from` and `verdict_from`: the full SHA of the original judged head, which is the
    `gate_from` or `verdict_from` of the `carry` it chained from, when it chained.
  Only the keys that carried are written.
- **What `ship` prints:**
  - one line `carried: long gate and verdict from <sha7> (clean rebase onto <the base
    branch>)`. When only one carried, or the two came from different heads, the line is
    `carried: long gate from <g7> …` or `carried: verdict from <v7> …`;
  - for one that does not carry, an `off:` line: `off: the pass at <g7> does not carry: <why>`, or
    `off: the verdict VERIFIED at <v7> does not carry: <why>`;
  - the existing `off: no long gate passed at <sha7> (`chantier gate`)` is not printed when the gate
    carried.
- **A release CR** has no verdict: only its gate is carried. A CR with no judged head yet logs no
  `carry` and prints no carry line.
- `ship` keeps no git write and reads no forge beyond its existing `read_state`.

### 5. One explicit reader of a recorded carry; the existing readers stay

`core/heads.py` `gate_passed` and `commands/crs.py` `last_verdict` keep their meaning, unchanged:
only the head's own `gate` and `verdict` events count. So does the scenario's helper `gate_passed`
(`scenario/run_scenario.py:3431`, used at 3513 and 4462), which wraps the CLI's.

There is one new reader, `carry_at(events, head)` in `commands/crs.py`. It returns the last `carry`
event at that head, or None. It also returns None when a `ship` with `conflict: true` is at or after
that carry (§3). It is called explicitly by:

- `ship` (§4): it logs no second `carry` at a head that already has one.
- `commands/driver_checks.py` `handback_refusals`:
  - before the gate check (line 221) and the verdict check (line 225), a `carry_at(events, head)`
    with a `gate_from` sets `basis.carried`, and one with a `verdict_from` sets
    `basis.verdict_carried`; each skips its check;
  - otherwise `_gate_missing` and `_verdict_missing` run as now, with the new `carry_check` and the
    new head's base by §1's rule (in place of the start base);
  - the `handback` event records `gate_from` and `verdict_from` (the original judged head);
  - the ready line stays `long gate and verdict carried from <sha7> (clean rebase onto <base>)`;
  - the refusal texts keep their form: `refused: no long gate passed at <head> (the pass at <g7>
    does not carry: <why>) (gate …`, and the verdict's.
- `commands/facts.py` `_carried_lines` (`handoff`'s boxes; the loop at lines 173-181): a
  `carry_at` with the key gives `carried from <sha7> (clean rebase onto <base>)` directly. Only
  when there is none does it call `carry_check`, with the new head's base by §1's rule.
- `status/gate.py` `gate_view`: a new branch between the `passed` branch (line 119) and the
  hand-back's `gate_from` branch (line 121). A `carry_at(mine, c.head)` with a `gate_from` gives the
  state `carried` with the head `gate_from[:7]`, at any status, before a `handback ready` too. The
  words are `carried from <sha7>`. A pass of the head's own still shows as `passed`.
- `status/steps.py` `step_entries`: a `carry` event makes the step `("Carried", "", "long gate and
  verdict from <sha7>")`, or the one that carried. `STATUS.md`, `STATUS.json`'s `steps`, the pane
  and the board then show the carry at the moment of the restack.
- `commands/crs.py` `last_gate_pass` and `last_verdict_head` return the judged head to carry from,
  with its base. That head is the latest of the head's own passes or `VERIFIED` verdicts and the
  `carry` events with that key, after the last `ship --conflict` (§3). The next restack then compares
  with the last head shipped, on the base recorded there. A later `NOT VERIFIED`, at a later head
  or at the same one, still blocks any verdict carry, as now.
- `board/state.py`: `carry` joins `EVENT_KINDS`, so the board's journal lists it. `EVENT_KEYS` is
  unchanged: the journal shows its time, actor, kind and CR, as for a `ship`.
- `evals/kit/audit.py`, check C7 (lines 418-438): a `carry` event at the CR's head counts like a
  hand-back's `verdict_from` or `gate_from`. The check's label names it ("or a `verdict_from`
  hand-back or `carry`"), and so does `evals/SCORECARD.md`'s C7 row if it names the hand-back keys.

Only `ship` writes a `carry` event. No new command; one new flag, `ship --conflict`.

### 6. Cards and docs

Replace the replay wording everywhere, say that `ship` records the carry, and state the
`--conflict` rule once:

- `skills/chantier/references/driver.md`:
  - the long-gate bullet, lines 209-215:
    - "the replay of the gated commits onto the base is clean and gives the head's tree" becomes
      "the CR's own commits, above the base recorded with the pass and the verdict, have the same
      exact patch-ids";
    - `ship` records the carry as a `carry` event, and `handback ready` reads it;
    - the general rule of §3 is stated there once: any `ship` after a rebase during which a
      conflict was resolved takes `--conflict`, and that head and every judged head before it never
      carry.
    The places that rebase (lines 655-665, 676-678, 686-689, 691-697, 750-757, 840-842, 876-880,
    893-904) refer to that rule and repeat nothing;
  - line 658: "which `handback ready` checks with git" becomes "which `ship` records
    (`carried:`)";
  - line 677: "checked by `handback ready`" becomes "recorded at `ship`";
  - line 697: "only when the carry does not hold" gains "(`ship`'s `off: … does not carry` line)";
  - the stack driver's "A clean restack" sentence, lines 751-753: each moved CR's `ship` records
    the carry; read it in that CR's `carried:` or `off:` line;
  - the drop, lines 902-904: "a drop's `rebase --onto` changes the commit count, so it never
    carries" becomes "a drop carries when the CR's own commits are unchanged, as `ship` says";
  - "Recording a restack": the `restack: judged at <head7>` note is also due after a `carried:`
    line, since the carry is the judgment.
- `skills/chantier/references/concepts.md`:
  - lines 379-381: the carry is proved by exact patch-id above the judged base and recorded at
    `ship`, and "a rebase with a conflict needs a new gate" stays, naming `--conflict`;
  - line 393;
  - line 611, in the same words as the verifier card.
- `skills/chantier/references/verifier.md` lines 32 and 100: "proved by git at `handback ready`"
  becomes "proved by git's exact patch-ids, recorded at `ship`".
- `skills/chantier/references/status-layout.md` lines 30 and 122: `carried from <sha7>` can show
  before the hand-back (after a restack), and the "Carried" step appears.
- `docs/gates.md` lines 13-15. `scenario/README.md` lines 246-251: unit 12f's text, and the old-git
  test, now at 2.39.
- `agents/` and `com.github.copilot/agents/` are not touched: the contract is in the cards.

## Out of scope

- The other retro points of batch-23: `take`'s base on the nearest CR with a PR, the Driver's
  pre-push checks, the force-push allow rule, the prompt skeleton's `writes:` line. Each is its own
  CR.
- Any change to when a `verifier` or an `inspector` is due, beyond what the carry result and
  `--conflict` decide.
- Carrying anything over a merge of the base into the branch: merge commits never carry.
- The Foreman's early conflict check by `git merge-tree`.
- Rewriting batch-23's record, or adding bases to past events (Q11).

## Evidence

- `just check` and `just test` pass, `just test` within its budget (AGENTS.md). The CLI's files
  stay within the structure tests' line limits.
- **`--verbatim` and git 2.39.** The PR's Internal references cite git's 2.39 release notes, the
  line that adds `git patch-id --verbatim`. This is the source of `PATCH_ID_GIT = (2, 39)`.
- **Unit tests** in `skills/chantier/scripts/cli/tests/`:
  - `test_gate_carry.py`:
    - The old-git test becomes the 2.39 one (`git 2.38.1 is older than 2.39`, `no patch-id
      --verbatim`), and the version-reading test stays.
    - A new parametrized test runs on a small prepared git repository (in `tmp_path`, few commits,
      fast) and calls `carry_check` in-process, with these cases:
      - (a) CR-316's real shape: a CR judged on one CR's branch, with that base recorded, then moved
        onto a different CR's branch whose history holds the first CR rewritten. Called with the
        base §1's rule finds (the second CR's tip), it carries;
      - (b) a commit added after the judged head: `the rebase changed the patch`;
      - (c) a whitespace-only change to one commit: `the rebase changed the patch`;
      - (d) a merge commit in the range: `a merge commit in …`;
      - (e) no recorded base: `recorded no base`.
    - The round's notes show the old method refusing case (a) once, on the same repository. That
      run is a note, not a test.
  - `test_cli_units.py`:
    - `carry_at`: the last `carry` at the head;
    - `last_gate_pass` and `last_verdict_head` with `carry` events: a carry is a judged head, and a
      later `NOT VERIFIED` blocks it;
    - one test of `ship --conflict`: a pass, a verdict and a carry recorded, then a `ship` with
      `conflict: true`. Both readers return None and `carry_at` returns None, at that head and at a
      later head;
    - `gate_passed` and `last_verdict` are unchanged by a `carry`.
  - One in-process test of the base rule (§1) on a prepared repository: a restack's window. A CR
    is rebased onto its planned place and shipped while `c.pr_base` still names the old branch, and a
    long gate is re-run before `forge-stack rebuild`. Its `gate` events record the planned place's
    tip (the nearest ancestor tip), not the old branch's, and a later clean move carries that pass.
    A head on none of the three candidates records no `base`.
  - One in-process test of `ship` with a base ref git cannot read: exit 0, the PR and head
    recorded, no `carry` event, and the `off: … does not carry: … cannot be read` line printed.
- **Scenario unit 12f** (`scenario/run_scenario.py`, `gate_carry`):
  - The clean case: after the `ship` of the rebased head, the event log holds one `carry` event
    with `gate_from == old`, `verdict_from == old` and a `base`. `ship` prints the `carried:` line,
    and `STATUS.md` shows `carried from <old7>` before the hand-back. Then `handback ready` is
    accepted as now, with the same line and the same event keys. The unit's `gate` and `verdict`
    events carry `base`.
  - The conflict case: the scenario ships with `--conflict`. `ship` logs no `carry`, and `handback
    ready` is refused with `does not carry: the rebase resolved a conflict` twice. This expectation
    replaces `the replay conflicts`.
  - The commit-after-verdict case is unchanged (`the rebase changed the patch`).
  - New, CR-316's real shape in a stack batch:
    1. A CR is started on CR A's branch, gated and verified there.
    2. `stack` places it on CR B's branch instead (B holding A's commits rewritten).
    3. The CR is rebased onto B's branch and shipped.
    4. A `carry` is logged with B's fork point as `base`, and `handback ready` is accepted with no
       new gate and no new verdict.
  - New, the restack after the hand-back: a CR already `ready` is rebased and shipped, as the stack
    driver does. A `carry` is logged at the new head, the CR stays `ready`, and the eval kit's C7
    rule (`audit.py`) finds a verdict at the CR's final head on that record.
- **The long gate:** `just scenario` passes locally (`chantier gate`), and the pipeline's `just
  scenario (ubuntu-latest)` job is green at the PR's head. AGENTS.md asks for both for a change to
  the CLI and the cards.
- **Known gaps (Q11):** the PR's Known gaps names the one-time cost. CRs judged before this CR
  merges have no recorded base, so they get a new long gate and Verifier at their next move.
- **The pane:** the `gate` text of `STATUS.json` that the pane shows can now read `carried from
  <sha7>` before a hand-back, and a "Carried" step appears. Per AGENTS.md, the PR's Deliverables
  carry one screenshot of the pane showing it, from a real Claude Code session at the PR's head,
  captioned with the head's SHA. Until then, Known gaps says "no screenshot of the pane from a real
  session".

## Open questions

None. The answers settle the behaviour. The method is this specification's: the judged base
recorded at `gate` and `verdict`, the same rule at `ship` (the branch the head sits on), `git patch-id --verbatim`, the record
at `ship`, and `ship --conflict` as the way the one who resolved the conflict says so (Q10).
