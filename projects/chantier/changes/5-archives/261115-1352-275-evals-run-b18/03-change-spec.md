# Change Specification: run the real-foreman and real-direct evals on the chantier batch-18 leaves on main

## Goal

The user's words: "rajoute une CR qui pilotera les evals après tout (donc en dépendance de toutes
les autres tâches ouvertes du batch). Il me faudra les exécutions sur le nouveau Chantier."

Once every other open CR of batch-18 is merged, run each of the two quick sandbox campaigns once:
`real-foreman` ([evals/real-foreman/RUNBOOK.md](../../../../evals/real-foreman/RUNBOOK.md)) and
`real-direct` ([evals/real-direct/RUNBOOK.md](../../../../evals/real-direct/RUNBOOK.md)). Run them
with the chantier that `main` holds then, and deliver both reports and the campaigns' rows of
`evals/README.md` on one PR. The point is to measure the new chantier on the path a user takes,
with the Foreman and in direct mode, and to bring back findings.

## Decisions carried from the grill (02-answers.md, 2026-11-15)

1. Source: the user's word, quoted above.
2. The CR joins batch-18 on top of the stack and waits for every other open CR of the batch: the
   steering session records `order after <this CR> --note <every other open CR id, comma
   separated>`. At filing these were CR-268 to CR-274, with CR-274 being `workers-read-card` once it
   is added.
3. The two campaigns: `real-foreman` and `real-direct`, each once, on the sandbox, with main's
   chantier after the stack's merge.
4. Open points with no default: the recommended reading below stands, decided by the Chief of
   Staff. Each one is marked **(CoS reading)**. The user's own steps at the desktop are named
   exactly (section "The user's steps").

## Who does what

A campaign needs an operator session in the eval workspace, a new Code session of the Claude
Desktop app typed in by the user (not under Remote Control). Neither this CR's Driver nor the
batch's Foreman can start that session. The work splits in three.

| Part | Who | Why |
| --- | --- | --- |
| Pre-run checks (section "Phase 1") | this CR's Driver | read-only: `status`, `git`, `gh` |
| Sandbox reset (`sandbox.py reset --yes`) | the user, in a terminal | `evals/README.md`, "Preparation": the user does it; the only force push on the sandbox |
| Staging (`setup.py <campaign> <workspace>`) | the user, in the same terminal **(CoS reading)** | `evals/README.md` lists it under the user's preparation; it writes outside this repository (the workspace, its `.run.json`), where a Driver's worktree rules do not reach |
| Auto-fix off for the operator's session | the user, at the desktop | `evals/README.md`, "Before you start"; how to turn it off is **unproved** (`hosts/claude-code.md`, "Auto-fix events") |
| The operator's session: the go, merges, answers, audit, cost, `close --yes` | the operator session, started by the user's pasted prompt | the runbooks |
| Reading transcripts, writing both reports, the README rows, the PR | this CR's Driver (section "Phase 2") | `evals/README.md`, steps 5 and 6 |

**(CoS reading)** The operator does not write the report and opens no PR. It stops after
`close --yes` and leaves the audit's and the cost's outputs in a file next to the workspace (the
prompt's suffix below). So both reports come from one Driver, on one PR, under the batch's
Verifier and Inspector. The suffix changes nothing the run measures: it acts after `close --yes`,
when the batch is over.

## Order of the runs **(CoS reading)**

1. `real-foreman` first: it has never run on the sandbox.
2. Then `real-direct`.

One run at a time on the sandbox. A reset ends the run before it, so the second reset happens only
after the first operator has written its audit file and run `close --yes`.

## Modes **(CoS reading)**

- `real-foreman` in **`stack`** mode. Batch-18 itself ran as a stack, and most of its CRs touch
  that mode: the stack's one long gate and the per-CR waiver (CR-266), `ship` reading the PR's
  base from the forge (CR-270), the gate race on merge (CR-268), the mode switch (CR-267).
- `real-direct` in **`parallel`** mode, so it compares line by line with its run 1 (2026-11-12,
  parallel, same sandbox base if `kit/sandbox.json` has not changed since:
  [report](../../../../evals/results/real-direct-2026-11-12-run1.md)).

## The main checkout during the runs

AGENTS.md: during an eval the main checkout (`C:/Users/gaeta/Projets/chantier`) changes neither
its files nor its branch. The workspace gets the plugin from the user's install, which reads this
checkout live.

- Before the first reset, the main checkout is on `main`, at `origin/main`, with every CR of
  batch-18 merged. The steering session's fast-forward after the last merge puts it there.
- Its tracked files are clean (`git status --porcelain --untracked-files=no` prints nothing). The
  untracked files at its root (`commands.py`, `concepts.md`, `state.py` at the time of writing)
  are not plugin files. The Driver names them in its Phase 1 note and does not touch them.
- From the first reset to the second operator's `close --yes`, no merge, no fast-forward, no
  checkout and no edit of tracked files happens in the main checkout. Batch-18 has nothing left to
  merge then (this CR is its last), and the user starts no other work there. Writes of the planning
  folder (`.agents/changes/`, untracked) are the batch's record, not plugin files, and are allowed.

## Phase 1: the Driver's pre-run checks, then the user's steps

When it takes the CR, the Driver:

1. Checks that every other CR of batch-18 is `merged` or `cancelled` (`$CHANTIER status`).
2. Checks that `git -C C:/Users/gaeta/Projets/chantier rev-parse HEAD` equals `git -C
   C:/Users/gaeta/Projets/chantier ls-remote origin refs/heads/main`. Also checks that the branch is
   `main` and that `git status --porcelain --untracked-files=no` is empty.
3. Checks that `gh auth status` succeeds and that the account can push to
   `gsemet/chantier-eval-sandbox`
   (`gh api repos/gsemet/chantier-eval-sandbox --jq .permissions.push` prints `true`).
4. Records one note: `$CHANTIER note <cr> "pre-run: main at <sha7>, clean; gh ok; untracked at
   root: <list or none>"`.
5. If a check fails, it hands back `blocked question: <the failed check, as printed>` and ends.
6. Otherwise it hands back `$CHANTIER handback <cr> blocked question: the eval runs need the user
   at the desktop: run "The user's steps" of 03-change-spec.md, then answer done with the two
   workspace paths`, and ends. The CR waits, not the Driver: no Driver stays alive through two
   desktop runs.

The steering session passes the steps to the user. When the user says done, it sends the answer
with `order note <cr> --note "answer: done: <workspace 1>, <workspace 2>"`. A Driver is then taken
back as usual for a `question:` that has been answered.

## The user's steps

All commands run in PowerShell from `C:/Users/gaeta/Projets/chantier`. `<date>` is the day of the
run (`YYYY-MM-DD`). If the workspace folder already exists, add `b` to its name.

### Run 1: real-foreman, stack

1. In a terminal:

   ```powershell
   uv run --no-project python evals/kit/sandbox.py reset
   ```

   Read the plan, then:

   ```powershell
   uv run --no-project python evals/kit/sandbox.py reset --yes
   uv run --no-project python evals/kit/setup.py real-foreman C:/Users/gaeta/Projets/chantier-eval/real-foreman-<date>
   ```

   Keep what setup prints: the run's number `<n>`, the prefix, the `open` line, the `merge` line.
2. In the Claude Desktop app: open a new Code session on
   `C:/Users/gaeta/Projets/chantier-eval/real-foreman-<date>` (not under Remote Control). Turn
   Auto-fix off for it if you find the setting; either way, say whether it was off.
3. Type in that session:

   ```text
   /chantier:chief-of-staff foreman Run the chantier eval campaign real-foreman in stack mode: follow C:/Users/gaeta/Projets/chantier/evals/real-foreman/RUNBOOK.md. After close --yes, write the audit's output and both cost outputs, verbatim, to C:/Users/gaeta/Projets/chantier-eval/real-foreman-<date>.audit.md, then stop: write no report and open no PR in the chantier repository; batch-18's Driver for this eval CR writes it.
   ```

4. Do not type in that session or in the Foreman's session while it runs, except `ping` in the
   Foreman's session when the runbook asks for it (the 10-message limit; the report counts each
   `ping` as a human step). Wait until the operator says the audit file is written.

### Run 2: real-direct, parallel

1. In the terminal (only after run 1's operator has finished):

   ```powershell
   uv run --no-project python evals/kit/sandbox.py reset
   ```

   Read the plan, then:

   ```powershell
   uv run --no-project python evals/kit/sandbox.py reset --yes
   uv run --no-project python evals/kit/setup.py real-direct C:/Users/gaeta/Projets/chantier-eval/real-direct-<date>
   ```

2. A new Code session in the Claude Desktop app on
   `C:/Users/gaeta/Projets/chantier-eval/real-direct-<date>`, with Auto-fix as in run 1.
3. Paste:

   ```text
   /chantier:chief-of-staff direct Run the chantier eval campaign real-direct in parallel mode, in direct mode: follow C:/Users/gaeta/Projets/chantier/evals/real-direct/RUNBOOK.md. After close --yes, write the audit's output and both cost outputs, verbatim, to C:/Users/gaeta/Projets/chantier-eval/real-direct-<date>.audit.md, then stop: write no report and open no PR in the chantier repository; batch-18's Driver for this eval CR writes it.
   ```

4. Wait until the operator says the audit file is written.

### After both runs

Tell the Chief of Staff "done", with both workspace paths and whether Auto-fix was off in each.
Archive the Foreman's session of run 1 (`evals/README.md`, step 7). Keep the workspaces until the
PR of this CR is merged.

## Phase 2: the Driver writes the reports

Taken back after the user's "done", the Driver reads, read-only:

- each `<workspace>.audit.md` (the audit's run table, checks, judge and scorecard; `cost
  --explain`; `cost --by cr`) and each `<workspace>.run.json`;
- the workspaces' batch records (`uv run --locked --project C:/Users/gaeta/Projets/chantier
  chantier log <cr>`, run from the workspace, for the rows SCORECARD.md marks `by hand`);
- the transcripts of the run's sessions under `~/.claude/projects/` (the folders of the two
  workspaces and their `.worktrees`), and a sample of the PR diffs on the sandbox, read against
  each frozen CR's specification (`gh pr diff <n> -R gsemet/chantier-eval-sandbox`; the PRs stay
  readable after the reset closed them).

It re-runs neither the audit nor the judge: the audit runs before `close --yes`, and the sandbox
has been reset since run 1.

In its worktree, on its branch, it writes:

1. `evals/results/real-foreman-<date>-run<n>.md` and `evals/results/real-direct-<date>-run<n>.md`.
   These are the sandbox form of the name in `evals/README.md`, "Campaigns", with `<n>` the run
   number setup printed. The request's `<campaign>-<date>.md` is the staged campaign's form.
   Each report follows `evals/README.md`, "The report": verdict; the audit's `## The run` table
   pasted; what was tested; what happened per CR; numbered findings (what, why it matters, what to
   do); the scorecard of `evals/SCORECARD.md`, every rail marked `seen, right`, `seen, wrong` with
   evidence, or `not seen`; numbers (duration, cost total, breakdown and by CR, agents started,
   audit checks passed, steering share, `Judge: <n> pass, <n> fail, <n> not run`); for
   maintainers (chantier's version and commit, failed audit checks verbatim).
   Each report also says:
   - the mode, and whether Auto-fix was off;
   - any Auto-fix event seen and how the steering session handled it (the trial of
     `hosts/claude-code.md`, "Auto-fix events");
   - each `ping` and each refused send (J15);
   - any budget raise (to $30, once) or drop.
   The real-direct report names each unproved host line of its runbook ("What it proves on top of
   real-foreman") it saw work. It also compares line by line with run 1 when the sandbox base is
   the same.
2. In `evals/README.md`, table "Campaigns":
   - the `real-foreman` row: its "Last run" cell becomes `<date>, run <n>, stack: <verdict>, <m> of
     5 CRs merged, judge <line>, audit <passed>/<total>, $<cost>, [report](results/…)`, keeping
     the link to the 2026-11-12 report as the run before the sandbox. Its "Cost" cell is written
     from this first sandbox run (budget $20; the run's cost and duration), as real-direct's cell
     was after its first run.
   - the `real-direct` row: its "Last run" cell in the same form, for this run.
3. In `evals/real-foreman/RUNBOOK.md`, the "Cost and time" row of the table, written from this
   first run's report, as that row says it will be **(CoS reading)**. It is campaign
   documentation, not a file from the run.

Nothing else is committed: no transcript, no log, no screenshot, no audit file (`evals/README.md`,
step 6). It commits, pushes, opens the PR (title and body as the batch's rules say), runs the
Verifier and Inspector, and hands back ready.

The PR body lists each finding of both reports as a one-line candidate inbox item. The Chief of
Staff offers them to the user after the merge (systematic retro); the Driver files none.

## Checks and evidence

- `just check` passes at the PR's head (AGENTS.md).
- No long gate: AGENTS.md, "a change to the docs or the eval kit alone needs none". The PR changes
  only `evals/results/`, `evals/README.md` and `evals/real-foreman/RUNBOOK.md`. The steering
  session records it with `order waive <cr> --note "AGENTS.md: docs and eval reports only"` if the
  batch's frame asks for a gate. `evals/kit/` does not change, so `just eval-dry-run` and the
  kit's independent review do not apply.
- The Verifier checks against this specification:
  - both report files exist, with the README's sections in order;
  - each `## The run` table is the audit's, verbatim from `<workspace>.audit.md`;
  - each judge line and audit count match that file;
  - every SCORECARD.md row is marked;
  - cost is `not measured` rather than $0.00 where the CLI could not price it;
  - the README rows link to the new reports;
  - the diff touches only the three paths above.
- The scenario (`just scenario`) is not run: nothing it covers changes.

## Out of scope

- The campaigns `full`, `claude-planted`, `ticket-summary` and `copilot`.
- Copilot and GitLab: these runs are on Claude Code with GitHub only. The Copilot and GitLab
  trials stay the user's, later; both reports say "not covered: Copilot, GitLab".
- Fixing what the runs find: each finding becomes a candidate inbox item, not a change in this PR.
- Any change to `evals/kit/`, the runbooks' steps, the cards or the CLI.
- A second run of either campaign, or a run in the other modes.

## Open questions

None left for the user: the grill gave the open points to the Chief of Staff's reading, marked
**(CoS reading)** above (who stages, the operator stopping before the report, the order of the
runs, the modes, the real-foreman runbook's cost row).
