# SC20: New cards: the CR, stack, QA and release Drivers

Child 20 of 28 of the program `simplify-cards-and-prompts`. The program's `03-change-spec.md`
("Common to children 19 to 23", "Child 20"), its `02-answers.md` (answers 17 to 22) and
`work/study-*.md` rank above this file. Where they say more than this file, they win. Child 19's
specification (`1-inbox/sc19-cards-workers/03-change-spec.md`) fixes where the new files live, the
budgets and the proof method for the whole family of card children. It was not written when this
file was written. This file follows the program's text on those three points. If child 19's
specification says otherwise, child 19's wins, and the Driver follows it without asking.

## Intent

Write the four Driver cards of the target card set, with their help topics, in
`skills/chantier/cards-next/`, a folder that nothing loads. The cards are for the CR driver, the
stack driver, the QA driver and the release driver.

Today the four Drivers share `skills/chantier/references/driver.md` (54,955 bytes on `origin/main`
8a960d34) and 16 pieces of about 82 KB. Study-fable-v2 measured what they read at the start: the
CR driver 44 KB (n=279), the stack driver 56 KB, the release driver 28 KB, and no run of the QA
driver. The target is a card of 4, 4, 3 and 2 KB, plus the floor and one host row. Every rare case
moves to a help topic, a `next:` line, a refusal or `--help`.

## Place in the chain

- **Base:** child 19's branch, the batch's stack top when this child joins (program rule F16).
- **Builds on:**
  - child 1: `chantier push`;
  - child 6: the quiz cases and the baseline of the old cards;
  - child 7: the topic format and today's Driver topics;
  - child 8: host capabilities and rows;
  - child 10: `brief` with `--cards`, and the floor;
  - child 12: `next` and the `next:` lines;
  - child 13: `msg steering`;
  - child 18: `roles.yaml`;
  - child 19: `cards-next/`, its `floor.md`, and the first `cards-next/topics.json` if child 19
    writes one.
- **Next:** child 21 (the Foreman) builds on this branch. Child 21 adds the Foreman's side to the
  shared topics this child starts (`lease`, `refused-push`).
- **Later children:**
  - child 23 writes the shared cards this child's cards link to (`concepts.md`, `pr-template.md`,
    `release-template.md`, `forges/`), the final `topics.json` and the final `floor.md`;
  - child 24 swaps the set in and points each Driver role at its own card;
  - child 25 reviews every removed rule.
- **Merge:** under the program's merge rule (answers 14 and 22: F2, F11, Q8).
  - The merge waits for the owner.
  - Children 19 to 28 merge as one unit, in order, in one sitting, with no session started in
    between.
  - They merge only after child 28's campaign has passed.
  - The Driver records `$CHANTIER wait <cr> merge <child 28's PR>`. If child 28's PR does not
    exist yet, it records the wait on child 28's CR with a `--note` that says so, and the steering
    session updates it.

## Decisions carried

| Source | Decision | Where in this CR |
| --- | --- | --- |
| Answer 1 | No role is added, removed or merged, and no role's responsibility changes | the four cards keep today's duties |
| Answers 14, 17; F2 | Total rewrite, written beside the old set, nothing loaded until the swap | `cards-next/` only |
| Answer 8; F3 | The refused-push route stays for good: the Driver hands back, the steering session runs the push | topic `refused-push` |
| F21 | `chantier push` is a Driver's one way to publish its branch. It never retries a refused `git push`, and a refused `chantier push` is never followed by a raw push | CR, stack and release cards; topic `refused-push` |
| Q6 | The steering session keeps the plain `git push --force-with-lease` | named in topic `refused-push` as the steering session's step, not the Driver's |
| F5 | A rule that protects the user or the repository lives in the floor, the card or a refusal, never in a topic alone. The cap on nevers gives way before such a rule | each card's nevers |
| Answers 4, 13; F8 | `msg steering anomaly|blocked|note`. With no watcher it prints `not delivered` and exits non-zero. Then the Driver uses its host means or the hand-back | CR, stack and release cards |
| Answer 11 | `next` is advice. Safety steps are refusals | cards point to `next:` lines; no step lists |
| Answer 10 | A rare incident rule with no CLI trigger becomes a topic with `review_by` set to the next minor version | `topics.json` rows |
| Q4 | Budgets are targets. A card or topic above its target is listed in Known gaps with its size | evidence |
| M3 | No dates, batch names or trial stories in a card or topic | all files |
| F17 | An unproved claim is marked "unproved" | all files |
| F20 | The child states the seconds it adds to `just test` | evidence |
| Pending item `driver-card-leads-left-by-role-cards-sti` | Three leads carried as card lines or topics | section 4 |
| Pending item `release-drafts-are-a-worker-s-job-not-th` | The release driver's card is written as the release driver works today. That item changes it after the swap | out of scope |
| Pending item `driver-context-second-cut` | Absorbed here for the Drivers' cards and topics. Prompts, manifest, `take` and `handoff` go to children 10 and 24 | section 1 |

## What changes

All files are new, under `skills/chantier/cards-next/`. Sizes are LF bytes. No existing file
changes.

### 1. Four Driver cards

One file per role. There is no shared Driver card: study-fable 4.2 sets one boot per role (card,
floor and host row), and a shared card would load the other three roles' text.

| File | Role (`roles.yaml` name) | Target |
| --- | --- | --- |
| `cards-next/cr-driver.md` | `cr-driver` | 4 KB (4,096) |
| `cards-next/stack-driver.md` | `stack-driver` | 4 KB (4,096) |
| `cards-next/release-driver.md` | `release-driver` | 3 KB (3,072) |
| `cards-next/qa-driver.md` | `qa-driver` | 2 KB (2,048) |

Each card has the five parts of the common rules, in this order:
1. the role's goal;
2. what it owns;
3. its nevers;
4. how it ends;
5. its reply format.

A card holds nothing that is already in one of these:
- the floor (`cards-next/floor.md`: rebase only, no fallback, a CLI that cannot run, never discard
  the worktree's work, refusals verbatim, no process stopped by pattern);
- a topic;
- a CLI refusal;
- a `next:` line (round, gate, push, ship, verdict, handback: child 12);
- a command's `--help`;
- the host rows that `brief` adds (message steering, start a child, ending, compacting, write
  guard: child 8's capabilities `driver-hand-back`, `driver-messages-steering-direct`,
  `start-driver`, `end-turn-background`, `stop-own-background-task`, `compact`, `write-guard`,
  `driver-start-folder`).

A card names a capability by its id (`chantier host <id>`) and restates no row. A card names a
topic as `chantier help <topic>`, with the moment that sends the role there.

**`cr-driver.md`**, from `driver.md` "CR driver", "CR driver: ship and proof", "CR driver: the
closing" and the shared "Means:" sections:

- *Goal:* take one CR from its specification to a green PR, proved at its pushed head, and hand
  it back.
- *Owns:*
  - git and the forge for its own CR branch, by the project's rules;
  - the worktree's commits;
  - `<work folder>/pr-body.md`, its notes and, when `take` prints an archive path, the archive.

  Every change to a project file goes through a `coder`. Its own reading of code is an
  `investigator` or a `debugger`. The `Team:` review steps run in order.
- *Steps:* one line saying that `chantier next <cr> --lease <n>` and the `next:` line at the end of
  each command give the next step. The card lists no step order that `next` gives.
- *Lines no tool carries, kept short:*
  - every `APPROVE` is noted at once, with its `head`, before any other step;
  - a box of `pr-body.md` cites only a recorded note;
  - a gap is written in the body's Known gaps first;
  - the PR is opened as a draft, from `pr-template.md` (child 23) or the project's own template;
  - the body is a file, posted from that file;
  - the evidence plan is the Driver's;
  - the closing at 115,000 tokens or more is a `context: closing:` hand-off (topic `closing`).
- *Nevers*, from five, more where F5 asks:
  1. edit no project file itself, the shell included;
  2. publish the branch only with `chantier push <cr> --lease <n>`, and never retry a refused push
     by another means (F21; topic `refused-push`);
  3. never call the host's hand-back before `$CHANTIER handback` is accepted;
  4. never `git stash`, never `git add -A`, never a merge commit (rebase only: floor 2);
  5. never comment on, close or reopen an issue;
  6. never turn a PR ready on a base other than the default branch.

  Each of these protects the repository or the user, so the cap gives way before it (F5).
- *End:* background tasks stopped first (`chantier host stop-own-background-task`), then
  `handback ready|blocked`, then the host's hand-back, whose first line is the line `handback`
  printed. The reasons and forms of a hand-back are in `handback --help` and topic
  `handback-other`.
- *Reply format:* the one line `handback` printed, unchanged.

**`stack-driver.md`**, from "Stack driver" and the four `stack-driver-*` pieces:

- *Goal:* one native stack on the forge, read back as ready to merge, with its mergeable part
  ready and the drafts on top.
- *Owns:* the order of the stack (`stack <cr>…`), and the rebase and push of every CR with no live
  Driver (`chantier push <cr> --lease <n> --unit stack`, one command per branch). It also owns
  `forge-stack`, the turning ready of the mergeable part, and heavy CI at the top.
- *Nevers:*
  1. never rebase or push a `working` CR's branch;
  2. open no PR;
  3. edit no project file;
  4. never a loop or a script over branches;
  5. never read matching forge bases as proof of the chain. Check with
     `merge-base --is-ancestor`, and an exit code other than 0 or 1 is not "based".
- *Topics:* `stack-restack`, `stack-make`, `stack-joins`, `stack-changes`, `lease`,
  `refused-push`, `conflicts`.
- *End and reply:* `[stack→foreman] hand-back …` through the host's hand-back, after
  `forge-stack show` passed its five checks (topic `stack-make`).

**`release-driver.md`**, from "Release driver" and the four `release-driver-*` pieces:

- *Goal:* run one release CR by the project's own procedure, adding nothing from habit.
- *Owns:*
  - the version (from the specification; otherwise from its own pick, explained in the PR and a
    note, never asked);
  - the release PR, ready on the default branch and a draft on any other base;
  - `phase <cr> release "<step>"` at each step;
  - `release start|go|published`.
- *Nevers:*
  1. no irreversible action without `release go` for that action (floor 6);
  2. never fix code, and start no children: a defect becomes `<work folder>/fix-<n>.md` and
     `handback blocked fix:`;
  3. never undo half-done irreversible work: `blocked question:` says what is out;
  4. never post the announcement thread;
  5. publish only with `chantier push`.
- *Lead 1:* the line on the typed `pipeline` wait (section 4).
- *Topics:* `release-notes`, `release-ship`, `release-merged`, `release-end`, `lease`,
  `refused-push`.
- *End and reply:* the line `handback` printed.

**`qa-driver.md`**, from "QA driver":

- *Goal:* use the project as its user would, at the head of the default branch, and report what
  breaks.
- *Owns:* a detached worktree of its own, removed at its end. It also owns the work folder:
  `04-result.md` (one finding per bullet, with steps, expected and actual, or "No findings.") and
  `evidence/`.
- *Lease:* `lease O-k renew --lease <n>` at each wake, and `lease O-k hold` before a long test
  (topic `lease`).
- *Nevers:*
  1. never test an unmerged PR;
  2. never fix, and start no children;
  3. report nothing it has not reproduced;
  4. keep no screenshot that fails the look (floor 8; topic `pr-extras`).
- *End and reply:* `[qa→foreman] qa done <folder> <n> findings` through the host's hand-back. The
  QA driver cannot send `msg steering` (child 13).

### 2. Driver topics

Each topic is one file, `cards-next/topics/<name>.md`, with a target of 1.5 KB (1,536 bytes). Each
gets one row in `cards-next/topics.json`, in child 7's format:
- `version` 1;
- `readings` relative to `cards-next/`;
- `roles` from `roles.yaml`;
- `trigger` quoting the CLI line's start in backticks where a line names the topic;
- `review_by` optional, as `X.Y.Z`.

If child 19 has written `cards-next/topics.json`, this child adds its rows to it. If not, it
creates the file with `version` 1 and the `paths` key of child 7's file. Child 23 finalizes it.

Rule for names: every Driver topic name in child 7's table stays, so `help --for <role>` and any
CLI line that names one (`help lease`, `help refused-push`) still resolves after the swap. A topic
too big for its target may be split into new names. The old name then stays as the row whose
`readings` list the parts.

| Topic | Roles | Substance (source on `origin/main`) |
| --- | --- | --- |
| `lease` | D | renew, `hold` (45 min by default, 90 at most), `not confirmed`, `claim lost` (stop at once, record nothing more), `take --reclaim` (`driver-session.md`, "the lease"). Child 21 adds the steering side as a second reading |
| `refused-push` | D | section 3 below (`driver-refused.md`) |
| `retake` | `cr-driver` | a first `take` that shows a `PR:` link; carried verdicts; `at <head7> (carried from <sha7>)` (`driver-retake.md`) |
| `restart` | D | a `take` note `resume:`, `rebase:`, `context:` (`driver.md`, "a Driver started again") |
| `checkpoints` | D | checkpoint commits and their messages (`driver-session.md`) |
| `steering-messages` | D | `msg steering` kinds and what wakes the steering session (answer 4); the host means when `not delivered`; `inbox` (`driver-session.md`) |
| `trouble` | D | a worker that fails, escalation, a remote command that fails, stopping a long gate, a git command in the wrong place (`driver-trouble.md`, 13,350 bytes: split, see the naming rule) |
| `ci` | D | the forge's checks as the only source, the head first, "no CI" seen in two looks a minute apart, the note's form, a failure log saved under the work folder; with leads 2 and 3 (section 4) (`driver.md`, "CI"; `driver-trouble.md`, "CI beside the long gate", "CI lists no check") |
| `conflicts` | D | a carry, a conflict, the early push, `ship --conflict`, a move after a judgment (`driver-conflicts.md`) |
| `handback-other` | D | hand-backs out of the ordinary, `--wait`, `blocked waits:`, `--no-gate` (`driver-handback-other.md`) |
| `closing` | `cr-driver` | the four closing steps and their notes, and the 115,000 and 130,000 token rules (`driver.md`, "CR driver: the closing") |
| `pr-extras` | D | the archive in the PR, images and the look, GitLab forms (`driver-pr-extras.md`) |
| `matrix` | `cr-driver` | the matrix probe, the board's write paths (`driver-matrix.md`) |
| `stack-restack` | `stack-driver` | the restack pass, `restack:` notes, resuming (`stack-driver-restack.md`, "Recording a restack", "Resuming") |
| `stack-make` | `stack-driver` | making the stack, the five checks, the final-order take (`stack-driver-make.md`) |
| `stack-joins` | `stack-driver` | a join, a draft turning ready, a merge, a deadline (`stack-driver-joins.md`) |
| `stack-changes` | `stack-driver` | an insertion, a drop, a hold, a park, a conflict, heavy CI (`stack-driver-changes.md`) |
| `release-notes` | `release-driver` | the notes, the drafts, the PR body (`release-driver-notes.md`) |
| `release-ship` | `release-driver` | the release PR; a `ship` refused in an ordered batch (`release-driver-ship.md`) |
| `release-merged` | `release-driver` | after the merge (`release-driver-merged.md`) |
| `release-end` | `release-driver` | the end (`release-driver-end.md`) |

`D` stands for `cr-driver`, `stack-driver`, `qa-driver` and `release-driver`, limited to the
roles the topic serves (the QA driver gets `lease`, `trouble` and `pr-extras` only).

**`review_by`.** Answer 10 sets it to the next minor version after the version in
`.claude-plugin/plugin.json` on the base (`X.(Y+1).0`). It goes on each topic that only holds rare
incident rules with no CLI trigger: the `trouble` parts on a git command in the wrong place and on
stopping a long gate, `matrix`, and the GitLab-forms part of `pr-extras`. The PR lists which rows
carry it and why.

No rule that F5 names (the floor's rules, and the nevers above) lives in a topic alone. A topic
may repeat the command form of a never, but never the never itself.

### 3. The refused-push route (answer 8, F3, F21), topic `refused-push`

The Driver's side, written for `chantier push` (child 1):

- **`chantier push` exits 4** (`push <cr>: git refused the push of <branch>; nothing recorded`,
  then git's text): the remote moved or refused.
  1. `note <cr> "refused: chantier push <cr> -> <git's exact text>"`.
  2. Never retry, and never run a raw `git push` (F21).
  3. Hand back `blocked refused <exact text>` (floor 9).
- **The host refuses the command** (`chantier push`, or `git rebase` before it), with the work
  committed:
  1. `note <cr> "refused: <exact command> -> <host's exact text>"`.
  2. `note <cr> "next after push: <steps>"`.
  3. `handback <cr> blocked waits: push <branch> <expected remote sha> <local sha>`. For a rebase,
     the hand-back is `waits: rebase <branch> <base>`.
  4. Send the line `handback` printed, and end.

  The steering session runs the plain `git push --force-with-lease` (Q6). That side is children
  21 and 22's, and child 21 adds it as a second reading of this row.
- **A fresh Driver** reads the `push:` answer in its `take` notes:
  - `pushed`: go on from the `next after push` note;
  - `push failed`, or `push refused … no long gate`: as the note says;
  - any other refusal: `blocked refused <exact text>`.
- The ladder: Driver, steering session, Chief of Staff, user.

The topic quotes the triggers `` `push <cr>: git refused the push` `` and a host's refusal of
`chantier push`. The cards name it in their push never.

### 4. The three leads (`1-inbox/driver-card-leads-left-by-role-cards-sti`)

1. **The typed `pipeline` wait for a long run on main.** One line in `release-driver.md`: a step
   that waits for a long pipeline on the default branch is recorded as a typed wait, either
   `handback <cr> blocked <reason> --wait pipeline=<sha>` or
   `wait <cr> add pipeline --ref <sha> --link <PR link> --note "<text>"` when the release driver
   goes on with other steps. It never polls. `release-merged` gives the details.
2. **Read a project guideline by section, not whole.** One line in each of the three pushing
   Driver cards' "owns" part: after `$CHANTIER rules`, read the first instruction file whole, and
   any other guideline only by the section that touches the step (Grep the heading, then Read with
   an offset and a limit).
3. **Wait only in a background shell.** One line in `cr-driver.md` and `stack-driver.md` (and in
   topic `ci`): a long wait (CI, a long gate's end) is one command in a background shell, followed
   by `lease <unit> hold --lease <n>`, then the end of the turn (`chantier host
   end-turn-background`), so the command's end wakes the Driver. Topic `ci` adds: "A Monitor tool
   used from a subagent is unproved; use the background shell" (F17).

### 5. Evidence helpers, outside the repository

`brief` (child 10, read through `roles.yaml` since child 18) with `--cards <folder>` reads
`<folder>/<the role's card file>`. On the base, that card file is `driver.md` for all four
Drivers. Child 24 points them at the four new files. Until then, the Driver builds one staging
folder per Driver role in the session's scratch folder, never in the repository:
- `driver.md`, a copy of `cards-next/<role>.md`;
- `floor.md`, a copy of `cards-next/floor.md`;
- `topics/` and `topics.json`, copied from `cards-next/`.

It runs `brief` and `quiz` with `--cards <staging folder>`. This is the program's single method
(`brief`/`quiz --cards`), fed with this family's files. The PR's Internal references name the
staging step. See question 1.

## Out of scope (must not)

- Any edit to `skills/chantier/references/`, the CLI (`src/`), `hooks/`, `types/`, the wrappers in
  `agents/` and `com.github.copilot/agents/`, the four `SKILL.md`, `roles.yaml` or
  `startup-manifest.json` (common rules; child 24 points the card paths).
- The shared cards and templates in `cards-next/` (`concepts.md`, `pr-template.md`,
  `release-template.md`, `forges/`), the host topics, the final `topics.json` and the final
  `floor.md`: these are child 23's. This child links to them by their target names.
- The Foreman's and the Chief of Staff's sides of the refused-push route and of `lease`: children
  21 and 22.
- New quiz cases or any change under `evals/` (child 25 writes cases for rows it finds uncovered).
- The release-drafts pending item: it changes the release card after the swap.
- Removing any old file: child 24.
- Any change to what a role is responsible for (answer 1).

## Acceptance evidence

All of it in the PR, at its pushed head.

1. **Bytes.** A table of LF bytes per new file (`wc -c` after `tr -d '\r'`, or the Python
   equivalent), against each target. Each file above its target goes in Known gaps with its size
   (Q4).
2. **Boot per role.** The bytes of `brief <role> --cards <staging folder for role>` for
   `cr-driver`, `stack-driver`, `release-driver` and `qa-driver`. They stand beside the old start
   readings (44, 56 and 28 KB, and "no run" for QA, from study-fable-v2) and beside the boot
   targets (6, 6, 5 and 4 KB, study-fable 4.2).
3. **Quiz under F4.** For each role, `just quiz <role> --cards <staging folder> --against
   evals/results/quiz-<date>-baseline-old-cards-<role>.json --save cards-next-<role>`, with the
   default cap (`--max-usd 10`) and `--plan` printed first.
   - No case may score 0/3 that the old cards passed.
   - It must show the `cr-driver` cases whose `rules` hold `floor-1`, `floor-2`, `floor-5` and
     `floor-9`.
   - A role with no case (likely `qa-driver`) is reported "no case".
   - If a Driver cannot run headless `claude -p`, it hands back with the commands and the staging
     folders, and the Chief of Staff runs them (child 6's risk). The Known gap names it until then.
4. **Links.** Every relative link and `chantier help <topic>` name in the new files resolves
   inside `cards-next/`. The exceptions are the files child 23 writes, listed by name in the PR. A
   short script run from the scratch folder prints the check, and its output goes in the PR.
5. **`topics.json`.** It loads with child 7's loader pointed at it: `load_topics(path)`, the
   tests' path form. Every reading exists, every role is in `roles.yaml`, and every `review_by`
   matches `X.Y.Z`.
6. **Rule rows for child 25.** A list in the PR (and in `evidence/cards-inventory-drivers.md` of the CR folder) of
   the old rules the family covers. Each rule of `driver.md` and of the 16 pieces gets a row:
   - its source line;
   - where it went: card, topic, floor, refusal, `next:` line, `--help`, or "inferable" with its
     reason;
   - never "inferable" for an F5 rule.
7. **The leads.** The three lines of section 4, quoted with their file and line.
8. **Gates.** `just check` green. The long gate `just scenario (ubuntu-latest)` green at the PR's
   head (a card change owes it). The local `chantier gate <cr> scenario` is owed only if this CR is
   the top of the stack, by AGENTS.md's stack rule. `just eval-dry-run` and `just mod` are not owed
   (no change under `src/`, `evals/kit/`, `hooks/` or `types/`).
9. **`just test`: 0 seconds added.** No test file changes, and no test reads `cards-next/` (on
   `origin/main` no test globs the cards folder; `test_board_read_key.py` reads only
   `references/*.md`). The PR states the measured `just test` time before and after.
10. **The merge wait** on child 28, recorded.
11. **Known gaps:** at least "real run not done (child 28)", each file above its target, and the
    staging step for `brief`/`quiz` until child 24.

## Risk

- Long gate owed. No AGENTS.md change. No `just mod`.
- Quiz spend falls on the user's machine, capped at $10 per call and printed first. Four roles
  cost at most $40 if each call reaches its cap.
- Headless `claude -p` from a Driver is unproved (child 6). See the fallback in evidence item 3.
- The cuts are deep (about 137 KB down to about 13 KB of cards plus topics). A rule cut without a
  home is caught by child 25's review, so the row list (evidence 6) must be complete.
- The release driver's new attempt today runs `git reset --hard <base>` in its worktree, which
  floor 5 forbids in general. See question 2.

## AGENTS.md

None.

## Open questions

1. sc20-Q1 (scope, method): `brief --cards <folder>` reads `<folder>/driver.md` for every Driver
   role until child 24 changes `roles.yaml`. That makes the staging folders of section 5 needed.
   Should an earlier child (10 or 18) make `--cards` prefer `<folder>/<role>.md` when it exists, so
   that children 20 and 23 run `--cards skills/chantier/cards-next` as written? Default if
   unanswered: staging folders in scratch; child 24 points the paths.
2. sc20-Q2 (behaviour, risk): today the release driver starts a new attempt with
   `git -C <worktree> reset --hard <base>`, and floor 5 says never discard the worktree's work.
   Should the new card require a new worktree for each attempt (`git worktree add` on the base,
   the old one removed by the steering session), keeping the floor without an exception? Or should
   it keep `reset --hard` as a named exception in the release card? Default if unanswered: a new
   worktree per attempt, no exception, with the change named in the PR for child 25.
