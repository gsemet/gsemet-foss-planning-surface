# Change Specification: `forge-stack rebuild` takes the forge's empty unstack reply as a success

## Goal

In batch-22, while the release CR-307 (PR #259) joined stack #258, `$CHANTIER forge-stack rebuild`
exited 4 with `error: gh api -X POST repos/gsemet/chantier/stacks/258/unstack -F pull_requests[]=251 … : not JSON: `.
GitHub had dissolved the stack. Its unstack call answers 2xx with an empty body, and the CLI tried
to parse that body as JSON. The rebuild stopped half done: the PRs were unstacked and no stack was
left on the forge. The stack driver had to work out the state and run `forge-stack create` itself
(stack #260).

The user's decision (`02-answers.md`, rebuild-Q1, 2026-11-17): P1, in the next batch.

1. An empty body on a 2xx unstack reply is a success, and `rebuild` goes on: retarget, create,
   read the stack back.
2. When a `rebuild` fails after the unstack, it says plainly that the stack is dissolved and that
   the next step is `forge-stack create`.

The CR has no `issue:` line.

## What changes

### 1. The CLI: `skills/chantier/scripts/cli/src/chantier/commands/forge_stack_gh.py`

**`gh(args, host)`** takes a keyword argument `empty_ok: bool = False`. When it is true, the call
exits 0 (`gh api` exits non-zero on any HTTP status of 400 and above, so exit 0 means a 2xx) and
`p.stdout.strip()` is empty, `gh` returns `None` and does not parse. Everything else stays as it
is today:
- a non-zero exit raises `gh api <args>: <stderr or stdout>` (exit 4);
- a non-empty body that is not JSON raises `gh api <args>: not JSON: <first 200 chars>` (exit 4),
  with `empty_ok` or without;
- without `empty_ok`, an empty body still raises `not JSON` (exit 4). The other calls (list, read,
  create, PATCH) need a body: `_make` reads the new stack's number from it.

**`unstack(...)`** passes `empty_ok=True` on its `POST repos/{owner}/{name}/stacks/{n}/unstack`
call. It never reads that call's reply. After each POST the loop already reads the stacks back
(`stacks(host, owner, name)`), so that read is what decides the result, as it does today:
- the stack is read back gone or not open: `unstacked #<n>`, plus the `held_outside` remark;
- it is still open after `UNSTACK_TRIES` (5) tries: today's error.

`forge-stack unstack` (`unstack_action`) calls the same `unstack()`, so it also takes an empty
reply as a success. That is the same forge call; nothing else in `unstack_action` changes.

### 2. The CLI: `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py`, `_rebuild`

"After the unstack" means once the unstack phase is over: the loop over `stacks(...)` has ended
and every open stack that held a planned PR has been read back gone. A later forge failure can
then come only from `retarget(...)` or `_make(...)`. If one of them raises a `ChantierError`
with `EXIT_EXTERNAL` **and** this run unstacked at least one stack, `_rebuild` raises exit 4 with
these lines, in this order:

1. the lines of what was done (`done`, as today: `unstacked #<n> …`, `#<pr> base <old> -> <new>`);
2. the forge's exact error (`str(e)`, as today);
3. one new last line:
   `stack #<n> is dissolved and no stack replaces it yet: run `forge-stack create``.
   When this run unstacked more than one stack, the line names each one:
   `stacks #<a> #<b> are dissolved and no stack replaces them yet: run `forge-stack create``.

The numbers are those of the stacks this run unstacked. Keep them in a list next to `done`; do
not parse them back out of the text.

The output stays as it is today, with no new line:
- the run fails before the unstack phase ends: the first `stacks(...)` read; an unstack POST
  refused; the read-back after a POST failing; a stack still open after 5 tries. A stack the
  batch's PRs still sit in is open, or its state is not known, so `create` would be the wrong
  advice.
- the run unstacked no stack (nothing held the planned PRs): nothing was dissolved by this run.
- the error is not `EXIT_EXTERNAL`: it propagates as it does today.

`_create` and `_show` do not change. `_create` keeps its `(`forge-stack rebuild` replaces a
stack)` remark.

### 3. The fake forge: `scenario/fake_gh.py`

The unstack branch takes a new state flag, `unstack_empty`. When it is true, the fake dissolves
the stack exactly as it does today (drops the named PRs, closes the stack once it is empty, saves
the state), then prints nothing and exits 0, as GitHub did. `unstack_ignored` keeps its meaning
and is checked first.

### 4. The scenario: `scenario/run_scenario.py`, `forge_stack_cli`, GitHub part

- **Step 3** (the forge refusal mid-way, `patch_refused`): this fails in `retarget` after stack
  #150 is unstacked. The check also asserts that the last stderr line is
  `stack #150 is dissolved and no stack replaces it yet: run `forge-stack create``, alongside
  today's `unstacked #150` and `HTTP 403`.
- **Step 3b** (a stack still open after five tries): the check also asserts that `is dissolved`
  is **not** in the stderr.
- **New step 3c**, after 3b's successful rerun:
  - Turn on `unstack_empty`, using the open stack 3b's rerun left. Run `forge-stack rebuild`.
    Check: exit 0; `unstacked #<that stack>` in the output; a `stack #<m> …` line; the stack read
    back `ready to merge` (or only `check 4` draft lines, as the step's state gives); a single
    open stack holds the planned PRs.
  - With `unstack_empty` still on, set `stack_refused=True` and run `forge-stack rebuild` again.
    Expect exit 4. Check that stderr holds, in order:
    - `unstacked #<the stack just made>`;
    - `HTTP 403: stacks are not allowed`;
    - the last line, `stack #<it> is dissolved and no stack replaces it yet: run `forge-stack create``.

    Then clear both flags and run `forge-stack create`. Check exit 0 and one open stack. This
    proves that the advice works.
- **Step 5** (`forge-stack unstack`): leave as is. The empty reply goes through the same
  `unstack()`, which 3c proves.

Keep the new checks within the scenario's time budget. 3c reuses the world steps 3 and 3b
already set up.

### 5. The scenario's description: `scenario/README.md`

In the `forge-stack` (GitHub) bullet, add:
- the empty unstack reply (`unstack_empty`: `rebuild` completes);
- the dissolved line on a failure after the unstack, and its absence after the five tries;
- `create` run after that failure.

Keep `tests/test_scenario_coverage.py` passing if it reads that file.

### 6. The unit test: `skills/chantier/scripts/cli/tests/test_cli_units.py`

Add one parametrized test of `forge_stack_gh.gh`'s reply parsing. Use the
`test_board_forge_read.py` pattern: monkeypatch `shutil.which` to `"/bin/gh"` and
`subprocess.run` to return a `SimpleNamespace(returncode, stdout, stderr)`. The cases:

| `empty_ok` | returncode | stdout | expected |
|---|---|---|---|
| True | 0 | `""` | returns `None` |
| True | 0 | `"\n  "` | returns `None` |
| True | 0 | `'{"number": 1}'` | returns the dict |
| True | 0 | `"<html>"` | raises `not JSON`, exit 4 |
| False | 0 | `""` | raises `not JSON`, exit 4 |
| True | 1 | `""`, stderr `HTTP 404` | raises with `HTTP 404`, exit 4 |

This is one test function with six parameter rows. It adds well under a second to `just test`.

## Out of scope

- The GitLab path (`forge_stack_gitlab.py`): it has no unstack.
- Any other forge call accepting an empty body.
- Changing `_create`'s refusal text, or what `show` checks.
- A retry, or an automatic `create` after a failed `rebuild`. The CLI says what to run; an agent
  runs it.
- The cards (`driver.md`, `foreman.md`, `chief-of-staff.md`): no change is decided. See the open
  question.

## Evidence

- `just check` passes (Linux, macOS, Windows), including the new unit test.
- `just scenario` passes at the PR's head on the pipeline's `just scenario (ubuntu-latest)` job,
  because this changes the CLI and the scenario. As the top CR of its batch, it also passes
  locally on Windows (`chantier gate`).
- The scenario checks of section 4: step 3 and the second run of 3c show the dissolved line; 3b
  shows its absence; the first run of 3c shows `rebuild` completing on an empty unstack reply;
  the `create` at the end of 3c shows the advice holds.
- No CI job is added or changed.

## Open questions

1. A refused `rebuild` is an `anomaly` with the exact text and "no other means" (`driver.md`,
   around lines 744-750). Running `forge-stack create` is not authorised by the card. Should the
   stack driver run `forge-stack create` itself when the error ends with the new line? (In
   batch-22 it did.) Or does it stay an `anomaly`, with the line in the exact text, for the
   Foreman and the Chief of Staff to decide? If the former, the change in `driver.md` (one
   sentence, next to "A `rebuild` refused …") joins this CR.
