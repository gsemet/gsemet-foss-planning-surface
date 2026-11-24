# Push a CR's own branch through the CLI: `chantier push`

Child 1 of 28 of the program `simplify-cards-and-prompts` (its `03-change-spec.md`, "Child 1", and
its `02-answers.md` answers 5-8 and 17-22 rank above this file). One PR of the stack batch
batch-31. Paths below: `src/` is `skills/chantier/scripts/cli/src/chantier/`, `tests/` is
`skills/chantier/scripts/cli/tests/`, both in the chantier repository. Code was read at
`origin/main` `8a960d34`.

## Goal

The owner's words (answer 7): the host's auto-mode classifier refuses a Driver's force push of its
own CR branch, the Driver stops, and the Chief of Staff asks the user a question it should settle
alone. Chantier is about PRs, so a sub-agent's force push of its own CR branch must not stop it. A
CLI subcommand runs the `--force-with-lease` push itself, for GitHub and GitLab, and **says plainly
that it exists to declare the operation legitimate** in what the Driver is doing: chantier's own
update of the CR's own branch after a rebase, with the lease held.

Measured cost (study-classifier, `work/study-classifier.md` of the program): 13 classifier refusals
of force pushes in 12 days, each one a lost Driver, and 4 questions to the user; 83 % of the force
pushes agents typed were compound commands that no allow rule matches (12 of the 13 refusals were
compound).

## Place in the chain

- **Base:** batch-31's stack top when this CR joins: CR-485's branch
  (`chantier/batch-31/cr-485-tui-tab-zones-per-panel-scroll-newest-fi`), unless CR-485 has merged,
  then `main` (program F16).
- **Depends on:** nothing of the program; it is the first child.
- **Depended on by:**
  - child 2 (`sc02-cli-near-misses`) and every later child: built on this branch;
  - child 3 (refusals name the next step): this command's refusals already name it, child 3's gate
    will check them;
  - child 5 (`sc05-behaviour-measure`): counts `chantier push` refusals, the proof of this child;
  - child 12 (`next:` lines): prints a `next:` line at the end of `push`;
  - children 20 and 22 (the new Driver and Chief of Staff cards): name `chantier push` as the
    Driver's one way to publish, keep the refused-push route;
  - child 28 (real run): measures the `chantier push` refusal rate.
- **The smoke trial** below is recorded in this PR before any card child (19 and up) starts
  (answers 18 and 22, F3).

## Decisions carried

| Source | Decision | Where below |
| --- | --- | --- |
| Answer 7 (Q5) | A CLI subcommand runs `--force-with-lease` itself, GitHub and GitLab; it states the operation's legitimacy; rails: recorded `chantier/*` branch, never the default or a protected branch, lease held, clean worktree; AGENTS.md gains a git exception and a network use; a trial in auto mode, compound form, before any card is cut; refused through `cli.run` like `gate` | Command, Rails, AGENTS.md, Trial |
| Answer 8 (Q5b) | The steering session's refused-push route stays (the Chief of Staff runs a refused `--force-with-lease` push of a batch CR branch alone and reports) | Out of scope; AGENTS.md sentence |
| Answer 18 | Tools first; the push subcommand comes first and its trial runs before any card is cut | Place in the chain |
| Answer 22, F3 | The trial is a smoke test: 5 tries in compound form, permission mode recorded; one refusal recorded, tried once alone, then the program stops; the proof is the rate measured later | Trial |
| Answer 22, F16 | Base: batch-31's stack top when it joins | Place in the chain |
| Answer 22, F17 | A claim about the host or the classifier not proved here is marked "unproved" | Trial, Risk |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | Evidence |
| Answer 22, F21 | `chantier push` is the one way a Driver publishes its branch; never a retry after a refused `git push`; a refused `chantier push` is not followed by a raw push | AGENTS.md |
| Answer 22, Q2 | Five tries as the smoke test | Trial |
| Answer 22, Q6 | The steering session keeps plain `git push --force-with-lease`: no lease-free form | Rails, Out of scope |
| Answer 22, Q7 | No forge read of branch protection; the forge's own refusal printed verbatim | Push |
| Answer 22, Q8 | Nothing merges while the owner sleeps; the child is presented as ready | Hand-back |

## What changes

### 1. The command (`src/declare/delivery.py`, new `src/commands/push.py`)

`chantier push <cr> --lease N [--unit stack|O-k]`.

- Declared in `src/declare/delivery.py`'s `register` with `add_command(sub, "push",
  "chantier.commands.push:push", <help>, BATCH)`, a positional `cr`, `add_lease(s, required=True)`
  and an optional `--unit` (below). No `--epoch`, no `--force`, no `--no-verify`, no remote or
  branch argument.
- The help text says why the command exists, in substance: "push the CR's own recorded `chantier/*`
  branch from its worktree with `git push --force-with-lease`: chantier's own update of the CR's
  branch after a rebase, declared legitimate by this command, with the lease held; never another
  branch, never `--force`, never `--no-verify`, no forge call". Keep it one sentence family; the
  Driver words it.
- **Which lease** (the program: three leases count, the CR's own, the stack's for a CR of a stack
  batch's chain, an order's for a QA order's unit). One `--lease N` cannot tell three units apart
  (lease numbers are small and repeat across units, and a stale CR lease number could match the
  stack's), so the unit is named:
  - no `--unit`: the CR's own lease (the CR Driver, the Release driver);
  - `--unit stack`: the stack lease; refused unless the batch's mode is `stack` and the CR is in
    `stacks.chain(d)` (`src/stacks.py`);
  - `--unit O-k`: that order's lease; refused unless the order exists, is of kind `qa` and its
    `cr` field names this CR (so no order can push a branch that is not its own CR's).
  - A unit with no lease at all (`leases.lease_of(...) is None`: a batch opened before leases) is
    refused: "push needs a held lease; <unit> has none" (no lease-free form, Q6).

### 2. Rails, all checked before any git write

Each refusal exits non-zero, runs no `git push`, records nothing, and says what to do next.

| Rail | Check | Exit | The refusal names |
| --- | --- | --- | --- |
| CR known | `crs.batch_cr(repo, args.cr, args.batch)` | 1 (as today) | the batch |
| Branch recorded | `CrEntry.branch` is not empty | 2 | `take <cr>` records it |
| `chantier/*` | `c.branch.startswith("chantier/")` | 2 | "push only pushes a CR's recorded chantier/* branch" |
| Not the default | `c.branch != repo.config["default_branch"]` | 2 | same |
| Lease given | `leases.require(repo, d, unit, args.lease, f"push {c.id}")` (not `ended_ok`) | 2 | "needs --lease <n> (the number take printed)" |
| Lease held | `leases.claim(b, unit, args.lease, what=f"push {c.id}", required=True)` (not `ended_ok`, no `epoch`) | 3 `claim lost` | as `claim` says today |
| Worktree exists | `crs.cr_worktree(c)` | 2 | as today (its Driver creates it) |
| Worktree clean | `git status --porcelain --untracked-files=normal` empty, in the worktree | 2 | "commit first, then push" |
| HEAD on the branch | `git symbolic-ref --quiet --short HEAD` in the worktree equals `c.branch` (a detached HEAD fails too) | 2 | "check out <branch> in <worktree>" |

Order of work, so that the batch's lock (`LOCK_TIMEOUT_S` = 30 s, `src/core/files.py`) is never
held during a network push:

1. Reads with no lock: the CR, the unit, `leases.require`, the branch rails, the worktree rails.
2. A short session that claims the lease: `leases.renewed_in_session(repo, batch, unit,
   args.lease, what=f"push {c.id}", required=True)` (it saves the renewal with its `lease` event).
   A lost claim stops here: nothing pushed.
3. The push (section 3), outside any lock.
4. A second short `RenderedBatch(repo, batch, actor="driver")` that runs `leases.claim` again and
   `b.log("push", c.id, unit=unit, branch=c.branch, head=<pushed sha>, expected=<expected sha or
   "">)`. Should the claim be lost between 2 and 4 (another session took the unit meanwhile), the
   command prints that the push ran at `<sha>` and that nothing was recorded, and exits 3.

The `push` event is free-form (`EventRecord` takes extra keys): no journal type, no
`hub/schemas.json` change. The Driver checks that no reader takes the `head` of every event kind
(readers filter by kind today, e.g. `crs.py`'s `verdict` read).

### 3. The push

From the worktree (`cwd=cr_worktree(c)`):

```
git push --force-with-lease=<branch>:<expected> <remote> HEAD:refs/heads/<branch>
```

- `<remote>`: `repo.config["remote"]`.
- `<expected>`: `git rev-parse --verify --quiet refs/remotes/<remote>/<branch>` in the worktree.
  Absent: the expectation is empty (`--force-with-lease=<branch>:`), so git creates the branch
  only if the remote has none.
- No fetch before the push: the expectation is what the worktree last saw, which is the point of
  the lease.
- Never `--force`, never `--no-verify`, never `-u` (not needed: `ship` reads
  `refs/remotes/<remote>/<branch>`, which git updates after the push through the remote's fetch
  refspec).
- Run through `subprocess` (or a small helper beside `core/git.py`'s `git`) so that git's own
  stderr is kept as git printed it: `core/git.py`'s `git()` rewrites it into one line prefixed
  with the command.
- When git refuses (a stale lease, a protected branch, a server hook): one chantier line
  (`push <cr>: git refused the push of <branch>; nothing recorded`), then git's text verbatim,
  exit `EXIT_EXTERNAL` (4). Nothing is retried. No forge read of branch protection (Q7).
- Success prints one line: `pushed <branch> at <short sha> (was <short expected> | new branch on
  <remote>)`.
- The same code serves GitHub and GitLab: git only, no `gh`, no `glab`.

### 4. Never through a profile or the server

- `src/core/remote_wire.py`: `"push"` joins `NEVER_REMOTE`.
- `src/clients/remote.py`, `forward`: today `gate` is the one `NEVER_REMOTE` command that a profile
  refuses (the others run locally). `push` joins it: a new constant beside `GATE`, e.g. `PUSH =
  "push runs on the machine that holds the worktree, not through a profile: run it there, or here
  with --profile local"`, raised with `EXIT_USAGE`, with the server never called.
- `src/board/cli_run.py`, `judge`: refuses `push` already once it is in `NEVER_REMOTE`
  (`cli.run: push does not run through the server`); the test proves it.

### 5. Lines that point to it (CLI output only; no card text)

- `src/driver_prompt.py`, `_rewrites_line`: the rebase half is unchanged; the push half names
  `$CHANTIER push <cr> --lease <n>` in place of `git -C <worktree> push --force-with-lease -u
  <remote> <branch>`:
  - `own branch`: `git -C <worktree> rebase <base>, then $CHANTIER push <cr> --lease <n>, one
    command each, on your own CR branch only (<branch>): …` with `<cr>` filled from the block's
    `fill["<cr>"]`, `<n>` left as the placeholder `take`'s `lease:` line fills;
  - `batch branches`: `for each CR branch of the stack listed above (chantier/*), git -C <worktree>
    rebase <base>, then $CHANTIER push <cr> --lease <n> --unit stack, one command per branch, …`;
  - the scope sentence (`chantier's normal flow, pre-authorized by the playbook; never the default
    branch, a protected branch, another branch, a plain --force or a rebase --exec.`) stays.
- `src/commands/driver.py`, `_take_stack`: the stack's `lease:` line adds `push <cr> --unit stack`
  to the commands that take `--lease <n>`.
- `src/commands/delivery.py`, `_off_worktree`: the "not pushed" line keeps its words `is not
  pushed` / `is at <sha>` (the scenario reads them) and names the command: `… not this head: push it
  with chantier push <cr> --lease <n>, then ship again`.
- `src/commands/allow_samples.py` (P10): unchanged. It keeps its force-push samples, since the
  steering session keeps the plain push (Q6), and adds none for `push`. Whether the user's
  `chantier *` allow rules match what agents type is **unproved**: study-classifier found such rules
  seldom match compound forms.

Known and accepted gap: `references/concepts.md` ("A Driver's prompt", "The two texts the CLI
copies"), `driver.md` (the Push bullet) and `hosts/claude-code.md` still quote the `git push
--force-with-lease` form; this child changes no card's text (program rule "Card text"); children 20,
22 and 23 rewrite them. The PR's Known gaps names it.

### 6. AGENTS.md

Edit the repository's root `AGENTS.md` (as on `origin/main`):

- **The CLI's named git exceptions** (the bullet "The CLI has named git exceptions: …"): add
  `push`: one `git push --force-with-lease=<branch>:<expected>` of a CR's recorded `chantier/*`
  branch (never the default branch), from its worktree, by a caller holding the lease, never
  forced, never `--no-verify`, nothing retried. Fix the closing "The rest of the CLI keeps no git
  write." so that it stays true.
- **The "writes only" sentence** of the no-setup bullet: add that `chantier push` updates a CR's
  recorded branch on the remote (and the worktree's tracking ref), so the sentence stays true.
- **The network list** (the no-setup bullet's "except …"): add `chantier push`'s push.
- **Profiles:** `push` joins `gate` wherever AGENTS.md lists the commands that never run through a
  profile: the `cli.run` list ("any but `serve`, `webui`, `watch`, `live`, `login`, `logout` and
  `gate`") and the `login` paragraph ("(`gate` is refused there)").
- **The named-exceptions paragraph** gains a `push` entry, with:
  - what it is (as above) and that the command states the operation's legitimacy: chantier's own
    update of the CR's own branch after a rebase, with the lease held;
  - its source: the user's answers simplify-cards-Q5 (2026-11-24, answer 7) and Q22 (answer 22),
    and study-classifier's measure: 13 classifier refusals of force pushes in 12 days, each one a
    lost Driver, and 4 questions to the user; 83 % of the force pushes typed as compound commands
    that no allow rule matches;
  - F21: `chantier push` is the one way a Driver publishes its branch; it is never run as a retry
    after a refused `git push`, and a refused `chantier push` is not followed by a raw push from
    the Driver; the refused-push route of answer 8 (the steering session) stays.

The PR quotes answer 7 as the owner's word for this subcommand.

## Out of scope (must not)

- Push any branch but the CR's recorded one; take a branch or remote argument.
- Read or write the forge (no `gh`, no `glab`, no branch-protection read: Q7).
- Push through a profile or the server.
- Add `--force`, `--no-verify` or a retry.
- Change a card's text (`references/`, `SKILL.md`, the agent files).
- Run a rebase, or offer a rebase subcommand (study-classifier: 1 refusal in 721 rebases).
- Give the steering session a lease-free form (no `--epoch`): it keeps plain `git push
  --force-with-lease` and its refused-push route (Q6, answer 8).
- Change P10's samples or write the host's auto-mode configuration.

## Acceptance evidence

### Pytest: new `tests/test_push.py`

Parametrized, in-process (the `chantier` fixture), on a prepared batch with a bare remote (the
helpers of `tests/batch_helpers.py`, `stack_world.py` for the stack case). Add `"push"` to
`tests/lease_args.py`'s `GUARDED`, so that the fixture passes the CR's lease, and to the scenario's
`World.lease_unit` the same way.

- Each refusal exits non-zero, records no `push` event and runs no `git push` (the remote's branch
  is unchanged, and a spy on `subprocess` or the remote's ref shows no push): branch not recorded,
  not `chantier/*`, the default branch, no `--lease`, a stale lease (`claim lost`, exit 3), a dirty
  worktree, HEAD on another branch, a unit with no lease, `--unit stack` outside a stack's chain,
  `--unit O-k` for an order that does not name the CR.
- A valid call (new branch: empty expectation; and an update after a rebase) pushes, the remote's
  branch is at the worktree's head, one `push` event holds `branch`, `head`, `expected`, and the
  lease's expiry moved later.
- `--unit stack` from the stack lease pushes a chain CR's branch.
- The remote moved since the tracking ref (a second clone pushed to the branch): git refuses, the
  command exits 4, its output holds git's text (`stale info` or `rejected`), nothing recorded.
- `push` is refused through a profile (exit 1, the server never called, as
  `test_remote_cli.py`'s gate case) and by `cli_run.judge` (`does not run through the server`).
- `test_driver_prompt.py`'s `_check_rewrites`: assert the new push half (`push <cr> --lease`, and
  `--unit stack` for the stack) and the unchanged rebase half and scope sentence.

**Time added to `just test`:** estimated 2 to 4 s (several bare-remote states); the PR states the
measured seconds, before and after on the same machine (F20).

### Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- A new case function (e.g. `push_own_branch`) in which a Driver commits, rebases on its base, runs
  `push <cr> --lease <n>`, then `ship` prints no "not pushed" line; and a refused `push` from a
  dirty worktree records nothing. Add it to the `gates` unit (GitHub) and to the `gitlab` unit in
  `UNITS`, raising their budgets if the measured time needs it.
- The scenario's `push` helper (rebase then raw `git push --force-with-lease`) may switch to the new
  command for the CR Driver's path; keep at least one raw push where the scenario plays the
  steering session's route.
- `scenario/README.md`, "## Coverage": one bullet naming `(unit: gates, gitlab)` and `(test:
  test_push.py::<the refusal test>)`, so that `tests/test_scenario_coverage.py` passes.
- The `take` check in `check_driver_skeleton` (it asserts `--force-with-lease` in the `Rewrites:`
  line) is updated to the new push half.

### Gates owed (AGENTS.md)

- `just check` and `just eval-dry-run` (a change under `src/`) at the rebased head before the first
  push.
- The long gate: `just scenario (ubuntu-latest)` green at the PR's head (CLI and scenario change).
- The local Windows `chantier gate <cr> scenario` only while this CR is the stack's top; it moves to
  the next child when that one joins on top.
- No change to `hooks/` or `types/`: no `just mod`.

### The smoke trial in auto mode (answers 7 and 22, F3, Q2)

Run by this child's own Driver (a subagent, in auto mode as the host shows it), once `push` works in
the worktree, before the PR is presented as ready:

- Build: `uv sync --locked --project <worktree>` once, then the compound form agents type, five
  times, each after a small commit or a rebase:
  `C="uv run --no-sync --project <worktree> chantier --project <planning>"; $C push <cr> --lease
  <n> 2>&1 | tail -3`.
- For each try, the PR's Deliverables record the exact command text, the session's permission mode
  as the host shows it, and the host's verdict: ran (with the command's line), or the refusal's
  text.
- The user's allow rules name the main checkout's path, so this worktree-build command is always
  judged by the classifier: the harder case; the record says so.
- On a refusal: record it, then try once more, alone, as a plain command. If that also fails, the
  Driver hands back blocked with the text, and the program stops for the owner. No workaround.
- The trial is a smoke test, not the proof. The proof is the `chantier push` refusal rate, measured
  later by child 5's tool (child 28's run). Until then the classifier's verdict on this text is
  **unproved**, and the PR says so.

### Host and default matrix

- **Claude Code, auto mode, shipped defaults:** the smoke trial (5 tries) and the scenario.
- **Claude Code, other permission modes:** not tried; the command does not depend on the mode.
- **Copilot:** untested (no run seen); the command is host-independent, and its classifier
  behaviour is unknown.
- **A project's `chantier.yaml` `remote` / `default_branch`:** the tests use the shipped `origin` /
  `main`; one refusal case sets a recorded branch equal to the configured default branch.

## Risk

- The long gate is owed (CLI and scenario).
- AGENTS.md: a third git exception, a network use, a profile refusal and the F21 sentence; answer
  7 gives the owner's word, quoted in the PR.
- The classifier's verdict on the command text is unproved until the trial, and only measured
  afterwards.
- Until the cards children, the prompts' `Rewrites:` line names `chantier push` while the cards
  name the raw push; both are allowed paths for the Driver meanwhile.

## Hand-back

Presented as ready; nothing merges while the owner sleeps (Q8). Children 1 to 18 may merge in
order once the owner says so. Deliverables: the trial's five records, the seconds added to `just
test`, the long gate's result. Known gaps: the cards still quote the raw push (children 20, 22,
23); the classifier rate unmeasured (children 5, 28).

## Open questions

1. **A stack driver's push of a CR whose own Driver still holds its lease.** With `--unit stack`,
   should `push` refuse while the CR's own lease is live or not confirmed (its Driver may still be
   working on that branch), or allow it, as today's raw push does? This specification allows it
   (no new refusal beyond the program's rails); a refusal would guard against two writers on one
   branch but could block a restack until `agents set <cr> - --epoch <n>`.
