# Change Specification: `forge-stack rebuild` takes the forge's empty unstack reply as a success

## Goal

In batch-22, while the release CR-307 (PR #259) joined stack #258, `$CHANTIER forge-stack rebuild`
exited 4 with `error: gh api -X POST repos/gsemet/chantier/stacks/258/unstack -F pull_requests[]=251 … : not JSON: `.
GitHub had dissolved the stack. Its unstack call answers 2xx with an empty body, and the CLI tried
to parse that body as JSON. The rebuild stopped half done: the PRs were unstacked and no stack was
left on the forge. The stack driver had to work out the state and run `forge-stack create` itself
(stack #260).

The user's decisions (`02-answers.md`, 2026-11-17):

1. rebuild-Q1: P1, in the next batch. An empty body on a 2xx unstack reply is a success, and
   `rebuild` goes on: retarget, create, read the stack back. When a `rebuild` fails after the
   unstack, it says plainly that the stack is dissolved and that the next step is
   `forge-stack create`.
2. rebuild-Q2: when a refused `rebuild` ends with that dissolved line, the stack driver runs
   `forge-stack create` itself. One sentence changes in `driver.md`.
3. rebuild-Q3: the line names `forge-stack create`, and `chief-of-staff.md` changes so that the
   Chief of Staff runs the command the line names.
4. rebuild-Q4: the dissolved line appears only when `retarget` failed or the forge refused the
   create call. When the create call succeeded but its reply cannot be read, a different line
   says that the stack's state is unknown and that the next step is `forge-stack show`.

The CR has no `issue:` line.

## What changes

### 1. The CLI: `skills/chantier/scripts/cli/src/chantier/commands/forge_stack_gh.py`

**A new error class, `Unreadable(ChantierError)`**, defined in this module. It is for a call the
forge accepted (`gh api` exit 0) whose reply cannot be read. It keeps exit 4 (`EXIT_EXTERNAL`)
and today's text. It is a subclass, so every `except ChantierError` and every
`e.code != EXIT_EXTERNAL` test keeps working as it does today.

**`gh(args, host)`** takes a keyword argument `empty_ok: bool = False`.
- When `empty_ok` is true, the call exits 0 (`gh api` exits non-zero on any HTTP status of 400
  and above, so exit 0 means a 2xx), and `p.stdout.strip()` is empty: `gh` returns `None` and
  does not parse.
- Everything else behaves as it does today, except for the class of one error:
  - a non-zero exit raises `ChantierError` `gh api <args>: <stderr or stdout>` (exit 4), not
    `Unreadable`;
  - a reply that is not JSON raises `Unreadable` `gh api <args>: not JSON: <first 200 chars>`
    (exit 4). This holds with `empty_ok` or without, and for a non-empty body;
  - without `empty_ok`, an empty body still raises `Unreadable` `not JSON` (exit 4). The other
    calls (list, read, create, PATCH) need a body: `_make` reads the new stack's number from it.
- `gh: not found on PATH` stays a plain `ChantierError`.

**`unstack(...)`** passes `empty_ok=True` on its `POST repos/{owner}/{name}/stacks/{n}/unstack`
call. It never reads that call's reply. After each POST the loop already reads the stacks back
(`stacks(host, owner, name)`), so that read decides the result, as it does today:
- the stack is read back gone or not open: `unstacked #<n>`, plus the `held_outside` remark;
- it is still open after `UNSTACK_TRIES` (5) tries: today's error.

`forge-stack unstack` (`unstack_action`) calls the same `unstack()`, so it also takes an empty
reply as a success. It is the same forge call; nothing else in `unstack_action` changes.

### 2. The CLI: `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py`

**`_make`**: when the forge answers the create call without a stack number (the reply is JSON
but has no `number`), raise `Unreadable` instead of `ChantierError`. The text stays
`gh api: the forge answered no stack number: …`, with exit 4. So every failure of `_make` is one
of two kinds:
- the forge **refused** the create call: a plain `ChantierError` from `gh`'s non-zero exit;
- the forge **accepted** the create call and its reply **cannot be read**: `Unreadable`, either
  from `gh` (not JSON, or empty) or from `_make` (no number).

Import `Unreadable` from `forge_stack_gh`.

**`_rebuild`**: the phases are the unstack loop, then `retarget(...)`, then `_make(...)`. "After
the unstack" means once the unstack phase is over: the loop over `stacks(...)` has ended and
every open stack that held a planned PR has been read back gone. Keep in a list, next to `done`,
the numbers of the stacks this run unstacked. Do not parse them back out of the text. Also note
which phase raised: set a marker just before the `_make(...)` call.

When a `ChantierError` with `EXIT_EXTERNAL` is raised after the unstack phase, `_rebuild` raises
exit 4 with these lines, in this order:

1. the lines of what was done (`done`, as today: `unstacked #<n> …`, `#<pr> base <old> -> <new>`);
2. the forge's exact error (`str(e)`, as today);
3. at most one new last line, chosen in this order:
   - **the create call was accepted and its reply cannot be read** (`_make` raised `Unreadable`):
     `the forge accepted the create call but its reply cannot be read, so the stack's state is unknown: run `forge-stack show``.
     This line does not depend on whether this run unstacked a stack. It replaces the dissolved
     line: the dissolved line is never printed in this case.
   - **`retarget` failed, or the forge refused the create call** (any other `EXIT_EXTERNAL` error,
     `Unreadable` from `retarget`'s PATCH included), **and** this run unstacked at least one
     stack:
     `stack #<n> is dissolved and no stack replaces it yet: run `forge-stack create``.
     When this run unstacked more than one stack, the line names each one:
     `stacks #<a> #<b> are dissolved and no stack replaces them yet: run `forge-stack create``.
   - otherwise: no new line.

The output stays as it is today, with no new line, in these cases:
- the run fails before the unstack phase ends: the first `stacks(...)` read; an unstack POST
  refused; the read-back after a POST failing; a stack still open after 5 tries. A stack the
  batch's PRs still sit in is open, or its state is not known, so `create` would be the wrong
  advice.
- `retarget` failed or the create call was refused, and the run unstacked no stack (nothing held
  the planned PRs): this run dissolved nothing.
- the error is not `EXIT_EXTERNAL`: it propagates as it does today.

`_create` and `_show` do not change. `_create` keeps its `(`forge-stack rebuild` replaces a
stack)` remark.

### 3. The stack driver's card: `skills/chantier/references/driver.md`

In "Making the stack", the paragraph that ends at about line 750 says: "A `rebuild` refused (by
the forge or the permission check) is an `anomaly` with the exact text, as above; no other
means." Replace that sentence with one that keeps the rule and adds the exception, in this
sense:

> A `rebuild` refused (by the forge or the permission check) is an `anomaly` with the exact text,
> as above; no other means, except one: when its error ends with the line `… dissolved and no
> stack replaces it yet: run `forge-stack create``, run `$CHANTIER forge-stack create` yourself
> and go on as after a `rebuild` (a `create` refused is an `anomaly` with the exact text).

The unknown-state line (`… run `forge-stack show``) gets no exception: that refusal stays an
`anomaly` with the exact text. See the open question.

The card lives only in `skills/chantier/references/`; the agent files (`agents/`,
`com.github.copilot/agents/`) do not change.

### 4. The Chief of Staff's card: `skills/chantier/references/chief-of-staff.md`

At about lines 1070-1072, the text says: "An `anomaly` of the stack driver or the Foreman on a
refused `$CHANTIER forge-stack rebuild` reaches the user as an ask with the exact text; on the
user's yes, run `$CHANTIER forge-stack rebuild` yourself (no raw `gh api`)." Change the part after
"on the user's yes" to this sense:

> on the user's yes, run yourself the command the refusal's last line names (`$CHANTIER
> forge-stack create` after the dissolved line, `$CHANTIER forge-stack show` after the
> unknown-state line), or `$CHANTIER forge-stack rebuild` when it names none (no raw `gh api`).

The ask itself does not change: the exact text, the dissolved or unknown-state line included,
reaches the user.

### 5. The fake forge: `scenario/fake_gh.py`

Two new state flags:
- **`unstack_empty`**, in the unstack branch. When it is true, the fake dissolves the stack
  exactly as it does today (drops the named PRs, closes the stack once it is empty, saves the
  state). It then prints nothing and exits 0, as GitHub did. `unstack_ignored` keeps its meaning
  and is checked first.
- **`create_unreadable`**, in the stacks endpoint's `POST` branch. When it is true, and the create
  passes today's checks (`broken`, `stack_refused`, `taken`), the fake creates and saves the
  stack as today. It then prints a reply that is not JSON (for example `<html>`) and exits 0.

### 6. The scenario: `scenario/run_scenario.py`, `forge_stack_cli`, GitHub part

- **Step 3** (the forge refusal mid-way, `patch_refused`): this fails in `retarget` after stack
  #150 is unstacked. The check also asserts that the last stderr line is
  `stack #150 is dissolved and no stack replaces it yet: run `forge-stack create``, alongside
  today's `unstacked #150` and `HTTP 403`.
- **Step 3b** (a stack still open after five tries): the check also asserts that neither
  `is dissolved` nor `state is unknown` is in the stderr.
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

    Then clear `stack_refused` and run `forge-stack create`. Check exit 0 and one open stack.
    This proves that the advice of the dissolved line works.
- **New step 3d**, after 3c:
  - With `unstack_empty` still on, set `create_unreadable=True` and run `forge-stack rebuild`.
    Expect exit 4. Check that stderr holds, in order:
    - `unstacked #<the stack 3c's create made>`;
    - `not JSON`;
    - the last line, `the forge accepted the create call but its reply cannot be read, so the stack's state is unknown: run `forge-stack show``.

    Check that `is dissolved` is **not** in the stderr.
  - Clear both flags and run `forge-stack show`. Check exit 0 (or only `check 4` draft lines, as
    the step's state gives) and one open stack holding the planned PRs: the stack the fake made.
    This proves that the advice of the unknown-state line works.
- **Step 5** (`forge-stack unstack`): leave as is. The empty reply goes through the same
  `unstack()`, which 3c proves.

The scenario does not run the agents, so the card changes (sections 3 and 4) have no scenario
step. Keep the new checks within the scenario's time budget: 3c and 3d reuse the world that steps
3 and 3b already set up.

### 7. The scenario's description: `scenario/README.md`

In the `forge-stack` (GitHub) bullet, add:
- the empty unstack reply (`unstack_empty`: `rebuild` completes);
- the dissolved line on a failure after the unstack, its absence after the five tries, and
  `create` run after that failure;
- the unknown-state line when the create reply cannot be read (`create_unreadable`), and `show`
  run after it.

Keep `tests/test_scenario_coverage.py` passing if it reads that file.

### 8. The unit test: `skills/chantier/scripts/cli/tests/test_cli_units.py`

Add one parametrized test of `forge_stack_gh.gh`'s reply parsing. Use the
`test_board_forge_read.py` pattern: monkeypatch `shutil.which` to `"/bin/gh"` and
`subprocess.run` to return a `SimpleNamespace(returncode, stdout, stderr)`. The cases:

| `empty_ok` | returncode | stdout | expected |
|---|---|---|---|
| True | 0 | `""` | returns `None` |
| True | 0 | `"\n  "` | returns `None` |
| True | 0 | `'{"number": 1}'` | returns the dict |
| True | 0 | `"<html>"` | raises `Unreadable`, `not JSON`, exit 4 |
| False | 0 | `""` | raises `Unreadable`, `not JSON`, exit 4 |
| True | 1 | `""`, stderr `HTTP 404` | raises `ChantierError` with `HTTP 404`, exit 4, **not** `Unreadable` |

This is one test function with six parameter rows. It adds well under a second to `just test`.
The choice of `_rebuild`'s last line needs a prepared batch and a forge, so the scenario proves it
(section 6), not a unit test.

## Out of scope

- The GitLab path (`forge_stack_gitlab.py`): it has no unstack, and its `gl` keeps its errors.
- Any other forge call accepting an empty body.
- `_create`: its refusal text and remark do not change. A `create` whose reply cannot be read
  gets no unknown-state line in this CR.
- What `show` checks.
- A retry, or an automatic `create` or `show` inside the CLI after a failed `rebuild`. The CLI
  says what to run; an agent runs it.
- The Foreman's card (`foreman.md`): no change was decided.
- The agent files (`agents/`, `com.github.copilot/agents/`).

## Evidence

- `just check` passes (Linux, macOS, Windows), including the new unit test.
- `just scenario` passes at the PR's head on the pipeline's `just scenario (ubuntu-latest)` job,
  because this changes the CLI, the cards and the scenario. As the top CR of its batch, it also
  passes locally on Windows (`chantier gate`).
- The scenario checks of section 6:
  - step 3 and the second run of 3c show the dissolved line;
  - 3b shows that neither new line appears;
  - the first run of 3c shows `rebuild` completing on an empty unstack reply;
  - the `create` at the end of 3c shows the dissolved line's advice holds;
  - the first run of 3d shows the unknown-state line instead of the dissolved line;
  - the `show` at the end of 3d shows the unknown-state line's advice holds.
- The card changes (sections 3 and 4) are read in the PR's diff: one sentence in `driver.md`,
  one in `chief-of-staff.md`, each quoting the line the CLI prints.
- No CI job is added or changed.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17): the unknown-state line stays an
`anomaly` for the stack driver, as section 3 says. Before it raises it, the stack driver may run
`forge-stack show` (a read) and quote its output in the anomaly; it does not carry on from it. This
reply is rare, and the Chief of Staff decides what follows on the user's word.
