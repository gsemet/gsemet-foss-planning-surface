# Answers: take-base-from-forge

## 2026-11-20, grilled by the Chief of Staff alone

Every answer below: Settled by the Chief of Staff (2026-11-20, the user asks no questions).

Facts read before the answers (the code at main, the two batches' records):

- `take` and `handoff` already read the forge for a stacked CR that has a PR
  (`commands/forge_base.py`, `stacked_read`): its printed base is the PR's base on the forge. The
  wrong bases were printed for CRs with no PR yet, where the base comes from the record alone
  (`stacks.py`, `start_on_for` and `stack_start`).
- Studio's batch-06: CR-427 was given the branch of CR-351, whose PR 429 was already merged on
  the forge and not yet recorded merged (its Driver's first note says so). CR-424 started on the
  same CR-351 and was rebased onto main after that merge. CR-429 was given CR-424's branch, an
  open draft PR of a working CR; the Foreman's take note sent it to origin/main.
- chantier's batch-29: CR-391, CR-392, then CR-407, 408, 409, 410 and 413 read `PR in draft` while
  their PRs were out of draft on main. `ready_word` asks that every CR under them in the recorded
  order be out of draft; the CRs under them were working, with no PR, and no stack driver had
  placed any of them (`stacked` false). Their `pr_base` in the record was `main`, as `ship` read it.

Q1. Does `take` gain a forge read to find the base of a CR with no PR?

No. `take` reads the project's journal (`forge-journal.jsonl`), which the forge hub already fills:
a `merged@1` line for each PR of the running batch that the forge shows merged and the record does
not hold. A CR with such a line, for its recorded PR, is no base. The agent passes nothing and the
CLI adds no network read. Settled by the Chief of Staff (2026-11-20, the user asks no questions).
Reason: AGENTS.md names the CLI's network reads and `take` is not to add one; the journal already
holds the one forge fact that made the printed base wrong, at no call; a base passed by the
Foreman would be an unchecked claim and one more step at every take.

Q2. Which CRs does that rule take out, and where?

For the start base only (`start_on_for`, `stack_start`, `start_base`), a CR of the batch with a
`merged@1` line for its recorded PR reads as ended: it is not the nearest earlier CR with a PR, not
the owner of a live `start_on`, not an open dependency, not a series' predecessor, not the release's
top. `take` uses it when it records `start_on`, and `take` and `handoff` when they print the base.
The views, `stack`, `forge-stack` and the rails read the record as today. Settled by the Chief of
Staff (2026-11-20, the user asks no questions). Reason: the narrowest place that fixes the printed
base; the record catches up at `order merged`, which the same journal line already asks for.

Q3. Does `take` say that it left a CR out?

Yes, one line under the `worktree:` line, in `take` and `handoff`, only when the journal changed
the base: it names the CR left out and its PR. Settled by the Chief of Staff (2026-11-20, the user
asks no questions). Reason: the Foreman and the Driver must see why the base is not the one the
order gives, and that `order merged` is still owed.

Q4. With no hub and no watcher running, the journal has no line. What then?

The base is the record's, as today; nothing is refused and nothing is read. Settled by the Chief
of Staff (2026-11-20, the user asks no questions). Reason: no fallback read in the CLI; the
Foreman's card keeps the forge check a Driver already does before it creates its worktree.

Q5. CR-429's case: is the branch of a working CR with an open draft PR still a base?

Yes, unchanged: the nearest earlier CR with a PR, whatever its status and draft state. Settled by
the Chief of Staff (2026-11-20, the user asks no questions). Reason: this is the user's own answer
of 2026-11-17 (stack-Q4, `take-base-nearest-pr`: one linear stack, not a tree), and no forge fact
of the retro makes an open PR's branch a wrong base; changing it is a new decision for the user,
filed apart (`take-base-on-working-draft`).

Q6. From what does a ready CR of a stack batch read `ready to merge` or `PR in draft`?

A CR the stack driver has placed (`stack <cr>…`, `stacked`) reads as today: every CR under it in
the stack's order is out of draft. A CR not placed yet, with its PR's base recorded (`pr_base`, as
`ship` last read it on the forge), reads from that base: on the default branch and out of draft,
it is ready to merge, whatever the recorded order; on an open CR's branch, it is ready to merge
only when that CR is; on a merged CR's branch, or with no base recorded, today's rule. Settled by
the Chief of Staff (2026-11-20, the user asks no questions). Reason: the recorded order of CRs not
placed is only the order they were opened in, not a stack on the forge; a placed CR's order is the
stack driver's and the scenario already fixes its rule (step 13b, checks 4 and 11).

Q7. And what a PR in draft waits for?

The same split. Not placed, base recorded: on the default branch it waits for its turn out of
draft, never for a CR of the recorded order; on an open CR's branch it waits on that CR while that
CR is not ready to merge. Placed, or no base recorded: as today. Settled by the Chief of Staff
(2026-11-20, the user asks no questions). Reason: the stale "after CR-425" label named a CR the
PR did not sit on.

Q8. Does the label read the forge, or the journal?

Neither: it reads `pr_base` and `pr_draft`, which `ship` records from the forge. Settled by the
Chief of Staff (2026-11-20, the user asks no questions). Reason: the label is drawn at every write
of the record, far too often for a read; the cards already ask for a `ship` after every change on
the forge (draft, ready, retarget).

Q9. Does the release CR change?

No: its base, its word and what it waits for stay on today's rules. Settled by the Chief of Staff
(2026-11-20, the user asks no questions). Reason: neither retro names it.

Q10. Does the CR pane owe a screenshot?

No: no `STATUS.json` field is added or renamed and no label takes a new form; a CR only reads one
of the three existing words sooner. Settled by the Chief of Staff (2026-11-20, the user asks no
questions). Reason: AGENTS.md asks for one when what the pane draws changes.

Q11. What is split out?

Two inbox items: `take-base-on-working-draft` (Q5, a decision for the user) and
`agents-md-names-cli-forge-reads` (AGENTS.md's network sentence does not name the forge reads
`ship`, `take`, `handoff` and `forge-stack` already make with `gh` or `glab`). Settled by the Chief
of Staff (2026-11-20, the user asks no questions). Reason: neither is needed to fix the two
retro points, and the second is a rule's wording, the user's.
