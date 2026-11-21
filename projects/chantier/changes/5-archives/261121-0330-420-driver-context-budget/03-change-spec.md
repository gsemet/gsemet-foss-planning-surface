# A CR Driver reaches ready without a context hand-back

## Goal

In batch-29 nearly every CR Driver handed its CR back `blocked context:` before the CR closed. Each
hand-back costs a fresh Driver, a new reading of the cards and often a lost lease. After this CR a
CR Driver reads less of its card before each step, a restarted Driver reads only what is left to
do, and the closing step starts in the same Driver up to 115,000 tokens. The aim: a CR that takes
three rounds reaches `handback ready` in one Driver.

This CR changes cards, the startup manifest, one test file and one scenario check. It changes no
CLI code and no agent file.

## The measure (batch-29, 2026-11-19 and 2026-11-20)

Read from the batch's `events.jsonl` and from the transcripts of its 69 CR Driver runs (27 first
takes, 42 restarts), all on the Claude Code host. "Context" is the prompt size of a call, as
`round` and `note` print it.

| What | Figure |
| --- | --- |
| Hand-backs `blocked context:` | 25, of which 19 are the closing hand-off (`context: closing: VERIFIED at …`) |
| Hand-backs `ready` | 33 |
| Context at a Driver's first call (the host's own prompt, the tools, the project's rules) | about 25,000 tokens (23,500 to 28,000) |
| Context when a first-take Driver starts its first worker | about 77,000 tokens (61,000 to 103,000) |
| Context when a first-take Driver ends | median 113,000 tokens (88,000 to 131,000) |
| Context added from the first worker to the Verifier's start | 25,000 to 40,000 tokens; round 1 adds 10,000 to 13,000, a later round 3,000 to 5,000 |
| Context added by a closing after its description pass starts (restarted Drivers) | 2,000 to 6,000 tokens |

What a first-take Driver takes into its context, in bytes, average per run (184 KB in all):

| Source | Bytes | Share |
| --- | --- | --- |
| `driver.md`, by the Read tool (3.2 reads a run) | 55,250 | 30% |
| `driver.md` and the cores, printed by a shell command | 9,819 | 5% |
| `pr-template.md` | 11,354 | 6% |
| `concepts.md` ("Starting an agent", 13 KB when read) | 8,243 | 4% |
| The cores and `startup-manifest.json` | 5,515 | 3% |
| The host's reference | 3,164 | 2% |
| The specification | 23,027 | 13% |
| Its own tool calls (workers' prompts, command lines, `pr-body.md`) | 29,161 | 16% |
| The CLI's outputs | 9,215 | 5% |
| Git, the forge, the gates, the workers' replies, the rest | about 29,000 | 16% |

So the cards are 93 KB of 184 KB. Before its first Coder a Driver reads 33,000 to 47,000 bytes of
`driver.md`: the opening (5,449 bytes), three to eight `Means:` sections (18,000 to 32,000) and
"CR driver" (9,174). A restarted Driver reads 34,000 bytes of `driver.md` on average (28 KB by
Read, 6.5 KB by a shell command), whatever step it resumes at.

Two causes follow. The reading before the first Coder takes half of the room a Driver has (from
25,000 to 130,000 tokens). And the closing hand-off at 100,000 tokens sends most CRs to a second
Driver, which reads the card again.

## What changes

### 1. `skills/chantier/references/driver.md`: readings by step

No rule of the card is dropped or changed in meaning, except the threshold of part 3. A rule moves
with its text. Where a section loses a rare case, it keeps one line that names the section holding
it, in the card's usual form (`<case>: "<section>"`).

Byte figures are LF bytes of the file as it ships.

**The opening** (the text before the first `## `): at most 2,500 bytes (5,449 today). It keeps:

- what a Driver is and what is its own (the first paragraph);
- the project's rules first (`$CHANTIER rules`), whole for the instruction file, by part for the
  rest;
- the specification: what the Driver reads of it and what it leaves to the workers;
- how to read a card (Grep the heading, Read with offset and limit; a section in full; never
  printed with `cat`, `sed`, `awk` or `Get-Content`; never read again once in context);
- "A rule you did not read still binds you";
- the steps and their readings, for a CR Driver, as a short list that names the manifest's three
  lines (part 2): before the first Coder, `cr-driver`; before the first commit, `cr-driver:ship`;
  at the pushed-head `VERIFIED`, `cr-driver:closing`; a hand-back at any moment, "Means: your end";
- one line for a Driver started again: read "Means: a Driver started again" first.

It loses, each moved as said:

- the "By section, when the step comes" list: each link goes to the section of the step that uses
  it (`concepts.md` "Starting an agent" to "Means: the record and the workers"; `pr-template.md`
  to "Means: commits, the PR's state and the evidence"; the host's reference parts to the bullets
  that already name them; a worker's own card to "Means: the record and the workers");
- "Images and git": the image rule to "Means: images and the look", the branch-listing and
  `git status` rule to "Means: the worktree";
- the "A Driver started again" bullets: to the new section below.

**New section `## Means: a Driver started again`** (a trigger section, in no manifest line; at
most 2,000 bytes): the text of today's "A Driver started again" bullets (`handoff <cr>` and
`log <cr>` first; `resume: closing`; `rebase:`, `restack`, `folded:` and other re-take notes), and
this rule, new: a Driver started again reads the sections of the steps still to do and never
those of the steps done. A `resume: closing` Driver reads the `cr-driver:closing` line only; a
Driver resumed before the first push reads `cr-driver:ship` and no part of `cr-driver` but
"Means: the record and the workers" when it starts a worker.

**`## Means: worktree, rebase and push`** is split in two:

- `## Means: the worktree`: its first bullet (the worktree is the first step: the fetch, the
  `worktree add`), with the branch-listing rule moved from the opening;
- `## Means: rebase and push`: the three other bullets (the rebase, the checks before the first
  push, the push and the PR).

**`## CR driver`** is split in three, in this order in the file:

- `## CR driver`: the contract (the first four paragraphs: what it never edits, the board's write
  paths line, the lease, never discarding the worktree's work), the step before round 1, the
  round up to `All approved`, and the paragraph "Every `APPROVE` is recorded at once". It ends
  with one line that names `cr-driver:ship` as the next reading.
- `## CR driver: ship and proof`: from "All approved: first check nothing changed since the
  review" to the `closing: VERIFIED at` note (the commit, the matrix probe's line, the rebase,
  the checks before the first push, the long gate, the push, the PR, `ship`, CI, the Verifier at
  the pushed head), the "After a move" paragraph and the "A gap you judge left" paragraph.
- `## CR driver: the closing`: the closing's four steps, the hand-off rule and the context rule
  during the closing.

"Means: the record and the workers" and "Means: context and your folder" are shortened to fit the
first limit of part 5. What may move out of them: the format checks of a reply the Driver sees
only later (the Verifier's to "CR driver: ship and proof", the Conflict resolver's to "Means:
carries, conflicts and the early push"), and the list of large outputs never taken whole (to the
sections of the steps that produce them: the long gate, CI). The context rule itself (the
`context:` line, 130,000 tokens, the host asking for the hand-back, never ending a turn to wait
for a child) stays in "Means: context and your folder".

Every reference to a renamed section follows, in the card and in the other cards: `driver.md`
(the lines that say `"Means: worktree, rebase and push"`, `"CR driver"` for the closing, "the
closing paragraph of "CR driver""), `foreman.md` and `hosts/*.md` when they name one. The
`## Startup core` section keeps its text.

### 2. `skills/chantier/references/startup-manifest.json`: the CR Driver's three lines

In `actions`:

```json
"cr-driver": ["driver.md#Means: the record and the workers", "driver.md#Means: context and your folder", "driver.md#Means: the worktree", "driver.md#CR driver"],
"cr-driver:ship": ["driver.md#Means: rebase and push", "driver.md#Means: the long gate", "driver.md#Means: CI", "driver.md#Means: commits, the PR's state and the evidence", "driver.md#CR driver: ship and proof"],
"cr-driver:closing": ["driver.md#CR driver: the closing", "driver.md#Means: your end"],
```

`stack-driver`, `qa-driver` and `release-driver` keep one line each, with "Means: worktree,
rebase and push" replaced by "Means: the worktree" then "Means: rebase and push", and nothing
else changed. `version`, `limit`, `roles` and `startup_sections` do not change.

The card's "Deferred" sentence in the opening is rewritten to say it: a CR Driver's common path
is the three lines, each read when its step comes; a `Means:` or `CR driver:` section that no
line lists is a trigger section.

### 3. The closing hand-off threshold: 100,000 becomes 115,000 tokens

A Driver carries the closing out itself when the last `context:` line it read is below 115,000
tokens; at 115,000 or more, or with `context: not measured`, it hands off (`handback <cr> blocked
context: closing: VERIFIED at <sha7>; next: …`). The 130,000 rule does not change, nor the rule
during the closing.

The four places that write the figure:

- `driver.md`, "Means: context and your folder" ("at 100,000 or more at `VERIFIED`");
- `driver.md`, "Means: your end" ("at the pushed-head `VERIFIED` at 100,000 tokens or more");
- `driver.md`, the closing ("below 100,000 tokens", "At 100,000 tokens or more"), now in "CR
  driver: the closing";
- `foreman.md`, "A hand-back `blocked context: …`" ("with 100,000 tokens or more").

The card says why in one clause, as it does for 130,000: a closing adds about 15,000 tokens to a
Driver that holds the cards and wrote the body (batch-29).

### 4. `skills/chantier/references/concepts.md`: "Starting an agent" in parts

The section `## Starting an agent` gets level-3 headings, its text unchanged and in the same
order:

- `### The agent and the model`: from the section's start to the `Needs:` bullet;
- `### The prompt`: from "The prompt is the agent's whole brief" to the end of the first-lines
  table;
- `### The Chief of Staff's subagents`: the two paragraphs "A subagent of the Chief of Staff …"
  and "Every file a subagent writes …";
- `### An agent that ends before its part is done`: the bold paragraph and its four bullets (the
  bold lead-in becomes the heading);
- `### The specification's agents and the Retro critic`: the last paragraph (Spec-writer, Spec
  critic, Retro critic);
- `### A Driver's prompt`: unchanged, and its table stays directly under its heading
  (`driver_prompt.py`'s `driver_table` reads it there).

`driver.md` then names what a Driver reads: "The agent and the model" and "The prompt" before its
first worker's start, "An agent that ends before its part is done" only when a worker ends
early ("Means: a worker that fails" names it). A card that names `"Starting an agent"` for
another role keeps doing so: the whole section still exists under that heading.

### 5. `skills/chantier/scripts/cli/tests/test_startup_manifest.py`: the limits

- `_check_actions`: the four Driver lines keep their checks (the last reading is the role's
  section, the others are `Means:` sections). Added for `cr-driver:ship` and `cr-driver:closing`:
  each reading is a section of `driver.md`, exactly one of them is a `CR driver: …` section, the
  three lines share no reading, and no other role's section is in them.
- `test_cr_driver_common_path_reads_at_most_the_card_budget` is replaced by one parametrized
  test, three cases, each summing the opening (up to the first `## `) and the named sections of
  the shipped `driver.md`:

  | Case | Sections | Limit (bytes) |
  | --- | --- | --- |
  | before the first Coder | `actions["cr-driver"]` | 18,000 |
  | the whole common path | the three `cr-driver` lines | 36,000 |
  | a `resume: closing` restart | "Means: a Driver started again" and `actions["cr-driver:closing"]` | 13,000 |

  Each case also keeps today's checks: every reading resolves to a non-empty section of the card.
- One more assertion, in the same test or beside it: the opening is at most 2,500 bytes.
- The `MOVED_IN` row for `driver.md`'s Startup core stays. One row is added: the phrase "never
  those of the steps done" in `driver.md`, section "Means: a Driver started again".

No test is added elsewhere; the file stays fast (it reads a few files, no CLI call).

### 6. `scenario/run_scenario.py`: the card check

In section 12c, the check "driver.md names the 100,000-token closing threshold and the three
`closing:` step notes; …" reads `"115,000 tokens" in flat_driver` and its title names 115,000. It
also asserts that `"100,000 tokens"` is no longer in `driver.md` nor `foreman.md`. Nothing else in
the scenario changes.

## Decisions carried from the answers

1. The measure is the one above, made from batch-29's transcripts; the CR adds no measuring tool
   (`round`, `note` and `cost --by cr` already print a Driver's context).
2. The figures of "The measure" size the cut; the request's "about 100k at the first read" is the
   context at the first worker's start.
3. The cut is on the CR Driver's reading of `driver.md` and of "Starting an agent", by sections
   read step by step; no rule is dropped.
4. Three byte limits checked on the shipped card: 18,000 before the first Coder, 36,000 for the
   whole common path, 13,000 for a `resume: closing` restart.
5. The CR Driver's readings are three manifest lines: `cr-driver`, `cr-driver:ship`,
   `cr-driver:closing`. The three other Drivers keep one line each.
6. A Driver started again reads the cores, the opening, "Means: a Driver started again" and the
   sections of the steps still to do, never those of the steps done.
7. The closing hand-off threshold is 115,000 tokens; the 130,000 rule stays.
8. No CLI change, and no change to a Driver's prompt lines.
9. Stack, QA and Release drivers are out of scope, but for the shared sections and their manifest
   lines following the renamed sections.
10. Done in this CR: the limits hold on the shipped card and the scenario checks the threshold.
    Done for the request: in the first batch that runs the merged cards, a CR that takes three
    rounds reaches `handback ready` with no `blocked context:` hand-back, read by the Chief of
    Staff at that batch's retro from `events.jsonl` and `cost --by cr`.
11. Split out as the inbox item `driver-context-second-cut`: the reading of the specification,
    of `pr-template.md` and of the manifest, the CLI's outputs to a Driver, and the size of its
    tool calls.
12. Studio's 46 restarts are evidence of the same cause, not a second scope.

## Out of scope

- Any CLI code (`skills/chantier/scripts/cli/src/`), `driver_prompt.py` and the prompt lines
  `take`, `take stack` and `order qa` print.
- The agent files (`agents/`, `com.github.copilot/agents/`): none changes, so both hosts stay
  identical.
- The role sections "Stack driver", "QA driver" and "Release driver", and the trigger sections,
  but for a text moved into one.
- The 130,000-token rule, `autoCompactWindow` and the Driver's model.
- `pr-template.md`, `startup-core.md`, `role-core.md`, the host cores and the host references.
- A new CLI tool or a new record field for the measure.
- A real eval. The measure on real Drivers is the next batch's own record (decision 10).
- What `driver-context-second-cut` holds (decision 11).

## Expected effect, stated as an estimate

The reading cut takes about 16 KB out of a first take (the common path from 44,974 to 36,000
bytes, "Starting an agent" from 13 KB to about 6 KB), about 5,000 tokens, and a restart at the
closing reads at most 13,000 bytes of the card where it read 34,000. The threshold moves the
closing into the first Driver for a CR verified below 115,000 tokens: in batch-29 a one-round CR
started its Verifier at 85,000 to 112,000 tokens. A three-round CR started its Verifier at about
105,000 to 125,000 tokens in batch-29; after the cut some will still pass 115,000. These are estimates: the next batch's record is the proof, and `driver-context-second-cut`
is the next step if a three-round CR still hands back on context.

## Evidence

This CR changes cards and the scenario: it owes `just check` at the pushed head and the
pipeline's `just scenario (ubuntu-latest)` job green at the PR's head. It changes nothing under
the CLI's `src/` nor the eval kit, so it owes no `just eval-dry-run`. It changes neither `hooks/`
nor `types/`, so no `just mod`. It adds or changes no CI job.

No host and default matrix: the readings and the thresholds are the same on both hosts and under
any configuration.

The checks that guard a shipped file read that file from the repository as it ships, at the head
under test: `test_startup_manifest.py` reads `skills/chantier/references/driver.md` and
`startup-manifest.json` through `conftest`'s `SKILL`, and the scenario reads `driver.md` and
`foreman.md` from `HERE.parent / "skills" / "chantier" / "references"`. No check uses a prepared
copy of a card.

Claims and their proof:

1. The three limits and the opening's limit hold: `just test` (the parametrized test of part 5),
   with the `startup-bytes` figures it prints quoted in the PR, before and after (44,974 bytes
   for the whole common path at `main`).
2. The manifest's three CR Driver lines resolve, share no reading and end on the right role
   section; the three other Drivers' lines resolve: the same test file.
3. The threshold reads 115,000 in the four places and 100,000 in none: the scenario's check of
   part 6, and `grep -n "100,000" skills/chantier/references/driver.md
   skills/chantier/references/foreman.md` printing nothing.
4. No rule dropped: the Inspector compares the card at the base and at the head, section by
   section. The Coder writes in `r<n>.md` a table of the moves: each paragraph or bullet that
   left a section, with the section it is in now. A paragraph absent from that table and absent
   from the head is a blocking item.
5. Every link to a section resolves: for each `"Means: …"` and `"CR driver…"` name quoted in
   `driver.md`, `foreman.md`, `concepts.md` and `hosts/*.md`, a `## ` heading of that name exists
   in `driver.md` (a command in the Verifier's proof, its output quoted).
6. `driver_table` still reads "A Driver's prompt": `just test` (`test_driver_prompt.py`,
   unchanged, passes).
7. Both hosts' agent files are untouched: `git diff --stat <base>..<head> -- agents
   com.github.copilot` prints nothing.

Not provable in this CR, and said so in the PR's Known gaps: "no real Driver has read the new
cards; the three-round measure is the next batch's" (a worktree's cards load only once merged
into the main checkout).

## Open questions

None. Every point was settled on 2026-11-20 without the user, as `02-answers.md` records.
