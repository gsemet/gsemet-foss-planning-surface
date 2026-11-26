# Evidence 8: no stale card name; the CLI lines of section 3

Worktree `batch-31-CR-510`, uncommitted tree (base `88d9ab40`), 2026-11-26. `$W` is the worktree,
`$S` the CR folder's `work/scratch`.

## `test_card_names.py` at head

`uv run --directory $W --locked --group dev pytest -v -p no:randomly
skills/chantier/scripts/cli/tests/test_card_names.py`, exit 0:

```text
skills/chantier/scripts/cli/tests/test_card_names.py::test_no_string_of_the_cli_or_the_hook_names_a_card_that_is_gone PASSED [ 50%]
skills/chantier/scripts/cli/tests/test_card_names.py::test_a_removed_card_named_in_a_source_fails_naming_it PASSED [100%]
============================== 2 passed in 1.73s ==============================
```

## The prepared stale name fails

The second case above asserts the scan's finding. To quote a failure line, a throwaway test
(`$S/e8_stale_test.py`) runs the shipped scan test with its source folder pointed at
`$S/e8-prepared/prepared.py`, whose two lines are the prepared case's:
`skill = "x"` and `line = f"{skill}/references/startup-core.md"`.
`uv run --directory $W --locked --group dev python -B -m pytest -vv -p no:cacheprovider
-p no:randomly --tb=short -c $W/pyproject.toml --rootdir $S $S/e8_stale_test.py`, exit 1, as
expected:

```text
skills\chantier\scripts\cli\tests\test_card_names.py:86: in test_no_string_of_the_cli_or_the_hook_names_a_card_that_is_gone
    assert found == []
E   AssertionError: assert ['prepared.py:2: references/startup-core.md', 'prepared.py:2: startup-core.md'] == []
============================== 1 failed in 0.56s ==============================
```

## The CLI lines of section 3, before and after

Before: base `88d9ab40`. After: head. Read from
`git diff 88d9ab40 -- skills/chantier/scripts/cli/src` (19 files, 197 insertions, 221 deletions).
`<...>` in these quotes stands for a value the CLI fills.

### 3.1 `take`, `take stack`, `order qa`

Before, after the state lines, the whole prompt to copy (`driver_prompt_lines`):

```text
<role> prompt (copy it whole, without the two leading spaces, and fill each <…>; add no line and drop none):
  <first line>
  Read <skill>/references/startup-core.md, the host core, role core, and the short startup section named by <skill>/references/startup-manifest.json; defer the rest until an action names it.
  Card: <skill>/references/<card>: its Startup core now, each other section when its step comes, as the card's opening says;
  <the rules line, contract lines, CLI, command lines, lease, writes>
  Team: <the team: lines, as printed, then the review steps>
  Steering: <who> <the host's means, from its reference's row "A Driver messages its steering session">
  Needs: ...
  Note: <why this is with the Driver>
```

(A Driver with no `writes:` line had `(no writes: line: this Driver gets none; ` in the heading.)

After:

```text
<the lease: line>
brief: <how the CLI runs> brief <role> <unit> --lease <n> --batch <b>
next: run it and pass its output, unchanged, as the Driver's whole prompt
```

The facts `brief` writes for the Driver (the same builder, no heading, first line, `Read` line,
`Card:` line or `Note:` placeholder):

| Line | Before (in the skeleton) | After |
| --- | --- | --- |
| `Team:` | `Team: <the team: lines, as printed, then the review steps>`, or `Team: <lines>; <review steps>` | `Team: <the team: lines, or "the plugin's agents">; review step <name>: <text>` (one per configured step, none: nothing more) |
| `Rewrites:` (CR) | `git -C <tree> rebase <base>, then $CHANTIER push <cr> --lease <n>, ...`, `<worktree>`, `<branch>`, `<base>` left when not printed | `git -C <tree> rebase <base>, then $CHANTIER push <CR-n> --lease <number>, ...` (filled) |
| `Rewrites:` (stack) | `git -C <worktree> rebase <base>, then $CHANTIER push <cr> --lease <n> --unit stack` | `git -C its row's worktree rebase its row's base, then $CHANTIER push with its row's CR --lease <number> --unit stack` |
| `Steering:` | `<who> <the host's means, from its reference's row "A Driver messages its steering session">` | `<who> (host means: the host rows below)` |
| `Note:` | `Note: <why this is with the Driver>` when empty | `Note: <the take's or order's note>`, no line when there is none |

(The `Team:` and `Rewrites:` rows hold round 2's fix of the Inspector's item.)

### 3.2 `round`, `handoff`, `facts`

Before:

```text
cards: <skill>/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
<role> prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
  <the worker's first line>
  Read <skill>/references/<card>;
  the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
worker writes line (copy it unchanged, without the two leading spaces, into each worker's prompt):
  writes: <worktree>; <CR folder>
```

(the block once per worker agent file).

After:

```text
brief: `brief <role> <cr>` gives each role its card, the floor and its facts; the project's rules rank above them: `rules`
...
workers: $CHANTIER brief <role> <CR-n> --batch <b> (roles: <the roles roles.yaml says a Driver starts>)
```

### 3.3 `driver:refused`

No manifest, so no `driver:refused` action. The `refused-push` topic of the swapped `topics.json`
reads only `topics/refused-push*.md` (seven files; roles cr-driver, stack-driver, release-driver,
foreman, chief-of-staff): no `foreman-refused.md`. `test_card_names.py` passes, so no CLI string
names it.

Also changed so that no string names a removed card:

| File | Before | After |
| --- | --- | --- |
| `commands/access.py` | `a rewrite uses --force-with-lease (driver.md)` | `a rewrite uses --force-with-lease (floor rule 2)` |
| `playbook/config.py` | `(hosts/<host>.md, "Models at an agent's start")` | `(references/hosts/<host>.json, row "model-at-start")` |

### 3.4 The Foreman's start

| Line | Before | After |
| --- | --- | --- |
| `open`, `next:` (empty batch) | `next: complete the brief <path>, then start the Foreman (direct mode: steer it yourself); each CR joins it by ...` | `next: complete the brief <path>, then start the Foreman: its first step is `brief foreman --batch <b> --epoch <n>` (direct mode: steer it yourself); each CR joins it by ...` |
| `open`, `next:` (with CRs) | `next: complete the brief <path>, then start the Foreman` | `next: complete the brief <path>, then start the Foreman: its first step is `brief foreman --batch <b> --epoch <n>`` |
| `open --direct`, `next:` | `... then steer it yourself` | unchanged |
| `foreman set` | `foreman <session> epoch <n>` | the same line, then `next: $CHANTIER brief foreman --batch <b> --epoch <n>` |

### 3.5 The stack line

Before (one line):

```text
shape stack: next <step>; stack driver: <agent>; native stack: <...>; alone asks: <...>; rules: <skill>/references/foreman-stack.md (reread after a compaction)
```

After (two lines, printed by `status --refresh` and in `brief foreman`'s facts on a stack batch):

```text
shape stack: next <step>; stack driver: <agent>; native stack: <...>; alone asks: <...>
shape: stack: read `$CHANTIER help stack` now and after each compaction
```

### 3.6 Preflight, permissions, the allow block

| Line | Before | After |
| --- | --- | --- |
| `preflight`, P10 gap | `...; the rules are in hosts/claude-code.md, "Capabilities and their commands"` | `...; the rules are in <skill>/references/hosts/claude-code.md, "Allow rules"` |

Not printed lines (comments and docstrings), changed to name the kept file or row:
`commands/allow_samples.py` (docstring and two comments), `commands/permissions.py:28`
(`help host-allow-not-add`), `board/griller_host.py`, `playbook/models.py`,
`playbook/timing_check.py`, `stack_shape.py` (docstrings).

Not done, by D9 (launcher not switched): the launcher's `SAMPLES` row and allow rule, the
`claude-code.md` launcher row, the "replaced by" and `_stale` launcher handling in
`permissions.py`.

### 3.7 The board Griller and the batch line

| Line | Before | After |
| --- | --- | --- |
| `board/griller.py` `BRIEF` | `Your card: <skill>/references/griller.md, its section "Started from the board" first; your host's reference: <skill>/references/hosts/<host_file>.md.` | `Your card: <skill>/references/griller.md, its section "Started from the board" first.` (the `host_file` field is gone from `Headless`) |
| the batch line (`status/ready_line.py`) | `...; merges: the user...; rules: <skill>/references/reload-rules.md (reread after a compaction)` | `...; merges: the user...; rules: <skill>/references/floor.md (after a compaction, run your brief again)` |
