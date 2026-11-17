# Change Specification: the partial-stack ask says whether the local gate ran at its top

## Goal

In batch-24 a partial stack was merged before the local Windows `just scenario` had run at its
top: the record holds one `gate` event only (CR-334 at 796686b), and the CRs of the mergeable part
had handed back with `--no-gate` (the pipeline job is chantier's long gate). The project's rule
says the stack's top also passes `just scenario` locally (`chantier gate`) at its head before the
user merges, and "when a CR joins on top, the local run moves to it". For a partial stack, what
the user merges is the mergeable part, whose top had no such run.

After this change, when the project's rules ask the stack's top for a local run, the stack driver
keeps one invariant: the top of the mergeable part has passed that local gate at its head. It runs
the gate at the mergeable top before it hands back the first stack, and again at each new top of
the mergeable part (a draft turned ready, a restack after a partial merge, an insertion, a drop),
skipping a head that already has a pass or a carried pass. Each partial `stack-ready-to-merge` ask
states the result (`local gate <cr> at <sha7>: passed|failed|not run`); the Foreman sends it only
on `passed` (a `deliver by` time excepted); the Chief of Staff tells the user what the clause says
before it says the stack is mergeable. Every choice comes from `02-answers.md` (the user's word of
2026-11-17 and the points settled by the Chief of Staff, the growth of the mergeable part
included).

Cards only: no CLI, hook, pane, `STATUS.json` or scenario change.

## Terms

- **The rule**: a project rule that asks the stack's top for a local run of the long gate (the
  wording already used by `driver.md`, the CR driver's long-gate bullet: "A rule that also asks the
  stack's top for a local run"). In chantier: `AGENTS.md`, "Windows coverage". With no such rule,
  nothing below applies and no ask carries the new clause.
- **The mergeable top**: the CR whose PR is the top of the mergeable part, the one whose head is the
  `<sha7>` that `forge-stack show` prints in "partial stack mergeable below <sha7>". Not the stack's
  top draft.
- **The clause**: `local gate <cr> at <sha7>: passed|failed|not run`, `<cr>` the mergeable top
  (number and slug, as `concepts.md`, "A CR's name", asks of an ask), `<sha7>` its head. `passed`:
  the last `gate` of that CR at that full head passed, or a pass carried to that head (`ship`'s
  `carried:` line). `failed`: the last `gate` there failed. `not run`: neither (never started, or
  still running at a `deliver by` time).

## What changes

### 1. `skills/chantier/references/driver.md`, "Stack driver"

- **"Making the stack"** (~811-821): add one paragraph after the mergeable part is turned ready
  and recorded (`stack --out-of-draft`), before the hand-back:

  "**The local gate at the mergeable top.** When the project's rules ask the stack's top for a
  local run and the stack has drafts on top or CRs to come (a partial stack), the top of the
  mergeable part must have passed that local gate at its pushed head. Run it there when it has
  not: `$CHANTIER gate <cr> "<the project's command>"…` in that CR's worktree (clean, at the head
  you shipped), as any long gate (its queue, its lock, never stopped for slowness). A head with a
  pass is not run again: a `gate` that passed there, or that CR's `ship` printed `carried:` for the
  gate at that head (a clean restack). This holds at the first stack made and at each new top of
  the mergeable part, in any take: a draft that turns ready to merge, a restack after a partial
  merge, an insertion, a drop. Every hand-back that leaves a partial stack names the result for the
  mergeable top as it stands: `[stack→foreman] hand-back ready to merge <stack link> <cr>=<link>…
  local gate <cr> at <head7>: passed|failed`. A failed run is also `[stack→foreman] anomaly <cr>
  local gate failed at <head7>: <the log's path>`, sent before the hand-back; you change nothing
  for it (no round of your own: you edit no project file)."
- **A new top whose gate fails or has not run.** The same paragraph goes on: "A PR that would
  become the new mergeable top turns out of draft only once its local gate passed at its head;
  until then it stays a draft on top. When its gate fails, it stays a draft, the mergeable part
  keeps its previous top (whose pass still holds), and the anomaly above goes up." Wire it into:
  - "A draft that turns ready to merge" (~842-845): "turn its PR ready once the five checks hold"
    becomes "once the five checks hold and, under the rule, its local gate passed at its head";
  - the restack pass after a partial merge (~880-897), step 4: the local gate at the mergeable top,
    when its head carries no pass, before the hand-back (a clean restack carries the pass: no run);
  - the insertion (~916-934), step 5, and the drop (~936-959), step 6: the same check before the PRs
    above turn ready.
- **"Deliver by a time"** (~852-856): add "With the rule above, a local gate that has not passed
  by the time does not hold the hand-back: hand back at the time with `local gate <cr> at <head7>:
  not run` (or `failed`); a gate still running is not stopped and records its result as any gate."
- **The hand-back line after "The five checks"** (~866-867): the line gains the optional tail:
  `[stack→foreman] hand-back ready to merge <stack link> <cr>=<link>…[ local gate <cr> at <head7>:
  passed|failed|not run]`, present under the rule on every hand-back that leaves a partial stack.

### 2. `skills/chantier/references/foreman.md`

- **The partial ask** (~321-324): the form becomes `$CHANTIER asks "stack-ready-to-merge <stack
  link> partial stack mergeable below <sha7> <cr>=<link> gaps: …… local gate <cr> at <sha7>: passed
  to come: <cr> <cr>…"`, and the bullet adds: "Under a project rule that asks the stack's top for a
  local run, the clause is copied from the stack driver's hand-back and is a condition of every
  partial ask: send it only when it says `passed`, for the `<sha7>` the ask names. A hand-back with
  no clause under the rule is a failed check: `take stack --note "local gate at the mergeable
  top"`. With no such rule, no clause."
- **A failed local gate, in any take** (a new bullet beside `anomaly <cr> conflict: …`, ~332):
  "`anomaly <cr> local gate failed at <head7>: <log path>`: no ask for that top; `take <cr> --epoch
  <n> --note "local gate failed at <head7>: <log path>"` sends that CR to a Driver for a round; it
  joins the mergeable part at a later take, once its gate passes."
- **Each new partial ask.** Today a partial ask goes at the first stack made and at a `deliver by`
  time; a CR that later turns ready to merge reaches the user through the next report's
  partial-stack line, never as an ask. That stays: the invariant of section 1 guarantees that the
  mergeable part the report shows has passed the local gate at its top. No new ask is added for
  growth.
- **The complete ask** (~325-326): unchanged, no clause (the top's Driver hands back on its own
  local pass, with no `--no-gate`, by `driver.md`'s long-gate bullet).
- **"Deliver by a time"** (~298-305): after "send the `stack-ready-to-merge … to come: …` ask of the
  stack as it stands", add "with the local-gate clause as the hand-back gives it (`not run` or
  `failed` included: the time overrides the condition above)".
- **The asks list** (~403-404): the `stack-ready-to-merge` form becomes `stack-ready-to-merge
  <stack link> [partial stack] mergeable below <sha7> <cr>=<link>[ gaps: …]…[ local gate <cr> at
  <sha7>: passed|failed|not run] [to come: <cr> <cr>…]`.
- No change to the five checks, the gaps rule (~371-375) or the supersede rule (~407-410): a
  later partial ask still supersedes the earlier unread one (the CLI's `readiness_key` reads only
  the first word).

### 3. `skills/chantier/references/chief-of-staff.md`, "A stack batch" (~1056-1116)

- After the gap rule for each CR of the mergeable part (~1062-1068), add: "On a partial ask, in a
  project whose rules ask the stack's top for a local run, quote its `local gate <cr> at <sha7>:`
  clause in the user's language before the sentence that says the stack can be merged. `passed`:
  say the local gate ran and passed at that head. `not run` or `failed` (a `deliver by` time), or
  no clause: say the project's rule asks that gate at that head before the merge and it has not
  passed there; merging anyway is the user's choice, recorded as any merge (`order merged`), never
  questioned or refused. The record holds it: the last `gate` events of that CR at that full head
  in the batch's `events.jsonl` (`status`'s "Long gate" column keeps `exempt: <rule>` for a CR
  handed back with `--no-gate`)."
- Nothing else changes there: the heavy-CI clause (~1110-1116), the complete ask, the report's
  partial-stack line (the stack driver's invariant covers its top), the merge recording.

### 4. Agent files and docs

- `agents/` and `com.github.copilot/agents/`: unchanged (the contract lives in the cards).
- `README.md`, `CONTRIBUTING.md`, `docs/`: change only a line that quotes the
  `stack-ready-to-merge` partial form in full, if one does (the Driver greps for "partial stack
  mergeable below" outside `scenario/` and the CLI's source, whose `forge-stack show` output is not
  touched).

## Out of scope

- The CLI: `forge-stack show`'s "partial stack mergeable below" line, `asks`, `readiness_key`,
  `gate` and `status` stay as they are. `status`'s "Long gate" column, `STATUS.json` and the pane
  keep showing `exempt: <rule>` for a CR handed back with `--no-gate`, even after a later local pass
  (showing it there is a CLI and pane change, with the pane screenshot rule).
- A new ask for growth of the mergeable part (it stays told by the report's partial-stack line).
- The complete stack's ask; a series or a parallel batch; a stack waiver (`order waive stack`),
  whose top's gate already validates the lower CRs and whose merge offer already names it.
- Any Windows-specific wording in the cards: the rule is the project's, read generically.

## Evidence

- `just check` passes (Linux, macOS and Windows, by `AGENTS.md`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (the cards change).
- Windows coverage: when this CR is the top of the batch's stack, its Driver runs `just scenario`
  locally with `$CHANTIER gate` at its head (no `--no-gate`), per `AGENTS.md`; when a CR joins on
  top, the local run moves to it.
- No `just eval-dry-run` (no change under the CLI's `src/` or `evals/kit/`), no `just mod` (no
  change to `hooks/` or `types/`), no pane screenshot (nothing the pane draws changes).
- The Driver's review reads the three cards together: the clause's form is the same in
  `driver.md`'s hand-back, `foreman.md`'s partial ask and asks list, and `chief-of-staff.md`; the
  invariant is wired into each stack-driver path that changes the mergeable top (first stack,
  draft turned ready, restack, insertion, drop).
- Known gap (the PR names it, so the ready line quotes it): the behaviour is unproved until a real
  stack batch makes a partial stack under the rule; trial: the stack driver's hand-back carries the
  clause, the record holds a `gate` event of the mergeable top at that head before the ask (and of
  each later new top before its PR turns out of draft), and the ask quotes it.

## Open questions

None.
