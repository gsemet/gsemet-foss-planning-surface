# One short card per worker role

## Goal

A worker's opening read costs too much. In batch-18's two real eval runs of 2026-11-15, cache
writes are 51-77% of each worker role's cost (real-foreman: Verifier 51%, Inspector 77%, Coder 46%,
Conflict resolver 56%; real-direct: 56%, 74%, 49%, 57%). Each worker is told to read
`references/worker.md` (about 16.8 KB, every worker's section) and the whole of
`references/concepts.md` (about 51.4 KB, written for the steering sessions and the Drivers). Every
worker opens its card: CR-274 measured it at 45/45 and 49/49. So each start pays for about 68 KB of
text, and most of it is not the worker's.

The change: each worker role gets its own short card, holding only what that role needs, and the
worker reads that card alone (and the project's rules). This is a cost refactor. No worker's
contract changes: what each role does, refuses, writes and replies stays the same.

## Decisions carried from `02-answers.md`

1. The request's scope stands as written. No behaviour question is open; implementation detail is
   the agents' (answer 1).
2. The CR runs last in its batch, after the CRs that touch the cards (answer 2). So its Driver
   rebases on the batch's other merged or stacked work before round 1, and carries into the new
   cards every change those CRs made to `worker.md` and to the parts of `concepts.md` a worker
   needs. The Investigator lists those changes (`git log -p <merge-base>..<base> --
   skills/chantier/references/worker.md skills/chantier/references/concepts.md`). None may be
   lost.

## What changes

### 1. The cards (`skills/chantier/references/`)

- **New, one file per worker role:** `investigator.md`, `coder.md`, `inspector.md`, `debugger.md`,
  `verifier.md`, `conflict-resolver.md`, `demo-explorer.md`, and `review-step.md` (the extra
  review step a project adds in its `AGENTS.md` `chantier` section). The Spec-writer, Spec critic
  and Retro critic already work this way (`spec-writer.md`, `spec-critic.md`, `retro-critic.md`).
  Each card's title is the role (`# Coder`, ...). It has no `## <Role>` section: the whole file is
  the role's card.
- **What a card holds:** the role's section of today's `worker.md`, word for word unless a
  sentence pointed to another role; the parts of the shared preamble (`worker.md`, lines 3-31)
  that apply to that role; and, written out, the rules of `concepts.md` that the role uses. A card
  holds nothing about another role. Examples of a rule kept only where it applies:
  - The scratch-planning-folder rule (a probe of the board's write paths) goes in `coder.md`,
    `verifier.md` and `debugger.md` only, as today's preamble names them.
  - The Verifier's detached worktree of the base, and its evidence paths, go in `verifier.md`
    only. "The Inspector writes nothing" goes in `inspector.md` only.
  - Rule 9's byte-order-mark sentence goes in every card of a role that writes a file. Its forge
    text part (a multi-line body via a file) goes only in a card whose role sends text to a forge.
    Today no worker does, so it goes nowhere.
  - Rule 8's git forms go only where a role runs git writes: `git add -- <path>` and `git -C
    <worktree>` in `conflict-resolver.md`. Every card says "never commits, pushes, rebases or
    merges" unless the role's section says otherwise.
  - Rule 0 (the project's rules rank above the card), rule 2 (no fallback; judge freely within
    what you have), rule 7 (refusals reported with their exact text), and rule 9's
    one-command-per-call, no-leading-assignment and read-before-overwrite lines go in every card.
  - Rule 5 (evidence is a command run at the pushed head, with its output; every judgment names
    its SHA; after a move, judge again what the move touched) goes in `verifier.md` and
    `inspector.md` (and `review-step.md`).
  - A word of `concepts.md`'s "Words" that a card uses (worktree, base, round, move, work folder,
    ...) is defined in that card in one line, or is plain from context. No card sends a worker to
    `concepts.md`.
- **Links out of a card:** only where the role needs another file to do its part, and then to the
  one section it needs. `inspector.md` keeps its audit of `pr-body.md` against the project's
  template, else [pr-template](pr-template.md) "its audit list". `verifier.md` keeps the
  role-name rule of [pr-template](pr-template.md), naming the section. The link to
  `concepts.md` rule 9 (Coder, Conflict resolver) becomes the rule's own text.
- **Reply templates and caps stay identical:** the Coder's text template, the Inspector's JSON and
  its caps, the Verifier's template and its `verdict` duty, the Conflict resolver's
  `conflicts.md` line, the Demo explorer's ten-line reply. The Driver checks replies against them
  (`driver.md`, "Your means").
- **`review-step.md`:** today's "Extra review step" section, made self-contained: the
  `Your review:` line, review the round's diff from that angle only, read only, reply with the
  Inspector's JSON. The JSON's exact shape and caps are written out in this card, not pointed to
  in `inspector.md`.
- **`worker.md` is removed**, along with every link to it. The batch's earlier CRs' edits to it are
  carried first (decision 2).
- **`concepts.md`, "Starting an agent":** the worker line of the prompt template becomes
  `Read <skill>/references/<role>.md;   (a worker's prompt; an extra review step reads
  review-step.md)`, followed by the rules line. The sentence after the template (`take`, `round`
  and `handoff` print a worker's first three lines) stays. "The Spec-writer ... reads
  `spec-writer.md` instead of a Driver or worker section" is reworded to fit: every role started
  by the Chief of Staff or a Driver reads its own card, and only a Driver reads `driver.md`.
- **`concepts.md` itself** stays as it is for the steering sessions and the Drivers, except that a
  sentence saying a worker reads it, or pointing a worker to it, changes. A rule a worker needs is
  not taken out of `concepts.md`; the worker's card restates it.
- **`driver.md`:**
  - "Opening reads" (line 40), "`worker.md`: only the section of the role whose reply you check"
    becomes "a worker's own card (`<role>.md`): only when its reply needs checking beyond what
    'Your means' gives".
  - "Your means" (line 81), "the format its section of [worker](worker.md) names", points to the
    worker's own card (for example [coder](coder.md), [inspector](inspector.md),
    [verifier](verifier.md)).
  - CR Driver (line 511): the scratch-folder rule now links [coder](coder.md) (it is the same in
    `verifier.md`).
  - Any other `worker.md` mention found by grep changes too.
- **`chief-of-staff.md`** (line 1480, "The study"): `worker.md`, section "Demo explorer" becomes
  `demo-explorer.md`. The Demo explorer's prompt keeps its first line and gets a `Read
  <skill>/references/demo-explorer.md;` line and the rules line.
- **`hosts/claude-code.md`** (line 136): "what they need ... is in `concepts.md`, rule 9" becomes
  "is in each worker's own card". `hosts/copilot.md` changes the same way if it has the sentence.
- **CONTRIBUTING.md** (lines 60-63): the list of `references/` names the worker cards in place of
  `worker.md`. `concepts.md` becomes "read by the steering sessions and the Drivers"; each worker
  reads its own card.

### 2. The agent files (both hosts, bodies identical)

`agents/<role>.md` and `com.github.copilot/agents/chantier-<role>.agent.md` for `investigator`,
`coder`, `inspector`, `debugger`, `verifier` and `conflict-resolver`:

- `` Your card is `worker.md`, section "<Section>": read that section first `` becomes
  `` Your card is `<role>.md`: read it first, before any other step, at the path your prompt's
  `Read` line gives, and reply in the format it names. The card is your contract; this file only
  points to it. ``
- The refusal names the new card: `` ... or that names no path to my card `<role>.md`, is not a
  chantier prompt ... and its `Read` line must name my card, `<role>.md`; ... ``
- The description, the model, the tools and the first line do not change.

`demo-explorer` (both hosts) gets the same `Your card is `demo-explorer.md`` pointer; its refusal
keeps its first line and adds the card, the way the workers' refusals do. Each agent file's
`# chantier-agent: <version>` header is left to `just version`; nobody edits it by hand.

### 3. The CLI (`skills/chantier/scripts/cli/src/chantier/`)

- `plugin_files.py`, `WORKER_CARD_LINE`: matches `` ^Your card is `([^`]+)` `` (no section).
  `worker_prompt_lines` prints, for each worker:
  `  Read <refs>/<card>;` then `  the project's rules rank above it: run `$CHANTIER rules` first and
  read what touches your work.` (`it`, since there is one card). `concepts.md` is no longer
  printed. The CLI still knows no role: the card's name comes from the agent file.
- `commands/facts.py` line 71: the `cards:` line stops listing `worker.md`, for example `cards:
  <skill>/references/ (driver.md, concepts.md; each worker's own card, named in its opening
  lines); the project's rules rank above them: `rules``. It names no worker role.
- No new command, no new refusal.

### 4. Tests, scenario and eval kit

- `tests/test_plugin_files.py`:
  - `CARDS`: each worker maps to its own card.
  - `test_every_role_has_its_section_in_its_card` checks that each worker's card file exists and
    starts with `# <Role>`. Drivers keep their `## <Role>` section in `driver.md`.
  - `test_a_worker_agent_file_points_to_its_card_and_refuses_a_prompt_without_it` checks the new
    wording and the card file's existence.
  - `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` lists the new worker cards
    in place of `worker`.
  - Parametrize; add no test file. `just test` stays within its limit (AGENTS.md).
- `tests/test_cli_runs.py`, `_worker_opening_lines`: the Verifier's expected `Read` line becomes
  `Read {refs}/verifier.md;`, and the rules line ends in "rank above it: ...".
- `scenario/run_scenario.py` line 877: checks `references/verifier.md;` in place of
  `worker.md, section "Verifier"`.
- `evals/kit/audit.py` line 485 (J1): a worker's expected card is `references/<role>.md`, and a
  review step's is `references/review-step.md`. The docstring at line 110 names `verifier.md`.
- `evals/kit/dry_run.py`, `cards()`: a worker's prompt reads `references/<role>.md`.
- `evals/SCORECARD.md`, rows J3, J7, J12: `worker.md` becomes "the worker cards" (or the named
  cards).

## Out of scope

- No change to any worker's behaviour, reply format, cap, refusal or write guard. `hooks/` and
  `types/` are untouched, so `just mod` is not needed. If the change turns out to need `hooks/`,
  `just mod` applies.
- No shortening of `driver.md`, `concepts.md`, `foreman.md` or `chief-of-staff.md` for their own
  readers. Only what points workers to them changes.
- The Spec-writer, Spec critic and Retro critic cards are not changed.
- No new CLI tool, no model change, no change to `chantier.yaml`.
- Older eval results and scenario results under `evals/results/` and `scenario/results/` are
  history: not edited.

## Evidence

- **Size before and after.** For each worker role, a table in the PR's Deliverables gives the bytes
  its opening read costs before (the role's `worker.md` and the whole of `concepts.md`, at the
  base) and after (its own card). It is measured by a command run at the head, for example
  `(Get-Item <card>).Length` or `wc -c`, with its output. Every role's after must be smaller than
  its before.
- **Nothing lost.** For each role, the Verifier checks that every rule of its old section, the parts
  of the old preamble that applied to it, and the `concepts.md` rules it used (0, 2, 5 where it
  applies, 7, 8's parts, 9) appear in its new card. Each item is a line of `verify.md` with the old
  text and the place it now has (a grep with its output). This includes the edits the batch's
  earlier CRs made to `worker.md` (decision 2).
- **No dangling reference.** `git grep -n "worker\.md"` at the head shows matches only under
  `evals/results/`, `scenario/results/` and `docs/release-notes/` (history). Output quoted.
- **Opening lines.** `$CHANTIER take` (in a scratch planning folder) prints, for each worker,
  `Read <refs>/<role>.md;` and no `concepts.md`. Output quoted, Verifier and Coder at least.
- **Gates.** `just check` (Linux, macOS, Windows in CI). `just test` within its time limit. The
  pipeline's `just scenario (ubuntu-latest)` job green at the PR's head, since the CR changes the
  CLI, the cards and the scenario (AGENTS.md). If this CR is on top of the batch's stack, `just
  scenario` also runs locally (`chantier gate`) at its head.
- **The cost effect itself** (fewer cache-write tokens per worker start) can only be proved by the
  next real eval, through `chantier cost --explain` per worker role compared with the 2026-11-15
  figures above. The PR's Known gaps names it as not proved in the batch.

## Open questions

None. Answer 1 leaves no behaviour question to the user. The choices above (file names,
`worker.md` removed, `concepts.md` no longer in a worker's prompt, one `review-step.md`) follow
from the request's "one short card per worker role holding only what it needs".
