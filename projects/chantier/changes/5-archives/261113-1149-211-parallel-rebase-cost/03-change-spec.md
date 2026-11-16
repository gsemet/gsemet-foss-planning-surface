# Change Specification: parallel-rebase-cost

Source: `intake/request.md` (batch-11 retro; real-direct run 1 of 2026-11-12, finding 9),
`01-intent.md`, `02-answers.md` (2026-11-12: answers 1-8 by the Fable advisor in the user's place,
on the user's word, taken as the user's; the two "Open for the user" questions answered by the user
at the end of the file). Cards are relative to `skills/chantier/references/`; line numbers as on
`main` at 8c003ae.

## Goal

In a parallel batch, each merge sends every other open PR back to a Driver: rebase, push, long
gate, CI and Verifier again. With n PRs open, n merges cost about n²/2 such passes. The user wants
two things:

1. **The cost measured**, from what batch-11 and real-direct run 1 already recorded, so the
   project knows what the rebase passes cost and where.
2. **Rebases that would happen anyway avoided at the plan**: when two CRs' specifications edit the
   same lines (one shared table, one template block), the plan proposes that the second CR wait
   for the first, as an intra-batch dependency explained in the plan, so it starts on the first
   one's work instead of conflicting with it at each merge. In run 1, CR-101 delete-item kept
   working while four others merged into the same README Routes table and the same item
   template: three rebases, each with a conflict-resolver, $3.32 of the batch's $9.22, and one
   resolution added a byte-order mark that cost a round.

What does **not** change, on the user's word (2026-11-12, open question 1): every ready PR is still
rebased after each merge, in parallel and stack mode alike, so it always merges without a merge
commit. The advisor's "a ready PR the merge did not touch stays ready" is declined and is not part
of this CR.

## What changes

### 1. The measure, in the PR (no code, no new command)

The Driver builds one table and puts it in the PR description, under its own heading (for
instance "Cost of the rebase passes"), from the records alone. No new CLI command, no new eval
(answer 1).

Rows: one per merge in a parallel batch, for batch-11 and for real-direct run 1. Columns:

| Column | What it holds |
| --- | --- |
| Merge | the CR merged (number and slug) and when |
| Sent back | each CR sent back by that merge, and its state then (`ready`, `blocked`, `working`) |
| Patch changed by the rebase | no (clean, or context only) / yes (a resolved conflict), from the CR's notes or a range-diff |
| Pass cost | long gate minutes, agents started (Verifier, Inspector, conflict-resolver, Coder), dollars |

Then a total per batch: passes, passes whose patch did not change, gate minutes, agents, dollars.

Sources, read-only:

- **Batch-11:** the archived CRs of batch-11 in this repository's planning folder,
  `.agents/changes/5-archives/` (`261111-*-174-…` to `261111-2309-185-driver-liveness` and the
  others numbered 174 to 185): each `STATUS.json`'s `steps` and `notes` (the rebase notes, the
  long-gate passes with their heads and times, the verdicts), their `work/gates/*.log` where kept,
  and the batch's retro, kept in `5-archives/261111-2309-185-driver-liveness/retro.md` (the
  "Parallel mode made every merge cost a rebase pass" and "about 13 minutes of the long gate each
  time" lines). The batch's `events.jsonl` is no longer in the planning folder (the spec-writer
  found no `events.jsonl` left under `.agents/changes/`): use it only if the Driver finds it.
- **Real-direct run 1:** the report, `evals/results/real-direct-2026-11-12-run1.md` on `main`
  ("What happened", finding 9, "Numbers", `cost --by cr` at the audit), and, if the Driver can
  reach it, the run's workspace and its archive (`5-archives/261112-2003-101-delete-item/`, with
  the batch's `retro.md`).
- The batch-14 retro (`5-archives/261112-1924-191-eval-kit-end-to-end-dry-run/retro.md`) may be
  quoted for the gate queue the re-gates fed; it is not a row source.

A figure the records do not give is written "not recorded", never estimated (rule 2 of
`concepts.md`). Dollars per pass are given only where a record gives them (for instance a CR whose
only extra spend was the pass); otherwise the CR's total from `cost --by cr` or its archived
`STATUS.json` `cost_usd` is given as such, with the number of passes it includes.

The PR description also carries, in one paragraph, why the CR gives **no merge order** to follow
(answer 2): among PRs that overlap, each merge moves the others whatever the order, and the user
merges when and what they want; the saving is in not starting side by side the CRs that edit the
same lines.

### 2. A working CR rebases once per push (only if the measure shows the need)

`driver.md`, the paragraph at lines 213-226, already says: "A `note rebase: …` received while
working: rebase before the next push". Answer 4: a `working` CR rebases once, before its next push,
however many notes came; the CR makes this unmistakable only if the measure shows a Driver rebasing
once per note.

- If the table shows a working CR rebased more than once between two of its pushes because several
  `rebase:` notes came, add to that sentence of `driver.md`: "however many `rebase:` notes came
  since your last push, one rebase, onto the latest default branch", and to the matching words in
  `foreman.md`, "Parallel" bullet (lines 143-148): "a `working` one gets … `note rebase: <merged cr>
  merged`; it rebases once, before its next push".
- Otherwise `driver.md` is not changed, and the PR description says so in one line with the rows
  that show it.

### 3. The plan proposes a dependency for CRs that edit the same lines

The rule to name (open question 2, the user's yes, "if it is well explained"): when the
specifications of two CRs selected for a parallel batch edit **the same lines** of a file (one
shared table, one template block, one list both append to), the plan proposes that one waits for
the other: an intra-batch dependency, because the rebase it saves would happen anyway. It is a
proposal with its reason, approved by the user's go and refusable per CR; never for a merely
shared file; never without the go; the batch stays parallel.

It is recorded as the existing chain, an `after` with no real dependency, not as `depends.json`:
`depends.json` stays for a CR that needs the result of another, belongs to the CR's folder beyond
this batch, and the cards keep saying that CRs touching the same file do not depend on each other.
The CLI does not change: `order after <cr> --note "<cr>"` already makes a queued CR wait, and
`take` starts it, once the other is `ready`, on that CR's branch (`concepts.md`, "Dependencies").

Card changes:

- **`chief-of-staff.md`, the paragraph at lines 205-214** ("A batch is parallel unless …"). Keep
  "Touching the same file is no reason to wait, and two CRs editing the same file do not depend on
  each other." Replace "You may propose a queue with no real dependency, for instance when the work
  is small and rebasing it would cost more than waiting: …" with the rule, in this sense:
  - Read the specifications of the CRs selected for a parallel batch for **the same lines**: a
    shared table, a template block, a list each one appends to. For such a pair, propose in the
    plan that the later one waits for the other, and say why: both edit those lines, so each merge
    of one would make the other rebase with a conflict anyway; waiting, it starts on the first
    one's work.
  - The cost, said in the plan: the waiting CR starts only once the other is ready, so it takes
    longer on the clock and a slot may stay free.
  - A shared file alone is no reason. Small work whose rebase would cost more than waiting stays a
    reason too (the existing case). No threshold: you judge, and say why.
  - The user's go approves each such wait; the user may refuse it per CR, then the CR runs side by
    side as usual.
- **`chief-of-staff.md`, "Starting a batch", step 2 (lines 237-239):** the plan's line for each
  such CR names the two CRs (number and slug once `open` numbered them, else the slug), the file
  and the lines both edit (for instance "README.md, the Routes table"), and the reason in plain
  words: "a rebase with a conflict that would happen anyway". Keep "the reason of any queue that
  is no real dependency".
- **`chief-of-staff.md`, "Starting a batch", step 3 (after the `open` block, lines 252-263):**
  right after `open`, before the first `take` (direct mode) or before starting the Foreman
  (Foreman mode), record each wait the go approved: `$CHANTIER order after <cr> --note "<cr>"`
  then `$CHANTIER order note <cr> --note "chain: <reason>"`, the same pair as the existing "A
  chain" bullet (lines 348-352). `order after` replaces the CR's whole `after`: when the CR already
  waits for a real dependency from `depends.json`, list it too, comma separated. `order after`
  carries no `--epoch` (line 529).
- **`chief-of-staff.md`, "A chain" bullet (lines 348-352):** say it also covers a chain the plan
  proposed and the go approved, recorded at `open` as above; the rest is unchanged (the next
  report's Notes line, `order after <cr> --note -` to turn it off while the CR is queued).
- **`foreman.md`, the chain bullet (lines 110-115):** align the reason with the Chief of Staff's:
  "for instance small work, or two CRs whose specifications edit the same lines (one table, one
  template block), whose rebase would conflict anyway; a shared file alone is no reason". The rest
  is unchanged.
- **`concepts.md`:** line 94, "a chain the Foreman decided (`order after`)" becomes "a chain the
  Foreman decided, or the plan proposed and the user's go approved (`order after`)"; line 139-140,
  "A chain is an `after` with no real dependency, which the Foreman decided for a queued CR"
  likewise. Line 144 ("CRs that touch the same file do not depend on each other") stays.
- **`status-layout.md`, line 87:** "queued after another by the Foreman's decision" becomes
  "queued after another by the Foreman's decision or the plan's, with no real dependency".
- **`docs/use-cases-foreman.md`, the Parallel paragraph (lines 30-33):** one sentence: when two
  CRs edit the same lines, the plan may propose that one waits for the other, with its reason;
  you approve or refuse it at the go. `docs/use-cases-direct.md` (lines 54-56) refers to Foreman
  mode and needs no change unless its wording then contradicts it.

The agent files (`agents/`, `com.github.copilot/agents/`) are not touched: the rule lives in the
cards.

### Decisions carried, with no change of text

- **Parallel only** (answer 3): series and stack already rebase only the next CR or restack once.
- **A `blocked` CR with an open PR** (answer 5): follows the same rule as a ready one, which the
  user kept as today: it is rebased after each merge (`foreman.md` lines 143-148 unchanged).
- **A project whose rules require an up-to-date branch before a merge** (answer 6): its rules rank
  above the cards; with every open PR rebased after each merge, nothing differs for it.
- **Where the judgement lives** (answer 7): in the cards, by the steering session; nothing in the
  CLI or `rails.py`.

## Out of scope

- A ready or blocked PR left un-rebased after a merge, even when the forge reports it mergeable and
  the merge touched none of its files: declined by the user (2026-11-12). Every open PR is rebased
  after each merge, conflict or not.
- A merge-order advice line in reports, or an order to follow (answer 2).
- Series and stack batches, and the stack driver's restack (answer 3).
- Any CLI change: a new command, a new refusal in `rails.py`, a forge read by the CLI (answers 1, 7).
- Writing `depends.json` for a shared-lines pair (it stays for a real need).
- The batch-wide gate lock (item `stop-own-gate`), the race of a rebase note with a ready hand-back
  (item `rebase-note-check-status`), byte-order marks (item `check-rejects-bom`).
- The SVG diagrams (`docs/batch-modes.svg`, `docs/cr-lifecycle*.svg`) and their `*-texts.md`.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes (answer 8: the CR changes cards, and the scenario plays a parallel batch).
  It already checks the mechanism the plan reuses: "a chain through `order after` starts on the
  ready CR's branch; `--note -` puts the …" (`scenario/run_scenario.py` around line 2891) and the
  `order after` refusals (around lines 3781-3800). No scenario step is added: the change is a
  judgement in the cards, and the CLI is unchanged.
- The PR description holds the measure table of section 1, each row naming its source file, the
  totals, and the no-merge-order paragraph.
- A reading check, quoted in the PR: `chief-of-staff.md`, `foreman.md`, `concepts.md` and
  `status-layout.md` all give the same rule (same lines, not same file; proposed in the plan with
  its reason; approved at the go, refusable per CR; recorded with `order after` and `order note
  "chain: …"`), and `driver.md` is changed only if the table shows the need (section 2).

## Open questions

None.
