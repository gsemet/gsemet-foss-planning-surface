# SC09: AGENTS.md: roles are data, the CLI advises and refuses

Child 9 of 28 of the program CR `simplify-cards-and-prompts` (its `03-change-spec.md`, "Child 9",
and its `02-answers.md` answers 11 and 17 to 22 rank above this file). One Driver, one PR, in the
running stack batch (batch-31). Code read: `origin/main` at `8a960d34`. The change is one
paragraph of the repository's root `AGENTS.md`; no code, card, test or hook changes.

## Goal

The owner's words (answers 11, 22 F7): the tools this program adds (`brief`, `help --for`, `next`,
`msg steering`, `judge`, `roles.yaml`) would contradict four sentences of `AGENTS.md` as they
stand: "the parent ... names the card in its prompt", "the CLI (`rails.py`) says what it refuses",
"The CLI knows no role", and nothing yet says that the CLI's advice never decides. One child,
before the brief child, rewrites them: roles are data the CLI reads; the CLI advises with `next`,
refuses with its rails, and never decides a merge or a take-back; `judge` only words the ask.
Children 10 to 14 and 18 then cite these sentences instead of each rewording the rule.

## Place in the chain

- **Base:** child 8's branch (`sc08-host-rows-and-proofs`, the CR's recorded `chantier/*`
  branch), the previous CR of the stack. Child 8 adds its own `host` line to `AGENTS.md`'s named
  exceptions (in the long "The CLI's scope" bullet); this child does not touch that line and
  rebases over it with no overlap (the edited paragraph is a different bullet, lines 43 to 49 at
  `8a960d34`).
- **Depends on it:**
  - child 10 (`brief-prompts`) builds on this branch; its own AGENTS.md change (the `brief` line,
    `chantier/briefs/` in the git folder's write list) leaves the role sentences to this child;
  - child 11 states "AGENTS.md: none beyond child 9";
  - child 12 (`next`) and child 14 (`judge`) cite the wording "advises with `next` ... never
    decides a merge or a take-back" and "`judge` only words the ask";
  - child 13 (`msg steering`) and child 18 (`roles.yaml`) rely on "the CLI knows roles only as
    data (`skills/chantier/roles.yaml`, ...)": child 18 adds no AGENTS.md line because of it.
- The wording below is therefore binding for those children: change it only by an answer of the
  owner.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 22, F7 | One child before the brief child rewrites the four AGENTS.md sentences: roles are data the CLI reads; the CLI advises with `next`, refuses with rails, never decides a merge or a take-back; `judge` only words the ask | the whole CR |
| Answer 11 (simplify-cards-Q11) | `next` is advice for the choice of the CR and the wording; safety steps are refusals, not advice; the CLI words the ask to the user (the Foreman may add one sentence) | sentences 2 and 4 below |
| Program child 9, Scope | The three "Becomes:" texts and the `judge` sentence; tests reading these sentences updated if any | "What changes" |
| Program child 9, Must not | No other AGENTS.md rule changed; no tool added; no card edited | "Out of scope" |
| Program child 9, Risk | No long gate (docs only); the wording binds every later child | "Gates", "Place in the chain" |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Evidence" |
| Answer 22, F9 | Project roles are a later CR: `roles.yaml` holds the plugin's roles only | the sentence names `skills/chantier/roles.yaml`, no project key |
| Answer 14 / merge rule (answer 22, Q8) | Nothing merges while the owner sleeps; the child is presented as ready | "Gates" |

## What changes

One file: `AGENTS.md` at the repository root. One bullet: the one that starts "A role's contract
lives in `skills/chantier/references/`" (lines 43 to 49 at `8a960d34`).

### Today (verbatim)

```
- A role's contract lives in `skills/chantier/references/` (the cards), never in an agent file
  or in the CLI: the parent that starts an agent names the card in its prompt. A card says what
  the role judges; the CLI (`rails.py`) says what it refuses; a user's project rules rank above
  both. The CLI knows no role; two named exceptions: the cost code knows the two specification
  agents by their agent type (`spec-writer`, `spec-critic`), to put them on the grill line, and the surface
  server knows the board's Griller (`board-griller`), to start it with its brief and read its
  `[griller→board]` line (below).
```

### After (the text to commit)

```
- A role's contract lives in `skills/chantier/references/` (the cards), never in an agent file
  or in the CLI. The CLI reads the roles as data (each role's card, wrapper, first line and kind)
  and prints a role's brief whole: the parent starts an agent with the short prompt `brief`
  prints, which names the brief file holding the card. A card says what the role judges; the CLI
  refuses with its rails (`rails.py`), advises with `next` and its `next:` lines, and never
  decides a merge or a take-back: `judge` only words the ask to the user, the steering session
  decides, and the user's yes merges. A user's project rules rank above both. The CLI knows roles
  only as data (`skills/chantier/roles.yaml`, read by `brief`, `help --for` and `msg steering`);
  two named exceptions: the cost code knows the two specification
  agents by their agent type (`spec-writer`, `spec-critic`), to put them on the grill line, and the surface
  server knows the board's Griller (`board-griller`), to start it with its brief and read its
  `[griller→board]` line (below).
```

How each of the four sentences maps:

1. "the parent that starts an agent names the card in its prompt" becomes "The CLI reads the
   roles as data (each role's card, wrapper, first line and kind) and prints a role's brief
   whole: the parent starts an agent with the short prompt `brief` prints, which names the brief
   file holding the card." The opening clause ("A role's contract lives in ... (the cards), never
   in an agent file or in the CLI") is kept: the program's "a role's contract lives in the cards"
   says the same, and the CLI reading roles as data does not put a contract in it.
2. "A card says what the role judges; the CLI (`rails.py`) says what it refuses" becomes "A card
   says what the role judges; the CLI refuses with its rails (`rails.py`), advises with `next` and
   its `next:` lines, and never decides a merge or a take-back". "A user's project rules rank
   above both" is kept unchanged, as its own sentence.
3. "The CLI knows no role; two named exceptions: ..." becomes "The CLI knows roles only as data
   (`skills/chantier/roles.yaml`, read by `brief`, `help --for` and `msg steering`); two named
   exceptions: ...". The two exceptions (the cost code's `spec-writer` and `spec-critic`, the
   surface server's `board-griller`) are kept word for word.
4. Answer 11, added inside sentence 2: "`judge` only words the ask to the user, the steering
   session decides, and the user's yes merges."

The Driver may re-wrap the lines (the file wraps near 100 columns, and the exception lines are
already longer); it changes no word of the "After" text but by a reply to a Verifier finding that
cites this specification.

### Kept as is, on purpose

- `AGENTS.md`, the surface server's paragraph inside "The CLI's scope": "it takes its dependencies
  like the rest of the CLI and knows no role but the board's Griller" (line 133 at `8a960d34`).
  It describes the surface server, which reads no role data and knows only the board's Griller;
  it agrees with sentence 3 and is another rule (Must not).
- Every other `AGENTS.md` line, child 8's `host` line included.

### Tests

None reads these sentences. Checked on `origin/main`: `git grep -n -i "knows no role\|role's
contract lives\|says what it refuses\|what the role judges" origin/main` finds them only in
`AGENTS.md`, `CONTRIBUTING.md:100` and `:122`, `references/hosts/claude-code.md:630` and four
docstrings in `src/` (`commands/__init__.py`, `driver_prompt.py`, `plugin_files.py`), and no file
under `skills/chantier/scripts/cli/tests/`. The Driver runs the same grep at its base (child 8's
head) and states the result in the PR; it changes no test and adds none (the program asks for
none).

The tests that read the shipped `AGENTS.md` as it ships, at the head under test, must still pass
unchanged; the edited bullet holds none of their phrases:

- `tests/test_board_running_lane.py` ("action `running-batch`", "writes no file in the CR's
  folder");
- `tests/test_gate_refusals.py` ("`chantier gate <cr> scenario`" and the long gate's line);
- `tests/test_launch_modes.py` ("when the session's project is chantier" and the stale-build
  sentence, once);
- `tests/test_board_read_key.py` (no "the board's key", no "revokes the key");
- `tests/test_command_names.py` (no `chantier board` old form).

## Out of scope

- Any other `AGENTS.md` rule, the surface server's "knows no role but the board's Griller"
  included (program, Must not).
- A tool, a command, a flag, `roles.yaml` itself (child 18), `brief` (child 10), `next`
  (child 12), `msg steering` (child 13), `judge` (child 14): this child names them only.
- Any card under `skills/chantier/references/`, `references/hosts/claude-code.md:630` included,
  and the wrappers in `agents/` and `com.github.copilot/agents/` (program, Must not; the card
  rewrite is children 19 to 24).
- The docstrings in `src/` that say "the CLI knows no role" (`commands/__init__.py:14`,
  `driver_prompt.py:149`, `plugin_files.py:174`, `:276`, `:385`): code comments in files that
  children 10 and 18 rewrite when the role data lands.
- `CONTRIBUTING.md:100` ("The CLI knows no role: the cards hold each role's contract, and the
  Foreman and the Drivers write the prompts"): the program scopes this child to `AGENTS.md`
  ("docs only: AGENTS.md"); see open question 2.
- A test that guards the new wording: the program does not ask for one.
- A version change (`just version` only, and not in this child).

## Gates

- **Before the first push:** `just check` in the worktree, at the rebased head it pushes.
  `just eval-dry-run` is not owed (nothing under `src/` or `evals/kit/`). `just mod` is not owed
  (no `hooks/` or `types/` change).
- **Long gate:** none owed for this child's own change: `AGENTS.md` is a docs-only change (program
  Risk; AGENTS.md: "a change to the docs ... alone needs none").
- **Stack's top:** in this stack batch only the CR on top owes the local Windows
  `chantier gate <cr> scenario` run, "a docs-only top included". If this CR is the stack's top
  when it is presented as ready, it owes that run at its head; when child 10 joins on top, the
  run moves to child 10.
- **Merge:** nothing merges while the owner sleeps; the CR is presented as ready, and the owner
  merges, in order, after child 8 (merge rule, answers 14 and 22 Q8).

## Evidence

- The diff: `AGENTS.md` only, one bullet, matching the "After" text above (re-wrapping aside).
  `git diff --stat <base>...HEAD` in the PR shows one file.
- `just check` passes at the pushed head (lint, test, release-notes).
- The grep of "Tests" above, run at the base, and its result in the PR.
- `just test` seconds (F20): the PR's Deliverables state the seconds this child adds, measured
  before (at the base) and after (at the head) on the same machine. Expected: 0 s, since no test
  is added or changed; the two measured durations are given anyway.
- The PR quotes, as the owner's word, to be confirmed at wake:
  - answer 11: "`next` is advice for the choice of the CR and the wording; the safety steps are
    refusals, not advice; the CLI words the ask to the user and the Foreman may add one
    sentence."
  - answer 22, F7: "one child before the brief child rewrites the four AGENTS.md sentences (roles
    are data the CLI reads; the CLI advises with `next`, refuses with rails, never decides a merge
    or a take-back; `judge` only words the ask)."
- The PR's Known gaps name open question 1 (below) while it is unanswered: until children 10 to
  18 land, and until child 24 switches `take`, `round` and `handoff` to `brief`, the new text
  names commands and a file that do not exist yet at this child's head.
- No host or default matrix: the change does not depend on the host or on a configured value.

## Cost

`just test`: +0 s expected. No scenario step. One short Driver round.

## Open questions

1. **An intermediate `main` that names tools not yet there.** Children 1 to 18 may each merge,
   in order, once the owner says so. After this child merges and before children 10 to 18 do,
   `AGENTS.md` names `brief`, `help --for`, `next`, `msg steering`, `judge` and
   `skills/chantier/roles.yaml`, none of which exists yet, and says the parent starts an agent with
   `brief`'s short prompt, while `take`, `round` and `handoff` keep printing the old prompts until
   child 24. An agent that reads `AGENTS.md` on that `main` may run a command that does not exist.
   The program places this child before the brief child (F7) and words the text in the present
   tense. This specification keeps that wording and the program's merge order, with the gap in
   Known gaps. Should the owner rather hold child 9's merge until children 10 to 18 can merge
   with it, or have the sentences worded so they hold at every step (for instance "as each
   lands")?
2. **`CONTRIBUTING.md:100`.** It says "The CLI knows no role: the cards hold each role's contract,
   and the Foreman and the Drivers write the prompts", which this child's sentences 1 and 3
   contradict once the tools land. Align it here (one more docs file, still no long gate), or
   leave it to the swap (child 24) or the read-and-compare review (child 25)? This specification
   leaves it out, as the program scopes the child to `AGENTS.md`.
