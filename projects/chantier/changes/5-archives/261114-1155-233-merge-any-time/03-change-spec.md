# Change Specification: a merge may come at any moment, one PR at a time, in any batch shape

## Goal

The user (2026-11-13): "I may merge little by little, so you and the Driver must be flexible."
No merge path is fixed at the go, whatever the batch's mode (parallel, series, stack). Each PR
whose CR was handed back `ready` on the default branch is mergeable now, and the user may merge
it on its own; the Chief of Staff, the Foreman and the Drivers follow whatever merges the user
makes, one at a time or a whole stack in one action. "You can merge" is said only after the
`ready` line, and a Driver whose CR was merged under it ends cleanly.

Source: batch-16's retro, points 5 and 12, reviewed by an advisor (`intake/request.md`).

## Root cause (from the request)

- The cards describe one merge path per shape. `chief-of-staff.md` ("A stack batch", around
  lines 552-564) knows only the one-action stack merge; `foreman.md` (around lines 151-162) starts
  the stack driver only once every open CR is ready or blocked, and its "Stack" bullet after a
  merge (around 210-212) knows only a restack. In batch-16 the user merged each stack PR on its
  own, so the stack driver and `forge-stack` never ran, and the Foreman improvised rebase notes.
- Point 12: CR-215 was merged while its Driver was still finishing (`gh pr ready`, a body edit),
  so its `handback ready` was refused by `handback` in
  `skills/chantier/scripts/cli/src/chantier/commands.py` (line 1916:
  `"{cr} is merged: no Driver to hand it back"`), and no card said what to do with that refusal.

## Decisions carried (02-answers.md)

1. The proposal as filed is the scope; points it does not settle take this specification's
   defaults, listed under "Open points".
2. The CR joins the running batch-17.
3. No merge path is fixed at the go, in any shape.

## What changes

Cards only, in `skills/chantier/references/`, plus one scenario check. No CLI code changes: the
refusal of `handback` on a merged CR stays as it is, text included (see "Open points", 1). No agent
file (`agents/`, `com.github.copilot/agents/`) changes.

### `concepts.md`, "Words", **Ready to merge** (lines 9-16)

Today it says that in a stack batch a PR is ready to merge only as part of a verified stack,
merged "in one action from its top PR". New meaning, in every mode:

- A PR is ready to merge when its CR was handed back `ready` and its base is the default branch.
  The user may merge it on its own at any moment, in any mode; a stack batch is no exception.
- In a stack batch, a native stack verified on the forge (the five checks) is a second way: the
  user may merge it in one action from its top PR, or merge its PRs one at a time from the
  bottom. Both are the user's choice, made merge by merge, never fixed at the go.
- Unchanged: any other CR's PR is a draft and says so; the release PR merges last and the
  steering session merges it only under the grant, never a stack that holds it.

Also in `concepts.md`, the **Stack** paragraph (around line 98-105): "the user merges it in one
action from the top PR" becomes "the user merges it in one action from the top PR, or one PR at a
time from the bottom", with the same "release commit last".

### `chief-of-staff.md`

- **"A plain `ready <cr> <link> gaps: …` ask"** (around 538): in every mode, a `ready` ask whose
  PR is on the default branch is offered to the user as mergeable now, on its own (in the user's
  language, with its gaps as today). A `ready … draft on <base>: waits for <cr>` ask is not: say
  what it waits for.
- **Point 12, one new rule in the same place:** say "you can merge" (or any equivalent) about a
  PR only after its `ready` line (or the `stack-ready` line for a stack) has reached you, never on
  a Driver's progress, a green CI or the PR's look on the forge. When the user merges a PR before
  its `ready` line, record it as any merge (`order merged <cr>`: the user's merge is a fact) and
  tell the Foreman in the same message; no reproach, no question.
- **"A series batch"** (546-551): keep it; add that the user may also merge the bottom PR as soon
  as it is ready, which is what the series already does, and nothing waits for a "go" of the user
  to merge.
- **"A stack batch"** (552-564): no longer the only path. Rewrite as:
  - Before the stack is made on the forge, each CR handed back `ready` on the default branch is
    an ordinary `ready` ask, offered as mergeable now (the bullet above); a CR above it, a draft
    on another CR's branch, waits.
  - On a `stack-ready` ask (unchanged five checks, `$CHANTIER forge-stack show`), tell the user
    the stack can be merged in one action from its top PR, **or** one PR at a time from the
    bottom, as they like.
  - After each merge action of the user (one PR or several), record `order merged` for every CR
    it merged, bottom first, all before telling the Foreman, in one message (unchanged).
  - Unchanged: a failing check sends it back through the Foreman; an `anomaly` on a refused
    `forge-stack rebuild` is an ask; the user always merges a stack themselves.
- **The plan at the go** (step 2, around 385-389): the stack recommendation (`gh stack`, or
  `forge-stack create`) stays, but the plan no longer presents the one-action merge as the way
  the batch will end: say that the user may merge each ready PR as it comes, or the stack in one
  action once it is made. Nothing about the merge path is recorded in `brief.md` as fixed.

### `foreman.md`

- **The stack driver's start** (151-162): keep "a stack driver takes the stack when its open CRs
  are all ready or blocked", and add that, until then, a stack batch runs like a parallel batch
  with chains: each CR handed back `ready` on the default branch is an ordinary `ready` ask (the
  user may merge it now), and a merge is handled by the rebase notes below, not by a restack.
- **After an `order merged`, by mode** (191-212): the opening rule (each ready draft waiting on
  the merged dependency goes back to a Driver with `rebase: <dependency> merged`; it holds in
  every mode) stays. The "Stack" sub-bullet becomes a choice the Foreman makes per recorded merge
  (or per group of merges recorded in one message), never fixed at the go:
  - **A restack** (one `take stack` for what remains, one stack driver, unchanged) when a native
    stack of the batch is on the forge, or when every open CR of the stack is ready or blocked.
  - **Rebase notes** otherwise (a Driver of the stack is still working, no stack on the forge):
    the parallel rules apply, scoped to the CRs whose base the merge changed: a `working` CR
    based on the merged CR's branch or on the default branch gets `[foreman→driver <cr>] note
    rebase: <merged cr> merged`; a `ready` or `blocked` one with a PR that no longer merges
    (`gh pr view --json mergeable`, `glab mr view`) or whose base was the merged CR's branch goes
    back with `take <cr> --note "rebase: <merged cr> merged"`. A ready PR on the default branch
    that still merges cleanly is left alone.
  - Nothing of the stack left open: neither.
  The Foreman says in its next line to the Chief of Staff which one it chose and why, in one
  clause.
- **Point 12:** a Driver's line `[driver <cr>→foreman] … <cr> is merged: no Driver to hand it
  back …` (with its note of what it left undone) is not an anomaly and not an ask: read the
  Driver's note (`log <cr>`), and when it names work still needed on the default branch, pass it
  to the Chief of Staff in one line (`[foreman→chief-of-staff] merged early <cr>: left undone:
  <the note>`), who offers it to the user as an inbox item. Nothing else: no `take`, no restart.
  The CR's worktree and branch are removed by the usual cleanup before `pause`, never while its
  Driver may still run.

### `driver.md`

- **"Your end"** (195-231), next to the existing refusals (`<cr> is ready`, `<cr> is blocked`,
  the head mismatch): a hand-back refused with `<cr> is merged: no Driver to hand it back` means
  the user merged the PR while you were finishing. Do not push, edit the PR, retarget it or turn
  it ready or draft any more. Record what you left undone in one line, `$CHANTIER note <cr>
  "merged before the hand-back; left undone: <what>"` (`none` when nothing), pass the refused line
  as printed to the steering session (`[driver <cr>→foreman] …`, by the host's means), and end.
- **"Stack driver"** (344-415): the opening ("Your end is one native stack … that the user merges
  in one go") says instead that the user merges it in one action from the top PR or one PR at a
  time from the bottom; the existing "After a partial merge" paragraph (398-404) is the procedure
  for both and stays as it is.
- **The rebase on `rebase: <cr> merged`** (327-342): unchanged; it already covers a working
  Driver's `note rebase:` and a ready one taken back.

### `scenario/run_scenario.py`

One check, near the existing handback checks: a CR marked merged by `order merged` while its
Driver is working; `handback <cr> ready <link>` is refused with a line naming `is merged`, and
`note <cr> "merged before the hand-back; left undone: none"` is accepted (exit 0). This pins the
behaviour the Driver card now relies on; it adds no CLI behaviour.

## Out of scope

- Any change to the CLI's behaviour or texts (`handback`, `order merged`, `take stack`,
  `forge-stack`): the refusal stays.
- The docs and README sentences that describe the one-action stack merge (`README.md` lines 107
  and 225, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`, the SVGs, `CONTRIBUTING.md`
  line 266) and the eval kit (`evals/`): see "Open points", 3.
- Any merge by an agent: the user merges, as today; the grant's rules for a release PR or a fix
  are unchanged.
- The release CR's ordering (it still merges last).

## Batch-17 and CR-221

This CR touches no CLI code: it edits cards and adds one check to `scenario/run_scenario.py`.
CR-221 moves the CLI's modules and only adjusts the scenario's imports; a shared file is no
reason to wait. **It need not wait for CR-221.** In batch-17 (stack mode) it goes on top by
`order add`, as any added CR. Its card changes reach the running batch only once merged into the
main checkout and reloaded (`/reload-plugins` or the next session); until then the Chief of Staff
applies the rule of batch-17's `brief.md` ("a PR is merged only once its Driver has handed back
`ready`").

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes (a change to the cards and the scenario), with the new check above.
- A reading pass, recorded in the PR's Test plan: `rg -n "one action" skills/chantier/references`
  shows every remaining mention offers the one-PR-at-a-time merge beside it; `rg -n "is merged:
  no Driver" skills/chantier/references/driver.md` finds the new rule; `concepts.md`'s **Ready to
  merge** no longer limits a stack batch to the one-action merge.
- The four cards stay consistent with each other: the Chief of Staff's, the Foreman's and the
  Driver's wording of the merged-early case names the same refused text.

## Open points (each with the default taken)

1. **The CLI refusal's text.** The request allows "at most its text gets clearer". Default: no
   change, the cards explain it. If the user wants a clearer text (for instance `"<cr> is merged:
   no Driver to hand it back; note what you left undone, then end"`), it edits `handback`, which
   CR-221 moves out of `commands.py`: that is a rebase conflict that would happen anyway, the one
   case where chaining it after CR-221 is justified.
2. **`concepts.md`.** The request lists three cards; `concepts.md`'s **Ready to merge** and
   **Stack** contradict the decision, so the default edits them too.
3. **Docs and README.** Default: out of scope (a docs-only follow-up, inbox item); the user may
   want them in this CR so the docs match the cards.
4. **The Foreman's choice after a merge** (restack or rebase notes). Default: restack when a
   native stack is on the forge or every open CR of the stack is ready or blocked; rebase notes
   otherwise, scoped to the CRs whose base moved or whose PR no longer merges.
5. **Work left undone by a Driver whose CR merged under it.** Default: the Foreman passes it to
   the Chief of Staff, who offers it as an inbox item; no automatic fix CR.
6. **The scenario check.** Default: one check added (refusal names `is merged`, `note` accepted).
   The alternative is a card-only change with no new check.
