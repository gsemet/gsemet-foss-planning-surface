# batch-09 retro

Restored by the Chief of Staff on 2026-11-11, after `close` deleted `4-batch/retro.md`. The user:
"les rétro peuvent être perdu ce serait bien qu'ils soient stocké dans la dernière CR du batch".
Rebuilt word for word from the Chief of Staff's own reading of the file before the close, and
from its own edits to it.

## 2026-11-11, pause after CR-164 to CR-170 (direct mode, the Chief of Staff steering)

Each line: the problem met, its state on main fde3da8, and the long-term fix. Every fix must hold
in any project chantier is installed in: no reliance on this repository's `just`, forge or OS.

- Workers wrote in the main checkout instead of their worktree (a stray edit of
  `scenario/run_scenario.py`, empty `commands.py` and `state.py` at the root, an empty
  `chief-of-staff.md` created then deleted): open. `worker.md` says "works only in the CR's
  worktree", nothing enforces it. Fix: the plugin's Claude Code hook refuses a worker's
  Write/Edit outside the worktree its prompt names; the Driver checks the main checkout is
  untouched (`git -C <main> status --porcelain` against its state at `take`) before hand-back.
- A Driver's `--force-with-lease` after a rebase was refused by the host's classifier ("Git
  Destructive"), not every time: fixed by CR-170 (the Chief of Staff judges and runs it).
  Unproved on a real refusal since.
- The Chief of Staff asked the user before that push although its card made the push its own:
  fixed by CR-170 (the card says it is not a question for the user).
- `handback ready` is accepted with no gate and no Verifier verdict at the pushed head; Drivers
  skipped a second Inspector after a fix (CR-164) and a last Verifier pass on the description
  (CR-167, CR-169): open (inbox `drivers-skip-verifier`). Fix: `handback ready` refuses unless
  the CR's record holds a passed gate and a Verifier `VERIFIED` note at the PR's head (CR-168
  binds proofs to a SHA); a step the card leaves to judgement stays the Driver's.
- The Chief of Staff told the Drivers to run "every step, the Investigator included", while
  `driver.md` makes the Investigator optional; two Drivers skipped it: open. Fix: a prompt never
  overrules a card; a step the user wants mandatory goes into the card or the playbook.
- A running direct batch refuses `order add`, and `pause` needs every CR merged: a new CR had to
  wait for the user's merge of CR-165: open. Fix: `order add` on a running direct batch queues
  the CR, as it does in Foreman mode.
- Grill and specification turns counted as steering, the steering share shown at 46 %: fixed by
  CR-165 (the pause report shows steering 30 %, the grill apart).
- The Chief of Staff's own `Explore` subagent is counted as "Driver Explore": open. Fix: an agent
  with no CR taken for it is the Chief of Staff's, in its own line.
- `gate <cr> "just check; just scenario"` failed on Windows (`shell=True` runs cmd.exe, which has
  no `;`): open. Fix: `gate` takes each command as its own argument and runs them in order,
  stopping at the first failure, on every OS.
- `ship 165` refused ("unknown CR 165"), `CR-165` needed: open. Fix: every command accepts the
  bare number, as `--batch` does.
- A second hand-back after a rebase was refused ("no Driver to hand it back"): open (inbox
  `handback-after-rebase`).
- The heartbeat showed odd ages (439 min while the loop was stopped): open (inbox
  `heartbeat-odd-values`).
- Spec-writers were refused for a wrong first prompt line; the relaunch made duplicates, three
  stopped by hand: open. Fix: the CLI prints the spec-writer's first line, as `take` prints a
  Driver's facts.
- The desktop app's Auto-fix asked, five times, to merge `main` into CR branches, against the
  project's rebase rule: open. Fix: `hosts/claude-code.md` says the Chief of Staff answers such an
  event in one line (the Driver rebases) and does not turn Auto-fix on for CR PRs.
- The Chief of Staff's brief stated a fact with no file behind it ("the Inspector approved
  rounds 2 and 3"); the Verifier could not trace it: open. Fix: a brief cites only the CR's
  notes and files.
- A Coder on Windows wrote a UTF-8 BOM before a shebang (`scripts/version.py`); another dropped
  the BOM of `scenario/run_scenario.py`: open. Fix: `worker.md` says a file keeps its encoding,
  and the Inspector checks the first bytes of each changed file.
- The reports pasted `cost` raw, with no template and no orchestration ratio: open (inbox
  `report-template`); the pause report now prints the ratio (CR-165).
- The retro's own behaviour (CR-165) could not be run by the Verifier: this section is its first
  real run.

Filed on the user's word (2026-11-11), after weighing rigidity and cost ("Le 6 oui je le veux.
7 ok tu peux discard.") and as one CR ("Une seule CR"): points 5, 6, 8, 9, 10, 11, 14 and 16
→ inbox `batch-09-retro-fixes`, which also absorbs `drivers-skip-verifier` (moved to trash).
That inbox item became CR-171, merged as PR 109. Point 7 (the prompt overriding the card) is
discarded; points 15 (Auto-fix) and 17 (the BOM) are not filed.

## 2026-11-11, pause after CR-171 (direct mode, the Chief of Staff steering)

- An empty `concepts.md` appeared at the main checkout's root at 12:43 while CR-171 ran: a
  worker again wrote outside its worktree. CR-171's hook was not loaded yet, since it loads only
  once merged. Fix: CR-171's hook, now on main; the next batch proves it or shows it unproved.
- CR-171's hook tests (`hooks/register.test.tsx`) were not run: the `claude` CLI is not on this
  machine's PATH, and CI does not run them. The Chief of Staff checked the event shapes against
  the engine's types by hand: `agent.spawn` resolves at start, and `tool.call` carries `tool`,
  `input` and `agentId`. Fix: CI runs `claude plugin test`, or the gap is stated in
  CONTRIBUTING.md.
- The CR-171 Driver used a round (`round 3`, note "x") only to read the `team:` lines. Fix: the
  Driver reads them with `handoff`, which counts nothing; `driver.md` says so.
- The CR-171 Driver passed its gate as one chained string (`just check && just scenario`): main's
  `gate` did not take several commands until CR-171's merge. It is fixed by CR-171 (the
  multi-argument form).
- `verdict` was not recorded for CR-171, because the command did not exist on main yet: the
  proof is in `work/verifier/`. The first real run of the two-gate refusal is the next batch.

Filed at the close, on the user's word: the second, third and fourth points → inbox
`cr-171-retro-fixes`, with a third about the `cost` label "Driver chief-of-staff with its
workers". The batch was closed at $84.06 of a $120 budget.
