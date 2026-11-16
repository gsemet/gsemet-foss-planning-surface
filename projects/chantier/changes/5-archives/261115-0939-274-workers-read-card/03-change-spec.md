# Change Specification: every worker reads its card before it works

## Goal

Every worker a Driver starts (Investigator, Coder, Inspector, Debugger, Verifier, Conflict
resolver) reads its section of `worker.md` before it works, and replies in the format that section
names. The measure below shows two causes, so this CR fixes both (02-answers: "if both causes
show, both fixes"):

- the Driver sometimes leaves the card out of the prompt. Fix: the CLI prints the opening lines of
  each worker's prompt, card included, and the Driver copies them unchanged;
- the worker much more often skips the card its prompt names. Fix: each worker's agent file names
  its own card and section, to read first, on both hosts with identical bodies.

The result is the same on Claude Code and Copilot. A path not proved on Copilot carries
"unproved".

## Evidence: the measure (step 1)

Source: batch-18's one Foreman session (`446cff2e-8291-4f73-9ff0-f19c29743e6e`, under
`C:/Users/gaeta/.claude/projects/C--Users-gaeta-Projets-chantier/`), its `subagents/` folder.
Each `agent-*.meta.json` gives the agent type and the parent agent. All 36 `chantier:cr-driver`
agents are the Foreman's children, and every worker is a Driver's child. The restart notes come
from `.agents/changes/4-batch/events.jsonl`.

Method, per worker transcript:

- **Prompt names the card:** the first user message contains `worker.md`.
- **Template form:** the prompt names it in the template's form ``section "<Role>"``.
- **Worker read the card:** the worker made at least one tool call (Read, Grep, Bash or
  PowerShell) whose input names `worker.md`. The final `SubagentHandback` does not count.
- **Window:** 149 finished workers, 2026-11-14T18:44Z to 2026-11-15T05:06Z. Six Coders started
  at 08:19Z were still running at the time of the measure, so they are left out.
- **After CR-256:** this column counts workers started after CR-256 merged
  (2026-11-14T23:34:59Z).

| Role | Workers | Prompt names `worker.md` | ... in the template's form | Prompt names no card | Named, never read | Read (main checkout / worktree copy) | After CR-256: workers / read |
|---|---|---|---|---|---|---|---|
| Verifier | 53 | 46 | 42 | 7 | 36 | 12 (8 / 3, 1 other) | 45 / 10 (7 / 3) |
| Inspector | 48 | 45 | 40 | 3 | 16 | 29 (28 / 0, 1 other) | 29 / 18 |
| Coder | 33 | 33 | 29 | 0 | 24 | 9 (6 / 3) | 17 / 5 |
| Conflict resolver | 11 | 8 | 6 | 3 | 7 | 1 (1 / 0) | 11 / 1 |
| Debugger | 2 | 2 | 1 | 0 | 2 | 0 | 1 / 0 |
| Investigator | 2 | 2 | 2 | 0 | 2 | 0 | 2 / 0 |
| **Total** | **149** | **136** | **120** | **13** | **87** | **51** | **105 / 34** |

The last column agrees with the request's count (44 Verifiers after CR-256, 7 read the card in
the main checkout and 3 the worktree's copy). The one-Verifier difference comes from the boundary
second. Two Verifiers whose prompts named no card read it anyway.

What the counts say:

- **The Driver leaves the card out (cause 1, minor).**
  - 13 of 149 prompts (9%) name no card.
  - All 13 started between 01:45Z and 03:34Z. All are follow-up starts after a rebase or a move:
    "Verify at new head", "Inspect conflict resolution", "Resolve rebase conflicts",
    "Description pass 3". The Driver wrote these prompts from scratch, late in its context.
  - Another 16 prompts name the card in a free form ("(verifier part)", "(inspector section)",
    "(coder)"); one names `worker.md` with no section.
  - 42 of 149 prompts do not carry the template's `Read ... worker.md, section "<Role>", and
    ... concepts.md;` line as their second line, and 27 carry no rules line.
- **The worker skips the card (cause 2, major).**
  - 87 of the 136 workers whose prompt named the card (64%) never opened it.
  - By role: Verifier 36 of 46, Coder 24 of 33, Conflict resolver 7 of 8, Debugger 2 of 2,
    Investigator 2 of 2, Inspector 16 of 45.
  - Only 39 of 149 workers ran the `rules` command their prompt names.
- **Skipping the card shows in the replies.** In-format replies, by whether the card was read:

  | Role and check | Card read | Card named, not read | No card named |
  |---|---|---|---|
  | Inspector: the reply is JSON with `verdict` exactly `APPROVE` or `FIX-REQUIRED` and a SHA `head` | 25 of 29 | 10 of 16 | 0 of 3 |
  | Verifier: the first line is exactly `VERIFIED` or `NOT VERIFIED` | 9 of 12 | 26 of 36 | 0 of 5 |

  The out-of-format replies include `"verdict":"pass"`, `"approve"`, `"APPROVED"`,
  `"changes_requested"`, `Verdict: PASS` and `VERIFIED (code and ...)`. The Drivers recorded
  14 `restart: reply out of format` notes: Inspector 7, Verifier 5, Coder 1, Conflict resolver 1
  (`Placeholder`).

Both causes show, so both fixes apply. The CLI's lines make the card's presence and form exact.
The agent file's pointer turns a named card into a card that gets read.

## What changes

### 1. The worker agent files (both hosts, identical bodies)

The files are `agents/{coder,conflict-resolver,debugger,inspector,investigator,verifier}.md` and
`com.github.copilot/agents/chantier-{coder,conflict-resolver,debugger,inspector,investigator,verifier}.agent.md`.
The frontmatter does not change. In each body, keep the first paragraph ("You are the chantier
<Role>. Your prompt is your whole brief: ...") and add this paragraph after it. The Verifier is
shown; the other roles use their own section name, which is exactly the heading in `worker.md`:
`Investigator`, `Coder`, `Inspector`, `Debugger`, `Verifier`, `Conflict resolver`.

```text
Your card is `worker.md`, section "Verifier": read that section first, before any other step,
at the path your prompt's `Read` line gives, and reply in the format it names. The card is
your contract; this file only points to it.
```

The refusal paragraph also names the card. A prompt without the card's path is refused like a
wrong first line, so the worker never runs without its card:

```text
A prompt that does not start with `chantier verifier`, or that names no path to my card
`worker.md`, is not a chantier prompt: answer
"I run inside a chantier batch only. My prompt must start with `chantier verifier for <cr> "<title>" of batch <batch>, in the project <root>.`, and its `Read` line must name my card, `worker.md`, section "Verifier";
a message to me gets this same answer: start a new agent with that line." and stop. Any later message gets the same answer.
```

The contract stays in `worker.md`. The agent file only points to it, and adds no rule of the role.
The `# chantier-agent: 0.9.0` version line keeps its place, and the version is not edited by hand.
The Driver, Chief of Staff and Stack driver agent files do not change (see Out of scope).

### 2. The CLI: the opening lines of each worker's prompt

`take`, `round` and `handoff` all print `cr_facts`
(`skills/chantier/scripts/cli/src/chantier/commands/facts.py`). `cr_facts` gains one block per
worker role, after the `team:` and `ci:` lines, so the existing lines keep their order. For the
Verifier of CR-273:

```text
verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
  chantier verifier for CR-273 "<title>" of batch batch-18, in the project C:/Users/gaeta/Projets/chantier.
  Read C:/Users/gaeta/Projets/chantier/skills/chantier/references/worker.md, section "Verifier", and C:/Users/gaeta/Projets/chantier/skills/chantier/references/concepts.md;
  the project's rules rank above them: run `$CHANTIER rules` first and read what touches your work.
```

- **The CLI knows no role.** A new function in
  `skills/chantier/scripts/cli/src/chantier/plugin_files.py`, `worker_prompt_lines(host, root,
  skill, cr, title, batch)` next to `chief_prompt_lines`, reads the roles and sections from the
  host's agent files (`_agent_files(host)`). A role gets a block when its agent file meets all
  three conditions:
  - its description says `Started by a Driver.`;
  - its `Prompt starts with:` line holds `<cr> "<title>" of batch <batch>`;
  - its body holds the line ``Your card is `<card>`, section "<Section>"`` (from area 1).
- **Filled-in values:**
  - `<cr>`, `<title>`, `<batch>` and `<root>` come from the CR, the batch and
    `repo.root.as_posix()`, as `chief_prompt_lines` fills `<root>`;
  - `<skill>` is `skill_dir().as_posix()`, as the `cards:` line has it;
  - the host is the batch's host (`d.host`).
- **Order:** the agent files' order, which is coder, conflict-resolver, debugger, inspector,
  investigator, verifier.
- **Lines kept and dropped:** the `cards:` line stays, because the Foreman writes the Driver's own
  card line from it. Roles that are not workers (cr-driver, stack-driver, qa-driver,
  release-driver, the Chief of Staff's subagents) get no block.
- **The CLI's refusals do not change.**

The lines are the template's lines from `concepts.md`, "Starting an agent" (the worker's `Read`
line and the rules line), now printed instead of typed. The Foreman passes the `take` facts into
the Driver's prompt, so a Driver holds these blocks from its start ("keep the ones `take` printed
in your prompt").

### 3. The cards

- `skills/chantier/references/driver.md`, the bullet "Every worker's prompt, whatever the role"
  (around line 140): replace "the first line, `chantier <role> for <cr> …`, and the card to read;"
  and the rules-line item with one item: "the role's opening lines, as `take`, `round` or
  `handoff` printed them under `<role> prompt, opening lines:`, copied unchanged at the top of
  the prompt (the first line, the card's `Read` line, the rules line), never retyped, shortened or
  rephrased, a follow-up start (a new head, a rebase, a description pass) included".
- `driver.md`, the restart rule (around line 65, "A worker refused for its first line, or ended
  by a host failure, gets one new start of the same role with the same brief"): add that a worker
  refused because its prompt names no card gets that one new start with the role's opening lines
  copied as printed; the rest of the brief stays the same.
- `skills/chantier/references/concepts.md`, "Starting an agent", the template's worker `Read`
  line (around line 393): add that `take`, `round` and `handoff` print a worker's first three
  lines under `<role> prompt, opening lines:`, to copy unchanged.
- `worker.md` does not change. Its top already says "Read only your section below".

### 4. Tests (`skills/chantier/scripts/cli/tests/`)

These are few and parametrized, as AGENTS.md asks:

- `test_plugin_files.py`, parametrized over the worker roles (the `ROLES` whose description says
  `Started by a Driver.` and whose first line holds `<cr>`). On both hosts:
  - the body holds ``Your card is `worker.md`, section "<S>"``;
  - `## <S>` is a heading of `skills/chantier/references/worker.md`;
  - the refusal names the card (`its `Read` line must name my card, `worker.md`, section "<S>"`).

  The existing test that the two hosts' bodies are identical still holds.
- `test_cli_runs.py`, in `test_the_plugin_runs_with_no_setup_and_writes_only_in_the_planning_folder`
  (already parametrized over both hosts), the output of `take`:
  - it has one `<role> prompt, opening lines` header for each of the six worker roles, and none
    for `cr-driver`;
  - under the Verifier's header, the next three lines (without their two leading spaces) are
    exactly the first line `chantier verifier for CR-101 "<title>" of batch <batch>, in the
    project <root>.`, the `Read <skill>/references/worker.md, section "Verifier", and
    <skill>/references/concepts.md;` line, and the rules line.
- `just test` stays within the budget AGENTS.md sets.

### 5. Scenario (`scenario/run_scenario.py`)

Extend the check "`take` prints the facts for the prompt" (around line 807): `fm.facts` holds a
`verifier prompt, opening lines` header, followed by the first line naming `CR-101` and a `Read`
line naming `worker.md, section "Verifier"`. The scenario's fake Driver copies those lines into
each worker prompt it builds, where it builds one.

## Decisions of 02-answers carried

- The source is batch-18's retro follow-up. The CR joins batch-18 on top of the stack, after
  CR-273 (this has no effect on the code; it sets the base).
- The measure decides the fix. Both causes show (table above), so both fixes apply: area 1 for
  the worker, area 2 and area 3 for the Driver.
- It is the same on Claude Code and Copilot: both agent folders change together with identical
  bodies (area 1), and the CLI reads either host's files (area 2). The Copilot paths are listed
  under Known gaps as "unproved".
- Open points with no default take this spec's recommended reading, decided by the Chief of Staff.
  They are listed at the end.

## Out of scope

- The Driver, Stack, QA and Release driver agent files, and the Chief of Staff's subagents. Their
  prompts already carry their card (the playbook's first line and the card line). This CR covers
  the six worker roles.
- The Demo explorer (a `worker.md` section, but the Chief of Staff starts it, with no CR) and the
  extra review step.
- A hook that refuses a worker start with no card line (`hooks/`). It would cover only Claude Code.
  The worker's own refusal (area 1) is host-neutral.
- Making workers run `rules` (39 of 149 did). The rules line is now printed for the Driver to copy
  (area 2), and `worker.md` already asks for `rules` first. Nothing more here.
- The CLI's check of a reply's format. CR-273 (`verdict VERIFIED` refuses a note without the head)
  stays as it is.

## Evidence that proves it

- `just check` passes on Linux, macOS and Windows (CI).
- `just test`, with the new parametrized tests of area 4:
  - each worker agent file, on both hosts, names its card and an existing `worker.md` section;
  - `take` prints the six blocks, and the Verifier's lines exactly as specified.
- `just scenario` passes with the extended check of area 5 (a CLI and cards change). The CR does
  not touch `hooks/` or `types/`, so `just mod` is not required.
- In `evidence/`: the output of `chantier handoff <cr> --batch <batch>` on a real CR, showing the
  six blocks (from the batch's own CR is fine).
- After the merge, at the next batch's retro (not a gate of this CR): rerun this spec's measure on
  that batch's worker transcripts. Expected: no prompt without its card's `Read` line, and most
  workers read their card. The Chief of Staff records the counts in the retro.

## Known gaps

- Copilot, unproved: that a Copilot worker reads the card its agent file points to and refuses a
  prompt with no card path; that a Copilot Driver copies the printed lines. The CLI and test part
  is host-neutral and tested on both hosts' files.
- Whether the pointer in the agent file raises the reading rate on Claude Code is proved only by
  the next batch's measure, not by this CR's gates.

## Open points, with the recommended reading (decided by the Chief of Staff, 02-answers)

1. Does a worker refuse a prompt that names no path to its card? Recommended: yes (area 1, with
   the Driver's one restart in area 3). In batch-18, none of the 8 Inspectors and Verifiers
   started without a card replied in format. A refusal at the first turn costs less than a full
   run that is then restarted.
2. Which commands print the blocks? Recommended: `take`, `round` and `handoff` alike, through
   `cr_facts`. This is one place, and the Driver keeps them from its prompt. The cost is about 24
   lines (roughly 600 tokens) per call, against 14 worker restarts in batch-18. The alternative
   is `take` and `handoff` only.
3. Does the Demo explorer get the same pointer? Recommended: no, for now (Out of scope). The
   Chief of Staff starts it outside any CR, and this measure did not count it.
