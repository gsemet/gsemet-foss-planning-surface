# Change Specification: a clean rebase carries the Verifier's verdict

Short name: `rebase-verify`. No issue.

## Goal

A parallel batch pays a full Verifier after every rebase. In batch-18's real eval runs of
2026-11-15, real-direct run 3 (parallel) ran 25 Verifiers against 15 in run 1, and one CR
(CR-101) cost $2.98 with 11 Verifiers, 5 long gates and 15 ships (audits:
`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md` and
`real-direct-2026-11-15.audit.md`; batch-18 retro point R6). Since CR-265 the long gate's pass
already carries over a clean rebase, proved by git. The Verifier's verdict does not, so each
rebase still costs a Verifier.

After this change, a rebase with no conflict that leaves the CR's own patch unchanged carries the
Verifier's `VERIFIED` verdict to the new head, as the long gate's pass already does. CI must still
be green at the new head. No new Verifier runs then. A rebase that resolved a conflict, or that
changed the patch, still gets a Verifier given the move, as today.

## Decisions carried (`02-answers.md`)

1. Q1, **what a clean rebase still proves** (answer A): a rebase with no conflict and the CR's own
   patch unchanged (the same patch before and after) carries the Verifier's verdict. CI must still
   pass green at the new head. No new Verifier then.
2. Q2, **modes** (answer A): the same rule in parallel and stack modes. Series is the same code
   path (`stack_base` gives the base), so it follows too.
3. Q4: specify, and add the CR to batch-18 with the others.

The user accepts one known risk with answer A. A clean rebase can bring base changes that interact
with the CR's behaviour without a textual conflict (a semantic conflict). From now on, CI at the new
head is the only thing that catches it. The Verifier's delta rule ("the base brought changes to what
the proof runs") no longer starts a Verifier on its own after a clean rebase whose patch is
unchanged.

## What "clean, patch unchanged" means: the same proof as the gate carry

The proof is the existing `carry_check(wt, base, head, g)` in
`skills/chantier/scripts/cli/src/chantier/commands/crs.py`. Replaying `g`'s commits onto `base`
(`git merge-tree --write-tree --merge-base <mb> <base> <g>`) must be clean and give exactly the
head's tree, with as many commits (`rev-list --count <mb>..<g>` equals `<base>..<head>`). Git
proves it, not the Driver's word. No second method is added. The verdict uses it unchanged, with
`g` = the head of the verdict that carries and `base` = `<remote>/<stack_base(record, cr, repo)>`,
the same base `_gate_missing` uses. Its refusal reasons stay as they are: `the replay conflicts`,
`the rebase changed the patch`, `git <v> is older than 2.38: no merge-tree to prove it`.

So these do **not** carry, and get a Verifier given the move as today: a rebase during which a
`conflict-resolver` ran, any commit added, edited or folded after the verdict (a round, a
checkpoint, an amend), and a rebase that dropped or split commits (such as a `rebase --onto` that
removes a dropped CR's commits, or a commit already upstream that the rebase skipped). The commit
count differs in those cases, so the proof fails. This is the conservative side, the same as for
the gate.

## What changes

### 1. CLI: `handback ready` accepts a carried verdict

File: `skills/chantier/scripts/cli/src/chantier/commands/crs.py`.

- Add `last_verdict_head(events) -> str | None`: the head of the latest `verdict` event of the CR
  (any result), returned only when `last_verdict(events, that head) == "VERIFIED"`, else None. A
  later `NOT VERIFIED` at a later head blocks any carry from an older `VERIFIED`. So does a
  description-only `NOT VERIFIED` at the same head, since the last verdict at a head decides.

File: `skills/chantier/scripts/cli/src/chantier/commands/driver_checks.py`.

- Add `_verdict_missing(repo, b, c, events) -> tuple[str, str]`, shaped like `_gate_missing`. It
  returns the refusal text and the carried head (exactly one of the two is empty). With no verdict
  `VERIFIED` at `c.head`, take `v = last_verdict_head(events)`. If `v` exists and
  `carry_check(cr_worktree(c), base, c.head, v)` is None, the verdict carries from `v`. Otherwise,
  refuse with today's text plus a clause when `v` exists:
  `refused: no verdict VERIFIED at <head> (the verdict VERIFIED at <v7> does not carry: <why>) (the last verdict there: <x or none>)`.
- `handback_refusals`: the verdict check (`if not prepared and last_verdict(...) != "VERIFIED"`)
  now goes through `_verdict_missing`. A prepared release still needs no verdict.
- `GateBasis` gains `verdict_carried: str = ""`. `event_keys()` adds `"verdict_from": <full SHA>`
  when it is set. The `handback` event in `events.jsonl` then records `verdict_from`, next to
  `gate_from`. `EventRecord` reads extra keys as attributes, so `core/records.py` needs no change,
  and so do `types/` and `hooks/`.
- The order of refusals and the head check (`the worktree's head … is not the head ship recorded`)
  do not change. The carry is read only at the head `ship` recorded.

File: `skills/chantier/scripts/cli/src/chantier/commands/driver.py`, `_record_ready`.

- The ready line names the carried verdict after the gate words. When both carry from the same
  head, one clause: `, long gate and verdict carried from <sha7> (clean rebase onto <base>)`. When
  only the verdict carries (the gate passed at the head, or `--no-gate`, or a waiver):
  `, verdict carried from <sha7> (clean rebase onto <base>)`, after the gate words. When they carry
  from different heads, two clauses: `, long gate carried from <g7> (…), verdict carried from <v7> (…)`.

File: `skills/chantier/scripts/cli/src/chantier/commands/facts.py`, `_gate_lines` (the
`handoff` checklist).

- When no `VERIFIED` is recorded at the head and the verdict carries (the same
  `last_verdict_head` + `carry_check`), the verdict box reads
  `[x] verdict VERIFIED carried from <sha7> (clean rebase onto <base>)`. Do the same for the long
  gate box with `last_gate_pass`, so a Driver reading `handoff` after a clean rebase sees nothing
  left to run. Otherwise both boxes stay as they are. This is read-only git, as in the hand-back.

### 2. Cards

`skills/chantier/references/driver.md`, every place that starts a Verifier after a rebase. The
rule, in one sentence the places repeat or point to: a rebase with no conflict that leaves the
CR's patch unchanged needs no new `verifier` and no new long gate. The verdict and the pass carry,
and `handback ready` checks both with git (it records `verdict_from` and `gate_from`). CI must be
green at the new head. A rebase that resolved a conflict, or that changed the patch (the hand-back
refuses with `does not carry: <why>`), gets a `verifier` given the move, as before.

- "Rebase first" bullet (~line 186) and the long gate bullet (~line 203, "After a rebase with no
  conflict, run no long gate…"): add the verdict next to the pass. The sentence "you read CI at
  the new head and give the `verifier` the move as before" becomes: read CI at the new head. The
  `verifier` gets the move only when the carry does not hold.
- The refused hand-back after a moved head (~line 451, "`ship` at this head, then the long gate
  and a new `verifier` given the move"): unless the move was a clean rebase, whose pass and
  verdict carry.
- "A move is any change of the head…" (~line 572): a clean rebase that leaves the patch unchanged
  is a move that touches no judgment. No `verifier` and no `inspector` are due for it. Every
  `verifier` started after the first still gets the previous `verify.md` and the move.
- CR driver, the `rebase: <cr> merged` paragraph (~line 600-611): "The `verifier`, given the
  move, judges again what it touched before `handback ready`" applies only after a resolved
  conflict or a refused carry. "A clean rebase and green CI start no new `coder` round" becomes
  "… start no new `coder` round and no new `verifier`". The same goes for the `note rebase: …`
  received while working (~line 618-623), and for the `rebase: mode <mode>` paragraph (~line 628-635):
  "run the long gate and CI again at the new head" becomes: CI at the new head; the long gate and
  the Verifier only when the carry does not hold.
- The PR description after a carried verdict: the Driver marks each proof whose SHA left the head's
  history as `carried from <sha7>` in `pr-body.md` (the Test plan items, the `Verified at` box, the
  evidence captions), as `ship`'s `off: pr-body.md line <n> names …` lines guide (these lines
  already skip `carried from`). Then it runs its pre-post audit and posts the file. This edit only
  changes SHA marks to `carried from`. It needs no description pass by a `verifier`, an exception
  to "any later edit runs the pass again" (~line 553) that the card states there. Any other edit
  of the body still runs the pass.
- Stack driver, "For each PR it moves" (~line 688-692): a `verifier` is started only when the move
  changed that CR's patch (a `conflict-resolver` ran, or the carry is refused). The clause "or the
  base brought changes to what the proofs run" is dropped for a clean restack. An `inspector`
  still comes when the patch changed. The same goes for "Inserting into a stack" step 2 (~line
  801) and "Removing a dropped CR" step 3 (~line 824). Note that a drop's `rebase --onto` changes
  the commit count, so it never carries: a `verifier` is due there.
- The pushed-for-the-Driver `next after push` example (~line 473-474, "the verifier given the
  move"): add "(unless the rebase was clean: the verdict carries)".

`skills/chantier/references/worker.md`, Verifier:

- "Delta assessment" (~line 171): one sentence at its head. A Verifier is not started for a clean
  rebase that leaves the CR's patch unchanged, since its verdict carries, proved by git at
  `handback ready`. When it is started after a move, the delta rule stays as written, base changes
  included.
- "Each proof in the description names its SHA, which is the head or carried with its reason"
  (~line 151): `carried from <sha7>` after a clean rebase is a valid carried proof.

`skills/chantier/references/concepts.md`:

- The CLI paragraph (~line 342-344 and 356): "A pass carries over a clean rebase… (`handback
  ready` records `gate_from`)" also covers the verdict (`verdict_from`). "`handback <cr> ready`
  needs both at the PR's head" adds: "or carried to it over a clean rebase, proved by git".
- Rule 5 (~line 538-541): after "what the move touched is judged again and the rest is carried",
  add: a clean rebase that leaves the CR's patch unchanged, proved by git, touches no judgment.
  CI at the new head still runs.

`skills/chantier/references/status-layout.md`, ~line 121: "`carried from <sha7>` is a pass carried
over a clean rebase, not a gap" adds "and so is a verdict carried that way".

`skills/chantier/references/pr-template.md`, ~line 90: a proof carried over a move says so
(`carried from <sha7>`). Add "a clean rebase carries every proof whose patch it left unchanged".

No change to `agents/` or `com.github.copilot/agents/`: the contract lives in the cards.

### 3. Docs

- `docs/gates.md`, line 13-14: "`handback ready` requires it passed at the PR's head (or carried
  over a clean rebase, which the CLI checks with git), and the Verifier's `VERIFIED` there" becomes:
  "… and the Verifier's `VERIFIED` there. Both carry over a clean rebase that leaves the patch
  unchanged, which the CLI checks with git. CI still runs at the new head."
- `scenario/README.md`, ~line 229-230: section 12f's line also names the carried verdict
  (`verdict_from`).

### 4. Eval kit

`evals/kit/audit.py`, `event_checks` (check C7, ~line 388-399): a CR handed back ready counts as
verified when its last verdict at its head is `VERIFIED`, **or** when its ready `handback` event
carries `verdict_from`. The check's label adds "(or a `verdict_from` hand-back)".

## Out of scope

- The long gate's carry: unchanged (CR-265).
- Any CLI read of CI. The CLI reads no CI state. "CI green at the new head" is the Driver's reading
  (the stack driver's in a stack, heavy CI at the top as today), as it already is before any
  `handback ready`.
- A carry over a resolved conflict, or over a rebase that changed the patch: never.
- The Inspector's rules after a move: unchanged (an `inspector` only when the patch changed).
- What the CR board pane and `STATUS.json` show. The steps list still shows the old head's
  `Verdict VERIFIED <sha7>` and the `Long gate carried from` step, and no new `Verdict carried`
  step is added (see the open question). `hooks/register.tsx` and `status/` are not touched, so no
  pane screenshot is due.
- The release CR (no verdict) and the description-only Verifier pass in every other case.

## Evidence

- `just check` passes (lint, `just test` within its time bound, release notes) on Linux, macOS and
  Windows.
- This is a CLI and card change, so `just scenario` passes. The pipeline's `just scenario
  (ubuntu-latest)` job is green at the PR's head, and if this CR is on top of the stack, a local
  `chantier gate` run of `just scenario` passes on Windows, as AGENTS.md says. No `hooks/` or
  `types/` change, so no `just mod`.
- Scenario, section 12f (`scenario/run_scenario.py`, `gate_carry`, ~line 3944), renamed "A clean
  rebase carries the long gate and the verdict; a resolved conflict carries neither":
  - The check "after a clean rebase and a `ship`, `handback ready` still wants the verdict at the
    new head" is replaced. With no `w.verified(clean)` after the rebase, `handback ready` is
    accepted. The event has `gate_from == old` and `verdict_from == old`. No new `verdict` event is
    recorded for the CR (the count is the same as before the rebase). The line says
    `long gate and verdict carried from <old7> (clean rebase onto main)`. `STATUS.md` still shows
    `carried from <old7>` in the long gate column.
  - Before that hand-back, `handoff <clean>` shows both boxes `[x]` with `carried from <old7>`.
  - Conflict case: drop the `w.verified(clash)` before the hand-back. `handback ready` is refused
    (exit 2). Its stderr holds both `no long gate passed at` and `no verdict VERIFIED at`, each
    with `does not carry: the replay conflicts`. The CR is not ready and no `handback` event is
    recorded.
  - A third case, "a commit after the verdict": on the clean CR, before its hand-back, or on a third
    prepared CR if the clean one is already ready, add a commit after the verdict, `ship`, and run
    the long gate. `handback ready` is refused with `no verdict VERIFIED at` and
    `does not carry: the rebase changed the patch`.
- pytest, `skills/chantier/scripts/cli/tests/test_cli_units.py`, beside the `last_verdict`
  asserts (no new test file): `last_verdict_head` returns the head for [VERIFIED@a]. It returns
  None for [VERIFIED@a, NOT VERIFIED@b] and for [VERIFIED@a, NOT VERIFIED@a], and returns b for
  [NOT VERIFIED@a, VERIFIED@b]. `test_gate_waiver_handback.py` keeps passing. Its monkeypatched
  `last_verdict` refusal test still gets `no verdict VERIFIED` (patch `last_verdict_head` too if
  needed, so no git runs).
- The PR body quotes, from a scenario run at the head, the 12f ready line with
  `long gate and verdict carried from` and the conflict refusal's two `does not carry` clauses.

## Open questions for the user

1. The CR board pane and `STATUS.json`: should a carried verdict also show as its own step on the
   CR's page (for instance `Verdict carried from abc1234`, next to `Long gate carried from`)? The
   specification leaves it out. The hand-back line, the event (`verdict_from`) and `handoff` say
   it, and the page still shows the old head's `Verdict VERIFIED`. Showing it changes what the
   pane draws, so the PR would need a pane screenshot from a real session (AGENTS.md).
   Recommended: leave it out.
2. The PR description after a carried verdict: the specification lets the Driver rewrite the SHA
   marks to `carried from <sha7>` and post the body with no new description pass by a Verifier,
   which follows "No new Verifier then". Any other edit of the body still runs the pass. Is that
   the line you want, or should a short description-only Verifier pass still run after that edit?
