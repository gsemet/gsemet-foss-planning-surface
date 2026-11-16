# Change Specification: CI runs beside the long gate, when the project asks for it

## Goal

In the user's words (2026-11-14): "ça peut rentrer dans chantier lui-même pour que les
utilisateurs n'aient pas ces problèmes". A CR's CI runs while its local long gate runs. A failure
on a system the local gate does not cover then shows up early, in any project, not after the gate.

Today a Driver runs the local long gate first, then pushes, then reads CI. A CI matrix that
covers other systems (Linux and macOS when the user works on Windows) reports its failure only
after the gate, and that costs a round and an hour. In batch-17 (this repository), CR-221 had a
mypy error that did not show on Windows (a Windows-only constant). CR-222 had a socket that was
never `listen()`ed (Windows retries, Linux refuses at once). Each red CI came after a 35-minute
local gate and cost one or two more rounds.

chantier cannot know each project's checks, but it knows the order of a Driver's steps. This CR
changes that order, for a project that turns it on.

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. Grilled and specified first, then added at the end of batch-17's stack (one native stack, budget raised to $210). | "Place in batch-17" |
| 2. Off by default. The project turns it on with a `chantier.yaml` key. Without the key the Driver keeps today's order: the gate, then the push. | A (the key), B (the Driver's rules, "with the key only") |
| 3. chantier's own repository turns it on and adds mypy `--platform linux` and `--platform darwin` to `just check`. This is a separate project item, filed once this CR lands. | "Out of scope"; "After it lands" |
| 4. Grilled enough, after the full restatement: the key off by default, the early draft push, a red CI stopping the gate, the systems only CI covers in Known gaps, the Driver's rules rewritten for this mode, chantier's own repository as a separate project item. | A to E |

The critic's review in `intake/request.md` is carried too. The generic change contradicts three
rules of `driver.md`, which this CR rewrites for the mode. Today's numbering, in the main checkout:
line 112 (the long gate "before any PR"), line 168 (`ship` says "no long gate passed at it"),
line 293 (the push refusal "no long gate passed"). The mode spends CI minutes, so the project
chooses it, and it is off by default.

## What changes

### A. The `chantier.yaml` key, read and recorded by the CLI

Only the CLI reads `chantier.yaml` (`chief-of-staff.md`, line 87). The Driver and the Chief of
Staff learn the mode from the CLI's printed lines, never from the file.

- **The key** (default name, see open question 1):

  ```yaml
  ci:
    beside_gate: true
  ```

  `ci` is a new top-level key beside `roles`, `prices` and `board`. `beside_gate` is a boolean,
  `true` or `false`. If it is absent, or the file is absent, the value is `false`.
- **Validation** is in `skills/chantier/scripts/cli/src/chantier/playbook/config.py`, in `load`.
  It takes a new branch `elif key == "ci"` and a `_ci(node, kline, bad)` helper, written the way
  `_board` is written. Each refusal is `chantier.yaml:<line>: …`, exit 2, from `playbook`, `open`
  and preflight P12, as for the other keys:
  - `ci` that is not a mapping, or is empty: `"ci" holds its keys: \`beside_gate:\``.
  - An unknown key under `ci`: `ci: unknown key "<k>": one of beside_gate`.
  - `beside_gate` that is not `true` or `false`: `ci: "beside_gate" is true or false, found
    "<value>"`.
  - The top-level unknown-key message becomes `the top-level keys are "roles", "prices",
    "board" and "ci"`.
  - The resolved playbook that `load` returns carries `"ci": {"beside_gate": <bool>}`, and only
    when the key is set.
- **Recording:** `open` already records the resolved playbook without `prices`
  (`commands/opening.py`, `open_batch`, around line 283). The `ci` entry is recorded with it, in
  `batch.json`'s `playbook`. A running batch keeps the value it opened with, as it keeps its team.
  A file edited mid-batch counts from the next batch.
- **The printed line**, only when the recorded value is `true`:
  `ci: beside the long gate (chantier.yaml): push at the approved round, run the long gate while
  CI runs`.
  - `handoff` and `take` print it after the `team:` lines (`commands/facts.py`, `cr_facts`).
  - `playbook` and `playbook --batch` print it after the `prices:` lines and before `needs:`
    (`playbook/lines.py`, `playbook_lines`).
  - `brief.md` gets one line under "Team" (`opening.py`, `_brief_text`):
    `- CI beside the long gate: on (chantier.yaml).`
  - When the value is false or absent, nothing is printed. Every command's output stays as it is
    today.
- **Help and docs:**
  - `docs/agents-and-models.md`, line 28: "The file's other keys are `prices`, `board` … and
    `ci` (`beside_gate: true`: a CR's CI runs while its local long gate runs; it spends CI
    minutes on every approved round, off by default)".
  - `concepts.md`, "Starting an agent" (line 246), where `chantier.yaml`'s other contents are
    named: add `ci:` in the same sentence.
  - The CLI's code targets hold (CR-221, `brief.md`): file and function sizes, ruff, `mypy
    --strict`.

### B. The Driver's order with the key on (`skills/chantier/references/driver.md`)

Each rule below applies **only when `take` or `handoff` printed the `ci: beside the long gate`
line**. Without that line, every rule of `driver.md` stays word for word as it is. The CR
Driver's sequence with the key on:

1. A round is approved (Inspector and every review step of `Team:`).
2. Commit, as today.
3. Rebase, as today. The head pushed is still the head the gate runs on.
4. Push (plain push, or `--force-with-lease` after a rebase, as the Push bullet says).
5. Open the PR as a draft, or update it. The audit pass on `pr-body.md` comes first, as today.
6. `ship`.
7. Start the long gate and the CI watch, each in its own background shell, by the host's means:
   - `$CHANTIER gate <cr> "<command>"…`;
   - `gh pr checks <pr> --watch --fail-fast`;
   - on GitLab, `glab ci status --live`, which is unproved here (trial: a red job of a GitLab
     pipeline ends the watch or shows in its output before the pipeline's end).
8. Do everything that needs neither result: `pr-body.md`, the description as far as it goes, the
   archive's `delivery.md`, the notes.
9. End the turn. Whichever background shell ends first wakes the Driver.

The edits, section by section (today's line numbers):

- **"Your means", Context (lines 71 to 74).** "The one turn end that waits is the long CI wait"
  becomes "the long CI wait, and with the `ci: beside the long gate` line, the long gate and the
  CI watch running side by side in two background shells: the first to end wakes you".
- **The long gate bullet (line 112, "before any PR").** This becomes "before the first push and
  the PR; with the `ci: beside the long gate` line, at the head you pushed, started right after
  `ship`, while CI runs". The rest of the bullet stands: one command per argument, refused on a
  dirty tree, a moved head is no pass, and the stop rules. Its stop rule, "only when the run's
  result can no longer count", gains one case: a red CI job that is the CR's (the CI bullet
  below) means a round, so the head is about to move.
- **The Push bullet, around line 168** ("`ship` … says what is off (… no long gate passed at
  it)"). Add one sentence. With the `ci:` line, `ship` runs before the gate passes, so its
  `off: no long gate passed at <sha>` is expected there and is not a slip. `handback ready` still
  refuses a head with no passed long gate. The CLI's `ship` is unchanged (see open question 4).
- **The CI bullet (lines 207 to 221).** With the `ci:` line, the CI wait starts at the same time
  as the gate, not after it. The outcomes:
  - **A red job that is the CR's.** That is neither an infrastructure failure nor a job also red
    on the default branch, judged as the bullet says today. Do these at once, without waiting for
    the gate or the other jobs:
    1. `$CHANTIER gate <cr> --stop` (recorded `stopped`: no pass, not a failure, not a round);
    2. a `note` naming the job and the head;
    3. `gh run view <run> --log-failed > <work folder>/ci-<run>.log`;
    4. a `debugger` on it;
    5. the next round.
  - **An infrastructure failure, or a job also red on the default branch.** It keeps its rule
    (one re-run, or a note). The gate is not stopped, because its result still counts.
  - **The gate fails first.** It is a round, as today. Stop the CI watch's background shell (one
    you started, by its id, by the host's means). CI at that head no longer counts.
  - **The gate passes first.** Go on waiting for CI, as today's long wait.
  - **CI is green first.** Go on waiting for the gate: its background shell's end wakes you.
  - **Both are done.** The gate passed, and CI is green or judged by the rules: the `verifier` at
    the pushed head, as today.

  The 3-hour CI limit, the "No CI" two looks, the one bounded wait, the head check and the CI
  note's form all stay as they are.
- **"CR driver", the round sequence (lines 335 to 339).** Today: "rebase, the long gate (a
  failure is a round), push, the PR, `ship`, CI, then a `verifier` …". Add the form for the mode:
  "with the `ci: beside the long gate` line: rebase, push, the PR, `ship`, then the long gate and
  CI side by side (a failure of either that is the CR's is a round; a red CI job stops the gate
  first), then a `verifier` once the gate passed and CI is judged green".
- **The `rebase: <cr> merged` path (lines 383 to 389).** It already pushes before the gate. With
  the `ci:` line, it runs the gate and the CI watch side by side by the same rules.
- **The force-push exception (line 293)**, `push refused <branch>: no long gate passed at <sha>`:
  run the long gate and send the push line again. It stays for a batch without the `ci:` line.
  With the line, the Chief of Staff does not send this refusal (C), so a Driver that gets it
  anyway passes it to the steering session as printed, as any refused line.
- **Known gaps (the paragraph at line 348).** With the `ci:` line, the CR Driver reads the
  systems CI covers from the forge's list of checks at the pushed head (the CI bullet's only
  source; job names such as `just check (ubuntu-latest)` name their system). It compares them
  with the system the long gate ran on. In `pr-body.md`'s Known gaps it writes one bullet naming
  the systems only CI covers, and which commands of the long gate ran only there. For example:
  "The long gate ran on Windows only; Linux and macOS are covered by CI alone." The ready line
  quotes it, as for every gap ("Your end"). A forge that lists no check gives no such bullet.
  The "No CI" rule says what to write then.

The stack driver, the release driver and the QA driver do not change: the mode is the CR
Driver's (see open question 5).

### C. The Chief of Staff's force-push judgement (`skills/chantier/references/chief-of-staff.md`)

"A refused force push", step 2 (lines 587 to 592): "No gate pass at the local head is the Driver's
slip … `push refused <branch>: no long gate passed at <local sha>`". It gains one sentence. When
the `handoff` it ran in step 1 prints the `ci: beside the long gate` line, a push with no gate
pass at the local head is the mode's order and not a slip, so the gate check of step 2 is
skipped. `handback ready` still enforces the gate at the PR's head. Every other check of steps 1
to 6 stays.

The routing table at the top of the card (around line 33) gets one row:

| The user says | You do | Card |
| --- | --- | --- |
| "run CI beside the gate", "CI earlier", "push before the gate" | `ci: beside_gate: true` in `chantier.yaml`, edited only on the user's word, then `$CHANTIER playbook` to show it; it counts from the next batch, and it spends CI minutes on every approved round | The project |

### D. Both hosts

The cards are shared by both hosts. No agent file changes (`agents/`,
`com.github.copilot/agents/`). The background shells use each host's own means, already named for
the CI watch: Claude Code `Bash` with `run_in_background: true`, and Copilot's background shell.

### E. The scenario (`scenario/run_scenario.py`)

Section 17b ("The playbook: an optional chantier.yaml", around line 2441) gets these steps:

- **S2b.**
  - `ci:\n  beside_gate: true` beside a `roles:` entry: `playbook` prints the `ci: beside the
    long gate` line.
  - `open` records `{"beside_gate": true}` under `playbook.ci`.
  - `take` and `handoff` print the line.
  - `brief.md` holds `CI beside the long gate: on`.
- **S2c.** With `beside_gate: false`, and with no `ci` key, no `ci:` line is printed by `take`,
  `handoff` or `playbook`. This pins "off by default, output unchanged".
- **S3.** After `chantier.yaml` drops the key mid-batch, `take` of another CR still prints the
  line (the batch keeps what it opened with).
- **S4, refusals added to the table** (each exit 2 at its line, nothing moved):
  - `ci: true` (not a mapping);
  - `ci:\n  colour: red` (unknown key);
  - `ci:\n  beside_gate: maybe` (not a boolean);
  - a top-level unknown key's message names `"ci"`.

## Place in batch-17

The CR joins batch-17's stack on top of the CRs now in it: CR-222, 223 and 225 to 228 (pending),
and CR-232 to 235, 237 and 238 (active). CR-221, 224, 229 to 231 and 236 are done, and this spec
names their code as it stands in the main checkout. It needs no `depends.json`. No CR before it
is a real need of its, and a shared file is no reason (the user's rule). What it changes on top
of them:

- **CR-235 (gate-liveness), the gate's own CR.** CR-235 changes how the gate lock and its pids
  are judged (`commands/gate_lock.py`, `commands/gate.py`, `procs.py`), the `activity` lines
  (`gate running`, `gate queued behind <cr>`), and `foreman.md` lines 97 and 279. This CR changes
  no gate code. It only changes **when** a Driver calls `gate` and `gate --stop`, and it relies
  on what CR-235 keeps: `gate <cr> --stop` records `stopped` (no pass, not a failure), and a
  stopped run voids an earlier pass at that head. With CR-235, a Driver waiting on its two
  background shells shows `gate running` (or `gate queued behind <cr>`) while its gate runs or
  waits, so the Foreman's lost-Driver check skips it. Its CI-only wait, once the gate has passed,
  shows its age, as the CI wait does today. `order merged` stopping a merged CR's gate (CR-235's
  A) also covers a gate started beside CI. No change to `foreman.md`.
- **CR-233 (merge-any-time).** CR-233 edits `driver.md`'s "Your end" (the merged-early
  refusal), the "Stack driver" opening, and `chief-of-staff.md`'s ready-ask and stack-batch
  bullets. This CR edits other bullets of the same two cards: the long gate, Push, CI, the round
  sequence, Known gaps, and force-push step 2. The text is adjacent but the paragraphs differ.
  With the mode, a PR is pushed (as a draft) earlier. It is still mergeable only after its
  `ready` line, which is CR-233's rule, so the two hold together.
- **CR-222 (visualization-backend).** CR-222 keeps `chantier.yaml`'s `board:` key and its
  messages, and may move the board's settings into `board/address.py`. This CR touches `load`'s
  top-level dispatch and its unknown-key message in `playbook/config.py`. The Driver rebases onto
  whatever CR-222 left there.
- **CR-237 (root-pyproject-launch).** CR-237 moves the ruff and mypy configuration to the root
  `pyproject.toml`. The source stays in `skills/chantier/scripts/cli/src/chantier/`, so the paths
  above hold.
- **CR-238 (allow-rules-ask)** edits `driver.md`'s release publication (lines 558 to 564), and
  **CR-234** edits `forge-stack`. No overlap with either.

Batch-17 opened with no `chantier.yaml`, so this CR changes nothing for the running batch even
once merged. Its Drivers keep today's order.

## After it lands

The Chief of Staff files the project item of answer 3 for chantier's own repository:
- `ci:\n  beside_gate: true` in a `chantier.yaml` at the repository's root;
- mypy `--platform linux` and `--platform darwin` in `just check`.

Neither is part of this CR.

## Out of scope

- chantier's own `chantier.yaml` and the mypy platforms in `just check`: the separate project
  item above.
- The stack driver, the release driver and the QA driver keep their order.
- Any change to the gate's code, the gate lock, the queue, `activity`, or `foreman.md`. That is
  CR-235's.
- `handback ready`'s refusals: the gate pass and the `VERIFIED` verdict at the PR's head are
  still required.
- The project's CI files. The CR adds or changes no CI job: the Driver reads the forge's list of
  checks as the CI bullet says. No environment section is due.
- `hooks/` and `types/` do not change, so no `just mod`. The CR board pane draws nothing new
  (`STATUS.json` unchanged), so no screenshot.
- README and the other docs beyond `docs/agents-and-models.md`.

## Evidence

The CLI, the cards and the scenario change, so `just check` and `just scenario` (both forges)
apply (`AGENTS.md`).

- **E1.** `just check` passes on Windows locally, then in CI on Linux, macOS and Windows,
  including CR-221's lint (ruff, `mypy --strict`, sizes).
- **E2.** `just scenario` passes on both forges, with section 17b's new steps (E above). Each
  fails on the previous code: no `ci` key is accepted there, and no line is printed.
- **E3. Output unchanged when off.** On a scratch project with no `chantier.yaml`, `handoff`,
  `take` and `playbook` print exactly what they printed before (S2c). The Verifier keeps the
  before and after outputs in `evidence/`.
- **E4. A reading pass on the cards**, recorded in the Test plan:
  - `rg -n "ci: beside the long gate" skills/chantier/references` shows the rule in `driver.md`
    (Context, the long gate, Push, CI, the round sequence, `rebase:` merged, Known gaps) and in
    `chief-of-staff.md` (force-push step 2, the routing row);
  - `git diff` of `driver.md` shows every edit qualified by the line's presence, and none of
    today's sentences changed for a batch without it.
- **E5. Unproved until a real batch.** No agent runs in `just scenario`, so the Driver's new
  order is proved only by a batch on a project whose `chantier.yaml` turns the key on. The
  card's new text carries "unproved; trial: a CR Driver of a batch with the line pushes at the
  approved round, runs its gate while CI runs, and on a red CI job stops its gate and starts a
  debugger before the gate ends", in the form the cards use for the GitLab file form. This
  repository's own item (answer 3) gives that first batch. The PR's Known gaps names it.

## Open questions (each with the default this spec took)

1. **The key's name and shape.** Default: `ci: beside_gate: true`, a mapping that leaves room for
   more CI settings. The alternatives are a flat `ci_beside_gate: true`, or a key under a
   `driver:` mapping.
2. **A red CI job that is not the CR's.** The request says "a red CI job stops the gate". Default:
   only a red job that the CI bullet judges the CR's stops the gate. An infrastructure failure
   (one re-run) and a job also red on the default branch leave the gate running, because its
   result still counts. The alternative stops the gate on any red job.
3. **Known gaps without the key.** The request lists "the systems only CI covers" among the
   mode's points. Default: only with the key on. Answer 2 keeps today's behaviour without it.
   The alternative asks every CR Driver, in every project, for that bullet.
4. **`ship` before the gate.** Default: `ship` is unchanged and still prints `off: no long gate
   passed at <sha>`. The card says this is expected with the key on, and `handback ready` still
   enforces the gate. The alternative changes `ship`'s line in the mode, for example `long gate
   not passed yet at <sha> (CI beside the gate)`.
5. **Other Drivers.** Default: the CR Driver only. The stack driver ("heavy CI once at the top")
   and the release driver (the project's procedure) keep their order.
