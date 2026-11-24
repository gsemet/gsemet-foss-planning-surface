# Rewrite the role cards: minimal boot, progressive disclosure

Program specification. It does not land as one PR: it is cut into the ordered chain of child CRs
of `## Children`, each one Driver and one PR, stacked in that order. Every child is written so
that a later Spec-writer can turn it into a full Change Specification without asking anything
but the open questions at the end.

Code read: `origin/main` at `8a960d34` (chantier 0.15.1 plus CR-471's cut of the cards by
moment and the Foreman's own watcher). Paths below are relative to the chantier repository; the
CLI's source is `skills/chantier/scripts/cli/src/chantier/` (written `src/` below), its tests
`skills/chantier/scripts/cli/tests/` (written `tests/`), the cards
`skills/chantier/references/` (written `references/`).

## Goal

In the owner's words (answers 1, 17, 18, 20): the cards are far too heavy and detailed, the
result of dozens of runs and retros that each added a small correction, and they cost a lot at
every role's start. Rely on Opus 5.5 and Sonnet 5.5 inferring from a vital minimum. Rewrite the
card mechanism completely: the smallest possible cards, no behaviour lost, progressive
disclosure to the fullest (a model that stumbles runs `--help` or `help <topic>`; the watcher,
the server and the CLI's lines remind it where it stands; agents message each other through the
board instead of waking each other). Simpler role cards also let outside people bring their own
roles. Go straight to the desired state in one total rewrite, then verify by reading and
comparing that nothing important was lost and that everything removed is easy for the agents
to find again, or already in the model's weights.

Fixed (answer 1): the roles themselves (not their cards: no role is added or removed), the
working with the surface server (improvable), the Foreman orchestrating with the tools it is
given. The work is mostly better tools and per-role progressive disclosure.

The end state, measured by the program's last child:

- Every role boots on one short card plus one shared floor plus its facts, printed whole by
  the CLI; no role reads a manifest, a core file or a host card at boot.
- What a role needs at a rare moment comes from a help topic that a refusal, a `next:` line or a
  state line names, never from a list of moments to remember.
- A rule lives in one place; no card holds dates, batch names, trial marks or incident stories.
- Pytest gates keep it so: a retro fix lands as code, a refusal, a `next:` line or a help topic,
  and a card grows only past a gate the user signs.

Starting figures (study-fable-v2, LF bytes): the cards are 829 KB in 70 files; declared start
reading on Claude is 202 KB for the Chief of Staff (110 KB of it the Claude host card), 91 KB
for the Foreman, 145 KB for the Griller, 24 to 34 KB for the Drivers; measured real reading on
the old cards is 218 KB (Chief of Staff), 144 KB (Foreman), 44 KB (CR driver), 17.5 KB
(Verifier). No role has yet run on CR-471's cards.

## Decisions carried

Each answer of `02-answers.md`, and where the program carries it. Answers 17, 18 and 20 rank
highest; answer 5 (simplify-cards-Q8) is replaced by answers 17 and 18 and is carried only in
what they keep of it.

| Answer | Decision | Carried by |
| --- | --- | --- |
| 1 framing | Smallest cards, no behaviour lost, progressive disclosure, total overhaul accepted if every boot is much lighter; roles, server and the Foreman's orchestration fixed | the whole program; budgets in child 15; measure in child 19 |
| 2 study-v2 | The design is judged on origin/main | this specification reads `8a960d34` |
| 3 Q6 stumbling | None on the common path, free on rare cases; a usage error or refusal seen in more than 2 % of a role's runs is a tool bug, not a card gap | child 2 (the known near-misses), child 3 (scratch writes), child 4 (the S-list), child 18 (M10) |
| 4 Q7 messages | `msg` and `inbox` exist; only `anomaly` and `blocked` wake the Foreman; notes wait for its next wake | child 10 |
| 5 Q8 scope | Replaced by 17 and 18. Kept from it: a program CR whose children regroup study-fable-v2 section 6; a real run measured on the new cards; `help <topic>` as the carrier of the pieces; the host card out of the start | `## Children` (all nine study children are regrouped: see the table in `## Order`) |
| 6, 7 Q5 | A CLI subcommand, working name `chantier push <cr>`, runs the `--force-with-lease` push itself, for GitHub and GitLab. It exists to declare that the operation is legitimate in what the Driver is doing (it states the intent, so the host's classifier can read it as such). Rails: the CR's recorded `chantier/*` branch, never the default or a protected branch, the caller holds the CR's lease, the worktree is clean. AGENTS.md changes (a named git exception, a network use). A trial in auto mode from a Driver, in the compound form agents type, before any card is cut. Refused through a profile's `cli.run`, like `gate` | child 1 |
| 8 Q5b | The Chief of Staff runs alone, and tells the user in the report: a refused `--force-with-lease` push or rebase of a `chantier/*` CR branch of the batch, a refused `gh pr ready` or `gh pr edit --base` on the batch's PRs, a chantier subcommand refused in a chain (run again alone). It still asks before: editing `settings.json`, stopping a process it did not start, publishing a release, deleting branches or folders, pushing a branch that is not the CR's own | child 15 (the Chief of Staff's card), child 6 (the help topic a refusal names) |
| 9 Q9 | Hard gates in pytest: budgets per card and per measured path (M1, M2), no history in a card (M3), a rule with an id and a check (M4), a refusal names the next command (M9), tests pin ids not prose (M13); the retro-fix ladder (M5); the periodic transcript measure `just behaviour` (M7). Budgets frozen per role; raising one needs the user's line in the PR (M11) | child 4 (M7, M8 runner, M10 list, M14 list), child 2 (M9), child 17 (M1, M2, M3, M4, M8, M12, M13), child 18 (M5, M6, M10, M11, M7 in the release claims) |
| 10 Q10 | A rare incident rule with no CLI trigger is kept as a help topic for one release; which topics are read is measured; the never-read ones are then deleted | child 6 (topics carry a review version), child 16 (the review files them so), child 4 (the measure counts `help` reads); the deletion itself is out of scope |
| 11 Q11 | `next` is advice for the choice of the CR and the wording; the safety steps are refusals, not advice; the CLI words the ask to the user and the Foreman may add one sentence | child 9 (`next`), child 11 (`judge`), child 15 (cards say it) |
| 12 Q12 | Roles from outside: review steps, critics and workers that write in the worktree; never a steering role (no Driver, Foreman or Chief of Staff) | child 14 |
| 13 Q15 | The Chief of Staff in direct mode gets the Foreman's card and tools (`next`, the watcher) | child 9 (`next` answers the direct-mode steering session), child 10 (its watcher carries the messages), child 15 (the card) |
| 14 Q16 | One card set only; the old cards are removed when the new ones merge; no `cards: v1` switch; a rollback is a git revert. The real-run measure and the quiz pass before the swap | child 15 removes the old set in the same PR; child 5 (quiz), child 19 (real run); the merge rule of `## Order` |
| 15 Q14 | No decision on a floor; a principle: files simple to edit, modular, loading what is needed when it is needed (a card is one short file, a rule lives in one place, a piece is loaded at its moment). Floor, its size and the nevers per role are left to the specification | judged below, "The floor"; children 8 and 15 |
| 16 Q13 | When a host function is used, the CLI says in one sentence that it was never tried for real here; the history of the trials leaves the cards for a proof file nobody loads | child 7 |
| 17 Q17 | A total rewrite of all the cards straight to the desired state; then a read-and-compare review: each removed rule kept, found again through a help topic, a refusal or a `next:` line, or judged inferable; no family-by-family migration | child 15 (one pass), child 16 (the review) |
| 18 Q18 | Order: the tools land first (`help <topic>`, `next`, `msg`/`inbox`, the push subcommand, the refusals), the push subcommand tried in auto mode from a Driver; then the total rewrite in one pass; then the read-and-compare review; plus the real-run measure and the maintenance gates that guard the result | `## Order` |
| 19 Q19 | Grilled enough | this specification |
| 20 Q20 | Destination batch-31, after the CRs that already ran; specified by an Opus sub-agent, criticised by a Fable sub-agent; the specification goes to the end of the rewrite, even cut into several chained CRs; by the end of the night, a stack of all these CRs, each validated and ready to merge in order | `## Children` is a chain for a stack; each child carries its own acceptance |

### The floor (answer 15, judged here)

Judged against the owner's principle: one floor file, `references/floor.md`, at most 1,200 LF
bytes, holding the ten rules study-fable-v2 section 5 lists (never merge without the user's
word; rebase only and `--force-with-lease` on the CR's own branch only; no fallback; a CLI that
cannot run is a stop; never discard the worktree's work; an irreversible release action waits
for the user; only the user starts work; no image shows the username or home folder; refusals
reported with their exact text, never worked around; never stop a process by name or pattern,
`close --yes` only on the user's yes). Why one floor: these rules protect the user, must be
known before a role types anything, and today sit in five to seven places each, two of them
(rules 5 and 8) in pieces read only on a condition since CR-471. One file keeps each rule in one
place; the CLI's `brief` (child 8) puts it in every prompt, so it is loaded at its moment
(boot) and no card restates it. Each card then holds at most five nevers of its own role. The
three rules "close behind" go where they apply: the Foreman's chat obeys only "stop" and "hold"
(Foreman card), nothing posted on a tracker issue without the user's approval (Chief of Staff
card), an untested host path is said untested (the host row's sentence, child 7).

## What changes, by area

- **CLI** (`src/`): new commands `push`, `help`, `host`, `brief`, `next`, `msg`, `inbox`,
  `judge`, `conflicts`, `retro draft`, `roles lint`, `roles build`; near-miss arguments
  accepted; refusals that name the next command or topic; `status --since`; `take`, `round`
  and `handoff` printing a pointer to `brief` in place of every worker's opening lines (switched
  in the rewrite child only).
- **Hook** (`hooks/register.tsx`): the write guard lets scratch writes through; the reload
  message after a compaction names the floor; the deny list of never-commands only if open
  question 1 says so.
- **Cards** (`references/`, the four `SKILL.md`, the 30 wrapper bodies): one total rewrite;
  the startup manifest, the four core files and the 32 pieces are removed; help topics in
  `references/topics/`; host data files; the floor.
- **Docs**: `docs/proofs/claude-code.md`, `docs/proofs/copilot.md` (trial history),
  `docs/incidents.md` (the stories behind removed patches); links to removed cards fixed.
- **Eval kit** (`evals/kit/`): `behaviour.py` (`just behaviour`) and `quiz.py` (`just quiz`);
  results in `evals/results/`.
- **Tests and CI**: budgets and lints as pytest gates; one `ci.yml` step for the user's
  approval line; phrase tests converted to rule ids.
- **AGENTS.md**: the push subcommand's git and network exception; each new tool's line with its
  measure or answer; the journal's new `msg@1` writer; generated wrappers (open question 3);
  the release claims' behaviour measure.

## Out of scope

- Adding, removing or merging roles; changing what a role is responsible for (answer 1).
- The surface server's protocol and the board's pages, but for the `msg@1` journal type and its
  `events` delivery (child 10).
- The deletion of never-read help topics one release after this program (answer 10): a later CR,
  listed by M12's candidates.
- Fixing every line of the S-list (study-behaviour 3.2) beyond those named in children 2 and 3:
  the others go through M10 (filed as inbox items or accepted), not through this program.
  Among them: S4 (waiting calls blocked by the host), S7 (a role's tool list), S8, S11, S13.
- A rebase subcommand (study-classifier: 1 refusal in 721 rebases).
- Writing the host's auto-mode configuration, or asking the user to leave auto mode
  (study-classifier option D): the user's own setting.
- The hook recording an agent's id at spawn in place of `agents set` (study-fable 4.4): not in
  the nine children; left to M10 if `agents set` shows in the S-list.
- Copilot campaigns beyond what each child's tests can show: Copilot has no hook and no run was
  seen (studies); its wrappers are generated in child 14 and its roles boot through `brief`.
- `reply-check` (study-fable 4.4; not in study-v2's children).

## Order

Four steps, as answer 18 sets them. Answer 20 allows a step to be cut into several chained CRs;
step 1 is cut into fourteen, each small enough for one Driver.

1. **Tools first** (children 1 to 14). Each is additive: it adds commands, flags, lines, files
   and data, and removes no output the current cards rely on and changes no card text (but the
   new files it adds: the floor, topic index, host data, proofs). So every intermediate `main`
   still works with the old cards. The push subcommand comes first and is tried in auto mode
   from a Driver before any card is cut (answer 7).
2. **The total rewrite** (child 15): all the cards in one pass, the old set removed in the same
   PR, and the old CLI outputs the new cards no longer use switched in the same PR.
3. **The read-and-compare review** (child 16): the inventory of every rule of the old cards,
   each one classified; what is lost is restored as a topic, a refusal or a `next:` line.
4. **The gates and the measure** (children 17 to 19): the pytest and process gates of answer 9,
   then one real run on the new cards, measured against the old, with the quiz on both sets.

**Merge rule of the stack (answer 14).** The real-run measure and the quiz pass before the
swap: child 15 (the swap) is not merged before child 19's measure and child 16's review have
passed at the stack's head. Children 1 to 14 may merge in order as each is ready (they keep the
old cards working). Each child's PR in 15 to 18 names this in its Known gaps ("do not merge
before child 19's measure passes"), so the ready line quotes it.

Study-fable-v2 section 6, regrouped (answer 18):

| Study child | Here |
| --- | --- |
| 1. Measure the new cards for real | child 4 (the tool), child 19 (the run) |
| 2. The carrier for the pieces | child 6 |
| 3. The host card out of the start | child 7 (data, proofs), child 8 (the host row in `brief`), child 15 (the cards) |
| 4. Quick cuts | child 13 (launcher), child 9 (`status --since`), child 8 and 15 (`handoff` without every worker's lines), child 15 (`driver:refused` without the Foreman's piece) |
| 5. The tools | children 8 to 12 |
| 6. Refusals | child 2 (CLI), child 3 (hook) |
| 7. The rewrite, by family | child 15, one pass (answer 17 replaces "by family" and the `cards:` key) |
| 8. Roles as data | child 14 |
| 9. Removal | child 15 (answer 14: removed when the new ones merge) |

## Rules for every child

- Base: the previous child's branch (a stack batch). Child 1's base is `main`.
- `just check` passes before the first push; a change under `src/` or `evals/kit/` also runs
  `just eval-dry-run` (AGENTS.md).
- Long gate: every child that changes the CLI, the cards or the scenario passes
  `just scenario (ubuntu-latest)` green at its PR's head. In this stack only the CR on top owes
  the local Windows run (`chantier gate <cr> scenario`); when a child joins on top, the run moves
  to it (AGENTS.md).
- A child that changes `hooks/` runs `just mod` itself before its PR; one that cannot stops and
  says so.
- A new command adds a scenario step to `scenario/run_scenario.py` and its coverage bullet
  (`tests/test_scenario_coverage.py`), and keeps `just test` within AGENTS.md's time limit.
- A new journal type regenerates `hub/schemas.json` with `just journal-schemas`.
- Each new CLI tool adds its line to AGENTS.md's named exceptions with its source: the measure
  (study-behaviour, study-classifier figures) or the user's answer (simplify-cards-Q…, this
  CR), as AGENTS.md does for `wait`, `access` and `live`.
- No child before 15 edits an existing card's text. No child edits a version by hand.
- Repository text in English; no date, batch name or trial story in a card (M3, enforced from
  child 17).

## Children

### Child 1: `push-own-cr-branch` — Push a CR's own branch through the CLI

- **Scope.**
  - New command `chantier push <cr> [--lease N]` declared in `src/declare/delivery.py`, handler
    `push` in a new `src/commands/push.py`. Help text says plainly that the command exists to
    declare that the operation is legitimate: chantier's own update of the CR's own branch
    after a rebase, the lease held.
  - Rails, checked before any git write, each refusal naming what to do: the branch is the CR's
    recorded one (`CrEntry.branch`), matches `chantier/*`, and is not the default branch
    (`repo.config["default_branch"]`); the caller holds the CR's lease, through
    `leases.require` then `leases.claim` (`src/core/leases.py`), the stack's lease (unit
    `"stack"`) accepted for a CR of a stack batch's chain and an order's lease for a QA order's
    unit; the worktree (`cr_worktree(c)`) is clean (`git status --porcelain
    --untracked-files=normal` empty) and its HEAD is on that branch.
  - The push, from the worktree: `git push --force-with-lease=<branch>:<expected>
    <remote> HEAD:refs/heads/<branch>`, `<remote>` from `repo.config["remote"]`, `<expected>`
    the worktree's remote-tracking ref `refs/remotes/<remote>/<branch>` (absent: the empty
    expectation, so the push creates the branch only if the remote has none). Never plain
    `--force`, never `--no-verify`. git's refusal (a stale lease, a protected branch, a hook)
    is printed verbatim and exits with the external-failure code; nothing is retried.
  - Records a `push` event on the CR (`b.log("push", cr, branch=…, head=…, expected=…)`) inside
    `RenderedBatch`, which renews the lease as other Driver commands do.
  - Same command for GitHub and GitLab (it is git; no forge call).
  - `src/core/remote_wire.py`: `push` joins `NEVER_REMOTE`; `src/clients/remote.py` refuses it
    through a profile with a line like `GATE` ("push runs on the machine that holds the
    worktree…"), and `src/board/cli_run.py`'s `judge` refuses it in `cli.run`.
  - `src/driver_prompt.py` `_rewrites_line`: the push half names `$CHANTIER push <cr> --lease
    <n>` (one command per CR branch for a stack); the rebase half is unchanged.
  - `src/commands/delivery.py` `_off_worktree`: the "not pushed" line names `chantier push`.
  - `src/commands/allow_samples.py`: P10 keeps its force-push samples (the steering session
    still pushes by hand, answer 8) and adds none for `push` (the `chantier *` rule covers it).
  - AGENTS.md: the CLI's named git exceptions gain `push` (one `git push --force-with-lease` of
    a CR's recorded `chantier/*` branch, from its worktree, never forced, never `--no-verify`);
    the network list gains its push; the named-exceptions paragraph gives its source: the
    user's answers simplify-cards-Q5 (2026-11-24) and the measure of study-classifier (13
    classifier refusals of force pushes in 12 days, each a lost Driver, 4 questions to the user;
    83 % of the pushes typed as compound commands no allow rule matches), and says that the
    command states the operation's legitimacy; `push` joins the commands that never run
    through a profile, beside `gate`.
- **Depends on:** nothing (base `main`).
- **Acceptance evidence.**
  - Pytest (`tests/test_push.py`, parametrized, in-process on a prepared state with a bare
    remote): each refusal (branch not recorded, not `chantier/*`, the default branch, no lease,
    a stale lease, a dirty worktree, HEAD on another branch) exits non-zero and runs no
    `git push`; a valid call pushes, records the event and renews the lease; a remote moved
    since the tracking ref makes git refuse and the command exits external with git's text;
    `push` through a profile and through `cli.run` is refused.
  - Scenario step in `scenario/run_scenario.py`: a Driver's rebase then `push`, then `ship`
    records no "not pushed" line; GitHub and the GitLab unit.
  - **The trial in auto mode (answer 7)**: the child's own Driver, a subagent in auto mode,
    pushes its own CR branch with the worktree's build, in the compound form agents type, for
    example `C="uv run --no-sync --project <worktree> chantier --project <planning>"; $C push
    <cr> --lease <n> 2>&1 | tail -3`, and records in the PR's Deliverables each try's exact
    command text and the host's verdict (ran, or the refusal's text). A refusal is not worked
    around: the Driver hands back blocked with the text, and the program waits for the user.
    How many tries make the proof: open question 2.
- **Must not.** Push any branch but the CR's recorded one; read or write the forge; push
  through a profile; add `--force` or `--no-verify`; change a card's text; run a rebase.
- **Risk.** Long gate owed (CLI and scenario). AGENTS.md changes (a third git exception and a
  network use) need the owner's yes in the PR (answer 7 gives it for this subcommand; the PR
  quotes it). The classifier's verdict on the command text is unproved until the trial.

### Child 2: `cli-near-misses` — Accept the CLI's near-miss forms; refusals name the next step

- **Scope** (answer 3: each line is seen in more than 2 % of a role's runs, study-behaviour 3.2):
  - S1: `--lease N` accepted on every command that takes a CR or a unit a Driver runs
    (`handoff`, `take` when run by a Driver is refused anyway, `verdict`, `rules`, `log`,
    `wait`, `lease`): through `add_lease` in `src/commands/registry.py`; a valid lease renews,
    a command that has no use for it ignores it, a stale one still exits `claim lost`.
  - S2: `phase <cr> "gate preflight"`: a first argument holding a space is split on its first
    space (`src/declare/driver.py`, `phase`).
  - S3: `take` run by a Driver: the refusal adds "`handoff <cr>` prints the take's facts".
  - S6: a CR folder path that repeats the planning prefix
    (`projects/chantier/changes/projects/chantier/changes/…`) and a path relative to a shell
    already inside a CR folder resolve to the CR folder; the CR's short name is accepted where a
    CR folder is expected (`summary`, `triage`, `file`).
  - S9: `summary lint` prints the title and summary limits; `summary lint`'s gap line prints the
    exact `summary set` form (study-behaviour S8).
  - S10: `--epoch` accepted in any position; `take` clears an ended Driver's recorded agent id
    itself when the record says the Driver ended, in place of refusing with "`agents set CR-N -`
    first".
  - M9: every refusal raised from `src/rails.py`, `src/rails_release.py`, `src/rails_idle.py`
    and `src/core/leases.py` contains a backticked command (or, after child 6, a
    `help <topic>`), but for an allow-list of final refusals ("stop now").
- **Depends on:** child 1.
- **Acceptance evidence.** Pytest, parametrized, one case per near-miss form (accepted, and the
  same effect as the canonical form); `tests/test_rail_refusals.py` extended to assert the
  backticked next step for each refusal (M9) with its allow-list counted and printed.
- **Must not.** Change what a valid canonical command does; accept a form that changes the
  meaning (a stale lease stays refused); touch a card.
- **Risk.** Long gate owed. No AGENTS.md change. A near-miss accepted wrongly can hide a real
  mistake: each accepted form is listed in the command's `--help`.

### Child 3: `hook-scratch-writes` — Let the write guard pass scratch writes

- **Scope** (answer 3; study-behaviour S5: 577 write-guard refusals, 490 of them scratch writes
  the host's own prompt recommends):
  - `hooks/register.tsx`, `writtenBy` and `judgeShell`: a redirection or write to `/dev/null`
    (and `NUL` / `$null` on Windows shells) is never judged a write; a write inside the session's
    scratchpad folder passes. How the hook learns the scratchpad's path is the child's to find
    in the host's API; if the host gives it no path, the child names `<cr>/work/scratch` as a
    `scratch:` folder on the prompt's `writes:` line instead (in `src/driver_prompt.py` and the
    worker lines of `src/plugin_files.py`), additive.
  - `hooks/register.test.tsx`: cases for both.
  - Only if open question 1 answers yes: a deny list on a segment's first words for the agents
    the guard judges (those with a `writes:` line): `git merge` (any form),
    `gh pr merge`, `glab mr merge`, `git reset --hard`,
    `git clean`, `git stash`, `git push --force` / `-f` (plain, not `--force-with-lease`),
    `git checkout -- <files>`, `git restore`, `pkill`, `killall`, the refusal text quoting the
    floor's rule and its id. `EXEMPT` then stops exempting those segments.
- **Depends on:** child 2.
- **Acceptance evidence.** `hooks/register.test.tsx` cases (scratch writes pass, writes outside
  still refused, and the deny cases if open question 1 says yes); `just mod` passes, run by the
  Driver.
- **Must not.** Guard the main session (it has no `writes:` line); judge inside an
  interpreter's inline code; refuse a call it cannot cut (it passes with a note, as today);
  change anything on Copilot (no hook).
- **Risk.** `just mod` owed (a change to `hooks/`). Long gate owed only if the scenario or CLI
  changes (the `scratch:` variant changes the CLI: then owed). A false refusal blocks a worker:
  the deny list, if any, matches first words only.

### Child 4: `behaviour-measure` — Measure what roles read and do from transcripts

- **Scope** (answer 9, M7, M8's runner, M10's list, M14's list; answer 10's read count):
  - `evals/kit/behaviour.py` and the `just behaviour [--since <date>] [--prune]` target in the
    `justfile`: reads the user's local Claude Code transcripts (`~/.claude/projects`, main
    sessions and `subagents/`, role from `meta.json` `agentType`, else the prompt's first line,
    a Foreman from `chantier Foreman n°`, a Chief of Staff or Griller from its skill), and
    writes `evals/results/behaviour-<version>.json` and `.md`: per role, runs, tool calls, model
    calls, card bytes read (Read results and shell reads naming a card path, each result once),
    files read, CLI usage errors and refusals by message, `--help` by command, `help <topic>`
    reads by topic, host denials, write-guard refusals, waits, Driver runs per CR, the
    Foreman's and the Chief of Staff's wake shares, "tool not in the role's list" (M14), and the
    S-list: each usage error or refusal message above 2 % of a role's runs (M10).
  - Detectors (M8): regexes on tool calls read from a data file (`evals/kit/detectors.json`
    now; child 17 moves them into `references/rules.json`), each with a positive and a negative
    example; the measure prints each detector's rate and a "regressions" list (a detector worse
    by more than 5 points than the previous file, a new S-list line).
  - The baseline, on the old cards: `evals/results/behaviour-0.15.1.json` and `.md`, from the
    transcripts since 2026-11-17.
  - Throwaway scripts of the studies are not copied: written anew, run with `python -I`.
- **Depends on:** child 3.
- **Acceptance evidence.** A fixture of a few redacted transcript lines under
  `evals/kit/fixture/` and its expected figures, checked by `just eval-dry-run`; the baseline
  files committed; the detectors' examples checked (each matches its positive, not its
  negative).
- **Must not.** Run in CI (transcripts are local); send transcript text anywhere; commit a
  transcript, a username or a home path (the results hold counts and message templates only).
- **Risk.** No long gate if the change stays inside `evals/` (a `justfile` target is outside the
  eval kit: then the long gate is owed). `just eval-dry-run` owed. No AGENTS.md change.

### Child 5: `situation-quiz` — A cheap quiz of a role's boot on one situation

- **Scope** (answer 14's quiz; study-fable section 5, check 3):
  - `evals/kit/quiz.py` and `just quiz <role> [--cards <git ref>] [--case <id>]`: builds the
    role's boot text from the cards at `<ref>` (default the working tree), adds one situation,
    asks "what do you do next", runs it on the model the shipped playbook gives that role
    (`config/chantier.defaults.yml`) with the host's headless CLI, three times, and has the
    eval kit's judge (`evals/kit/judge.py`) read the reply against the case's expected
    behaviour; prints pass counts per case and per role.
  - Cases in `evals/quiz/<role>/<id>.json`: id, role, situation, expected behaviour, the rule
    it proves (the floor rule's number now; an `R-nnn` id from child 15). Seed: one case per
    floor rule for the roles it binds, and one per rail of `evals/SCORECARD.md` of kind
    judgement that names a role.
  - The baseline: the quiz on the old cards (`--cards 8a960d34` or the stack's base), results in
    `evals/results/quiz-0.15.1.json`.
  - Before child 15 the boot text of the old cards is the role's declared start reading (the
    files `tests/test_start_reading.py` resolves); after child 15 it is `chantier brief
    <role>`'s output.
- **Depends on:** child 4.
- **Acceptance evidence.** `just eval-dry-run` runs the quiz's plumbing with no model (a staged
  reply); the baseline file committed with its pass counts.
- **Must not.** Run in CI; spend on a model in `just check`; judge with the role's own model.
- **Risk.** As child 4 (no long gate inside `evals/` alone). Model cost on the user's machine.

### Child 6: `help-topics` — `chantier help <topic>` carries the rare cases

- **Scope** (answer 18's `help <topic>`; answer 10; study-fable-v2 child 2):
  - New `references/topics.json`: topic name → readings (a file or `file#heading`, the same
    reading form the manifest uses today), the roles it serves, its trigger (the refusal, line
    or moment that names it), and `review_by` (a version, for answer 10's rare topics). In this
    child every manifest action of `references/startup-manifest.json` that is a piece or a
    rare-case section becomes a topic pointing at today's file (for example `lease`,
    `refused-push`, `retake`, `conflicts`, `lost-driver`, `hold`, `release`, `stack-restack`,
    `pr-extras`).
  - New command `chantier help [<topic>] [--for <role>]` (declared in a new
    `src/declare/help.py`): with a topic, prints its readings whole (in full output, like
    `rules`); with `--for`, lists that role's topics with their trigger, one line each; no
    argument lists all topics. Reads only the plugin's files; works with no batch.
  - The CLI names topics: the lease refusals of `src/core/leases.py`, the push refusals of
    child 1, the `restack owed:` line (`src/commands/orders_merged.py`, `restack_line`), the
    `handed back:` line (`src/status/ready_line.py`), the watcher's end lines
    (`src/hub/watch_lines.py`), each add `help <topic>` where one exists.
- **Depends on:** child 5.
- **Acceptance evidence.** Pytest: every topic's readings resolve on both hosts' cards; every
  `help <topic>` a CLI line prints names a topic that exists (scan of the source strings); `help
  --for <role>` lists only that role's topics; a scenario step runs `help lease`.
- **Must not.** Remove the manifest or a piece; change a card's text; read the network.
- **Risk.** Long gate owed. AGENTS.md: a line for `help` (source: simplify-cards-Q18).

### Child 7: `host-rows-and-proofs` — Host capabilities as data; trial history to a proof file

- **Scope** (answer 16; study-fable-v2 child 3):
  - New `references/hosts/claude-code.json` and `references/hosts/copilot.json`: one row per
    capability of today's "Tools" tables (`hosts/claude-code.md#Tools`, `hosts/copilot.md#Tools`)
    and of the other sections a role acts on (heartbeat, a Driver messages its steering session,
    start a child, end, compacting, reload, the write guard): capability, means (two to four
    lines, this host only), and a mark of one word, `proved` or `untested`.
  - New command `chantier host [<capability>]` (host from the batch's record, else the session's
    host as the CLI resolves it today): prints the row(s); a row whose mark is not `proved`
    ends with one sentence, the same everywhere, saying that this path was never tried for real
    here.
  - New `docs/proofs/claude-code.md` and `docs/proofs/copilot.md`: every trial, date, batch,
    model and "proved/unproved" story of the two host cards, copied there, by capability. The
    host cards keep their text until child 15 removes it (no card is cut before the rewrite).
- **Depends on:** child 6.
- **Acceptance evidence.** Pytest: every row has a means and a mark of the two words; every
  `untested` row prints the sentence; every capability of the data appears as a heading of the
  proof file; `host` with an unknown capability lists the known ones.
- **Must not.** Edit the host cards; claim a mark the cards do not hold (a row is `proved` only
  where the card's mark says proved for the shipped default model; any doubt is `untested`).
- **Risk.** Long gate owed (CLI). AGENTS.md: a line for `host` (simplify-cards-Q13).

### Child 8: `brief-prompts` — `chantier brief` prints a role's whole prompt

- **Scope** (study-fable design line 3; answer 15's floor as judged above):
  - New `references/floor.md`, at most 1,200 LF bytes: the ten rules of "The floor" above, one
    line each.
  - New command `chantier brief <role> [<cr>] [--lease N] [--epoch N]` (`src/declare/brief.py`,
    handler in `src/commands/brief.py`; the CLI knows no role: the role's card, wrapper and
    first line are read from the data `src/plugin_files.py` and the Driver's prompt table
    already read). It writes the prompt to `<cr folder>/work/brief-<role>.md` (no CR: the
    planning folder's `work/`), byte-stable for a role, a version and a CR's facts, holding in
    order: the role's card whole, the floor, the facts (CLI, worktree, folder, specification,
    PR, rounds, notes, lease, `writes:`, `Rewrites:` for a Driver, `Team:`), the host rows the
    role uses (child 7), and the line "`$CHANTIER next` says what is due; `$CHANTIER help
    <topic>` when a line names one". It prints the short prompt to pass: the role's first line
    unchanged (the wrappers check it), then "Read <the file> whole, first.".
  - `driver_prompt.py`'s `driver_prompt_lines` and `plugin_files.py`'s `worker_prompt_lines`
    and `chief_prompt_lines` become the facts' source for `brief`; their current outputs in
    `take`, `round`, `handoff` and `order qa` stay unchanged in this child (switched in
    child 15).
- **Depends on:** child 7.
- **Acceptance evidence.** Pytest: `brief` for each of the 15 roles and both hosts writes a file
  that starts with the card and holds the floor once; two runs give the same bytes; the printed
  first line equals the wrapper's `Prompt starts with:`; a Driver's brief carries the same facts
  as `take`'s skeleton. Scenario step: a Driver started from `brief cr-driver <cr>`.
- **Must not.** Change `take`, `round` or `handoff`'s output; edit an existing card.
- **Risk.** Long gate owed. AGENTS.md: a line for `brief`; the rule "a role's contract lives in
  the cards … the parent names the card in its prompt" stays true (the CLI prints the card, it
  holds no contract of its own); the line says so.

### Child 9: `next-and-delta` — `chantier next`, `next:` lines and `status --since`

- **Scope** (answer 11; answer 13; study-fable 4.3 and 4.5):
  - New command `chantier next [<cr>] [--lease N | --epoch N]` (`src/declare/next.py`): advice,
    read-only. With `--epoch`, the steering session's due list for the batch, from the record:
    a free slot and the next CR to take, a CR handed back with no ask (`judge <cr>`), an order
    not done, a `restack owed`, a stale lease (`take --reclaim`), else `nothing due: wait`;
    the same for the Chief of Staff in direct mode (its `--epoch` as steering session). With
    `<cr> --lease`, the Driver's next step from the CR's events (`src/core/phases.py`): round,
    gate, push, ship, CI, verdict, handback. With neither, the Chief of Staff's view: asks to
    carry, ready CRs, a watcher not running.
  - `next:` lines at the end of `round`, `gate`, `push`, `ship`, `verdict`, `handback`, `order
    merged` and `order done`, from the same function, beside the four that exist
    (`src/commands/endpause.py:47`, `src/commands/opening.py:277` and `:333`,
    `src/rails_release.py:215`).
  - `status --since <seq>`: only what changed since a journal or event sequence, merged CRs as
    one count; prints the sequence to pass next time. Plain `status` is unchanged.
  - A `state:` line (the `batch:` line's counts by state and the due count) on the watcher's
    told blocks (`src/hub/watch_lines.py`) for the steering session.
- **Depends on:** child 8.
- **Acceptance evidence.** Pytest, parametrized over prepared records: each due kind appears in
  `next --epoch`; each Driver step in `next <cr>`; `status --since` lists only the changes.
  Scenario steps: `next` at three moments of a batch; a Driver follows `next:` lines.
- **Must not.** Record anything; order the safety steps (they stay refusals, answer 11); change
  plain `status`'s output.
- **Risk.** Long gate owed. A wrong `next:` line misleads every run: each is a scenario check.
  AGENTS.md: a line for `next` (simplify-cards-Q11, study-behaviour 3.5: the Foreman's
  heartbeat is 37 to 64 % of its weighted tokens).

### Child 10: `msg-inbox` — Agents message the steering session through the board

- **Scope** (answer 4; answer 13):
  - New commands `chantier msg <to> <kind> <text> [--lease N]` and `chantier inbox [--read
    <id>|all]` (`src/declare/msg.py`). `<to>`: `steering` (the batch's Foreman, or the Chief
    of Staff in direct mode), `cr:<id>` (that CR's Driver), `user`. `<kind>`: `anomaly`,
    `blocked`, `note`. One `msg@1` line per message in the project's `forge-journal.jsonl`
    through the one append function, its schema in `src/hub/schemas.py` and
    `hub/schemas.json`.
  - Delivery: the surface server's `events` topic carries `msg@1` lines; the Foreman's watcher
    (`src/hub/watch_reads.py`, which reads today only `merged@1`, `checks-red@1`,
    `wait-cleared@1`) wakes its session on `anomaly` and `blocked` addressed to `steering`;
    `note` lines wake nobody and are listed by `inbox` and at the steering session's next told
    block; in direct mode the Chief of Staff's watcher does the same for its batch. A Driver
    reads its own messages with `inbox --lease N`.
- **Depends on:** child 9.
- **Acceptance evidence.** Pytest: schema round-trip; a `note` does not wake, `anomaly` and
  `blocked` do; `inbox --read` marks read. Scenario step: a Driver's `msg steering blocked …`
  wakes the Foreman's watcher.
- **Must not.** Let the board or the server send anything to an agent itself; carry a message
  across projects.
- **Risk.** Long gate owed. AGENTS.md: the journal's writers and the watcher's subscribed lines
  gain `msg@1`; a line for `msg` and `inbox` (simplify-cards-Q7).

### Child 11: `judge-asks` — The CLI words the ask to the user

- **Scope** (answer 11):
  - New command `chantier judge <cr> --epoch N` (`src/declare/judge.py`): from the CR's
    hand-back and the `handed back:` line's facts (`src/status/ready_line.py`: gaps, owed
    before the merge, the long gate's result, waits), prints either the ask ready to record,
    worded by the CLI, or the take-back command with its note; with `--record ["<one
    sentence>"]` records it through the same record `asks` writes, the Foreman's optional one
    sentence appended.
- **Depends on:** child 10.
- **Acceptance evidence.** Pytest over prepared hand-backs (ready, ready with gaps, a waiver, a
  local-run rule, a stack's top, blocked); the recorded ask equals the printed one. Scenario
  step: the Foreman's `judge` then the ask in `status`.
- **Must not.** Decide a merge; drop a gap or an owed item from the wording.
- **Risk.** Long gate owed. AGENTS.md: a line for `judge`.

### Child 12: `conflicts-and-retro-draft` — The early conflict check and the retro's draft

- **Scope** (study-fable-v2 child 5; answer 9's M5 fields):
  - New command `chantier conflicts <cr> --epoch N`: the early conflict check
    `foreman-conflict.md` describes, run over the CR and the batch's other working CRs, notes
    recorded on the CRs, one ask printed. Read-only git (`git merge-tree`, in the form that
    writes no ref); AGENTS.md names it.
  - New command `chantier retro draft --epoch N`: draft retro points from the batch's events
    (asks, blocks, refusals, Driver restarts, red gates, cost outliers), each with the fields
    `home:` (the M5 ladder: CLI, refusal, `next:` or state line, help topic, card line),
    `count:` and `why not code:` left for the author to fill.
- **Depends on:** child 11.
- **Acceptance evidence.** Pytest on a prepared repository with two conflicting branches and
  one clean pair; on prepared events for the retro draft. Scenario steps for both.
- **Must not.** Write a ref, a branch or the worktree; file a retro point.
- **Risk.** Long gate owed. AGENTS.md: lines for `conflicts` (and its read-only git) and `retro
  draft`.

### Child 13: `launcher` — One launcher in place of the `$CHANTIER` paragraph

- **Scope** (study-fable-v2 child 4): a launcher shipped with the plugin that decides the dev or
  plugin mode, checks `uv sync --check` and prints `sync pending: held by …` itself, running the
  CLI by the one method AGENTS.md describes (`uvx --from <plugin root>`, or in dev mode `uv run
  --no-sync --project`). The four `SKILL.md` keep their paragraph until child 15 replaces it
  with one line naming the launcher.
- **Depends on:** child 12.
- **Acceptance evidence.** Pytest of the mode choice on prepared folders; a trial in a real
  session that the host's allow rule matches the launcher as it matches today's `uv run` form
  (study-fable 8 left this unproved), recorded in the PR. A refused or unmatched launcher is not
  worked around: the child hands back blocked.
- **Must not.** Change the run method; install anything.
- **Risk.** Long gate owed. P10's sample commands (`src/commands/allow_samples.py`) change with
  the launcher: the allow rules the user granted may need one new rule (asked by preflight as
  today). AGENTS.md: the run-method paragraph names the launcher.

### Child 14: `roles-as-data` — Role data, its lint and generated wrappers

- **Scope** (answer 12; study-fable 4.7):
  - New `skills/chantier/roles.yaml`: per role, name, kind (`steering`, `driver`, `worker`,
    `review-step`, `critic`), started by, tools, writes (`none`, `worktree`, `cr-folder`), reply
    format, card file, first line, description, host specifics.
  - New commands `chantier roles lint` (a role's card under its budget once child 17 sets them,
    no date, batch name or trial mark, a reply format that exists, a kind that may be an
    outside role) and `chantier roles build` (writes `agents/*.md` and
    `com.github.copilot/agents/chantier-*.agent.md` from the data). In this child the generated
    wrappers are byte-identical to the committed ones.
  - Project roles: a `roles:` list in a project's `chantier.yaml`, each naming its card file and
    kind; `roles lint` refuses any kind but `worker`, `review-step` and `critic` (answer 12);
    the floor and the write guard apply to them as to chantier's own.
- **Depends on:** child 13.
- **Acceptance evidence.** Pytest: `roles build` output equals the committed wrappers for both
  hosts (replacing the "bodies identical" half of `tests/test_plugin_files.py`); `roles lint`
  refuses a steering kind in a project role, a missing card, a missing reply format.
- **Must not.** Add, remove or rename a role (answer 1); change a wrapper's bytes in this child.
- **Risk.** Long gate owed. AGENTS.md: "`agents/` and `com.github.copilot/agents/` are
  hand-written" becomes "generated by `roles build` from `skills/chantier/roles.yaml`": needs
  the owner's word (open question 3); until it is given, the child keeps the wrappers
  hand-written and `roles build` serves only as a check.

### Child 15: `cards-rewrite` — Rewrite every card in one pass; remove the old set

- **Scope** (answers 14, 15, 17; the swap):
  - Every file under `references/` (role cards, the 32 pieces, `concepts.md`, the session-start
    cards, the host cards, templates and layouts, `routing.md`, `init.md`, `review-step.md`,
    `forges/`), the four `SKILL.md` and the wrapper bodies (through `roles build` if open
    question 3 allows, else by hand, both hosts identical), rewritten to the desired state in
    one PR.
  - A card holds: the role's goal, what it owns, at most five nevers of its own, how it ends,
    its reply format; nothing the floor, a topic, a refusal, a `next:` line or `--help` holds.
    Card budgets (study-fable 4.2, the targets, open question 4): Chief of Staff 6 KB, Griller
    4 KB, Foreman 4 KB, CR and stack drivers 4 KB, release driver 3 KB, QA driver 2 KB,
    Verifier 3 KB, Inspector 2 KB, the other workers and critics 1.5 KB, board-griller 2 KB;
    floor 1.2 KB; a topic 1.5 KB.
  - Rare cases become topic files in `references/topics/`, `topics.json` repointed to them;
    `foreman-stack.md` becomes the `stack` topics; a stack batch adds one line through `brief`.
  - The host cards leave the start: their rows are the data of child 7 printed by `brief` and
    `host`; their history is already in `docs/proofs/`; what stays is topics.
  - Removed in the same PR: `startup-manifest.json`, `startup-core.md`, `role-core.md`,
    `host-core-claude-code.md`, `host-core-copilot.md`, the 32 pieces, `reload-rules.md`
    (the floor replaces it), and every old card text not carried.
  - Carried into the cards: answer 8's list (the Chief of Staff settles alone a refused
    `--force-with-lease` push or rebase of a `chantier/*` CR branch of the batch, a refused
    `gh pr ready` or `gh pr edit --base` on the batch's PRs, a chantier subcommand refused in a
    chain run again alone, and tells the user in the report; it still asks before the five
    listed); answer 13 (direct mode: the Chief of Staff gets the Foreman's card and tools);
    answer 11 (`next` is advice, safety steps are refusals, the CLI words the ask); answer 4
    (only `anomaly` and `blocked` wake); the three "close behind" rules where they apply.
  - CLI outputs switched in the same PR: `take`, `take stack` and `order qa` print the lease and
    the `brief` command in place of the skeleton; `round` and `handoff` stop printing every
    worker's opening lines (a Driver runs `brief <role> <cr>`); `driver:refused` no longer reads
    the Foreman's piece; `src/status/ready_line.py`'s `rules:` names the floor;
    `src/board/griller.py`'s fixed brief names the Griller card's section "Started from the
    board" (kept by that name, as AGENTS.md names it) and no longer the host card;
    `hooks/register.tsx`'s `session.compact` reload message names the floor.
  - Rule ids: every never/must/only/always sentence of a card and every floor line carries
    `[R-nnn]`; `references/rules.json` holds id, card, kind (`floor`, `role`, `format`); the
    phrase tests are converted to id pins in the same PR (M13): `tests/test_role_cards_split.py`,
    `tests/test_startup_manifest.py`, `tests/test_start_reading.py` (replaced by a per-role
    test of `brief`'s bytes), `tests/test_session_start_split.py`,
    `tests/test_stack_chain_cards.py`, `tests/test_rebase_rules.py`, `tests/test_reload_rules.py`,
    `tests/test_release_template_card.py`, and the card reads of the other tests listed by
    `git grep references tests/`.
  - Docs: links to removed files fixed (`docs/`, `README.md`, `CONTRIBUTING.md`);
    `docs/incidents.md` receives the stories behind removed patches.
  - The Driver works by Coder rounds, one family per round (workers, Drivers, Foreman, Chief of
    Staff and Griller, host and shared), in the one PR.
- **Depends on:** child 14.
- **Acceptance evidence.** `just check`; the per-role `brief` byte figures beside the old start
  readings in the PR's Deliverables; `just quiz` on every role with the new cards against the
  baseline of child 5 (the new cards score at least as well, per role); `just scenario` green;
  every link resolves (`tests/test_plugin_files.py`).
- **Must not.** Keep two card sets or a `cards:` switch (answer 14); add a role; leave a rule of
  kind floor out of the floor; merge before child 19 (the merge rule).
- **Risk.** The highest: every role's contract changes at once. Long gate owed; `just mod` owed
  (the hook's reload message). AGENTS.md: the lines that name the cards' layout (the startup
  manifest, the cores, the reload rules) follow the new layout. A Driver's context: the
  rewrite runs as Coder rounds, and a Driver that hands back on context is retaken as usual.

### Child 16: `cards-compare-review` — Read and compare: nothing important lost

- **Scope** (answer 17; answer 10; study-fable section 5):
  - The inventory: one row per behaviour of the old cards (at child 15's base), section by
    section, seeded by CR-471's `work/tables.md`
    (`4-batch/3-done/471-slim-the-startup-cards-of-the-three-role/work/tables.md` in the
    planning folder) and `evals/SCORECARD.md`'s rails: id, role, trigger, behaviour, source
    `file:line`, kind (a to f of study-fable 3), new home (card, floor, CLI refusal, `next:`
    line, help topic, proof file, incidents file, judged inferable), check.
  - Each row with no home is restored, as a topic, a refusal or a `next:` line (a card line
    only within its budget). A row "judged inferable" carries a quiz case (child 5) that the
    role's model passes three times out of three with no card text for it.
  - Rare incident rules with no CLI trigger become topics with `review_by` set to the next
    minor version (answer 10).
  - The inventory is committed as `docs/proofs/cards-inventory.md`; the PR's Known gaps names
    the two lists the owner reads (every row of kind a, every row "judged inferable" or moved to
    the incidents file).
- **Depends on:** child 15.
- **Acceptance evidence.** Every rule id of child 15's `rules.json` appears in a row; every row
  has a home and a check; every "inferable" row's quiz case passes 3 of 3; a test fails on a row
  whose home names a topic, refusal or line that does not exist.
- **Must not.** Grow a card past its budget to restore a rule; drop a row of kind a.
- **Risk.** Long gate owed if a topic, refusal or line is added (cards or CLI). No AGENTS.md
  change.

### Child 17: `card-gates-pytest` — Budgets, history lint and rule ids as pytest gates

- **Scope** (answer 9: M1, M2, M3, M4, M8, M12, M13):
  - M1: `references/budgets.json` (file, limit, owner role) and `tests/test_card_budgets.py`:
    each card's LF bytes at or below its limit, every `*.md` under `references/` has a row, the
    sum at or below a constant in the test. The limits are the sizes child 15 reached, each at
    or below its target (open question 4).
  - M2: each role's measured path (`brief`'s output plus the topics its common path names),
    per host, at or below the role's limit.
  - M3: no date, batch name, CR id, PR number, "proved", "unproved", "trial", "the user's
    answer", model name or token count in `references/**/*.md` and the wrappers; exceptions in
    `references/lint-allow.txt` with a rule id and a reason; a stale exception fails.
  - M4: every `[R-nnn]` in a card has one row of `rules.json` and the reverse; the row's `check`
    names an existing pytest node, scenario step, scorecard rail or quiz case; a row with no
    check has kind `inferred` and a quiz case.
  - M8: detectors move from `evals/kit/detectors.json` into `rules.json` (`detector`, its
    positive and negative example), checked by pytest.
  - M12: a retired row (`retired: <version>, <reason>`) stays, its id never reused and never in
    a card.
  - M13: no assertion in `tests/` on a card literal longer than 40 characters outside the
    registry test, but marked, counted exemptions.
- **Depends on:** child 16.
- **Acceptance evidence.** The new tests pass on the stack's head and fail on a prepared
  violation of each (a card over budget, a date in a card, an id with no row, a phrase pin);
  `just test` within AGENTS.md's time limit.
- **Must not.** Raise a limit above child 15's reached size; exempt a floor rule.
- **Risk.** Long gate owed (cards may gain ids or lose history lines). No AGENTS.md change.

### Child 18: `card-gates-process` — The retro ladder, the owner's line and the measure's place

- **Scope** (answer 9: M5, M6, M10, M11, M14, M7's place in the release):
  - M5: the Retro critic's card asks each point for `home:`, `count:` and `why not code:`, and
    drops a point without them; `chantier validate` checks those fields in a `retro.md`
    (read-only).
  - M6: the Inspector's card checks that a card diff quotes the measure line (key and count of
    `behaviour-<version>.json`) or carries the owner's line.
  - M10: `evals/results/behaviour-accepted.md` (accepted stumbling, re-asked when its rate
    doubles); the S-list of each measure is filed by the Chief of Staff after the release retro
    or answered there.
  - M11: a step of `.github/workflows/ci.yml` (job on `ubuntu-latest`, on `pull_request` only:
    a push event has no body) that fails a PR touching `references/floor.md` or
    `references/budgets.json` unless its body holds "Floor change approved: <user>, <date>" or
    "Budget change approved: <user>, <date>". Its environment: GitHub's runner, the PR's body
    from the event payload, no local cache; only its first CI run proves it.
  - M7: `evals/README.md` "Before a release: the claims" and `docs/release-process.md` list `just
    behaviour` for the version, newer than the last card change, with its regressions answered,
    or "no measure: <reason>" in the claims file.
- **Depends on:** child 17.
- **Acceptance evidence.** Pytest for `validate` on a prepared `retro.md` (fields present,
  missing); the CI step proved by its first run on this PR (a prepared touch of `budgets.json`
  without the line fails, then passes with it), recorded in the PR.
- **Must not.** Let a Driver write the owner's approval line (it is the user's word).
- **Risk.** Long gate owed (cards). A CI job change: the first run proves it.

### Child 19: `cards-real-run` — One real batch on the new cards, measured

- **Scope** (answer 14: the real-run measure before the swap; study-fable-v2 child 1):
  - One real batch run on the new cards at the stack's head (method: open question 5), measured
    with `just behaviour --since <the run's start>`, compared with the baseline
    `behaviour-0.15.1.json`: card bytes per role, turns, CLI errors and the S-list, Driver runs
    per CR, the Foreman's and the Chief of Staff's wake shares, cost per CR.
  - `just quiz` on every role, on the old cards and the new, side by side.
  - Results committed as `evals/results/behaviour-<version>-new-cards.json` and `.md` and
    `evals/results/quiz-<version>.json`; the budgets of child 17 confirmed at what the run read,
    or a raise asked with the owner's line (M11).
- **Depends on:** child 18. Top of the stack.
- **Acceptance evidence.** The measure files; every role's card bytes read below its old
  figure; no floor rule's detector worse than the baseline; every quiz case at least as good as
  on the old cards; the S-list's new lines filed or accepted (M10).
- **Must not.** Change a card to pass the measure without a new quiz and measure.
- **Risk.** Top of the stack: owes the local Windows long gate (`chantier gate <cr> scenario`)
  at its head, and the pipeline's `just scenario (ubuntu-latest)`. Model and agent cost of a real
  batch. No AGENTS.md change.

## Evidence for the program

- Each child's own acceptance, above.
- The push subcommand's auto-mode trial recorded in child 1's PR before child 15 cuts the cards.
- Child 19's measure: every role's real reading below the old one, and the quiz no worse on any
  role, before child 15 merges.
- Host and default matrix (the program changes what each host reads at boot):
  - Claude Code, shipped defaults: every child's tests and the scenario; child 1's trial; child
    19's real run.
  - Claude Code, a project with its own `chantier.yaml` roles (child 14): `roles lint` tests.
  - Copilot, shipped defaults: `brief` and `host` tests on the Copilot rows and wrappers (child
    8, 7, 14); no real run (none was ever seen on this machine): the host rows say untested.

## Open questions

1. **The hook's deny list.** Answer 18 lists "the refusals" among the tools; answers 6 and 7
   reframed the never-rules question without choosing. Does "the refusals" include the hook
   refusing, for the agents it guards, `git merge`, `gh pr merge`, `glab mr merge`, `git reset
   --hard`, `git clean`, `git stash`, plain `git push --force`, `git checkout -- <files>`, `git
   restore`, `pkill` and `killall` (child 3), or only the CLI's own refusals (child 2)?
2. **How many tries prove the push subcommand.** The classifier is not steady (study-classifier:
   five identical pushes in one turn, one refused). Is one passing try from a Driver enough, or
   how many passing tries, with no refusal, does the user want before the cards stop teaching
   the ladder?
3. **Generated wrappers.** AGENTS.md says `agents/` and `com.github.copilot/agents/` are
   hand-written. May child 14 make them generated by `roles build` (and change that line), or
   do they stay hand-written with `roles build` as a check only?
4. **Budgets.** Are study-fable 4.2's card budgets (6, 4, 3, 2 and 1.5 KB; floor 1.2 KB; topic
   1.5 KB) hard targets the rewrite must reach, or does child 17 freeze what child 15 reaches,
   each at or below its target or raised with the owner's line?
5. **The real run before the swap.** The plugin loads from the main checkout, and during an eval
   the main checkout does not change. How is child 19's real batch run on the new cards before
   child 15 merges: an eval whose session loads the plugin from the stack's top worktree, a
   batch run by hand on that worktree, or another way the user names?
6. **The steering session's push.** With `chantier push` requiring the CR's lease, does the
   Chief of Staff's route of answer 8 keep its plain `git push --force-with-lease` (as today), or
   may the steering session run `chantier push <cr> --epoch <n>` with no lease?
7. **A protected branch.** Answer 7's rails say "never the default or a protected branch". The
   CLI can refuse the default branch and any branch not `chantier/*` without the forge; a
   `chantier/*` branch the forge protects is then refused by the forge's own push rule. Is that
   enough, or must `push` read the branch's protection on the forge first (a new forge read)?
8. **Merging children 1 to 14 before the swap.** They keep the old cards working. May each merge
   as soon as it is ready, or does the user want the whole stack merged together after child
   19?
