# The batch-09 retro's fixes, in one CR

Batch-09 retro, 2026-11-11 (`4-batch/retro.md`). The user wants a fix strategy that "fonctionne
quand chantier sera déployé dans n importe quel type de projet", and worried that fixes
"rigidifie le process et ça augmente les coûts". The kept points, on the user's word ("Le 6 oui
je le veux. 7 ok tu peux discard."), filed as one CR on the user's word: "Une seule CR". Point 7
(a prompt overriding a card) is discarded; points 15 (Auto-fix) and 17 (the BOM) are left out.

Each part below is: what happened, then the proposed fix, to grill.

## 1. A worker cannot write outside its CR's worktree (retro point 5)

- **What happened:** workers wrote in the main checkout: a stray edit of
  `scenario/run_scenario.py`, empty `commands.py` and `state.py` at the root, and an empty
  `chief-of-staff.md` created then deleted. Nobody saw it until a `git pull --ff-only` was
  blocked. `worker.md` says a worker "works only in the CR's worktree"; nothing enforces it.
- **Fix:**
  - The plugin's Claude Code hook refuses a worker's Write or Edit outside the worktree its
    prompt names. It costs no token.
  - Before its hand-back, the Driver checks the main checkout is untouched, comparing
    `git status --porcelain` with its state at `take`.
  - Open: how the hook learns the worktree, and the Copilot host's equivalent.

## 2. `handback ready` refuses without a passed gate and a verdict at the head (retro point 6)

- **The user, asked how it works:** "Donc, le CLI donne les portes à passer comme des check list
  c est ca ?", then "C'est traduis sous quelle forme dans un fichier ? Un json".
- **What happened:**
  - In the 2026-11-10 retro, on which the user said "Oui c'est pas normal", the Drivers dropped
    proof passes "to save budget", although the CLI never refused on the budget:
    - CR-161 skipped the Verifier and recorded no long gate;
    - CR-162 skipped the Inspector on round 3, and the Verifier both at the pushed head and on
      the PR description;
    - CR-163 skipped the second Inspector and both Verifier passes.
  - Since then:
    - CR-164 skipped a second Inspector after a fix;
    - CR-167 and CR-169 skipped the last Verifier pass on the PR description.
- **What main records (fde3da8):**
  - `gate` logs `result`, `head` and `command` to `events.jsonl`.
  - `ship` stores `pr` and `head` in `batch.json`.
  - A verdict is free text only, so the CLI cannot read it.
  - `handback ready` checks only that a PR exists.
- **Fix agreed with the user:**
  - Two gates, no more, both at the PR's head:
    - the project's long gate passed;
    - a `VERIFIED` verdict.

    Every other step stays the Driver's judgement.
  - A command `verdict CR-x VERIFIED` reads the head from the worktree and logs
    `{"event": "verdict", "cr": ..., "result": "VERIFIED", "head": ...}`. The CLI knows a
    verdict, not a role.
  - `handback ready` looks for both gates at the head `ship` recorded, and refuses, naming the
    missing one.
  - `take` prints the gates up front, as a checklist.
  - A project with no long gate has no first gate.
  - Also find why the Drivers believed the budget stopped them (the card's wording, the budget
    shown to them).

## 3. `order add` queues a CR on a running direct batch (retro point 8)

- **What happened:**
  - `order add` was refused on a running direct batch ("strict"), and `pause` needs every CR
    merged.
  - CR-170 therefore had to wait for the user's merge of CR-165, then a pause, then an add.
- **Fix:** `order add` on a running direct batch queues the CR, as it does in Foreman mode. The
  Chief of Staff takes it when a slot frees.

## 4. `cost` puts the steering session's own subagents on their own line (retro point 9)

- **What happened:**
  - The Chief of Staff's `Explore` subagent, started with no CR, was counted under "Driver
    Explore".
  - This is linked to the user's remark: "Attention je pense que tu as pris ta session entière
    alors qu'on a enchaîné les batch dans la même session".
- **Fix:** an agent with no CR taken for it belongs to the steering session, or to grill and
  specification by CR-165's window, on its own line.

## 5. `gate` runs several commands the same way on every OS (retro point 10)

- **What happened:** `gate <cr> "just check; just scenario"` failed on Windows.
  - `gate` uses `shell=True`, which runs cmd.exe on Windows, and cmd.exe has no `;`.
- **Fix:**
  - Each command is its own argument (`gate CR-x "just check" "just scenario"`).
  - They run in order and stop at the first failure.
  - Each run is logged with its result and the head.

## 6. Every command accepts a CR's bare number (retro point 11)

- **What happened:** `ship 165` was refused ("unknown CR 165"), while `--batch` accepts a bare
  number.
- **Fix:** `165`, `CR-165` and `cr-165` are accepted alike.

## 7. The CLI prints the spec-writer's first prompt line (retro point 14)

- **What happened:**
  - Spec-writers were refused for a wrong first prompt line.
  - The relaunches made duplicates, and three had to be stopped by hand.
- **Fix:** the CLI prints the exact first line, as `take` prints a Driver's facts.

## 8. A brief states only facts it can cite (retro point 16)

- **What happened:**
  - A brief said "the Inspector approved rounds 2 and 3" with no source.
  - The Verifier could not trace it.
- **Fix:** in `chief-of-staff.md` and `foreman.md`, a brief states a past fact only with its
  source: a CR note, a file in the CR folder, or an event. Anything else is said as unknown.
