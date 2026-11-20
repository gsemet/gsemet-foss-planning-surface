# Change Specification: one CR Driver per CR in the common case, with a closing step that resumes from the record

## Goal

In batch-28, 62 CR Drivers drove 19 CRs: 43 were restarts on a CR that already had a Driver, and
Drivers cost 26% of the batch ($29.76 of $116.26). The user wants one Driver to take a CR from
its first take to `handback ready` in the common case. To get there, a Driver's context must grow
less: it reads less, by section, and it never reads what it does not need. When a Driver does
stop, the closing step (PR body, Test plan boxes, description pass, ready, hand-back) must resume
in a fresh Driver from the record and the CR's files, with no rereading of the rounds.

## What the measure shows (batch-28, 2026-11-20)

`cost --batch batch-28 --explain` refuses an archived batch (`error: unknown batch batch-28`), so
these figures come from the batch-28 archive (`5-archives/batches/batch-28.json`, each CR's
`STATUS.json` notes) and from the 62 `chantier:cr-driver` subagent transcripts of batch-28 under
`~/.claude/projects/C--Users-gaeta-Projets-chantier/*/subagents/`. Duplicated transcript lines
are counted once. Sizes are in characters of tool results; with this text, one token is about 3
characters.

**Why Drivers restarted.** 39 of the 43 restarts left a `back to a Driver: <note>` note. The other
4 belong to CR-381 and CR-382, dropped to the trash with no `STATUS.json`.

| Reason (the take's note) | Restarts | By design today |
| --- | ---: | --- |
| `resume: closing` | 17 | yes: `driver.md`, "CR driver", hands off at every pushed-head `VERIFIED` (since f3d3f56e, 2026-11-18) |
| `resume: context` | 4 | no: the context rule or a turn the host ended early |
| `rebase:` / `restack:` after a hand-back | 13 | yes: the Driver ended at `handback ready`; out of scope here |
| answers, `push:`, `rounds:` | 5 | yes: a re-take after a `blocked` hand-back; out of scope here |

So most "restarts" were the mandatory closing hand-off, not Drivers that ran out of context. Two
closing Drivers did not finish either: CR-375 (its closing note did not land) and CR-379 (it
posted the body but never ran `ship` or `handback`). A third Driver did the closing each time.

**Where a first-take Driver's context goes** (22 first takes; median peak 108k tokens, max 128k;
median start 24.7k, before any read):

| Source | Median characters per Driver | Note |
| --- | ---: | --- |
| `driver.md` | 65.7k | its largest single read. 7 Drivers read the whole card (≈63k characters at once) because the prompt says `Read <refs>/driver.md;`. The rest read "Your means" (52,772 bytes) and "CR driver" (17,121 bytes) in full, as the card asks |
| shell, git and CLI output | ≈35k | among them `git branch -a` / `git branch --list` (≈40k over the batch), `git status --short` in the main checkout (35k), and cards printed with `cat`, `sed` or `awk` (≈200k over the batch, on top of the `Read` calls) |
| the specification | 15.8k | |
| startup reads | 9.3k | |
| `pr-template.md` | 4.8k | read again by the closing Driver |
| worker replies | under 2k | already short: no change needed |
| the Driver's own output | ≈30k | worker prompts ≈10k, shell commands ≈11k, `pr-body.md` ≈3k |

Images: three Drivers read PNG evidence themselves (CR-380, CR-381, CR-382: 11 screenshots). The
CR-381 closing Driver peaked at 95k tokens, against a 58k median for closing Drivers.

A closing Driver grows by about 33k tokens (median peak 58k from a 25.5k start). About 11k of
that is rereading `driver.md` and its startup files, which the same Driver would already hold.
Closing in the first Driver therefore costs about 20k tokens more. That is why the first Driver
must reach `VERIFIED` well below 130,000 tokens.

**Conclusion.** Card changes can reach the aim, along with one prompt line the CLI prints (a
measured cost: 7 whole-card reads of ≈21k tokens each). The work needs no new role and no new
agent file. Worker hand-backs already stay short; the cuts are in what the Driver itself reads.

## What changes

### 1. The Driver's prompt names its card; it does not tell the Driver to read it whole (CLI)

- `skills/chantier/scripts/cli/src/chantier/driver_prompt.py`, the skeleton's lines (today
  `f"  Read {refs}/{row.card};"`): the line keeps naming the card's path under `references/`
  but says how to read it. Wording to keep in substance:
  `  Card: {refs}/{row.card}: its Startup core now, each other section when its step comes, as the
  card's opening says;`
  The line before it (startup core, host core, role core, startup section) and the rules line
  after it stay unchanged. This applies to all four Driver kinds (CR, stack, QA, release), which
  share the skeleton.
- The worker prompts (`plugin_files.py`, `Read {refs}/{card[1]};`) do not change. A worker's card
  is small (`coder.md` 4.7k bytes, `verifier.md` 14.5k bytes) and is read whole by design.
- Justification under AGENTS.md's CLI scope: a measured token cost (above), and the change is in
  text the CLI already prints. The CLI learns nothing about roles.

### 2. `driver.md`: the common path reads at most 45,000 bytes of the card (cards)

`skills/chantier/references/driver.md` is reorganised. **No rule is dropped:** each rule is moved
or condensed, never deleted.

- **Common path.** A CR Driver's first take through `handback ready`, with no conflict, no refused
  push, no forge server error, no archive in the PR, no matrix and no re-take note. On this path
  the Driver reads the opening (lines 1-63 today), the level-2 sections the manifest lists for
  `cr-driver`, and `## CR driver`. Together they total **at most 45,000 bytes**, against 74,666
  today (4,773 + 52,772 + 17,121).
- **Split "Your means".** `## Your means` becomes several level-2 sections, each read when its
  step comes. Examples: the record and the workers, the worktree and the push, the long gate and
  CI, the PR and its evidence, your end. Rules a trigger alone calls for move to their own level-2
  sections, read only when that trigger arises, never at the opening. Today's candidates (bytes
  today):
  - a remote command that fails with a forge server error (1,444);
  - the archive in the PR (1,879);
  - a force push the host refuses (2,629);
  - the steering session's messages to a Driver (868);
  - the `ci: beside the long gate` specifics;
  - the matrix probe;
  - conflicts and moves.
- **Split "CR driver".** In `## CR driver`, the re-take paragraphs (the CR taken with `rebase:
  <cr> merged`, `rebase: stacked on`, `rebase: mode`, `folded:`, the stack base; about 7,000 bytes
  from "A CR taken with the note `rebase: <cr> merged`" to the section's end) move to a level-2
  section such as `## CR driver: re-takes`. It is read only when the take's note or a received
  note is one of these.
- **Reading rules** in the card's opening, added or sharpened:
  - A card is read with Grep for the heading, then Read with offset and limit (today's rule). It
    is never printed by `cat`, `sed`, `awk` or `Get-Content`, and never read again once it is in
    context. A section a link names is still read in full.
  - A Driver never opens an image file (`.png`, `.jpg`, `.gif`, `.webp`). It attaches the images
    the Verifier or the Demo explorer names, by path and caption, and judges them from their
    reply.
  - A Driver never lists every branch (`git branch -a`, `git branch --list` with no pattern) and
    never runs `git status` outside its worktree. It names its branch or its worktree.
  - On a closing restart, the evidence files `work/verify.md` names are read by name and caption,
    not opened, except a text file a body line needs.
- **Rules that stay as they are:** the specification's "whole, or by part" rule, and the
  130,000-token context rule (`## Your means`, "Context" bullet, moved with its section).
- `skills/chantier/references/startup-manifest.json`: under `actions`, each Driver role
  (`cr-driver`, `stack-driver`, `qa-driver`, `release-driver`) lists the shared sections it reads
  on its common path, then its own role section, in place of `driver.md#Your means`. Trigger
  sections are not listed: the card's links name them. `startup_sections` stays
  `driver.md#Startup core`.
- Other cards and files that link to "Your means" (concepts.md, the host references, foreman.md,
  `evals/kit/`) are updated to the new section names. Search for `Your means` in the repository.

### 3. The closing step: in place by default, resumable from the record (cards)

In `driver.md`, `## CR driver`, the paragraph from "When that `verifier` replies `VERIFIED`" to
"needs no description pass" changes:

- **The closing note becomes a checkpoint.** At the pushed-head `VERIFIED`, the Driver always
  records the closing note as today (`closing: VERIFIED at <sha7>; PR <link>; base <branch>;
  pr-body.md posted at <sha7 or not yet>; evidence: …; UNVERIFIED: …; next: …`).
- **No more systematic hand-off.** If the last `context:` line the Driver read is below 100,000
  tokens, the same Driver carries out the closing itself, in the order the card gives today:
  1. the evidence in Deliverables and the Test plan boxes;
  2. the pre-post audit and the post;
  3. the short `verifier` pass on the posted description;
  4. the PR turned ready when its base is the default branch;
  5. `ship <cr> <link>`;
  6. `handback ready <link>` with the body's gaps.

  At 100,000 or more, or with `context: not measured`, it hands off as today: `handback <cr>
  blocked context: closing: VERIFIED at <sha7>; next: <what is left>`. The sentence "it always
  happens, whatever the context size" is removed.
- **One note per closing step**, written as each step finishes. A fresh Driver resumes at the
  first step with no note:
  - `closing: body posted at <sha7>` (evidence and boxes included);
  - `closing: description pass VERIFIED at <sha7>`;
  - `closing: PR ready` or `closing: PR kept draft on <base>`.

  `ship` and `handback` are already in the log as their own events.
- **During the closing, the context rule still applies.** At 130,000 tokens or more, or when the
  host asks for the hand-back, the Driver hands back `blocked context: closing: <last closing
  step done>; next: <what is left>`. This replaces "A Driver whose `log` holds a `closing:` note
  never hands off for the closing again."
- **The `resume: closing` reading rule** in the card's opening is kept and narrowed:
  - read `handoff <cr>`, `log <cr>`, `pr-body.md` and `work/verify.md`;
  - read the evidence files by name and caption (above);
  - read `pr-template.md` only before the first body edit, and only the sections that edit needs;
  - start at the first closing step with no `closing:` note.

  The Driver still reads no specification, `investigation.md`, `r<n>.md` notes or diff, and no
  `driver.md` section beyond the Startup core, the closing paragraph and the section of a step it
  carries out.
- `## Startup core` keeps its line on `Note: resume: closing`. If the wording changes, it stays
  within the startup limit of `startup-manifest.json` (`limit: 12544`).
- `skills/chantier/references/foreman.md`, the "A hand-back `blocked context: …`" bullet (around
  lines 727-741 today):
  - The closing hand-off now comes only above 100,000 tokens at `VERIFIED`, or at the context
    rule during the closing.
  - The restart path is unchanged (`agents set <cr> - --epoch <n>`, `take <cr> --note "resume:
    closing" --epoch <n>`, no round, no ask, before any queued CR).
  - New: a second `context: closing:` hand-back on the same CR, with no new `closing:` step note
    since the first, is an ask (`question <cr> driver out of context twice`), as for `context:`.
  - Reports and retros still call it "the closing step".
- The CLI's hand-back line in `commands/driver_checks.py` (`handback_blocked`, "the Foreman
  restarts a fresh Driver for the closing step") stays as it is.

### 4. Agent files

No change to `agents/cr-driver.md` or `com.github.copilot/agents/cr-driver.md`. Their bodies
already defer to the card's Startup core.

## Decisions carried from `02-answers.md`

- Grilled enough. The CR joins batch-29 (factory, stack) once specified.
- Aim of one Driver per CR in the common case: the reading cuts (1, 2) and the in-place closing
  (3).
- Measure first: the section "What the measure shows". Worker hand-backs stay short: they are
  measured short (under 2k characters per Driver) and keep their cards' reply formats; nothing to
  cut there. The Driver reads files by section: section 2.
- The closing step is restartable by design: section 3. Cards first; the only CLI change is the
  prompt line, a measured token cost.
- No new role and no new agent file: the measure shows card changes suffice.
- Evidence: below, with the reading of a later batch's `cost --explain` and the test and scenario
  impact.

## Out of scope

- Re-takes after a hand-back (`rebase:`, `restack:`, answers, `rounds:` grants): 18 of
  batch-28's 43 restarts. They are by design, since a Driver ends at `handback ready`. Shortening
  what a re-take reads is a separate CR.
- The 25k-token start of every agent (system prompt, tools, the project's `AGENTS.md`).
- The startup core and the startup manifest's limit.
- `cost` reading an archived batch (`unknown batch batch-28`).
- Worker cards and worker reply formats.
- The stack, QA and release Drivers' own sections, beyond the shared sections they now list in the
  manifest.

## Evidence

- **Shipped card budget** (new test in
  `skills/chantier/scripts/cli/tests/test_startup_manifest.py`). It reads `driver.md` and
  `startup-manifest.json` from the repository at the head under test. It sums the bytes of the
  card's opening (up to the first level-2 heading) and of each `driver.md#<heading>` section the
  manifest lists under `actions["cr-driver"]`, and asserts the total is at most 45,000 bytes. It
  asserts every listed heading exists with a non-empty body (the existing `_section_bytes` check).
- **Manifest test updated:** the assertion `manifest["actions"][role] == [f"{card}#Your means",
  f"{card}#{heading}"]` becomes: each Driver role's action list ends with `driver.md#<its role
  section>` and names no other Driver's role section.
- **No rule lost:** the Inspector's checklist line for `driver.md`. Each rule of the card at the
  base (each bullet and paragraph of "Your means" and "CR driver") is found, moved or condensed,
  at the head; the round's `r<n>.md` lists the moves. Trigger sections are each reached by a link
  or a named trigger from the common path.
- **Prompt line** (`skills/chantier/scripts/cli/tests/test_driver_prompt.py`, the assertions
  today at `block[3].endswith("/driver.md;")`): the line starts `  Card: `, names
  `/references/driver.md`, and no line of the skeleton starts `  Read ` with a path ending in
  `driver.md;`. `just eval-dry-run` passes: the eval audit's J1 (`evals/kit/audit.py`, "is told to
  read {card}") still finds `references/driver.md` in the prompt. Update `evals/kit/dry_run.py`'s
  `QA_BODY` to the new line.
- **Scenario** (`scenario/run_scenario.py`, `driver_liveness`):
  - the existing strings stay true (`` `resume: closing` `` and `` `context: closing:`` in
    `driver.md`, `resume: closing` in `foreman.md`);
  - the check that reads the shipped cards also asserts that `driver.md` names the 100,000-token
    closing threshold and the three `closing:` step notes, and that `foreman.md` names the second
    `context: closing:` ask;
  - the CLI path (`handback … blocked "context: closing: …"`, then `take … --note "resume:
    closing"`) is unchanged and stays green.
- **Gates:** `just check` and `just eval-dry-run` (a change under the CLI's `src/` and the eval
  kit), and the pipeline's `just scenario (ubuntu-latest)` job (a change to the CLI and the
  cards).
- **In a later batch (the measure of the aim), read once the batch closes:**
  - `cost --explain` for the batch: the `chantier:cr-driver` line's "N restarted on a CR that
    already had one", divided by the CRs that reached `handback ready`. In batch-28 it was 43 for
    18 CRs (2.4 per CR).
  - The retro sorts those restarts by the take notes (`back to a Driver: <note>` in each CR's
    notes). The aim holds when `resume: closing` plus `resume: context` restarts are at most one
    for every four CRs (batch-28: 21 for 18 CRs). The rest should be re-takes after a hand-back
    (rebase, restack, answers), which this CR does not change.
  - From the Driver transcripts, as measured here: first-take Drivers' median context at the
    pushed-head `VERIFIED` is below 100,000 tokens, and median `driver.md` characters read per
    first take is at most 45,000 (batch-28: 65.7k).

## Settled questions

1. The closing threshold is **100,000** tokens, as proposed (Chief of Staff, 2026-11-20).
2. `cost --explain` does not print the restart split in this CR: out of scope (no measured agent
   token cost); the retro sorts restarts from the notes (Chief of Staff, 2026-11-20).
