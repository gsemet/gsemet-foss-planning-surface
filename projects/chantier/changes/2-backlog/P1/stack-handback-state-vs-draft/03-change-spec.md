# Change Specification: the stack shows a CR's hand-back apart from its PR's draft flag

## Goal

In batch-22 the stack driver read a row `PR in draft` as "this CR is not handed back ready" and
stopped before making the forge stack; a second take was needed. The rows that `take stack` and
`stack` (with no CR) print must say, in one label, the CR's hand-back state and, apart from it,
its PR's draft flag as last recorded (`ship`, `stack --out-of-draft|--draft`), e.g.
`ready, PR draft (#251)`, so a CR handed back ready reads `ready` whatever its PR's draft flag.
The stack-driver card says that the stack is made from the hand-back state (`ready`), whatever
the PR's draft flag.

## Decisions carried from `02-answers.md`

- stack-state-Q1 (2026-11-17, the user): one combined label in one column, not two columns:
  e.g. `ready, PR draft (#251)`, `working` (the answer's `running` is read as `working`, per
  stack-state-Q2).
- stack-state-Q1: the stack-driver card says the stack is made from the hand-back state (`ready`),
  whatever the PR's draft flag.
- Spec critic on stack-state-Q1: it changes what `take stack` and `stack` print and the stack
  driver's card. Nothing else.
- stack-state-Q2 (2026-11-17, the user): a CR with a live Driver reads `working`, the stored
  status, the same word everywhere; never `running`.
- stack-state-Q3 (2026-11-17, the user): a PR out of draft reads `PR out of draft`, never
  `PR ready` (`ready` is the ambiguous word this CR removes).

## What changes

### 1. CLI: the stack rows (`take stack`, `stack` with no CR)

Code: `skills/chantier/scripts/cli/src/chantier/commands/facts.py`, `stack_lines()` (called by
`commands/driver.py::_take_stack` and `commands/delivery.py::stack`). Today each row is

```
<cr> <state_word> worktree <path> branch <branch> base <ref> PR <link|none> head <sha7|-> <restack…>[ not on its place…]
```

where `state_word` (`stacks.py`) is the derived word: `ready to merge`, `PR in draft` or
`ready locally` for a CR whose status is `ready`, else the status. That derived word folds the
hand-back state and the draft flag into one word, which is the confusion.

New: the second field of each row is the combined label, built by a new small helper (in
`stacks.py` next to `state_word`, or in `facts.py`; the Driver chooses), used by `stack_lines`
only:

- the CR's recorded status, as stored (`queued`, `working`, `ready`, `blocked`; the stack holds no
  merged or cancelled CR), never a derived word; a CR with a live Driver reads `working`, never
  `running` (stack-state-Q2);
- when the CR has a PR recorded (`c.pr`), followed by `, PR <flag> (<ref>)`:
  - `<flag>` is the recorded draft flag `c.pr_draft`: `draft` (True), `out of draft` (False,
    never `ready`: stack-state-Q3), `draft not read` (None; the same words `ship` prints);
  - `<ref>` is the PR's number: `#<n>` for a GitHub PR link, `!<n>` for a GitLab MR link (a link
    that `forge_stack_gitlab.GITLAB_LINK` matches); a link with no trailing number gives no
    parenthesis (`, PR draft`). `status/gate.py::pr_number` gives `#<n>` today; reuse or extend
    it, no new parser.
- with no PR recorded: the status alone.

Examples: `ready, PR draft (#251)`, `ready, PR out of draft (#250)`, `working, PR draft (#253)`,
`ready, PR draft not read (!12)`, `queued`, `working`.

The rest of the row is unchanged (`worktree … branch … base … PR <link> head … restack: …` and the
`not on its place` tail). The label holds a comma and spaces; it is followed by ` worktree `, so a
reader splits on that word, as today.

Not changed: `state_word` itself and its other callers, which keep the derived words of
[concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), "Words": `status` rows (`batch_status.py`), `handoff`/`cr_facts`
(`facts.py` line 75), `forge-stack` (`forge_stack.py`), the hand-back lines (`driver.py`
`_ready_lines`), `stack --out-of-draft|--draft` replies, STATUS.md, STATUS.json (`readiness`), the
pane and the board. No `STATUS.json` field changes, so no pane screenshot is due.

### 2. Card: the stack driver (`skills/chantier/references/driver.md`, "## Stack driver")

- Where it says what the stack is from `take stack` ("The stack is what your prompt gives from
  `take stack`, each CR with its base…"): add that each row's label is the CR's hand-back state
  and, after a comma, its PR's draft flag as last recorded (`ship`, `stack --out-of-draft|--draft`)
  (`ready, PR draft (#251)`), and that a CR is handed back ready when its label starts with
  `ready`, whatever its PR's draft flag; a PR still a draft is the stack driver's to turn ready,
  never a reason to wait. Add one sentence: in the rows, the mergeable part is the run from the
  bottom of rows that read `ready, PR out of draft (…)`, and "ready to merge" in this section
  means a CR of that run (so the section's other uses, `driver.md` lines ~687-693, 735, 757 and
  776, and [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), "Stack", lines ~216-218, read consistently with the rows).
- "**Making the stack.**": "Once two CRs are handed back ready with their PRs" reads as the
  rows' `ready` (state), whatever the draft flag: say so in that sentence. Replace "the CRs with a
  draft PR on top as drafts" by the CRs not handed back ready on top, as drafts; the CRs handed
  back ready form the mergeable part, turned ready after the stack is made (as today:
  `gh pr ready`, then `stack --out-of-draft <cr>…`).
- "**Ordering.**": "the ones ready to merge first … then the newly ready … then the drafts" is
  written against the row labels: first the CRs handed back ready (`ready, …`), those already in the
  mergeable part in their place, then the newly ready in their place order, then the CRs with a
  PR that are not handed back ready (`working, …`, `blocked, …`), in the order the paragraph gives
  today.
- No other rule of the card changes. The agent files (`agents/`, `com.github.copilot/agents/`)
  carry none of this text and are not touched.

### 3. Card: words (`skills/chantier/references/concepts.md`, "## Words")

"Ready (the status)" says "no person reads `ready` alone". Add the one place it is shown: the
stack rows of `take stack` and `stack` show it with the PR's draft flag (`ready, PR draft
(#251)`), for the stack driver, which makes the stack from it. The three derived words stay
everywhere else.

### 4. Scenario and its README

- `scenario/run_scenario.py`, `ready_words` (section 13b), the check at "4. `status` and the
  `stack` rows read the same word" (today `ln.startswith(f"{c} PR in draft worktree")`): it now
  checks that `status` reads `PR in draft` for c and that the `stack` row of c starts with
  `f"{c} ready, PR out of draft (#<n>) worktree"` (c is handed back ready, its PR recorded out of
  draft over b's draft), and that b's row starts with `f"{b} ready, PR draft (#<n>) worktree"`.
  Rename the check accordingly ("`status` reads the derived word; the `stack` rows read the
  hand-back state and the PR's draft flag").
- Add, in the same section, after "6. a CR taken back for a round", one check that the `stack` row
  of the CR taken back reads `working, PR …` and that `take stack` prints the same CR rows as
  `stack` (the take of section 13b's batch, or the existing take-stack case at the mode switch,
  line ~5398). Compare only the CR rows (the lines that start with a stack CR's id and contain
  ` worktree `), never the whole output: `reopened` lines already sit between `take stack`'s
  head and its rows, and the pending P1 take-prompt-skeleton-per-role adds a prompt block to
  `take stack`.
- One check of a row with no PR: at the `edit_cr(b, drop=("pr",))` step of section 13b (after
  `w.ready(b, …)`, line ~6402; the `drop` at line ~6427, before `edit_cr(b, pr=bpr)`), the
  `stack` row of b starts with `f"{b} ready worktree"`: a CR handed back ready with no PR reads
  `ready` alone. A `queued` or `working` no-PR check (`f"{x} queued worktree"`,
  `working worktree`), if the Driver adds one, is made only on a CR whose record really has no
  `pr` (never one whose PR was dropped while it is `ready`).
- A GitLab MR's `!<n>`: one check in the GitLab stack part of the scenario (the `w.gh(mrs=…)`
  cases, line ~4884) that a `stack` row reads `(!<n>)`.
- `scenario/README.md`, the bullet "the three words of a ready CR …" (line ~173): the `stack`
  rows no longer show the three words; name them apart: "the `stack` and `take stack` rows: the
  hand-back state and the PR's draft flag (`ready, PR draft (#n)`)".

### 5. Tests

None required: the row is a format, proved by the scenario. A unit test of the label helper
(parametrized: status × draft flag × GitHub/GitLab/no-number link × no PR) is allowed if it stays
in `tests/` and fast (AGENTS.md: few, parametrized, fast).

## Out of scope

- The derived words (`ready to merge`, `PR in draft`, `ready locally`) and their icons anywhere
  but the stack rows; `status`, STATUS files, the pane, the board, `handoff`, `forge-stack`.
- Any change of the record (`batch.json`), the events, or a rail: `stack --out-of-draft` keeps its
  refusals.
- The Foreman's card: it passes `take stack`'s output as it is.
- Renaming a stored status: `working` stays the word everywhere (stack-state-Q2).

## Evidence

- `just check` green (Linux, macOS, Windows per AGENTS.md).
- `just scenario`: the pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (a
  CLI and card change); the checks of section 4 above pass, the existing ones of 13b and the GitLab
  stack part unchanged otherwise.
- A pasted `stack` output from a scenario run in the PR's Deliverables, showing at least one
  `ready, PR draft (#n)` row and one `working` row.
- The card diff of `driver.md` and `concepts.md` in the PR: the three edits of section 2 and the
  one of section 3, nothing else.

## Open questions

None.
