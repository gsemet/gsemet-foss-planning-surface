# Rewrite the role cards: minimal boot, progressive disclosure

Program specification. It does not land as one PR. It is cut into the ordered chain of child CRs
in `## Children`: one Driver and one PR per child, stacked in that order. Each child stands on
its own, so a later Spec-writer can turn it into a full Change Specification without asking
anything.

This second version folds in answers 21 and 22. Answer 22 settles the spec critic's 21 findings
(F1 to F21) and the first version's eight open questions. The Chief of Staff settled it under the
owner's "totale autonomie" (answer 21), and the owner confirms it at wake.

Code read: `origin/main` at `8a960d34`. That is chantier 0.15.1, plus CR-471's cut of the cards
by moment, plus the Foreman's own watcher. All paths are relative to the chantier repository.
Short forms used below:
- `src/` is the CLI's source, `skills/chantier/scripts/cli/src/chantier/`.
- `tests/` is its tests folder, `skills/chantier/scripts/cli/tests/`.
- `references/` is the cards folder, `skills/chantier/references/`.

## Goal

The owner's words (answers 1, 17, 18, 20): the cards are far too heavy and detailed. They are the
result of dozens of runs and retros, each adding a small correction, and they cost a lot at every
role's start. What the owner asks for:
- Rely on Opus 5.5 and Sonnet 5.5 to infer from a vital minimum.
- Rewrite the card mechanism completely: the smallest possible cards, and no behaviour lost.
- Push progressive disclosure as far as it goes. A model that stumbles runs `--help` or
  `help <topic>`. The watcher, the server and the CLI's lines remind it where it stands. Agents
  message the steering session through the board instead of waking it.
- Keep role cards simple, so that outside people can later bring their own roles.
- Go straight to the desired state in one total rewrite. Then check, by reading and comparing,
  that nothing important was lost, and that everything removed is easy for the agents to find
  again or is already in the model's weights.

Fixed (answer 1):
- the roles themselves (their cards are not fixed; no role is added or removed);
- working with the surface server (it may be improved);
- the Foreman orchestrating with the tools it is given.

The work is mostly better tools and per-role progressive disclosure.

The end state:
- Every role boots on three things: one short card, one shared floor and its facts. The CLI
  prints them whole, in a brief. No role reads a manifest, a core file or a host card at boot.
- What a role needs at a rare moment comes from a help topic. A refusal, a `next:` line or a
  state line names that topic. No role keeps a list of moments to remember.
- A rule that protects the user or the repository lives only in the floor, in the role's card or
  in a CLI or hook refusal (F5).
- A rule lives in one place. No card holds dates, batch names, trial marks or incident stories.
- Pytest gates keep it so. A retro fix lands as code, a refusal, a `next:` line or a help topic.
  A card grows past a gate only with a line the user signs.

Starting figures, from study-fable-v2 (LF bytes):
- The cards are 829 KB in 70 files.
- Declared start reading on Claude:

  | Role | Declared start reading |
  | --- | --- |
  | Chief of Staff | 202 KB (110 KB of it the Claude host card) |
  | Foreman | 91 KB |
  | Griller | 145 KB |
  | Drivers | 24 to 34 KB |

- Measured real reading on the old cards:

  | Role | Measured reading |
  | --- | --- |
  | Chief of Staff | 218 KB |
  | Foreman | 144 KB |
  | CR driver | 44 KB |
  | Verifier | 17.5 KB |

- No role has yet run on CR-471's cards.

## Decisions carried

This table lists every answer in `02-answers.md` and the child that carries it. Answers 17, 18,
20, 21 and 22 rank highest. Answers 17 and 18 replace answer 5 (simplify-cards-Q8), which is
carried only in what they keep of it.

| Answer | Decision | Carried by |
| --- | --- | --- |
| 1 framing | Smallest cards, no behaviour lost, progressive disclosure. A total overhaul is accepted if every boot gets much lighter. Roles, server and the Foreman's orchestration stay fixed | the whole program; card children 19 to 24; measure in child 28 |
| 2 study-v2 | The design is judged on origin/main | this specification reads `8a960d34` |
| 3 Q6 stumbling | No stumbling on the common path; rare cases are free. A usage error or refusal in more than 2 % of a role's runs is a tool bug, not a card gap | children 2, 3 and 4; the S-list in child 5; M10 in child 27 |
| 4 Q7 messages | `msg` and `inbox` exist. Only `anomaly` and `blocked` wake the Foreman; notes wait for its next wake | child 13 (narrowed by F8) |
| 5 Q8 scope | Replaced by answers 17 and 18. What they keep of it: a program CR whose children regroup study-fable-v2 section 6; a real run measured on the new cards; `help <topic>` as the carrier of the pieces; the host card out of the start | `## Children`; see the regrouping table in `## Order` |
| 6, 7 Q5 | A CLI subcommand, `chantier push <cr>`, runs the `--force-with-lease` push itself, for GitHub and GitLab. It exists to declare that the operation is legitimate in what the Driver is doing. Rails: the CR's recorded `chantier/*` branch only, never the default or a protected branch; the caller holds the CR's lease; the worktree is clean. AGENTS.md gains a git exception and a network use. It is tried in auto mode from a Driver, in compound form, before any card is cut. It is refused through a profile's `cli.run`, like `gate` | child 1 |
| 8 Q5b | The Chief of Staff runs these alone, then tells the user in the report: a refused `--force-with-lease` push or rebase of a `chantier/*` CR branch of the batch; a refused `gh pr ready` or `gh pr edit --base` on the batch's PRs; a chantier subcommand refused in a chain (run again alone). It still asks before: editing `settings.json`; stopping a process it did not start; publishing a release; deleting branches or folders; pushing a branch that is not the CR's own | child 22 (Chief of Staff card); child 7 (the topic a refusal names) |
| 9 Q9 | Hard gates in pytest: M1, M2, M3, M4, M9 and M13. Also the retro-fix ladder (M5) and the transcript measure `just behaviour` (M7). Budgets are frozen per role, and raising one needs the user's line (M11) | child 3 (M9), child 5 (M7, M8 runner, M10 and M14 lists), child 26 (M1, M2, M3, M4, M8, M12, M13), child 27 (M5, M6, M10, M11, M7 in the release claims) |
| 10 Q10 | A rare incident rule with no CLI trigger is kept as a help topic for one release. Reads are measured, and the never-read topics are then deleted | child 7 (`review_by`), child 25 (files them), child 5 (counts reads). The deletion is out of scope |
| 11 Q11 | `next` is advice for choosing a CR and for wording. Safety steps are refusals, not advice. The CLI words the ask to the user, and the Foreman may add one sentence | child 12 (`next`), child 14 (`judge`), child 9 (AGENTS.md), card children |
| 12 Q12 | Roles from outside: review steps, critics and workers that write in the worktree; never a steering role | child 18 keeps the role kinds in its data. Loading a project's own roles is a later CR (F9) |
| 13 Q15 | In direct mode the Chief of Staff gets the Foreman's card and tools (`next`, the watcher) | children 12, 13, 22 |
| 14 Q16 | One card set only. The old cards are removed when the new ones merge; no `cards: v1` switch; a rollback is a git revert. The real-run measure and the quiz pass before the swap | children 19 to 23 write unloaded files; child 24 swaps; child 6 (quiz); child 28 (real run); the merge rule |
| 15 Q14 | No floor decision; a principle instead: files simple to edit, modular, loaded when needed | "The floor" below; children 10 and 23 |
| 16 Q13 | When a host function is used, the CLI says in one sentence that it was never tried for real here. Trial history moves to a proof file nobody loads | child 8 |
| 17 Q17 | A total rewrite straight to the desired state, then a read-and-compare review. Every removed rule is kept, found again through a topic, a refusal or a `next:` line, or judged inferable | children 19 to 24 (one target, written in one run of chained CRs, no family-by-family migration of loaded cards); child 25 (review) |
| 18 Q18 | Order: tools first, with the push subcommand tried in auto mode from a Driver; then the total rewrite; then the review; plus the real-run measure and the gates | `## Order` |
| 19 Q19 | Grilled enough | this specification |
| 20 Q20 | Destination batch-31. The specification goes to the end of the rewrite, cut into chained CRs. Goal: a stack of all these CRs, each validated and ready to merge in order | `## Children`, one stack |
| 21 Q21 | Batch budget $400; the plan suits the owner; total autonomy | "Cost" below |
| 22 Q22 | F1 to F21 and the first version's Q1 to Q8, settled as listed below; the owner confirms at wake | each one in the table below |

### Answer 22, finding by finding

| Item | Settled as | Where |
| --- | --- | --- |
| F1 | The short prompt that `brief` prints keeps the `writes:` and `worktree:` lines after its first line. The hook is unchanged. A test asserts it | child 10 |
| F2 | The rewrite is split. New cards and topics are written beside the old, as files nothing loads, one CR per family: workers; Drivers; Foreman; Chief of Staff and Griller; host and shared. Then one small swap CR does the CLI outputs, the hook message, the removal of the old set and the test conversion. Rule ids and `rules.json` go with the gates child. The family CRs and the swap merge as one unit | children 19 to 24, 26 |
| F3 | The trial is a smoke test: 5 tries in compound form, with the permission mode recorded. The proof is the refusal rate measured afterwards. The cards keep the refused-push route for good. A refusal in the trial is recorded and tried once alone before the program stops | child 1; child 5 measures the rate; child 22 keeps the route |
| F4 | A new judge in the kit (a named model). The Griller's proved headless flags. A spend cap printed first. "Inferable" rows grouped. Pass rule: no case scores 0 of 3 that the old cards passed | child 6; children 25 and 28 use it |
| F5 | A rule that protects the user or the repository lives only in the floor, the role's card or a CLI or hook refusal. Never in a topic alone, never "inferable". The cap on nevers gives way before such a rule | "The floor"; children 19 to 25 |
| F6 | Child 28 is a sandbox campaign, run by the user or on the user's word, with the plugin loaded from the stack's top worktree. Roles not seen are "no run", not failed. The card children are handed back validated, with the gap "real run not done" | child 28; children 19 to 27 Known gaps |
| F7 | One child before the brief child rewrites the four AGENTS.md sentences: roles are data the CLI reads; the CLI advises with `next`, refuses with rails, and never decides a merge or a take-back; `judge` only words the ask | child 9 |
| F8 | `msg steering` only. With no watcher subscribed it prints "not delivered: no watcher subscribed" and exits non-zero. No `user` or `cr:` targets | child 13 |
| F9 | Child 18 keeps `roles.yaml`, the lint and the wrapper check as a `just` target. Project roles become a later CR with their own grill | child 18; out of scope |
| F10 | Briefs are written in the git folder (`chantier/briefs/…`) and never published | child 10 |
| F11 | The children from the first card CR to the real run merge in one sitting, in order, with no session started in between. Each carries a typed merge wait on the last child | the merge rule; children 19 to 27 |
| F12 | `take` never clears a recorded Driver by itself. Of S10, only `--epoch` in any position is kept | child 2 |
| F13 | The CI step stays a reminder. Its proof uses a throwaway PR. The Inspector checks that the approval line quotes the user's words from `02-answers.md` | child 27 |
| F14 | M9 is split out of the near-misses child. `next` is split from `status --since` and its `state:` line. Conflicts and the retro draft are split | children 3, 11, 12, 15, 16 |
| F15 | A Pending items section | `## Pending items` |
| F16 | Child 1's base is the batch's stack top when it joins | `## Rules for every child`; child 1 |
| F17 | Unproved claims are marked | children 1, 4, 15 |
| F18 | The CLI lines that name removed cards are switched, with a test | child 24 |
| F19 | The floor reaches the three roles with no wrapper | children 10 and 24 |
| F20 | Each child states the seconds it adds to `just test` | `## Rules for every child` |
| F21 | `chantier push` is the one way a Driver publishes its branch. It is never run as a retry after a refused `git push` | child 1 |
| Q1 | No hook deny list in this program; filed separately | out of scope |
| Q2 | Five tries as a smoke test | child 1 |
| Q3 | Wrappers stay hand-written; `roles build` is a check | child 18 |
| Q4 | The gates child freezes what the rewrite reaches. A card above its target is listed in Known gaps | children 19 to 23, 26 |
| Q5 | The owner's question, handled as F6 | child 28 |
| Q6 | The steering session keeps the plain `git push --force-with-lease` | child 1 (must not), child 22 |
| Q7 | No new forge read; the forge's own refusal is printed verbatim | child 1 |
| Q8 | Nothing merges while the owner sleeps. Each child is presented as ready | the merge rule |

### The floor (answer 15, judged here; F5)

Judged against the owner's principle, the floor is one file, `references/floor.md`, of at most
1,200 LF bytes. It holds the ten rules listed in study-fable-v2 section 5, one line each:
1. Never merge without the user's word.
2. Rebase only, with `--force-with-lease`, and only on the CR's own branch.
3. No fallback.
4. A CLI that cannot run is a stop.
5. Never discard the worktree's work.
6. An irreversible release action waits for the user.
7. Only the user starts work.
8. No image shows the username or the home folder.
9. Report a refusal with its exact text; never work around it.
10. Never stop a process by name or pattern; use `close --yes` only on the user's yes.

Why one floor:
- These rules protect the user and must be known before a role types anything.
- Today each one sits in five to seven places. Two of them, rules 5 and 8, sit in pieces that are
  read only on a condition since CR-471.
- One file keeps each rule in one place.
- `brief` (child 10) puts the floor in every prompt, so it is loaded at boot, and no card
  restates it.

Each card holds the nevers of its own role, five as a target. Following F5, the cap gives way
before a rule that protects the user or the repository. Such a rule never goes to a topic alone
and is never judged inferable.

Three rules sit close behind the floor. Each goes where it applies:
- The Foreman's chat obeys only "stop" and "hold": the Foreman's card.
- Nothing is posted on a tracker issue without the user's approval: the Chief of Staff's card.
- An untested host path is said to be untested: the sentence in the host rows (child 8).

## What changes, by area

- **CLI** (`src/`):
  - New commands: `push`, `help`, `host`, `brief`, `next`, `msg`, `inbox`, `judge`,
    `conflicts`, `retro draft`.
  - Near-miss arguments are accepted.
  - Refusals name the next command or topic.
  - New `status --since`.
  - `take`, `round` and `handoff` print a pointer to `brief` instead of every worker's opening
    lines. This switch happens in the swap child only.
- **Hook** (`hooks/register.tsx`):
  - The write guard lets scratch writes through.
  - The reload message after a compaction names the floor (swap child).
- **Cards** (`references/`, the four `SKILL.md`, the 30 wrapper bodies):
  - One total rewrite, written beside the old set and swapped in one unit.
  - Removed: the startup manifest, the four core files and the 32 pieces.
  - Added: help topics in `references/topics/`, host data files and the floor.
- **Docs**:
  - New `docs/proofs/claude-code.md` and `docs/proofs/copilot.md`: trial history.
  - New `docs/proofs/cards-inventory.md`: the review's inventory.
  - New `docs/incidents.md`: the stories behind removed patches.
  - Links to removed cards are fixed.
- **Eval kit** (`evals/kit/`): `behaviour.py` (`just behaviour`), `quiz.py` (`just quiz`), and a
  judge for quiz replies.
- **Data and checks**: `skills/chantier/roles.yaml`, with a `just roles` check of the wrappers.
- **Tests and CI**:
  - Budgets and lints become pytest gates.
  - One reminder step in `ci.yml` for the user's approval line.
  - Phrase tests are converted to rule ids.
- **AGENTS.md**:
  - The push subcommand's git and network exception (child 1).
  - The four role sentences (child 9).
  - One line per new tool, with its measure or answer.
  - The journal's new `msg@1` writer.
  - The `conflicts` read's object writes.
  - The release claims' behaviour measure.

## Out of scope

- Adding, removing or merging roles, or changing what a role is responsible for (answer 1).
- The surface server's protocol and the board's pages, except the `msg@1` journal type and its
  delivery on the `events` topic (child 13).
- Deleting the never-read help topics one release after this program (answer 10). That is a later
  CR, listed from M12's candidates.
- A hook deny list of never-commands for the guarded agents (answer 22, Q1). The Chief of Staff
  files it as a separate inbox item.
- Loading a project's own roles: the `chantier.yaml` key, who starts them, their host files
  (answer 22, F9). A later CR with its own grill. This program keeps the role kinds in its data
  only.
- Generated wrappers: the wrappers stay hand-written (answer 22, Q3).
- A lease-free `chantier push` for the steering session, which keeps the plain push (Q6).
- A forge read of branch protection (Q7).
- The S-list items not named in children 2 and 4, such as S4 (waits blocked by the host), S7 (a
  role's tool list), S8, S11 and S13. They go through M10 (filed or accepted), not through this
  program.
- A rebase subcommand: study-classifier counted 1 refusal in 721 rebases.
- Writing the host's auto-mode configuration, or asking the user to leave auto mode.
- The hook recording an agent's id at spawn instead of `agents set`.
- `take` clearing a recorded Driver by itself (F12).
- `reply-check`.
- Copilot runs. Copilot has no hook, and no run was seen. Its roles boot through `brief`, and
  its host rows say "untested".

## Order

Four steps, as answer 18 sets them. Answer 20 allows a step to be cut into chained CRs.

1. **Tools first** (children 1 to 18). Each tools child only adds things: commands, flags, lines,
   files and data. It removes no output the current cards rely on, and it changes no text in an
   existing card. Every intermediate `main` keeps working with the old cards. The push subcommand
   comes first, and its smoke trial in auto mode runs before any card is cut (answers 7 and 22).
2. **The total rewrite** (children 19 to 24):
   - Five family CRs write the whole new card set in a folder nothing loads.
   - One swap CR switches the CLI and the hook to the new set, removes the old set and converts
     the tests.
   - This is one target state, reached in one pass of chained CRs. No family runs on new cards
     before the others (answers 14, 17, F2).
3. **The read-and-compare review** (child 25).
4. **The gates and the measure** (children 26 to 28): the pytest and process gates of answer 9,
   then the sandbox campaign on the new cards (F6).

**The merge rule (answers 14 and 22: F2, F11, Q8):**
- Nothing merges while the owner sleeps. Each child is presented as ready, and the owner merges.
- Children 1 to 18 keep the old cards working. Each may merge, in order, once the owner says so.
- Children 19 to 28 (the family CRs, the swap, the review, the gates and the real run) merge as
  one unit:
  - in one sitting, in order;
  - with no chantier session started in between, since the plugin is read live from the main
    checkout;
  - and only after child 28's campaign has passed on the stack's top worktree.
- Each of children 19 to 27 records a typed merge wait on child 28:
  `$CHANTIER wait <cr> merge <child 28's PR>`, so the `handed back:` line prints
  `do not merge: waits for …`.
- Each of children 19 to 27 is handed back validated, with the Known gap "real run not done (child
  28)" until child 28's results are in.

How study-fable-v2 section 6 is regrouped (answer 18):

| Study child | Here |
| --- | --- |
| 1. Measure the new cards for real | child 5 (the tool), child 28 (the run) |
| 2. The carrier for the pieces | child 7 |
| 3. The host card out of the start | child 8 (data, proofs), child 10 (host rows in `brief`), child 23 (cards) |
| 4. Quick cuts | child 17 (launcher), child 11 (`status --since`), child 24 (`handoff` without the worker lines; `driver:refused` without the Foreman's piece) |
| 5. The tools | children 10 to 16 |
| 6. Refusals | children 2, 3, 4 |
| 7. The rewrite, by family | children 19 to 24. Families are written separately but swapped as one (answer 17 replaces the `cards:` key) |
| 8. Roles as data | child 18 (narrowed by F9) |
| 9. Removal | child 24 |

## Rules for every child

- **Base.** In a stack batch, each child's base is the previous child's branch. Child 1's base is
  batch-31's stack top when it joins: CR-485's branch, unless CR-485 has merged (F16).
- **Before the first push.** Run `just check`. A change under `src/` or `evals/kit/` also runs
  `just eval-dry-run` (AGENTS.md).
- **Long gate.**
  - A child that changes the CLI, the cards or the scenario passes `just scenario
    (ubuntu-latest)`, green at its PR's head.
  - In this stack only the CR on top owes the local Windows run, `chantier gate <cr> scenario`.
    When a child joins on top, that run moves to it.
  - A child that changes only `evals/` or `docs/` owes no long gate.
- **Hook changes.** A child that changes `hooks/` runs `just mod` itself before its PR. One that
  cannot stops and says so.
- **New commands.** A new command adds a step to `scenario/run_scenario.py` and its coverage
  bullet (`tests/test_scenario_coverage.py`).
- **`just test` time (F20).** Each child states in its PR, under Deliverables, the seconds its
  tests add to `just test`, measured before and after on the same machine. The ceiling is still
  open (`2-backlog/P2/test-ceiling-decision`).
- **Journal types.** A new journal type regenerates `hub/schemas.json` with `just journal-schemas`.
- **AGENTS.md lines.** Each new CLI tool adds its line to AGENTS.md's named exceptions, with its
  source: the measure (figures from study-behaviour or study-classifier) or the user's answer
  (simplify-cards-Q…). AGENTS.md does the same today for `wait`, `access` and `live`.
- **Card text.** No child before 19 edits an existing card's text. Children 19 to 23 write only
  the new, unloaded set.
- **Versions.** No child edits a version by hand.
- **Text style.** Repository text is in English. No date, batch name or trial story goes in a
  card (M3, enforced from child 26).
- **Unproved claims.** A claim about the host, a tool version or the classifier that this program
  has not proved is marked "unproved" in the child's specification and in its PR (F17).

## Pending items (F15)

These inbox and backlog items edit the same files as the program. Each line says which child
absorbs the item, or when it is re-read.

| Item | Overlap | Handling |
| --- | --- | --- |
| `1-inbox/driver-checkpoint-and-a-ready-restart-br` | "`take` prints a ready brief file" for a replacement Driver | Child 10 absorbs the brief file; child 24 makes `take` print it. The Driver's checkpoint and the lease reclaim are re-read after the swap |
| `1-inbox/pr-conflict-detect-and-rebase-order` | A server-side conflict scan after a merge, beside the early `conflicts` check | Child 15 names the item and stays read-only and Foreman-run. Batch-31's CR-484 split it out; the two do not share code. Re-read after CR-484 and child 15 |
| `1-inbox/foreman-idle-wakes` | Set aside by the owner "until a structural study". It concerns the Foreman's wakes, which children 11 to 13 cut | Re-read after child 28's measure, which repeats the wake-share measure the item asks for |
| `2-backlog/P3/evals-rework` | Renames `evals/results/` reports date-time first, in UTC | Children 5, 6 and 28 name their result files by the convention of `evals/results/` at their base. If evals-rework has merged, they use its date-first form |
| `1-inbox/driver-context-second-cut` | Cuts the Driver's specification, worker prompts, `pr-template.md`, the manifest and what `take` and `handoff` print | Absorbed by children 10, 20 and 24 for the prompts, the manifest and `take`/`handoff`. The specification and `pr-template.md` are re-read after the swap |
| `1-inbox/driver-card-leads-left-by-role-cards-sti` | Three leads in `driver.md`: the typed `pipeline` wait for a long run on main, reading a guideline by section, waiting only in a background shell | Child 20 carries the three leads into the Drivers' cards or topics, and child 25 checks them |
| `1-inbox/session-start-split-fix-citation-re-read` | Citations and the re-read moment in the session-start cards and `hosts/copilot.md` | Superseded by children 22 and 23, which rewrite those files. Re-read after the swap, and closed if nothing is left |
| `1-inbox/release-drafts-are-a-worker-s-job-not-th` | Moves the release drafts from the Release driver to a worker | Re-read after the swap. Child 20 writes the Release driver's card as it stands; the item then changes that card |
| `2-backlog/P2/test-ceiling-decision` | The `just test` ceiling | Each child reports its added seconds (F20) |

## Cost

The batch budget is $400 (answer 21). When the critic read the batch, it held $139.25 spent. Its
CRs cost $1 to $20 each. Children 6, 25 and 28 also spend on models outside the batch's `cost`:
the quiz and the campaign. Each prints its spend cap first (F4). The Chief of Staff watches the
batch's spend against the 28 children, and a budget order is the owner's.

## Children

### Child 1: `push-own-cr-branch` — Push a CR's own branch through the CLI

- **Scope.**
  - New command `chantier push <cr> [--lease N]`. It is declared in `src/declare/delivery.py`,
    with its handler `push` in a new `src/commands/push.py`.
  - The help text says plainly why the command exists: to declare that the operation is
    legitimate, as chantier's own update of the CR's own branch after a rebase, with the lease
    held.
  - Rails, checked before any git write. Each refusal says what to do.
    - The branch is the CR's recorded one (`CrEntry.branch`), matches `chantier/*` and is not
      the default branch (`repo.config["default_branch"]`).
    - The caller holds the lease, checked through `leases.require` then `leases.claim`
      (`src/core/leases.py`). Three leases count: the CR's own; the stack's (unit `"stack"`),
      for a CR in a stack batch's chain; and an order's, for a QA order's unit.
    - The worktree, `cr_worktree(c)`, is clean: `git status --porcelain
      --untracked-files=normal` is empty. Its HEAD is on that branch.
  - The push runs from the worktree:
    `git push --force-with-lease=<branch>:<expected> <remote> HEAD:refs/heads/<branch>`.
    - `<remote>` comes from `repo.config["remote"]`.
    - `<expected>` is the worktree's ref `refs/remotes/<remote>/<branch>`. When that ref is
      absent, the expectation is empty, so the push creates the branch only if the remote has
      none.
    - Never plain `--force`, never `--no-verify`.
  - When git refuses (a stale lease, a protected branch, a hook):
    - git's text is printed verbatim and the command exits with the external-failure code;
    - nothing is retried;
    - there is no forge read of branch protection (Q7).
  - The command records a `push` event inside `RenderedBatch`:
    `b.log("push", cr, branch=…, head=…, expected=…)`. This renews the lease, as other Driver
    commands do.
  - The same command serves GitHub and GitLab. It is git only, with no forge call.
  - Never through a profile or the server:
    - `src/core/remote_wire.py`: `push` joins `NEVER_REMOTE`.
    - `src/clients/remote.py` refuses it through a profile with a line like `GATE` ("push runs
      on the machine that holds the worktree…").
    - `src/board/cli_run.py`'s `judge` refuses it in `cli.run`.
  - `src/driver_prompt.py`, `_rewrites_line`: the push half names `$CHANTIER push <cr> --lease
    <n>`, one per CR branch in a stack. The rebase half is unchanged.
  - `src/commands/delivery.py`, `_off_worktree`: the "not pushed" line names `chantier push`.
  - `src/commands/allow_samples.py`: P10 keeps its force-push samples, because the steering
    session keeps the plain push (Q6), and adds none for `push`. Whether the user's
    `chantier *` allow rules match what agents type is unproved: study-classifier found they
    seldom match compound forms.
  - AGENTS.md changes:
    - The CLI's named git exceptions gain `push`: one `git push --force-with-lease` of a CR's
      recorded `chantier/*` branch, from its worktree, never forced, never `--no-verify`.
    - The network list gains this push.
    - `push` joins `gate` among the commands that never run through a profile.
    - The named-exceptions paragraph gives its source. First, the user's answers
      simplify-cards-Q5 (2026-11-24) and Q22. Second, study-classifier's measure: 13 classifier
      refusals of force pushes in 12 days, each one a lost Driver, and 4 questions to the user;
      83 % of the pushes were typed as compound commands that no allow rule matches.
    - The paragraph says the command states the operation's legitimacy.
    - It also says (F21) that `chantier push` is the one way a Driver publishes its branch. It
      is never run as a retry after a refused `git push`, and a refused `chantier push` is not
      followed by a raw push from the Driver. The refused-push route of answer 8 stays.
- **Depends on:** batch-31's stack top (CR-485's branch unless merged).
- **Acceptance evidence.**
  - Pytest, in a new `tests/test_push.py`: parametrized, in-process, on a prepared state with a
    bare remote.
    - Each refusal exits non-zero and runs no `git push`: branch not recorded, not `chantier/*`,
      the default branch, no lease, a stale lease, a dirty worktree, HEAD on another branch.
    - A valid call pushes, records the event and renews the lease.
    - When the remote has moved since the tracking ref, git refuses, and the command exits
      external with git's text.
    - `push` is refused through a profile and through `cli.run`.
  - A scenario step in `scenario/run_scenario.py`: a Driver rebases, then runs `push`, then
    `ship` prints no "not pushed" line. Run on GitHub and on the GitLab unit.
  - **The smoke trial in auto mode (answers 7 and 22, F3; Q2).**
    - The child's own Driver, a subagent, pushes its own CR branch five times with the
      worktree's build, in the compound form agents type. Example: `C="uv run --no-sync
      --project <worktree> chantier --project <planning>"; $C push <cr> --lease <n> 2>&1 | tail
      -3`, after a small commit or rebase each time.
    - For each try, the PR's Deliverables record the exact command text, the session's
      permission mode as the host shows it, and the host's verdict: ran, or the refusal's text.
    - The user's allow rules name the main checkout's path, so the worktree build's command is
      always judged by the classifier. That makes it the harder case, and the record says so.
    - On a refusal: record it, then try once more, alone, as a plain command. If that also
      fails, the Driver hands back blocked with the text, and the program stops for the owner.
      It is not worked around.
    - The trial is a smoke test, not the proof. The proof is the `chantier push` refusal rate,
      measured afterwards by child 5's tool on later runs.
- **Must not.**
  - Push any branch but the CR's recorded one.
  - Read or write the forge.
  - Push through a profile.
  - Add `--force` or `--no-verify`.
  - Change a card's text.
  - Run a rebase.
  - Give the steering session a lease-free form (Q6).
- **Risk.**
  - The long gate is owed (CLI and scenario).
  - AGENTS.md changes: a third git exception, a network use and the F21 sentence. Answer 7
    gives the owner's word for this subcommand, and the PR quotes it.
  - The classifier's verdict on the command text is unproved until the trial, and is only
    measured afterwards.

### Child 2: `cli-near-misses` — Accept the CLI's near-miss argument forms

- **Scope.** Answer 3 applies: each form below shows in more than 2 % of a role's runs
  (study-behaviour 3.2).
  - **S1.** `--lease N` is accepted on every command a Driver runs against a CR or unit:
    `handoff`, `verdict`, `rules`, `log`, `wait` and `lease`. It is added through `add_lease` in
    `src/commands/registry.py`.
    - A valid lease renews.
    - A command with no use for the lease ignores it.
    - A stale lease still exits `claim lost`.
  - **S2.** `phase <cr> "gate preflight"`: a first argument holding a space is split on its first
    space (`src/declare/driver.py`, `phase`).
  - **S3.** When a Driver runs `take`, the refusal adds "`handoff <cr>` prints the take's facts".
  - **S6.** These path forms resolve to the CR folder:
    - a CR folder path that repeats the planning prefix
      (`projects/chantier/changes/projects/chantier/changes/…`);
    - a path relative to a shell already inside a CR folder.

    The CR's short name is also accepted wherever a CR folder is expected (`summary`, `triage`,
    `file`).
  - **S9.** `summary lint` prints the title and summary limits. Its gap line prints the exact
    `summary set` form (study-behaviour S8).
  - **S10.** `--epoch` is accepted in any position. Following F12, `take` does not clear a
    recorded Driver by itself: the refusal "`agents set CR-N -` first" stays as it is.
  - Every accepted near-miss form is listed in that command's `--help`.
- **Depends on:** child 1.
- **Acceptance evidence.** Pytest, parametrized, one case per near-miss form: the form is
  accepted and has the same effect as the canonical form. The added `just test` seconds are
  stated.
- **Must not.**
  - Change what a valid canonical command does.
  - Accept a form that changes the meaning (a stale lease stays refused).
  - Weaken the one-Driver-per-CR rail (`src/rails.py:256-260`).
  - Touch a card.
- **Risk.** The long gate is owed. No AGENTS.md change. A form accepted wrongly could hide a real
  mistake, which is why each one is listed in `--help`.

### Child 3: `refusals-name-next-step` — Every CLI refusal names the next command (M9)

- **Scope** (answer 9, M9):
  - Every refusal raised from `src/rails.py`, `src/rails_release.py`, `src/rails_idle.py` and
    `src/core/leases.py` contains a backticked next command.
  - Exception: final refusals that only say "stop now". They are kept in an allow-list in the
    test, each with its reason.
  - Refusal texts that lack a next command are completed. Their meaning is not changed.
- **Depends on:** child 2.
- **Acceptance evidence.**
  - `tests/test_rail_refusals.py` is extended to assert the backticked next step for each
    refusal.
  - The allow-list is counted and printed.
  - The added `just test` seconds are stated.
- **Must not.**
  - Change a refusal's condition or exit code.
  - Turn a refusal into advice.
  - Touch a card.
- **Risk.** The long gate is owed, since the scenario reads some refusal texts. No AGENTS.md
  change.

### Child 4: `hook-scratch-writes` — Let the write guard pass scratch writes

- **Scope.** Answer 3 applies. Study-behaviour S5 counted 577 write-guard refusals, 490 of them
  scratch writes that the host's own prompt recommends.
  - In `hooks/register.tsx`, `writtenBy` and `judgeShell`: a redirection or write to `/dev/null`
    is never judged a write. Neither is `NUL` or `$null` in a Windows shell.
  - A write inside the agent's scratch folder passes. The child's own specification chooses
    which scratch folder, by reading the hook API the host ships, not the Driver (F17). Two
    variants:
    - a. The host gives the hook the session scratchpad's path. This is unproved: the host's
      hook types are not in the repository.
    - b. Otherwise, the guard treats as written the `scratch:` folder that the prompt names.
      `take` already prints `scratch: <cr>/work/scratch` (`src/commands/facts.py`). In this
      variant, `src/driver_prompt.py` and the worker lines in `src/plugin_files.py` add that
      `scratch:` line to the prompt the hook reads, as an addition.
  - Cases for both are added in `hooks/register.test.tsx`.
- **Depends on:** child 3.
- **Acceptance evidence.**
  - `hooks/register.test.tsx` cases: scratch writes pass, and writes outside them are still
    refused.
  - `just mod` passes, run by the Driver.
  - The added `just test` seconds are stated.
- **Must not.**
  - Add a deny list of commands (Q1, out of scope).
  - Guard the main session.
  - Judge inside an interpreter's inline code.
  - Refuse a call it cannot cut: it passes with a note, as today.
  - Change anything on Copilot, which has no hook.
- **Risk.**
  - `just mod` is owed (a change to `hooks/`).
  - The long gate is owed if variant b changes the CLI.
  - A false refusal blocks a worker.

### Child 5: `behaviour-measure` — Measure what roles read and do, from transcripts

- **Scope** (answer 9: M7, M8's runner, M10's list, M14's list; answer 10's read count):
  - New `evals/kit/behaviour.py` and a `justfile` target `just behaviour [--since <date>]
    [--prune]`.
  - Input: the user's local Claude Code transcripts in `~/.claude/projects`, main sessions and
    `subagents/`. The role is read as follows:
    - from `meta.json` `agentType`;
    - else from the prompt's first line: a Foreman from `chantier Foreman n°`, a Chief of Staff
      or Griller from its skill.
  - Output: a JSON and a Markdown results file in `evals/results/`, named by the folder's
    convention at the base (see Pending items, evals-rework). Per role, they hold:
    - runs, tool calls and model calls;
    - card bytes read: Read results and shell reads naming a card path, each result counted
      once;
    - files read;
    - CLI usage errors and refusals, by message;
    - `--help` reads by command, and `help <topic>` reads by topic;
    - host denials and write-guard refusals;
    - waits;
    - Driver runs per CR;
    - the Foreman's and the Chief of Staff's wake shares;
    - `chantier push` refusals (the proof of child 1);
    - "tool not in the role's list" (M14);
    - the S-list: each usage error or refusal message above 2 % of a role's runs (M10).
  - Detectors (M8): regexes on tool calls, read from `evals/kit/detectors.json`. Child 26 later
    moves them into `references/rules.json`. Each detector has a positive and a negative
    example. The measure prints each detector's rate and a "regressions" list: a detector more
    than 5 points worse than in the previous file, or a new S-list line.
  - The baseline, on the old cards: the results for 0.15.1, from the transcripts since
    2026-11-17.
  - The studies' throwaway scripts are not copied. The tool is written anew and run with
    `python -I`.
- **Depends on:** child 4.
- **Acceptance evidence.**
  - A fixture of a few redacted transcript lines under `evals/kit/fixture/`, with its expected
    figures, checked by `just eval-dry-run`.
  - The baseline files are committed.
  - Each detector matches its positive example and not its negative one.
- **Must not.**
  - Run in CI: the transcripts are local.
  - Send transcript text anywhere.
  - Commit a transcript, a username or a home path. The results hold counts and message
    templates only.
- **Risk.**
  - `just eval-dry-run` is owed.
  - The `justfile` target sits outside the eval kit, so the long gate is owed.
  - No AGENTS.md change.

### Child 6: `situation-quiz` — A cheap quiz of a role's boot on one situation

- **Scope** (answer 14's quiz; answer 22, F4):
  - New `evals/kit/quiz.py` and `just quiz <role> [--cards <git ref or folder>] [--case <id>]`.
    For one case, the quiz:
    1. builds the role's boot text from the cards given;
    2. adds one situation and asks "what do you do next";
    3. runs it three times on the role's model as the shipped playbook gives it
       (`config/chantier.defaults.yml`);
    4. has a judge read each reply against the case's expected behaviour;
    5. prints the pass counts per case and per role.
  - **The runner** uses the headless host CLI with the board Griller's proved flags
    (`src/board/griller_host.py`: `--setting-sources ""`, `--plugin-dir`,
    `--strict-mcp-config`). The user's settings, hooks and MCP servers therefore stay out.
  - **The judge** is new, `evals/kit/quiz_judge.py`. The existing `evals/kit/judge.py` runs
    hidden pytest files and reads no reply. The new judge:
    - uses one named model, not the role's own, set as a constant in the file;
    - reads the reply and the expected behaviour;
    - answers pass or fail with one line of reason.
  - **The spend cap.** Before any model call, the quiz prints the planned number of runs and the
    estimated spend, and stops if the estimate exceeds `--max-usd` (default 10). The batch's
    `cost` does not see this spend.
  - **Cases** live in `evals/quiz/<role>/<id>.json`. Each holds: id, role, situation, expected
    behaviour, and the rule it proves. The rule is the floor rule's number for now; an `R-nnn`
    id from child 26.
    - Seed: one case per floor rule for the roles it binds, plus one per rail of
      `evals/SCORECARD.md` of kind judgement that names a role.
    - Rows judged "inferable" in child 25 are grouped, several per case.
  - **Pass rule (F4).** A new card set passes when no case scores 0 of 3 that the old cards
    passed.
  - **Boot text by stage:**
    - Before child 24: for the old cards, the role's declared start reading (the files
      `tests/test_start_reading.py` resolves). For a folder of new cards, the output of
      `chantier brief <role> --cards <folder>` (child 10).
    - After child 24: `chantier brief <role>`.
  - **The baseline:** the quiz on the old cards at the stack's base. The result file is named by
    the convention of `evals/results/`.
- **Depends on:** child 5.
- **Acceptance evidence.**
  - `just eval-dry-run` runs the quiz's plumbing with no model: a staged reply and a staged
    verdict.
  - The spend cap's refusal is tested.
  - The baseline file is committed with its pass counts and its spend.
- **Must not.**
  - Run in CI.
  - Spend on a model in `just check`.
  - Judge with the role's own model.
  - Load the user's settings, hooks or MCP servers.
- **Risk.**
  - The long gate is owed only if a change falls outside `evals/`; the `justfile` target is
    outside it.
  - `just eval-dry-run` is owed.
  - Model cost falls on the user's machine, capped and printed.
  - Whether a Driver subagent may start a headless host CLI in auto mode is unproved. A refusal
    is not worked around: the Driver hands back with the plumbing and the cases, and the
    baseline is run by the Chief of Staff.

### Child 7: `help-topics` — `chantier help <topic>` carries the rare cases

- **Scope** (answer 18's `help <topic>`; answer 10; study-fable-v2 child 2):
  - New `references/topics.json` maps each topic name to:
    - its readings: a file, or `file#heading`, in the reading form the manifest uses today;
    - the roles it serves;
    - its trigger: the refusal, line or moment that names it;
    - `review_by`: a version, for answer 10's rare topics.
  - In this child, each action of `references/startup-manifest.json` that is a piece or a
    rare-case section becomes a topic pointing at today's file. Examples: `lease`,
    `refused-push`, `retake`, `conflicts`, `lost-driver`, `hold`, `release`, `stack-restack`,
    `pr-extras`.
  - New command `chantier help [<topic>] [--for <role>]`, declared in a new
    `src/declare/help.py`:
    - with a topic, it prints the topic's readings whole, in full output like `rules`;
    - with `--for`, it lists that role's topics, one line each with the trigger;
    - with no argument, it lists all topics.

    It reads only the plugin's files and works with no batch.
  - The CLI names topics where one exists, by adding `help <topic>` to:
    - the lease refusals of `src/core/leases.py`;
    - the push refusals of child 1;
    - the `restack owed:` line (`src/commands/orders_merged.py`, `restack_line`);
    - the `handed back:` line (`src/status/ready_line.py`);
    - the watcher's end lines (`src/hub/watch_lines.py`).
- **Depends on:** child 6.
- **Acceptance evidence.**
  - Pytest checks that:
    - every topic's readings resolve on both hosts' cards;
    - every `help <topic>` that a CLI line prints names a topic that exists (a scan of the source
      strings);
    - `help --for <role>` lists only that role's topics.
  - A scenario step runs `help lease`.
  - The added `just test` seconds are stated.
- **Must not.**
  - Remove the manifest or a piece.
  - Change a card's text.
  - Read the network.
- **Risk.** The long gate is owed. AGENTS.md gains a line for `help` (source:
  simplify-cards-Q18).

### Child 8: `host-rows-and-proofs` — Host capabilities as data; trial history to a proof file

- **Scope** (answer 16; study-fable-v2 child 3):
  - New `references/hosts/claude-code.json` and `references/hosts/copilot.json`, one row per
    capability. The rows come from:
    - today's "Tools" tables (`hosts/claude-code.md#Tools`, `hosts/copilot.md#Tools`);
    - the other sections a role acts on: the heartbeat; a Driver messaging its steering session;
      starting a child; ending; compacting; reloading; the write guard.

    Each row holds: the capability; the means, two to four lines, for this host only; and a mark
    of one word, `proved` or `untested`.
  - New command `chantier host [<capability>]`:
    - It reads the host from the batch's record, else the session's host as the CLI resolves it
      today.
    - It prints the matching rows.
    - A row whose mark is not `proved` ends with one sentence, the same everywhere: this path was
      never tried for real here.
  - New `docs/proofs/claude-code.md` and `docs/proofs/copilot.md`. Every trial, date, batch,
    model and "proved/unproved" story from the two host cards is copied there, grouped by
    capability.
  - The host cards keep their text until the swap.
- **Depends on:** child 7.
- **Acceptance evidence.**
  - Pytest checks that:
    - every row has a means and a mark that is one of the two words;
    - every `untested` row prints the sentence;
    - every capability appears as a heading in the proof file;
    - `host` with an unknown capability lists the known ones.
  - The added `just test` seconds are stated.
- **Must not.**
  - Edit the host cards.
  - Claim a mark the cards do not hold. A row is `proved` only where the card says proved for
    the shipped default model; any doubt is `untested`.
- **Risk.** The long gate is owed (CLI). AGENTS.md gains a line for `host` (simplify-cards-Q13).

### Child 9: `agents-md-role-rules` — AGENTS.md: roles are data, the CLI advises and refuses

- **Scope** (answer 22, F7; answer 11). This child rewrites the four AGENTS.md sentences that the
  new tools would contradict:
  - "A role's contract lives in `skills/chantier/references/` (the cards), never in an agent file
    or in the CLI: the parent that starts an agent names the card in its prompt." Becomes: a
    role's contract lives in the cards. The CLI reads the roles as data (the card, the wrapper,
    the first line, the kind) and prints a role's brief whole. The parent starts an agent with
    the short prompt `brief` prints, which names the brief file holding the card.
  - "A card says what the role judges; the CLI (`rails.py`) says what it refuses." Becomes: a
    card says what the role judges. The CLI refuses with its rails and advises with `next` and
    its `next:` lines. It never decides a merge or a take-back.
  - "The CLI knows no role; two named exceptions…" Becomes: the CLI knows roles only as data
    (`skills/chantier/roles.yaml`, read by `brief`, `help --for`, `msg steering`). It keeps the
    two named exceptions already listed.
  - Answer 11: `judge` only words the ask. The steering session decides, and the user's yes
    merges.
  - `tests/` tests that read these AGENTS.md sentences are updated, if any. Find them with
    `git grep "knows no role" tests/`.
- **Depends on:** child 8.
- **Acceptance evidence.**
  - The PR quotes answers 11 and 22 (F7) as the owner's word, to be confirmed at wake.
  - `just check` passes.
- **Must not.**
  - Change any other AGENTS.md rule.
  - Add a tool.
  - Edit a card.
- **Risk.** No long gate (docs only: AGENTS.md). The rewording binds every later child. Children
  10 to 14 cite these sentences.

### Child 10: `brief-prompts` — `chantier brief` writes a role's whole prompt

- **Scope** (study-fable design line 3; the floor as judged above; answer 22: F1, F10, F19):
  - New `references/floor.md`, at most 1,200 LF bytes: the ten rules of "The floor", one line
    each.
  - New command `chantier brief <role> [<cr>] [--lease N] [--epoch N] [--cards <folder>]`. It is
    declared in `src/declare/brief.py`, with its handler in `src/commands/brief.py`.
  - The role's card, wrapper, first line and `writes:` value are read as data: from what
    `src/plugin_files.py` and the Driver's prompt table already read, in the form child 18 later
    puts in `roles.yaml`.
  - **Which roles.** All 18: the 15 with a wrapper, and the three that boot with no parent to run
    `brief`: the Chief of Staff, the Griller and the Foreman (F19).
  - **The brief file.** `brief` writes the prompt to the repository's git folder, at
    `chantier/briefs/<batch or "none">/<cr or "none">-<role>.md`, never published (F10). For a
    given role, version and CR facts, the file is byte-stable. It holds, in order:
    1. the role's card, whole;
    2. the floor;
    3. the facts: CLI, worktree, folder, specification, PR, rounds, notes, lease, `writes:`,
       `Rewrites:` for a Driver, `Team:`;
    4. the host rows the role uses (child 8);
    5. the line "`$CHANTIER next` says what is due; `$CHANTIER help <topic>` when a line names
       one".
  - **The short prompt** (F1). `brief` prints the prompt to pass:
    1. the role's first line, unchanged, since the wrappers check it;
    2. the `writes:` and `worktree:` lines, exactly as `driver_prompt_lines` and
       `worker_prompt_lines` print them today, because the hook reads them from the spawn prompt
       (`hooks/register.tsx`, `writesOf`, `worktreeOf`);
    3. "Read <the brief file> whole, first."
  - `--cards <folder>` builds the brief from another folder of cards. Children 19 to 23 use it to
    check their unloaded set, and child 6's quiz uses it too.
  - The facts' source for `brief` is `src/driver_prompt.py`'s `driver_prompt_lines`, plus
    `worker_prompt_lines` and `chief_prompt_lines` from `src/plugin_files.py`. Their current
    outputs in `take`, `round`, `handoff` and `order qa` stay unchanged in this child. Child 24
    switches them.
- **Depends on:** child 9.
- **Acceptance evidence.**
  - Pytest, for each of the 18 roles and both hosts:
    - the file starts with the card and holds the floor once;
    - two runs give the same bytes;
    - the printed first line equals the wrapper's `Prompt starts with:`;
    - the short prompt carries `writes:` and `worktree:`, and the hook's `writesOf` on it returns
      the same list as on `take`'s skeleton. A case in `hooks/register.test.tsx` feeds it the
      short prompt; the hook itself is not changed.
    - a Driver's brief carries the same facts as `take`'s skeleton;
    - nothing is written under the planning folder.
  - A scenario step starts a Driver from `brief cr-driver <cr>`.
  - The added `just test` seconds are stated.
- **Must not.**
  - Change the output of `take`, `round` or `handoff`.
  - Edit an existing card.
  - Write a brief in the planning folder.
  - Change the hook's logic.
- **Risk.**
  - The long gate is owed. `just mod` is owed if the hook test file changes.
  - AGENTS.md: the CLI's write list gains `chantier/briefs/` in the git folder, and `brief`
    gets its line. The role sentences are child 9's.

### Child 11: `status-since-and-state-line` — `status --since` and the watcher's state line

- **Scope** (study-fable 4.3 and 4.5; F14):
  - `status --since <seq>` prints only what changed since a journal or event sequence. It shows
    merged CRs as one count and prints the sequence to pass next time. Plain `status` is
    unchanged.
  - A `state:` line goes on the steering session's told blocks (`src/hub/watch_lines.py`). It
    holds the `batch:` line's counts by state and the due count.
- **Depends on:** child 10.
- **Acceptance evidence.**
  - Pytest on prepared records: `--since` lists only the changes, and the count of merged CRs is
    correct.
  - A watcher test checks the `state:` line.
  - A scenario step.
  - The added `just test` seconds are stated.
- **Must not.**
  - Change plain `status`.
  - Record anything.
- **Risk.** The long gate is owed. AGENTS.md: none beyond child 9, since `status` already exists.

### Child 12: `next-advice` — `chantier next` and `next:` lines

- **Scope** (answers 11 and 13; the AGENTS.md wording of child 9):
  - New command `chantier next [<cr>] [--lease N | --epoch N]`, declared in
    `src/declare/next.py`. It is advice and read-only.
    - **With `--epoch`:** the steering session's due list for the batch, read from the record:
      - a free slot, and the next CR to take;
      - a CR handed back with no ask (`judge <cr>`);
      - an order not done;
      - a `restack owed`;
      - a stale lease (`take --reclaim`);
      - otherwise, `nothing due: wait`.

      The same list serves the Chief of Staff in direct mode, as steering session.
    - **With `<cr> --lease`:** the Driver's next step, from the CR's events: round, gate, push,
      ship, CI, verdict, handback. The order of the steps lives in a new table beside
      `src/core/phases.py`.
    - **With neither:** the Chief of Staff's view: asks to carry, ready CRs, a watcher not
      running.
  - `next:` lines are printed at the end of `round`, `gate`, `push`, `ship`, `verdict`,
    `handback`, `order merged` and `order done`, from the same function. They join the four that
    exist: `src/commands/endpause.py:47`, `src/commands/opening.py:277` and `:333`,
    `src/rails_release.py:215`.
- **Depends on:** child 11.
- **Acceptance evidence.**
  - Pytest, parametrized over prepared records: each due kind appears in `next --epoch`, and
    each Driver step in `next <cr>`.
  - Scenario steps: `next` at three moments of a batch, and a Driver that follows the `next:`
    lines.
  - The added `just test` seconds are stated.
- **Must not.**
  - Record anything.
  - Take the place of a safety step, which stays a refusal.
  - Decide a merge or a take-back.
- **Risk.**
  - The long gate is owed.
  - A wrong `next:` line misleads every run, so each line is a scenario check.
  - AGENTS.md gains a line for `next`. Its sources are simplify-cards-Q11 and study-behaviour
    3.5: the Foreman's heartbeat is 37 to 64 % of its weighted tokens.

### Child 13: `msg-steering` — A Driver messages the steering session through the board

- **Scope** (answer 4; answer 13; answer 22, F8):
  - New commands `chantier msg steering <kind> <text> --lease N` and `chantier inbox [--read
    <id>|all] --epoch N`, declared in `src/declare/msg.py`.
    - `<kind>` is `anomaly`, `blocked` or `note`.
    - `steering` means the batch's Foreman, or the Chief of Staff in direct mode.
    - There are no `user` or `cr:` targets.
  - One `msg@1` line per message goes to the project's `forge-journal.jsonl`, through the one
    append function. Its schema goes in `src/hub/schemas.py` and `hub/schemas.json`.
  - **Delivery.** The surface server's `events` topic carries `msg@1` lines. The steering
    session's watcher (`src/hub/watch_reads.py`, which today reads `merged@1`, `checks-red@1`
    and `wait-cleared@1`) handles them as follows:
    - it wakes its session on `anomaly` and `blocked`;
    - `note` wakes nobody: notes are listed by `inbox` and at the steering session's next told
      block.
  - **No subscriber.** When no watcher of the batch's steering session is subscribed (read from
    the watcher locks `chantier/watch-<project>/<session>.lock` and the server's subscriptions),
    `msg`:
    - still appends the line;
    - prints `not delivered: no watcher subscribed`;
    - exits non-zero.

    The Driver then uses its host means or the hand-back.
  - The Foreman's own watcher (CR-479) has never run in a real batch. Its delivery is unproved,
    and child 28 measures it.
- **Depends on:** child 12.
- **Acceptance evidence.**
  - Pytest:
    - a schema round-trip;
    - a `note` does not wake, while `anomaly` and `blocked` do;
    - `inbox --read` marks a message read;
    - with no subscribed watcher, `msg` prints the line and exits non-zero.
  - A scenario step: a Driver's `msg steering blocked …` wakes the Foreman's watcher.
  - The added `just test` seconds are stated.
- **Must not.**
  - Let the board or the server send anything to an agent itself.
  - Carry a message across projects.
  - Replace `note <cr>`.
- **Risk.**
  - The long gate is owed.
  - AGENTS.md: the journal's writers and the watcher's subscribed lines gain `msg@1`, and `msg`
    and `inbox` get their line (simplify-cards-Q7, Q22).

### Child 14: `judge-asks` — The CLI words the ask to the user

- **Scope** (answer 11; AGENTS.md as child 9 words it):
  - New command `chantier judge <cr> --epoch N`, declared in `src/declare/judge.py`.
  - It reads the CR's hand-back and the `handed back:` line's facts (`src/status/ready_line.py`):
    gaps, what is owed before the merge, the long gate's result and the waits.
  - It prints the ask to the user, worded by the CLI, ready to record. With no ask possible (a
    blocked hand-back), it prints the facts. The take-back stays the steering session's choice.
  - With `--record ["<one sentence>"]`, it records the ask through the record that `asks` writes
    (`src/declare/batch_status.py`), with the steering session's optional sentence appended.
- **Depends on:** child 13.
- **Acceptance evidence.**
  - Pytest over prepared hand-backs: ready; ready with gaps; a waiver; a local-run rule; a
    stack's top; blocked. The recorded ask equals the printed one.
  - A scenario step: the Foreman runs `judge`, then the ask shows in `status`.
  - The added `just test` seconds are stated.
- **Must not.**
  - Decide a merge or a take-back.
  - Drop a gap or an owed item from the wording.
- **Risk.** The long gate is owed. AGENTS.md gains a line for `judge`.

### Child 15: `conflicts-check` — The early conflict check as a command

- **Scope** (study-fable-v2 child 5; F14, F17):
  - New command `chantier conflicts <cr> --epoch N`. It runs the early conflict check that
    `foreman-conflict.md` describes, over the CR and the batch's other working CRs. It records
    notes on the CRs and prints one ask.
  - The git read is `git merge-tree --write-tree <a> <b>`. This form needs git 2.38 or later,
    which the repository does not pin. It writes objects to the object store and no ref.
    - The command checks `git --version` first. On an older git it refuses with the version
      needed.
    - AGENTS.md's git exceptions name the command, with the object writes.
  - It is distinct from `1-inbox/pr-conflict-detect-and-rebase-order` (a server scan after a
    merge). It shares no code with it and stays Foreman-run.
- **Depends on:** child 14.
- **Acceptance evidence.**
  - Pytest on a prepared repository: two conflicting branches, one clean pair, and a refusal on
    a faked old git version.
  - A scenario step.
  - The added `just test` seconds are stated.
- **Must not.**
  - Write a ref or a branch, or touch the worktree.
  - Start a rebase.
- **Risk.**
  - The long gate is owed.
  - AGENTS.md: a git exception, its object writes and its tool line.
  - The `merge-tree` form on the CI runners' git is unproved until CI runs.

### Child 16: `retro-draft` — The retro's draft from the batch's events

- **Scope** (study-fable-v2 child 5; answer 9's M5 fields; F14):
  - New command `chantier retro draft --epoch N`. It drafts retro points from the batch's
    events: asks, blocks, refusals, Driver restarts, red gates and cost outliers.
  - Each point carries three fields, left for the author to fill:
    - `home:`, the M5 ladder: CLI, refusal, `next:` or state line, help topic, card line;
    - `count:`;
    - `why not code:`.
  - It prints the draft, or writes it to `retro.md`'s draft section only when that file has none.
- **Depends on:** child 15.
- **Acceptance evidence.**
  - Pytest on prepared events.
  - A scenario step.
  - The added `just test` seconds are stated.
- **Must not.**
  - File a retro point.
  - Overwrite an author's text.
- **Risk.** The long gate is owed. AGENTS.md gains a line for `retro draft`.

### Child 17: `launcher` — One launcher in place of the `$CHANTIER` paragraph

- **Scope** (study-fable-v2 child 4):
  - A launcher shipped with the plugin. It:
    - decides the dev or plugin mode;
    - checks `uv sync --check` and prints `sync pending: held by …` itself;
    - runs the CLI by the one method AGENTS.md describes (`uvx --from <plugin root>`, or in dev
      mode `uv run --no-sync --project`).
  - The four `SKILL.md` keep their paragraph until child 23 replaces it with one line naming the
    launcher.
- **Depends on:** child 16.
- **Acceptance evidence.**
  - Pytest of the mode choice on prepared folders.
  - A trial in a real session that the host's allow rule matches the launcher as it matches
    today's `uv run` form, recorded in the PR. Study-fable left this unproved.
  - An unmatched or refused launcher is not worked around: the child hands back blocked.
- **Must not.**
  - Change the run method.
  - Install anything.
- **Risk.**
  - The long gate is owed.
  - P10's sample commands (`src/commands/allow_samples.py`) change with the launcher. The allow
    rules the user granted may need one new rule, asked by preflight as today. The ready ask
    names this.
  - AGENTS.md: the run-method paragraph names the launcher.

### Child 18: `roles-data-check` — Role data and a `just` check of the wrappers

- **Scope** (answer 12; answer 22: F9, Q3; study-fable 4.7):
  - New `skills/chantier/roles.yaml`. Per role, it holds:
    - name;
    - kind: `steering`, `driver`, `worker`, `review-step` or `critic`;
    - started by;
    - tools;
    - writes: `none`, `worktree` or `cr-folder`;
    - reply format;
    - card file;
    - first line;
    - description;
    - host specifics.

    It covers all 18 roles.
  - `brief` (child 10) and `help --for` (child 7) read it in place of their current tables, with
    the same output.
  - New `just roles` target running a new script, `scripts/roles_check.py`. It is not a CLI
    command and writes nothing in the plugin. It checks that each wrapper in `agents/` and
    `com.github.copilot/agents/` agrees with the data (name, description, tools, first line),
    that both hosts' bodies are identical, and that each card and reply format exists. A
    `--write` option prints the expected wrapper and writes nothing.
  - The wrappers stay hand-written (Q3).
- **Depends on:** child 17.
- **Acceptance evidence.**
  - `just roles` passes on the committed wrappers and fails on a prepared mismatch.
  - `brief`'s bytes are unchanged for each role.
  - It replaces the "bodies identical" half of `tests/test_plugin_files.py`.
  - The added `just test` seconds are stated.
- **Must not.**
  - Add a `roles:` key to a project's `chantier.yaml`. That key collides with
    `src/playbook/config.py:35`, and project roles are out of scope.
  - Write wrappers.
  - Add, remove or rename a role.
- **Risk.** The long gate is owed. No AGENTS.md change: the wrappers stay hand-written, and child
  9 already names `roles.yaml`.

### Common to children 19 to 23: the new card set, unloaded

Children 19 to 23 write the target card set in `skills/chantier/cards-next/`. That folder
mirrors the target layout of `references/`, and nothing loads it: no manifest, no CLI line, no
`SKILL.md` or wrapper names it. Child 24 swaps it in.

What a card holds:
- the role's goal;
- what the role owns;
- its own nevers, five as a target. The cap gives way before a rule that protects the user or
  the repository (F5);
- how the role ends;
- its reply format.

A card holds nothing that the floor, a topic, a refusal, a `next:` line or `--help` already
holds.

Card budgets, in LF bytes (study-fable 4.2), as targets (Q4):

| Card | Target |
| --- | --- |
| Chief of Staff | 6 KB |
| Griller | 4 KB |
| Foreman | 4 KB |
| CR driver, stack driver | 4 KB each |
| Release driver | 3 KB |
| QA driver | 2 KB |
| Verifier | 3 KB |
| Inspector | 2 KB |
| Other workers and critics | 1.5 KB each |
| Board Griller | 2 KB |
| Floor | 1.2 KB |
| A topic | 1.5 KB |

A card above its target is listed in its PR's Known gaps with its size. Only the owner raises a
target.

Rare cases become topic files in `cards-next/topics/`, listed in `cards-next/topics.json`.
Answer 10's rare rules carry `review_by` set to the next minor version.

Each child's evidence:
- the per-role byte figures of `brief <role> --cards skills/chantier/cards-next`, set beside the
  old start readings;
- `just quiz <role> --cards skills/chantier/cards-next` for each of its roles, against the
  baseline of child 6, under F4's pass rule;
- a row list of the old rules the family covers, as a first draft for child 25.

Each child records a typed merge wait on child 28, and carries the Known gap "real run not done
(child 28)".

Long gate: these children change only a folder nothing loads, but they are card changes, so
`just scenario (ubuntu-latest)` is owed.

None of these children edits `references/`, the CLI or the hook.

### Child 19: `cards-workers` — New cards: the workers, critics and review steps

- **Scope:** in `cards-next/`, the cards of the workers, critics and review steps. These are the
  wrappers' roles other than the Drivers, plus the board Griller. Today's sources are their
  cards in `references/` and the pieces the manifest names for them, with the help topics they
  need.
- **Depends on:** child 18.
- **Acceptance evidence:** the common evidence. Each card's bytes against its target.
- **Must not:** follow the common rules.
- **Risk:** the long gate is owed. No AGENTS.md change.

### Child 20: `cards-drivers` — New cards: the CR, stack, QA and release Drivers

- **Scope:**
  - In `cards-next/`: the cards of the CR driver, stack driver, QA driver and release driver,
    with their topics. Among them: the lease, retake, refused push (the route of answer 8 kept
    for good, F3), stack restack and PR extras.
  - The three leads of `1-inbox/driver-card-leads-left-by-role-cards-sti`, carried as card lines
    or topics:
    - the typed `pipeline` wait for a long run on main;
    - reading a guideline by section;
    - waiting only in a background shell.
  - The Driver publishes its branch with `chantier push` (child 1), and never retries a refused
    `git push` (F21).
- **Depends on:** child 19.
- **Acceptance evidence:** the common evidence. The quiz cases for floor rules 1, 2, 5 and 9 on
  the CR driver.
- **Must not:** follow the common rules.
- **Risk:** the long gate is owed. No AGENTS.md change.

### Child 21: `cards-foreman` — New card: the Foreman, with its topics

- **Scope:**
  - In `cards-next/`: the Foreman's card and topics. Its stack rules (`foreman-stack.md`) become
    the `stack` topics; a stack batch adds one line through `brief`.
  - The Foreman's chat obeys only "stop" and "hold".
  - Answer 4: only `anomaly` and `blocked` wake the Foreman.
  - Answer 11: `next` is advice, safety steps are refusals, and `judge` words the ask.
  - "The user's boundaries" (12.1 KB today, `foreman.md:59`) are sorted under F5. A rule that
    protects the user or the repository goes to the floor, the card or a named refusal. The rest
    becomes topics.
- **Depends on:** child 20.
- **Acceptance evidence:** the common evidence. A list of how "The user's boundaries" was split,
  rule by rule.
- **Must not:** follow the common rules.
- **Risk:** the long gate is owed. No AGENTS.md change.

### Child 22: `cards-chief-and-griller` — New cards: the Chief of Staff and the Griller

- **Scope:**
  - In `cards-next/`: the Chief of Staff's and the Griller's cards and topics, including the
    session-start cards they read today.
  - Carried into them:
    - Answer 8's list. The Chief of Staff settles alone a refused `--force-with-lease` push or
      rebase of a `chantier/*` CR branch of the batch, a refused `gh pr ready` or
      `gh pr edit --base` on the batch's PRs, and a chantier subcommand refused in a chain, run
      again alone. It tells the user in the report. It still asks before the five actions
      listed in answer 8.
    - The steering session's plain `git push --force-with-lease` (Q6).
    - Answer 13: in direct mode the Chief of Staff gets the Foreman's card and tools. Its
      `brief` adds the Foreman's card.
    - Nothing is posted on a tracker issue without the user's approval.
    - The Griller card's section "Started from the board", kept under that name because AGENTS.md
      and `src/board/griller.py` name it.
- **Depends on:** child 21.
- **Acceptance evidence:** the common evidence. The quiz cases for answer 8's list.
- **Must not:** follow the common rules.
- **Risk:** the long gate is owed. No AGENTS.md change.

### Child 23: `cards-host-and-shared` — New shared cards, host topics and SKILL.md lines

- **Scope:**
  - In `cards-next/`:
    - `concepts.md`, templates and layouts, `routing.md`, `init.md`, `review-step.md`,
      `forges/`;
    - the host topics, which are what stays of the host cards once their rows are child 8's data
      and their history is in `docs/proofs/`;
    - the final `topics.json`;
    - the final `floor.md`.
  - The four `SKILL.md` texts as they will be after the swap, kept in `cards-next/skills/`:
    - one line naming the launcher (child 17);
    - one line that runs `brief <role>` and reads the brief file (F19). This covers the Chief of
      Staff and the Griller, and the Foreman's start line does the same.
- **Depends on:** child 22.
- **Acceptance evidence:**
  - the common evidence;
  - every link inside `cards-next/` resolves;
  - `brief` for all 18 roles builds from `cards-next/`.
- **Must not:** follow the common rules.
- **Risk:** the long gate is owed. No AGENTS.md change.

### Child 24: `cards-swap` — Swap in the new cards; remove the old set

- **Scope** (answers 14 and 17; F2, F18, F19):
  - **The swap.** `skills/chantier/cards-next/` replaces `references/` in this PR. The four
    `SKILL.md` take their texts from `cards-next/skills/`. The wrapper bodies change only where a
    role's first line or card path changed, by hand, identical on both hosts, checked by
    `just roles`.
  - **Removed:**
    - `startup-manifest.json`, `startup-core.md`, `role-core.md`, `host-core-claude-code.md`
      and `host-core-copilot.md`;
    - the 32 pieces;
    - `reload-rules.md`, which the floor replaces;
    - every old card file not carried.
  - **CLI outputs switched:**
    - `take`, `take stack` and `order qa` print the lease and the `brief` command (the short
      prompt of child 10) in place of the skeleton.
    - `round` and `handoff` stop printing every worker's opening lines. A Driver runs
      `brief <role> <cr>`.
    - `driver:refused` no longer reads the Foreman's piece.
    - `src/status/ready_line.py`'s `rules:` names the floor.
    - `src/board/griller.py`'s fixed brief names the Griller card's section "Started from the
      board", and no longer the host card.
    - The lines naming removed cards (F18): `src/commands/facts.py:140` ("cards: …/references/
      (driver.md, concepts.md; …"); `src/commands/preflight.py:218` ("the rules are in
      hosts/claude-code.md"); `src/driver_prompt.py:172-173` (the cores and the manifest).
    - The Foreman's start line runs `brief foreman` (F19).
  - **The hook.** `hooks/register.tsx`'s `session.compact` reload message names the floor.
  - **The switched-lines test (F18).** A new `tests/test_card_names.py` scans every string
    literal under `src/` and `hooks/register.tsx` for a `*.md` or `*.json` name under
    `references/`. It fails on any name absent from `references/`.
  - **Tests converted** to the new layout: `tests/test_role_cards_split.py`,
    `tests/test_startup_manifest.py`, `tests/test_start_reading.py` (replaced by a per-role test
    of `brief`'s bytes), `tests/test_session_start_split.py`,
    `tests/test_stack_chain_cards.py`, `tests/test_rebase_rules.py`,
    `tests/test_reload_rules.py`, `tests/test_release_template_card.py`, and the card reads of
    the other tests `git grep references tests/` lists. Each phrase pin becomes a pin on a file
    and heading, until child 26 sets the rule ids.
  - **Docs.** Links to removed files are fixed in `docs/`, `README.md` and `CONTRIBUTING.md`.
    `docs/incidents.md` receives the stories behind removed patches.
- **Depends on:** child 23.
- **Acceptance evidence:**
  - `just check` and `just scenario` are green;
  - every link resolves;
  - the switched-lines test passes, and fails on a prepared stale name;
  - `just quiz` on every role with `brief`'s output passes F4's rule against child 6's baseline;
  - the per-role byte figures are set beside the old start readings;
  - the added `just test` seconds are stated.
- **Must not.**
  - Keep two loaded card sets or a `cards:` switch.
  - Add a role.
  - Leave a floor rule out of the floor.
  - Merge apart from children 19 to 28 (the merge rule; a typed merge wait on child 28).
- **Risk.**
  - The highest in the program: every role's contract changes at once.
  - The long gate is owed. `just mod` is owed for the hook.
  - AGENTS.md: none (child 9 rewrote the role sentences). The rule naming `register.tsx`'s pane
    is untouched.

### Child 25: `cards-compare-review` — Read and compare: nothing important lost

- **Scope** (answer 17; answer 10; answer 22: F4, F5):
  - **The inventory.** One row per behaviour of the old cards, at child 19's base, section by
    section. Seeds: the drafts of children 19 to 23; CR-471's `work/tables.md` (in the planning
    folder, `4-batch/3-done/471-slim-the-startup-cards-of-the-three-role/work/tables.md`); and
    `evals/SCORECARD.md`'s rails. Each row holds:
    - id, role, trigger, behaviour;
    - source `file:line`;
    - kind, a to f of study-fable 3;
    - new home: card, floor, CLI or hook refusal, `next:` line, help topic, proof file,
      incidents file, or judged inferable;
    - check.
  - **Restoring.** Each row with no home is restored as a topic, a refusal or a `next:` line. A
    card line is added only within its budget.
  - **Protecting rules** (F5). A row that protects the user or the repository (kind a) has its
    home only in the floor, the role's card or a refusal. It is never a topic alone and never
    "inferable".
  - **Inferable rows** are grouped into quiz cases (child 6), several per case. The role's model
    must pass them under F4's rule, with no card text for them.
  - **Rare incident rules** with no CLI trigger become topics with `review_by` set to the next
    minor version.
  - The inventory is committed as `docs/proofs/cards-inventory.md`. The PR's Known gaps name the
    two lists the owner reads: every kind-a row with its home, and every row judged inferable or
    moved to the incidents file.
- **Depends on:** child 24.
- **Acceptance evidence:**
  - every row has a home and a check;
  - a test fails on a row whose home names a topic, refusal or line that does not exist, and on
    a kind-a row homed in a topic or as inferable;
  - the inferable rows' quiz cases pass F4's rule;
  - a typed merge wait on child 28;
  - the added `just test` seconds are stated.
- **Must not.**
  - Grow a card past its target to restore a rule without listing it in Known gaps.
  - Drop a kind-a row.
- **Risk.** The long gate is owed if a topic, refusal or line is added. No AGENTS.md change.

### Child 26: `card-gates-pytest` — Budgets, history lint and rule ids as pytest gates

- **Scope** (answer 9: M1, M2, M3, M4, M8, M12, M13; F2's rule ids):
  - **Rule ids.** Every never/must/only/always sentence of a card and every floor line carries
    `[R-nnn]`. `references/rules.json` holds each id with its card, kind (`floor`, `role`,
    `format`) and check. The inventory's rows of child 25 take these ids.
  - **M1.** `references/budgets.json` lists file, limit and owner role, checked by
    `tests/test_card_budgets.py`:
    - each card's LF bytes are at or below its limit;
    - every `*.md` under `references/` has a row;
    - the sum is at or below a constant in the test.

    The limits freeze the sizes child 24 reached (Q4). A card above its target keeps its reached
    size as its limit and is listed in Known gaps.
  - **M2.** Each role's measured path, per host, is at or below the role's limit. The path is
    `brief`'s output plus the topics its common path names.
  - **M3.** None of these appears in `references/**/*.md` or the wrappers: a date, batch name,
    CR id, PR number, "proved", "unproved", "trial", "the user's answer", a model name or a token
    count. Exceptions go in `references/lint-allow.txt`, with a rule id and a reason, and a stale
    exception fails.
  - **M4.** Every `[R-nnn]` in a card has one row in `rules.json`, and the reverse. A row's
    `check` names an existing pytest node, scenario step, scorecard rail or quiz case. A row with
    no check has kind `inferred` and a quiz case. A kind-a row may not be `inferred` (F5).
  - **M8.** The detectors move from `evals/kit/detectors.json` into `rules.json` (`detector`,
    with its positive and negative example), checked by pytest.
  - **M12.** A retired row (`retired: <version>, <reason>`) stays. Its id is never reused and
    never appears in a card.
  - **M13.** No assertion in `tests/` pins a card literal longer than 40 characters, outside the
    registry test, except marked and counted exemptions. Child 24's heading pins become id pins.
- **Depends on:** child 25.
- **Acceptance evidence:**
  - the new tests pass at the stack's head;
  - each fails on a prepared violation: a card over budget, a date in a card, an id with no row,
    a phrase pin, an inferred kind-a row;
  - a typed merge wait on child 28;
  - the added `just test` seconds are stated.
- **Must not.**
  - Raise a limit above child 24's reached size.
  - Exempt a floor rule.
- **Risk.** The long gate is owed (cards gain ids). No AGENTS.md change.

### Child 27: `card-gates-process` — The retro ladder, the approval reminder, the measure's place

- **Scope** (answer 9: M5, M6, M10, M11, M14, M7's place in the release; F13):
  - **M5.** The Retro critic's card asks each point for `home:`, `count:` and `why not code:`,
    and drops a point that lacks them. `chantier validate` checks those fields in a `retro.md`,
    read-only.
  - **M6 and F13.** The Inspector's card checks that a card diff quotes the measure line (a key
    and count from the behaviour results), or carries the owner's line. That line must quote the
    user's words as recorded in the CR's `02-answers.md`.
  - **M10.** A new `evals/results/behaviour-accepted.md` lists accepted stumbling, re-asked when
    its rate doubles. After each release retro, the Chief of Staff files the S-list of each
    measure, or answers it there.
  - **M11, as a reminder (F13).** A step of `.github/workflows/ci.yml`, in a job on
    `ubuntu-latest`, on `pull_request` only, since a push event has no body.
    - Trigger: the PR touches `references/floor.md` or `references/budgets.json`.
    - Without "Floor change approved: <user>, <date>" or "Budget change approved: <user>,
      <date>" in the body, it prints a warning annotation. It does not fail the job.
    - Its environment: GitHub's runner, with the PR's body read from the event payload and no
      local cache.
  - **M7.** "Before a release: the claims" in `evals/README.md`, and `docs/release-process.md`,
    list `just behaviour` for the version. The measure must be newer than the last card change,
    with its regressions answered, or the claims file must say "no measure: <reason>".
- **Depends on:** child 26.
- **Acceptance evidence:**
  - pytest of `validate` on a prepared `retro.md`, with the fields present and missing;
  - the CI step proved on a throwaway PR (opened, shown, closed unmerged): a touch of
    `budgets.json` without the line shows the warning;
  - a typed merge wait on child 28;
  - the added `just test` seconds are stated.
- **Must not.**
  - Let a Driver write the owner's approval line.
  - Make the CI step fail a job.
- **Risk.**
  - The long gate is owed (cards).
  - A CI job change, proved by its first run.
  - Opening and closing the throwaway PR is a forge write. The Driver does it and records the
    PR's link.

### Child 28: `cards-real-run` — A sandbox campaign on the new cards, measured

- **Scope** (answer 14, the real-run measure before the swap; answer 22: F6, Q5):
  - A sandbox campaign: the eval kit's `real-foreman` campaign, five frozen CRs. It is run by the
    user, or on the user's word, with the plugin loaded from the stack's top worktree, outside
    the main checkout, which does not change during an eval. The Driver prepares the campaign's
    setup and runbook, and a session started by the user runs it.
  - The campaign is measured with `just behaviour --since <the run's start>` and compared, role
    by role for the roles seen, with child 5's baseline:
    - card bytes read;
    - turns;
    - CLI errors and the S-list;
    - the `chantier push` refusal rate;
    - Driver runs per CR;
    - the Foreman's and the Chief of Staff's wake shares;
    - `msg` deliveries;
    - cost per CR.
  - Roles not seen in the campaign are listed "no run", not failed. Among them, likely: the QA
    driver, the demo explorer, the board Griller and every Copilot role.
  - `just quiz` on every role, on the old cards and the new, side by side.
  - Results are committed in `evals/results/`, named by its convention. The budgets of child 26
    are confirmed at what the run read, or a raise is asked with the owner's line (M11).
- **Depends on:** child 27. Top of the stack.
- **Acceptance evidence:**
  - the measure files;
  - each role seen reads fewer card bytes than its old figure;
  - no floor rule's detector is worse than the baseline;
  - the quiz passes F4's rule on every role;
  - the S-list's new lines are filed or accepted (M10).

  Until the user has run the campaign, this child is handed back with the plumbing and the Known
  gap "campaign not run: waits for the user". Children 19 to 27 keep their merge wait.
- **Must not.**
  - Start a batch or a campaign without the user (floor rule 7).
  - Change the main checkout.
  - Change a card to pass the measure without a new quiz and measure.
- **Risk.**
  - As top of the stack, it owes the local Windows long gate (`chantier gate <cr> scenario`) at
    its head, as well as the pipeline's `just scenario (ubuntu-latest)`.
  - The model and agent cost of a campaign.
  - No AGENTS.md change.

## Evidence for the program

- Each child's own acceptance, above.
- Child 1's smoke trial, recorded in its PR before any card child starts. The `chantier push`
  refusal rate is measured in child 28.
- Child 28's campaign: every role seen reads fewer card bytes than before, and the quiz passes
  F4's rule on every role, before children 19 to 28 merge in one sitting.
- The host and defaults matrix (the program changes what each host reads at boot):
  - **Claude Code, shipped defaults:** every child's tests and the scenario; child 1's trial;
    child 28's campaign.
  - **Claude Code, a project's own `chantier.yaml` role settings:** `brief` reads the per-host
    agent and model as today (child 10's tests).
  - **Copilot, shipped defaults:** `brief`, `host` and `just roles` on the Copilot rows and
    wrappers (children 8, 10, 18). No real run, since none was ever seen here; the host rows say
    "untested".

## Open questions

None for the specification: answer 22 settled the critic's findings and the eight earlier
questions. Two items wait for the owner, as decided, and are not questions:
- the owner's confirmation of answer 22 at wake;
- the start of child 28's sandbox campaign, which only the user starts (F6, floor rule 7).
