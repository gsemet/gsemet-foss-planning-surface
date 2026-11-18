# Change Specification: explain a refusal before the user hits it, why, and what to do now

Type: docs (cards and user docs). No issue (verbal origin). Checked against `main` at `3a9afc2c`
(2026-11-18).

## Goal

When a rule (chantier's cards, the project's rules, the host) or the CLI will refuse what the user
asks, the Chief of Staff says so at once, before trying and not only after the refusal, in the
user's language, in three parts: what is refused, why the rule exists, and what the user can do
now (the alternatives). The owner's trigger (2026-11-13, a direct batch in another project): « tu
attends que le batch soit en pause. tu aurais dû l'indiquer. »

## What `main` already does (scoped out or corrected)

- **`order add` on a running direct batch is no longer refused.** Since CR-171 (2026-11-11,
  commit `204d4787`), `order add --note <folder>` on a running direct batch queues the CR (taken
  when a slot frees): `skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py`, `_add`;
  `chief-of-staff.md` ("A CR added while the batch runs is queued", ~line 1545) and `concepts.md`
  (~line 294) say so. So case 1 of `01-intent.md`, as written ("`order add` exits 2; only a release
  or a fix joins"), is not true at `main`. What still holds in a running direct batch, and what
  this CR explains instead (Part 2, row A):
  - the Chief of Staff does not grill (the grill waits for the pause; `chief-of-staff.md`, "Not
    while the batch runs");
  - `order qa` is refused (`commands/orders.py`, `_qa_row`: "a running direct batch takes no QA:
    order it once the batch is paused", exit 3);
  - `order add` needs a specified CR (`prepared_cr` in `commands/opening.py`), so a new idea joins
    only once grilled and specified.
- **The release note of case 1 is partly outdated.** At `main` a CR added before the release CR
  starts joins that release: the release waits for it and its procedure word is voided
  (`commands/orders_release.py`, `join_release`). Only once the release has started is `order add`
  refused (`check_release_open`: "Add a fix with `order add --fix-for <rel>`, or put the new work in
  the next batch"). Part 2, row B carries this true form.
- **Stale user docs are the likely source of the wrong explanation.** These still say a running
  direct batch refuses `order add`: `docs/use-cases-direct.md` (lines 21-23, 61, 114),
  `docs/tutorial-claude-code.md` (line 146), `docs/batch-lifecycle-texts.md` (the `<desc>` text
  and the box "🤵 direct mode: strict while running", lines ~74-79) and `docs/batch-lifecycle.svg`
  (its `<desc>`, line 3, and the box at lines ~56-62). Part 3 corrects them: the code is the
  target (`02-answers.md`, 2026-11-18).
- **Case 5 is mostly in place.** `references/hosts/claude-code.md` (lines 379-389) already
  describes the host's refusal of a subagent's Write of `report*`, `summary*`, `findings*`,
  `analysis*` `.md` names, says it comes before any permission check, and ends "Name a subagent's
  file with a number first". `references/concepts.md` (lines 524-526) still words it as advice
  ("prefer a numbered name"), and line 84 calls it "the advice". Part 4 makes it the rule.

## What changes

### Part 1: the rule (`skills/chantier/references/chief-of-staff.md`)

1. **"Hard rules"**: add one bullet, after "No fallback", titled **A refusal is said before it is
   met.** Content: when what the user asks will be refused by a rule (this card, the project's
   rules, the host's reference) or by the CLI, say so at once, in the turn the user asks, before
   any try, in the user's language, in three parts: what is refused; why the rule exists; what the
   user can do now, each alternative with its condition as "Offering options" says (only what they
   can do from where they are). A refusal already met is said the same way, its exact text first
   (concepts rule 7 holds). Never try the refused action to see; never offer a workaround the
   rules forbid ("No fallback" holds). Link to the new subsection of Part 2.
2. **"Steering a batch yourself", "What you accept while you steer"** (~lines 1566-1569): the
   line for a request to grill ("to grill in parallel, fork this session; the fork becomes a
   Griller") becomes the three-part answer of row A below, said at once.

### Part 2: the known refusals (`chief-of-staff.md`, "Offering options")

Add a subsection at the end of "Offering options", before "Steering a batch yourself", named
**Refusals to say before they are met**: one sentence that it applies the Hard rule, then a table
`| What the user asks | What is refused | Why | What the user can do now |`. Rows A to H,
only these (`02-answers.md`, 2026-11-18); each row's facts are checked against the code at the
Driver's head, and a row that no longer matches it is corrected to the code, saying so in the PR:

- **A. A new idea, a grill or a QA while a direct batch runs.** Refused: the Chief of Staff does not
  grill while it steers (the grill waits for the pause), and `order qa` is refused until the
  pause. Not refused: a CR already grilled and specified, which `order add` queues at once (taken
  when a slot frees), and filing or triaging the idea now. Why: in direct mode this session steers
  the batch; the limit protects that steering's attention (and the user's), and Foreman mode
  exists for this dynamism. What to do: grill it now in a Griller session (`/chantier:griller`, or
  a fork of this session on Remote Control), then `order add` queues it here; or file it now and
  grill it at the pause; or switch to Foreman mode ("Switching to Foreman mode", where the
  checklist allows it), where this session grills while a Foreman steers and a QA may be ordered at
  any time.
- **B. A new CR while the batch has a release CR.** Before the release starts: not refused, but
  the release then waits for the new CR and the user's word on its procedure is voided (asked
  again). Once the release has started: `order add` is refused. Why: a started release ships the
  work under it; what it ships must not change under it. What to do: before it starts, add the CR
  and give the procedure word again, or keep the CR for the next batch so the release is not
  delayed; once started, a fix of the release (`order add --fix-for <release-cr>`) if it belongs to
  this release, else the next batch (filed and grilled meanwhile). Also say (audit case a): a
  batch with a release CR pauses only once the release has ended, so the pause, and in direct mode
  the grill it opens, comes later; a CR kept for the pause misses that release.
- **C. A subagent's file named `report…`, `summary…`, `findings…` or `analysis…` (`.md`), on
  Claude Code.** Refused by the host itself, on the file name, before any permission check: not
  the auto-mode classifier and not a permission rule, so no allow rule and no setting fixes it.
  Why: the host wants a subagent to return such content as text. What to do: nothing for the user
  to set; the file takes a number prefix (`04-report.md`), as concepts says (Part 4). Say this when
  the user asks why a subagent's file has a number, or when such a refusal is met.
- **D. "Close the batch" while something still runs (audit case b).** Refused: `close` (with or
  without `--yes`) while a CR is not merged or cancelled, an order is open, a stack agent or a held
  agent still runs or cannot be read; on Copilot, an agent whose session file was written in the
  last 5 minutes counts as running (`concepts.md`, ~lines 181-187; `commands/closing.py`). Why:
  `close` deletes the batch's own files and prices its final cost; work still running would be cut
  off and left out of that cost. What to do: wait for the running agent's end (the refusal names
  it), then `close` again; on Copilot, wait until 5 minutes after its last write; a held agent that
  has ended and has no transcript: `agents set <cr> - --epoch <n>` on the user's word; a CR left
  open: merge it, or drop it (`order drop`) on the user's word.
- **E. The word to run the release procedure while other CRs are open (audit case c).** Refused:
  `order confirm <release-cr>` while another CR of the batch (fixes aside) is not merged or
  cancelled, or while the release PR is not merged (`commands/orders_apply.py`, `_confirm`). Why:
  the word covers exactly what the release ships; a CR merged or added after it would change that
  (an `order add` voids a word given before). What to do: merge or drop the open CRs first, then
  give the word; or give it with the merge go of the release PR, as the cards ask at the ready ask
  (commit `3a9afc2c`).
- **F. A batch (or `order add`) with a CR that has no specification (audit case d).** Refused:
  `open` and `order add` refuse a CR folder with no `03-change-spec.md` ("missing Change
  Specification: ...; grill the CR first", `lifecycle/stages.py`, `_specification`), except a CR in
  `3-ready` with `intake/request.md` (automatable: the request is its specification). Why: a Driver
  works from the specification alone; without one it would guess the user's intent. What to do:
  grill it and have the spec-writer write the specification (in direct mode while a batch runs, in
  a Griller, row A); or, when the CR is automatable, `triage --ready` it on the user's word so its
  request serves as specification.
- **G. More work on a CR past its round limit (audit case f).** Refused: `round` once a CR has used
  its rounds (three unless granted; "round limit <n> reached; hand back blocked, only the user
  grants more (`order rounds`)", `rails.py`); the CR comes back blocked. Why: the limit caps what a
  CR that does not converge may spend before the user looks at it. What to do: read the blocked
  CR's question, then grant more rounds (`order rounds <cr> --note <n>`), change or split the CR,
  or drop it.
- **H. A model with no price (audit case h).** Nothing is refused: `close` still runs and the cost
  is a floor (`commands/closing.py`; `concepts.md`, ~line 367); the budget check uses that floor.
  Why: chantier prices only models it knows a rate for, and never estimates one. What to do: add
  the model's price under `prices:` in `chantier.yaml` (exact model id, $/MTok,
  `docs/agents-and-models.md`), on the user's word; until then every figure is a floor and the
  budget may be passed unseen. Say it when the user picks such a model, not only when the cost
  report's not-priced line appears.

### Part 3: the user docs agree with the CLI

- `docs/use-cases-direct.md`: replace "The running batch is strict. No CR joins it while it runs:
  `order add` and `order qa` are refused..." (lines 21-23) with the truth at `main`: a specified CR
  joins a running direct batch (`order add` queues it, taken when a slot frees); `order qa` is
  refused until the pause; a release CR and its fixes join as ever; a paused batch takes any number.
  Line 61 ("The orders that add work to a running batch do not, as above") becomes: `order qa`
  does not, as above. Line 114 drops "since the running batch is strict about everything else" and
  keeps that a release CR and its fixes join a running direct batch. Add, in "No grill in the same
  session", one sentence that the Chief of Staff says this limit, its reason and the Griller way at
  once when the user asks for a grill.
- `docs/tutorial-claude-code.md` line 146: "(no CR joins a running batch, and that session holds
  no grill)" becomes "(that session holds no grill and orders no QA while the batch runs; a CR
  grilled elsewhere still joins it)".
- `docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg`, kept identical in their texts:
  the `<desc>` sentence "A running direct batch is strict: order add and order qa are refused,
  except a release CR and its fixes." becomes "A running direct batch takes no grill in its session
  and no order qa; order add queues a specified CR, and a release CR and its fixes join." The box
  title "🤵 direct mode: strict while running" becomes "🤵 direct mode: while running"; its two
  lines become "`order add` queues; `order qa` refused," and "no grill in this session". Keep the
  box's geometry; widen nothing unless a line overflows the 288-px box at its font size (check
  in a browser render).

### Part 4: the prefix rule (`skills/chantier/references/concepts.md`)

- Lines 524-526 become a rule: every file a subagent writes takes a number prefix (`04-result.md`,
  `04-report.md`), except a name a card fixes (`03-change-spec.md`, `delivery.md`, `STATUS.md`,
  `retro.md`, the `work/` files the cards name), which the probe of 2026-11-10 accepted. The parent
  that starts a subagent tells it so. Say that the host refuses some unprefixed names on the name
  alone (link to the host's reference): it is not the auto-mode classifier, and no allow rule
  fixes it.
- Line 84: "follow the advice for subagent files below" becomes "follow the rule for subagent
  files below".
- `references/hosts/claude-code.md` line 389: keep "Name a subagent's file with a number first",
  add "(the rule: concepts, 'Starting an agent'); this is the host's own rule on the name, before
  the auto-mode classifier and any permission check".

## Decisions of `02-answers.md`, carried

- 2026-11-13 and 2026-11-18, audit cases: case 1 (the trigger) is row A; case 5 is row C and
  Part 4; (b), (c), (d), (f), (h) are rows D to H; (a) folds into row B; (e) and (g) stay in the
  host references (out of scope).
- 2026-11-18, the code is the target for a running direct batch (`order add` queues it, CR-171;
  the factory mode, CR-370, builds on it): Part 3 corrects the docs and the SVG together.
- 2026-11-13, case 5: the refusal is not the classifier; the fix is a number prefix on the files a
  subagent writes: Part 2 row C and Part 4.

## Out of scope

- Any CLI change: no refusal message is rewritten, no command added or changed (the rule is the
  Chief of Staff's, a card's judgment; the CLI's refusal texts already name what to do in rows A
  and B).
- The Griller's, the Foreman's and the workers' cards (the intent names the Chief of Staff, who
  talks with the user).
- Bringing back the refusal of `order add` on a running direct batch: the code is the target.
- Audit cases (e), an action refused to a peer session, and (g), Remote Control limits: they stay
  in the host references, unchanged.
- Renaming the files whose names the cards fix; the Chief of Staff's own `report.md` in a release
  CR (the Chief of Staff is not a subagent; the host refuses only a subagent's write).
- `agents/` and `com.github.copilot/agents/`: unchanged.

## Host and default matrix (Part 4, row C)

- Claude Code: the host refuses a subagent's Write of the four name prefixes (probe 2026-11-10,
  `hosts/claude-code.md`); the number prefix avoids it: proved by that probe.
- Copilot: no such refusal is known; the prefix rule applies the same (harmless): unproved that
  Copilot refuses anything, and the docs say nothing of Copilot for row C.

No shipped default versus configured value is involved.

## Evidence

- `just check` passes at the head (cards and docs change; it includes the structure tests that
  read the shipped cards, e.g. `tests/test_startup_manifest.py`, `tests/test_plugin_files.py`).
- `just scenario` passes before the PR (a change to the cards: AGENTS.md); no scenario step is
  added (no CLI behaviour changes).
- No new test: the change is card and docs wording, and the project keeps tests to structure and
  the CLI's refusals.
- Checks in the PR's Deliverables, each a command at the pushed head with its output, reading the
  shipped files:
  - `git grep -n -e "strict while running" -e "no CR joins" -e "batch is strict" -- docs skills`
    finds nothing.
  - `git grep -n "A refusal is said before it is met" -- skills/chantier/references/chief-of-staff.md`
    finds the Hard rule, and `git grep -n "Refusals to say before they are met"` its subsection.
  - `git grep -n "prefer a numbered name\|the advice for subagent files" -- skills` finds nothing.
  - The texts of `docs/batch-lifecycle.svg` (its `<desc>` and the direct box) match
    `docs/batch-lifecycle-texts.md` word for word; one rendered screenshot of the SVG's direct box
    in the PR shows no overflowing line.
- A reviewer reads each row of Part 2 against the code paths named in "What `main` already does"
  and confirms every "refused" and "not refused" there matches the CLI at the head.

## Open questions

None: both were settled in `02-answers.md` on 2026-11-18.
