# `just scenario` under 5 minutes: independent units run in parallel

The second of three CRs (Scen-Q5, the user took Fable's plan whole): `baseline-and-legacy` comes
before it, `gate-rules` after it. This CR starts from main once `baseline-and-legacy` is merged:
a green long gate on main, and the legacy readers and their scenario cases (`old_words`,
`old_tree`, `backfill_cases`, the `confirmed` check of `release_on_stack` §15, `World.at`'s
prefix) already gone. If they are still there when the Driver starts, it stops and says so: they
are not this CR's to remove.

## Goal

The user's words: "Objectif: just scenario < 5 minutes". CR-228's long gate took 1,197.9 s on
GitHub and 1,195.5 s on GitLab, one after the other: about 40 minutes per gate. The scenario grew
about 8.5 times in ten days, every CR adding its cases to one long sequence on one temporary
repository, replayed whole for GitLab.

`just scenario` becomes about 9 independent units, each in its own temporary world, run 4 at a
time. GitLab runs only the forge-specific unit. The pure refusals move to pytest, in-process
and parametrized. Every coverage bullet of `scenario/README.md` still maps to a unit or a test,
a structure test checks it (FS-Q2), and a standing rule keeps the scenario from growing back. A
hung unit is killed and fails the run; slowness alone only warns (FS-Q1).

No change under `skills/chantier/scripts/cli/src/`. The CLI's behaviour does not move; only the
scenario, the tests, the justfile and the docs do.

## Inputs a Driver reads

- `scenario/run_scenario.py` (about 7,100 lines; its `scenario(w)` at l.540-1044 calls the
  cases in sequence; `main()` at the end), `scenario/README.md`, `scenario/fake_gh.py`,
  `scenario/fake_glab.py`, `scenario/fake_autosync.py`, `scenario/fake_session_usage.py`.
- `justfile` (the `scenario:` recipe runs `--forge github`, then `--forge gitlab`; `test:` runs
  pytest), `.github/workflows/ci.yml` (job `scenario`: `just scenario` on `ubuntu-latest`).
- `skills/chantier/scripts/cli/tests/` (pytest's `testpaths`): `conftest.py` has the `repo`
  fixture (a git repository, HOME and env isolated), the `chantier` fixture (calls
  `chantier.cli.main([...])` in-process) and `PLUGIN_ROOT`. Today: 72 tests, 18.5 s on the
  user's Windows machine (measured 2026-11-14 at `ce00ec3`).
- This CR's `analysis/scenario-analysis.md` (verdicts per case and section, duplicates, the
  split, the risks; line numbers as of 2026-11-14, before `baseline-and-legacy`) and
  `analysis/fable-advice.md` (the plan, the target units, measured process start times).
- `CONTRIBUTING.md` "Code standards": every `.py` file under `skills/`, tests included, keeps to
  at most 400 lines per file and 50 lines per function, enforced by `test_code_targets.py`.
  `scenario/` is outside `skills/` and is not held to them. `test_cli_runs.py` (324 lines) and
  `test_plugin_files.py` (250 lines) are already large: new tests go in new files.

## What changes

### Step 0: one instrumented run before any cut

Before any case moves, the Driver instruments today's scenario (main after
`baseline-and-legacy`) and runs it once per forge on the user's Windows machine. The run prints,
per case function and per section of the main batch (§1-§11), the seconds and the command count.
A command is a process the scenario itself starts (`subprocess.run` or `Popen`: `chantier`, the
fake forge, git, the sleepers), counted by one wrapper. The processes the CLI starts in turn are
not counted.

- The table and both totals go to `<work folder>/step0-baseline.md`, and the PR body quotes it.
- The unit budgets come from this table: the sum of the case seconds a unit keeps, minus the
  cuts below, rounded up. The budgets in Fable's table (below) are guesses until step 0 replaces
  them.
- The same counters stay in the runner afterwards: they feed the per-unit table printed on every
  run.

### The units

`scenario/run_scenario.py` gets a `UNITS` table, `{name: (budget_s, forges, [case, ...])}`, which
replaces the call sequence at the end of `scenario(w)`. The main batch's sections stay one
function, the first case of `parallel`. The target shape is Fable's 9 units. The Driver may move
a case from one unit to another when step 0 shows an imbalance; it keeps about 9 units and
records each move in the PR body.

| Unit | Forges | Cases (today's function names) | Budget (guess) |
|---|---|---|---|
| `parallel` | github | main batch §1-§11 slimmed (preflight once, open, CR rounds, ship and hand-back, steering: drop with its sleeper killed, order add and note; Foreman restart; lost Driver; merges and fast-forward of a clean main; one "cost line appears" check; event and forge call logs), `close_batch` (the close flow), `retro_cases` | 150 s |
| `stack` | github | `stack_batch`, `ready_words` (without its §8, which goes to pytest), `forge_stack_cli` (common part and GitHub part) | 120 s |
| `release` | github | `release` (it alone keeps "no approval covers the release PR's merge"), `granted_fixes` (live part), `release_last`, `release_on_stack` slimmed (the main path; §13 series dropped), `release_merge_on_approval` (its Windows-only close on a folder in use stays; its approval check folds into `release`) | 150 s |
| `gates` | github | `rails` (live part: the gate lock, the queue, the dead waiter, the reused pid), `gate_parallel` E2-E5, `cancel_during_gate`, `stop_own_gate` (live stop), `handback_proofs`, `gate_proof` | 120 s |
| `series-deps` | github | `batch_modes`, `dependencies` (live part: waits, a QA order holding a slot, the queued icons), `changes_tree` (live part: the folder following take, hand-back, merge and drop) | 70 s |
| `direct` | github | `direct_batch` (its `uuid-chief.jsonl` fixture written in the unit instead of restored from the main batch), `seat_handover` (batch-level part), `foreman_in_a_worktree` | 80 s |
| `surface-board` | github | `remote_board`, `external_surface`, `surface_autosync` | 100 s |
| `qa-driver` | github | `qa_on_head` (live part), `driver_liveness` (the restart path through a live Driver), `lost_messages` (its `.batch-number` and trash entry seeded in the unit instead of inherited from `release_merge_on_approval`) | 40 s |
| `gitlab` | gitlab | a slim ship and merge path (`open_pr`, `merge_pr` and the forge call-log shapes on `fake_glab.py`) and `forge_stack_cli`'s GitLab part | 70 s |

- **One process per unit, one world per unit.** Each unit builds its own `World` (or
  `SurfaceWorld`) in its own `mkdtemp`. `LOG`, `CHECKS`, `ARGS` and `OPENED` stay module globals,
  separate per process. No unit reads another unit's state: each hidden dependency the analysis
  names (`w.number_after`, `uuid-chief.jsonl`, `OPENED`, `previous = w.name`, the trashed CRs) is
  seeded inside its unit.
- **GitLab runs only the `gitlab` unit** (Scen-Q5, decision 3 of the intake). The other units run
  on GitHub alone, on both machines. P10's `gh extension list` block is GitHub-only already.
  `external_surface`'s GitLab branch differs only by forge commands, which the `gitlab` unit
  covers.
- **Scenario CLI calls stay real processes** (`[sys.executable, "-m", "chantier", ...]`), end to
  end. In-process calls belong to pytest only.
- **Every unit ends with one write-scope assertion:** `git status --porcelain` of the unit's
  project shows nothing outside the planning folder (today's `lifecycle_regressions` check, now
  at the end of every unit). The `lifecycle_regressions` function goes; its `open --remote
  nowhere` refusal goes to pytest.
- **Backlog items in the units are filed as today** (`prepare_cr`: `file` then `triage`). Writing
  backlog folders directly is for pytest only.

### Cuts inside the units

- **Duplicates** (analysis section B), each kept once:
  - the release PR's merge that no approval covers: in `release` only;
  - a release on the stack's top branch: in `release_on_stack` only;
  - series mode: in `batch_modes` only;
  - `take --note` reopening a ready CR: in the main batch, plus one pytest refusal;
  - `order add` on a paused batch staying paused: in one place;
  - budget exit 5: one parametrized pytest;
  - `gate --stop` per slot: in `gate_parallel` E4 only;
  - a gate waiting for the lock: in `gate_parallel` E5 only;
  - the no-`chantier.yaml` P12 preflight: in pytest;
  - a second `open` refused: in pytest;
  - the queued-icon matrix: in `dependencies` only;
  - the seat basics: in pytest;
  - the write scope: the end-of-unit assertion.
- **The pause, close and price tail** goes from every case that is not about closing. `w.reset()`
  is enough between cases of one unit. The tail stays in `parallel` (`close_batch`,
  `retro_cases`) and in `direct`.
- **Event-driven gates instead of fixed sleeps** in `rails` and `gate_parallel`. Today they use
  2 s held gates, 3 × 3 s queued gates, an a1 of 16 s and an a2 and a q1 of 8 s. The gate
  script blocks until a release file the scenario touches exists (a `Path.exists` poll), and
  the checks assert order, not duration. A lower bound such as `waited >= 1` stays true because
  the scenario touches the release file after at least 1 s.
- **The `time.sleep(1.1)` between gates** (gate logs are named by the second, `gate.py:244`)
  stay where two gates of one CR must get two logs. The CLI does not change.
- **`GATE`** (l.48, written into the test project's `AGENTS.md`) and `cancel_during_gate`'s slow
  gate run `"<sys.executable>" ...` instead of `uv run --no-project python ...`. This saves one
  uv start per gate and removes a source of variance under load; the checks quote the constant,
  so they still match.
- **`remote_board`**: the `line(1.5)` silence goes to 0.5 s, and the `sleep(1)` (l.1494) becomes a
  poll. `exits()` (up to 25 s) waits for the board's own seat watch, which is the CLI's: its
  upper bound stays.
- Optional, if step 0 shows it pays: one template world built once by the parent and copied per
  unit (`shutil.copytree`, then `git remote set-url`); and `stack_batch`'s `commit-tree` loop
  pinned to a known date and message so its first try gives an all-digit short SHA.

### The runner

`scenario/run_scenario.py` keeps one entry point:

- `--unit NAME` (repeatable) runs those units only; with no `--unit`, it runs every unit.
- `--forge github|gitlab` restricts the forge; with no `--forge`, both run, each unit on its
  table's forges.
- `--jobs N` sets how many units run at once. The default is 4 (Scen-Q3, amended in Scen-Q5).
- `--keep` and `--verbose` stay (`--verbose` with one unit prints its transcript live).
- `--external-only` goes: it is `--unit surface-board`.

The parent:

- spawns each unit as `[sys.executable, __file__, "--child", unit, "--forge", f, "--out",
  run_dir]` in its own process group (`start_new_session=True` on POSIX,
  `CREATE_NEW_PROCESS_GROUP` on Windows);
- orders the queue longest budget first;
- waits for each unit with a hang timeout (FS-Q1): 600 s, or 4 times the unit's budget when that
  is longer, counted from the unit's own start. A unit still running past it is killed with its
  whole process tree and counted as failed, "timed out (hung)", and the run fails. `psutil` is
  already a locked dependency of the package and does this on all three systems. This timeout
  catches a hang; it is not the budget: a unit over its budget but under its hang timeout still
  passes (see below);
- kills every unit's tree on exit or on Ctrl-C, so no gate or sleeper outlives the run;
- writes the transcript to `scenario/results/scenario-<YYYYmmdd-HHMMSS>-<pid>.md`: the units'
  transcripts concatenated in the `UNITS` table's order, whatever their finishing order;
- writes each unit's own `<unit>-<forge>.md` and `<unit>-<forge>.json` (`checks`, `failed`,
  `commands`, `seconds`) under `scenario/results/<stamp>-<pid>/`, which git ignores today;
- prints, on every run, one row per unit and forge (checks passed/total, commands, seconds,
  budget, `ok` / `FAIL` / `over budget` / `timed out`), then the wall time and the sum of the
  units' seconds;
- exits 1 if any check failed or any unit timed out (hung), and 0 otherwise. Slowness alone
  never fails a run: it is only the warning below.

A unit over its budget prints, in that table and as its own line,
`WARN <unit> (<forge>) over its budget: <s> s > <budget> s`, a line the Inspector of a later CR
reads in the gate's output.

`justfile`:

```
# The scripted scenario: independent units in parallel (4 at a time), GitHub and the GitLab unit
scenario *args:
    {{run-cli}} scenario/run_scenario.py {{args}}
```

`just scenario --unit gates` reruns one unit, and `just scenario --jobs 8` measures. The CI job's
step (`run: just scenario`) does not change.

### Pure refusals to pytest

The pure refusals move to pytest: those that need only a prepared state and one CLI call.
They run in-process (the `repo` and `chantier` fixtures) and are parametrized, so the tests stay
few and fast. They go in new files under `skills/chantier/scripts/cli/tests/` (each under 400
lines, each function under 50), except the cost arithmetic, which joins `test_costs.py`, and the
card text checks, which join `test_plugin_files.py`. A refusal that exists only in the middle of
a real run stays in its unit. What moves (analysis section A, the TESTS verdicts; Fable's list):

- `playbook_config` whole: S4's 19 `chantier.yaml` refusals (one parametrized test), S1-S3 and
  S5 (open and read), S2b's `ci:` line; and `gate_parallel` E6's `long_gate` refusals;
- the rails' refusals of `rails` l.3171-3236: a second `round`, the round limit, `slots 0`,
  `land`, the budget (exit 5, parametrized with `gate_proof`'s budget against rounds and
  `qa_on_head`'s spent budget), `take` on a ready CR without `--note`; `stop_own_gate`'s `cancel`
  without `--epoch`;
- the close refusals of `close_refusals`: the second `pause`, close refused while something runs
  (the loop, one parametrized test on a prepared paused `batch.json`), and a call after the pause
  counted as spend (a fixture transcript);
- triage, abandon and file refusals (§2); `changes_tree`'s triage moves and the stray-folder close
  refusal; `depends.json`'s cycle, unknown slug and malformed file; `batch_modes`' dependency
  before its CR; `granted_fixes`' usage and drop refusals; `qa_on_head`'s QA folder not openable;
  `forge_stack_cli`'s parallel-batch refusal; the second `open` refused; `open --remote nowhere`
  exits 4;
- cost and STATUS reading: §9's exact pricing arithmetic, §10's Copilot cost,
  `copilot_missing_transcript`, `unpriced_model`, `direct_batch`'s spec-writer and spec-critic
  pricing; STATUS rendering of a prepared record (`ready_words` §8: an old record with no draft
  state, a hand-edited ready CR with no `pr`); `board_index`'s folder without `STATUS.json` and
  its padding; `driver_liveness`'s lines from a crafted lock or ticket;
- `restore_cr`, `next_number`, `failed_opening`, `cr_summary` whole;
- `driver_liveness`'s card text checks (`foreman.md`, `driver.md`) into `test_plugin_files.py`;
- the preflight refusal and warning lines beyond the one preflight `parallel` keeps; the seat
  basics.

The board's HTTP refusals (POST 400/409, the 404s) stay in `surface-board`: `test_board.py`
checks structure only and has no in-process app harness, and building one is not this CR's.

`AGENTS.md`'s tests rule is rewritten. Today: "Tests check the structure only (`tests/`): keep
them few and fast; the batch workflow belongs to `just scenario`." It becomes, in substance:
"Tests (`tests/`) check the structure and the CLI's refusals on a prepared state, calling the CLI
in-process: keep them few, parametrized and fast (`just test` at most 30 s above its 18.5 s of
2026-11-14 on the user's Windows machine); the batch workflow belongs to `just scenario`."
`CONTRIBUTING.md`'s line on tests ("Tests check the structure ... in a few seconds. They do not
evaluate the batch workflow") follows it. The 30 s comes from Fable's advice. The PR body
records the measured `just test` time before and after.

### The README coverage list is the contract

`scenario/README.md`'s coverage list (today's bullets from "preflight refusing Claude in VS
Code" to "the batch's record") stays the list of what is proved (Scen-Q4).

- Each bullet ends with where it is proved: `(unit: <name>)`, `(test: <file>::<test>)`, or both
  when a bullet is split between them.
- A bullet whose behaviour was dropped as a duplicate names where the kept copy lives.
- A bullet that names something this CR removes says so in the PR body, quoting the bullet. The
  only such removals are `--external-only` and "run on both forges after the in-project batch".
- **A structure test checks the mapping (FS-Q2)**, in a new file under
  `skills/chantier/scripts/cli/tests/` (for example `test_scenario_coverage.py`), run by
  `just test` and so by `just check` on the three systems. It reads `scenario/README.md`'s
  coverage list (from `PLUGIN_ROOT`) and fails when:
  - a bullet carries no `(unit: ...)` and no `(test: ...)`;
  - a named unit is not a key of `run_scenario.py`'s `UNITS` table, read from the source (for
    example with `ast`), without importing or running the scenario;
  - a named test's file does not exist under `tests/`, or has no test function of that name.

  Its failure message names the bullet and the missing unit or test. It checks names only, not
  that the named place really proves the bullet's behaviour: that stays the Inspector's reading.
- The Inspector checks, beside the test, that each mapping is plausible (the named unit or test
  does exercise the bullet's behaviour) and that no bullet was dropped against today's list
  (`git diff` of the README).
- The intro and the end are rewritten: no "about two minutes per forge"; the units, `--jobs`,
  `--unit`, the results file names; Windows still runs one check more than Linux (in `release`).

### The standing rule against regrowth

A new section of `scenario/README.md`, "Adding a case", linked from `CONTRIBUTING.md`'s tests
line:

- A new case joins an existing unit's batch, or goes to pytest when it is a refusal on a
  prepared state. It never adds a unit without the user's word.
- A unit over its budget prints a warning the Inspector reads. The run never fails on time; only
  a hung unit, killed past its hang timeout, fails it.
- A new check maps to its README bullet like the others; the coverage structure test fails while
  a bullet names no existing unit or test.

### 4 against 8, measured once

On the user's Windows machine, once all the units pass, the Driver runs `just scenario` with
`--jobs 4` and with `--jobs 8`. It records both wall times, the per-unit table of each run and
the machine (Ryzen 7 7800X3D, 8 cores / 16 threads) in `scenario/README.md` and in the PR body.
The default stays 4 (Scen-Q5) whatever the result. A result that argues for another default is
put to the user in the PR's Known gaps, not applied.

## The risks of running in parallel, and what the CR does about each

- **Results file names.** Today's name is to the second (`<forge>-<time>.md`), so two runs in
  the same second collide. The fix: the parent's `scenario-<stamp>-<pid>.md` and a per-run folder.
- **Ports.** `free_port()` (bind 0, close, reuse) races with another unit.
  - A board that can take `--port 0` takes it, and the scenario reads the port from the start
    line.
  - The held-port check holds its own socket open while the board tries it.
  - Only the `board.port`-from-yaml check keeps `free_port()`, with one retry when the port turns
    out to be held.
  - Both board-starting cases are in one unit (`surface-board`), which also removes races
    between units.
- **The firewall prompt on `0.0.0.0`** (`remote_board` §10). Windows may show a prompt once per
  `python.exe` path. The prompt does not block the bind, and the check reads only the start
  line. Step 0 records whether a prompt appears on the user's machine; if one appears, the PR's
  Known gaps names it.
- **Timeouts under load.** Four units at once slow each call. Lower bounds (`waited >= 1`) are
  safe, but upper bounds flake. The event-driven gates remove the largest source. A deadline
  that only bounds a wait is raised: `lock_names` 10 s, `wait_tickets` 15 s, the autosync join
  poll 40 s, `communicate` timeouts. Raising it costs nothing on a green run. An upper bound that
  is itself the behaviour under test stays as it is, and the PR body names it.
- **A hung unit.** A unit that never ends would hold the run forever. The parent's hang timeout
  (600 s, or 4 times the unit's budget when longer, FS-Q1) kills it with its tree and fails the
  run, so a hang shows as `timed out` instead of a stuck gate.
- **Leaked sleepers.** The 60 s gates, the 120 s surface sleeper and the 300 s sleepers survive a
  crashed unit. The parent kills each unit's process tree on exit, on timeout and on Ctrl-C. Each
  unit's own `finally` keeps today's cleanup.
- **Global git config.**
  - Each unit sets `GIT_CONFIG_GLOBAL` to a file in its own temp folder (git 2.32 or later),
    holding only `user.name` and `user.email`, so no global hook, template, `core.autocrlf` or
    credential helper of the machine reaches it.
  - CI's identity step (`git config --global`) is then no longer read by the units, and the
    file carries the identity in its place.
  - The system config is left as it is.
  - `core.abbrev` stays set at the repository level (`gate_proof`).
- **Windows file locks at cleanup.** Defender or an indexer may hold a file while `rmtree` runs.
  Cleanup retries a failed removal (`onerror` handler), never fails the run, and prints one
  warning line naming what it left.
- **Safe already (no change):**
  - gate locks and queues are per planning folder (`gate_slots.py`, `gate_queue.py`);
  - the board key is in each repository's git folder, autosync state is per surface, and the
    fake forge's state is per world;
  - processes found by command line use paths unique per `mkdtemp`;
  - the uv cache is read concurrently.
- **The Linux CI runner's size.** Wall time there is about max(longest unit, sum / cores). A
  public repository's `ubuntu-latest` has 4 vCPUs; a private one has 2. Only the first CI run
  proves the time there (see below).

## CI

The `scenario` job of `.github/workflows/ci.yml` keeps its steps: checkout, setup-uv,
setup-just, the git identity, `run: just scenario`. With no job step changed, `CONTRIBUTING.md`'s
cold-cache run is not owed. What the job's environment differs in, and what only its first run
proves:

- `ubuntu-latest` (GitHub-hosted): 4 vCPUs on a public repository, 2 on a private one (not
  checked), against 16 threads locally. The 4 units at once may share fewer cores.
- An empty uv cache at each run: the scenario no longer calls uv per gate, but `uv run --locked`
  starts the parent once.
- No Defender, no firewall prompt, and a different git version (`GIT_CONFIG_GLOBAL` needs 2.32 or
  later; the runner's is newer).
- The first CI run at the PR's head proves the Linux time. It must be green and under 300 s,
  read from the runner's printed wall time, which the PR body quotes.

## Evidence (done when)

1. Step 0's table (`<work folder>/step0-baseline.md`), one run per forge, quoted in the PR body.
2. Three consecutive green `just scenario` runs (both forges, default `--jobs 4`) on the user's
   Windows machine, each under 300 s by the runner's printed wall time. Their three tables go in
   the PR body.
3. One green run under 300 s on Linux CI at the PR's head.
4. Every bullet of `scenario/README.md`'s coverage list maps to an existing unit or test, and no
   bullet was dropped against main's list: the coverage structure test passes in `just check`,
   and the Inspector checks the mappings and the README's diff.
5. `just check` passes on Linux, macOS and Windows. `just test` stays within its budget (at most
   30 s above 18.5 s on the user's machine), with times before and after in the PR body.
6. The 4-against-8 measurement is in `scenario/README.md` and in the PR body.
7. A check that fails still fails the run: shown once by flipping one check in one unit on a
   scratch branch (exit 1, the unit's row `FAIL`, the transcript naming it), not committed.
8. A hung unit is killed with its tree and fails the run: shown once on a scratch branch with a
   unit that sleeps past its hang timeout, the timeout shortened for the demonstration only
   (exit 1, the row `timed out`, no process of the unit left), not committed. The committed
   timeout is 600 s, or 4 times the unit's budget when longer.
9. The coverage structure test catches a gap: shown once on a scratch branch by removing one
   bullet's mapping and by naming a unit that does not exist (the test fails, naming the
   bullet), not committed.
10. `AGENTS.md`'s tests rule and `CONTRIBUTING.md`'s tests line say the new rule, and
   `scenario/README.md` has "Adding a case".

The long gate of this CR is its own `just scenario` (AGENTS.md: a change to the scenario passes
it before its PR).

## Out of scope

- Anything under `skills/chantier/scripts/cli/src/`: no CLI change, no test-only knob in the CLI
  (the board's seat-watch interval included).
- `baseline-and-legacy`'s work, done before this CR: the long gate on main and its fixes, the
  one-off migration, the legacy readers and their scenario cases, and `World.at`'s prefix.
- `gate-rules`' work, after this CR: the four long-gate rules (queue order, early push, clean
  rebase, the stack's one gate) and the scenario cases they add. `00-absorbed.md` still holds
  their source text, which this CR does not touch.
- An in-process harness for the board's HTTP app.
- A change to the CI workflow's steps, or a new CI job.
- The eval kit (`evals/`).

## Open questions

1. Is the repository public on GitHub (4 vCPUs on `ubuntu-latest`) or private (2)? On 2 vCPUs,
   300 s on Linux CI may need a larger runner, which would be a CI change outside this CR.

Settled: FS-Q1 (the hang timeout, 600 s or 4 times the budget, fails the run; slowness only
warns) and FS-Q2 (a structure test checks the README mapping beside the Inspector's reading).
