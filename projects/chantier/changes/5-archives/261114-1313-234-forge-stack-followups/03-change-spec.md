# Change Specification: forge-stack follow-ups from CR-214 and CR-215

## Goal

Batch-16's retro (points 10 and 11, reviewed by an advisor) found five gaps that CR-214 (forge
permissions checked at the start) and CR-215 (work on a stack after it is ready) handed back or left.
This CR fixes them, so that what the code does matches what those CRs' specifications say:

1. `preflight` P10 finds the `gh stack` extension through `gh extension list`, as CR-214's
   specification says, not by looking for a folder.
2. P10's count ("14 of 16" on the user's machine, where it was "19 of 19") is explained, and the
   card says what it counts.
3. `forge-stack rebuild` exits 4 and lists what it already did when a stack stays open after its
   five unstack tries, as CR-215's specification says for any forge refusal. Today it exits 2 and
   drops that list.
4. `ship`'s stale-SHA scan of `work/pr-body.md` no longer takes an all-digit token (a PR number, a
   date) for a commit.
5. The batch-15 base case (a stacked CR with an `after` keeps its old base after an insertion
   below it) is shown to fail on the code before CR-215, so the scenario step that covers it is
   known to catch it.

Sources: `intake/request.md`; the batch-16 retro in
`.agents/changes/5-archives/261113-1726-215-stack-after-ready/retro.md`; CR-214's archive
`.agents/changes/5-archives/261113-1431-214-forge-permissions-at-start/` (its `03-change-spec.md`,
`work/pr-body.md`, `work/04-p10-real-settings.txt`); CR-215's archive
`.agents/changes/5-archives/261113-1726-215-stack-after-ready/` (its `03-change-spec.md`,
`work/pr-body.md`, Known gaps).

## Decisions carried from `02-answers.md`

| # | Decision | Where in this spec |
| --- | --- | --- |
| A1 | The proposal as filed is the scope (the user: "ok pour tout. fait ca maintenant"). Points the request does not settle take this specification's defaults, listed as open points | Areas 1 to 5; "Open points" |
| A2 | The CR joins the running batch-17 now | "Order in batch-17" |

## What changes

### Area 1: P10 detects `gh stack` with `gh extension list`

File: `skills/chantier/scripts/cli/src/chantier/commands.py`, `_sample_groups` (about lines 276 to
307). After CR-221 merges, the same function is in `commands/permissions.py` (see "Order in
batch-17").

Today the `gh-stack` group is added when a folder `gh-stack` exists under
`$XDG_DATA_HOME` (or `~/.local/share`) or `%LOCALAPPDATA%`, in `gh/extensions` or
`GitHub CLI/extensions`. CR-214's PR said why: "the CLI runs no forge command". That reason does
not hold: `gh extension list` reads only what is installed on the machine, and `forge-stack`
already runs `gh`. The folder test also misses an install elsewhere (`GH_CONFIG_DIR`, another
data directory).

The change:

- When the `github` group applies and `gh` is on `PATH` (`shutil.which("gh")`), run
  `gh extension list` once (`subprocess.run`, `capture_output=True`, `text=True`,
  `encoding="utf-8"`, `errors="replace"`, `check=False`, a 10-second `timeout`).
- Add the `gh-stack` group when it exits 0 and a line of its output names the extension's
  repository ending in `/gh-stack` (the second tab-separated column, today `github/gh-stack`) or
  starts with `gh stack` (the first column). Measured on this machine, gh 2.103.3: the output is
  `gh stack\tgithub/gh-stack\tv0.3.0`, in 73 ms.
- When `gh` is not on `PATH`, exits non-zero or times out, the group does not apply: the
  `gh stack` sample is not checked and not reported, as when the extension is absent. A missing or
  broken `gh` is P9's to report, not P10's. Nothing else is tried (no folder test kept beside it).
- The folder test and its `XDG_DATA_HOME` / `LOCALAPPDATA` lines go. The docstring says
  "the `gh stack` extension when `gh extension list` names it".

### Area 2: P10's count, explained

Nothing is wrong in the count; what it counts changed with CR-214 and nothing says so. On this
machine `work/04-p10-real-settings.txt` reads `P10 warn 14 of 16 commands …`:

- 16 is the number of sample commands that apply to this project, plus `SendMessage`: 6 in the
  `always` group, 7 in `github` (the remote is on github.com), 1 in `gh-stack` (the extension is
  installed), 1 in `gh-release` (the project's rules name `gh release create`), and `SendMessage`.
- 14 is how many of them the settings do not let through. The user's six allow rules
  (`~/.claude/settings.json`: `git push --force-with-lease origin chantier/*`,
  `… --force-with-lease -u origin chantier/*` and `… --force-with-lease=chantier/* origin *chantier/*`, each in its
  `Bash` and `PowerShell` form) cover two samples: `git push --force-with-lease -u origin <branch>`
  and the steering session's route. The `git -C … push --force-with-lease` sample is not covered.
- The old "19 of 19" counted recommended rule **strings** (19 at the time) not found as written.
  The new line counts **commands**, so the two numbers are not comparable.
- On Windows, a sample counts as not allowed when its `Bash` form or its `PowerShell` form has no
  allow rule (`commands_not_allowed`, the `tools` loop), and the rules named for it are those of
  the missing forms.

The change (no change to the code's count or to the line's words):

- `skills/chantier/references/hosts/claude-code.md`, "Who reads it, when", after "P10 checks the
  commands the agents run, not the rules' text": one or two sentences saying that P10's
  `<k> of <n>` counts commands, `<n>` being the samples that apply to the project (the always
  group, the remote's forge, `gh stack` when `gh extension list` names it, the publication when
  the project's rules name it) plus `SendMessage`; that on Windows a command counts as allowed only
  when both its Bash and PowerShell forms are; and that a count from before 0.9.0 counted rule
  strings and is not comparable.
- The same file, the `gh stack*` row of the "Allow rules" table (about line 186): "only with the
  `gh stack` extension installed" becomes "only when `gh extension list` names `gh-stack`".
- The comment above `_SAMPLES` in the CLI says the same in one line ("P10 counts these commands,
  not rules").

### Area 3: `forge-stack rebuild` exits 4 after five unstack tries

File: `skills/chantier/scripts/cli/src/chantier/forge_stack.py`, `_rebuild` (about lines 109 to
152); after CR-221, `commands/forge_stack.py`.

Today the loop's `else` raises `ChantierError(f"stack #{n} is still open after unstack")` with the
default code, `EXIT_PRECONDITION` (2). The `except ChantierError` around it re-raises a non-4
error as is, so the lines of `done` (the stacks already unstacked) are lost. The specification of
CR-215 says: "Any forge refusal stops at once, prints what was already done and the forge's exact
text, exit 4."

The change:

- The error is raised with `EXIT_EXTERNAL` (4): the forge did not do what it answered for. The
  existing handler then prints `done` before it, as for any other forge refusal.
- Its text names the tries and what the forge still holds:
  `stack #<n> is still open after 5 unstack tries (the forge reads it back with #<a> #<b>)`; with
  no PR left in it, `(the forge reads it back open, with no PR)`.
- The `5` is a named constant (CR-221's targets refuse a bare magic number).
- The docstring's last sentence ("When the forge refuses, its exact text comes back (exit 4).")
  adds: "and when a stack stays open after its unstack tries".

`rebuild` stays idempotent: the next run finds the stack and tries again.

### Area 4: the stale-SHA scan skips all-digit tokens

File: `commands.py`, `_stale_body_shas` (about lines 2414 to 2434); after CR-221,
`commands/delivery.py`.

Today the token pattern is `\b[0-9a-f]{7,40}\b`, so `20261113` or a 7-digit number is tried as a
commit, and is named as stale when it happens to resolve to one outside the head's history.

The change: a token is taken only when it holds at least one letter `a` to `f`
(`\b(?=[0-9a-f]{0,39}[a-f])[0-9a-f]{7,40}\b`, or the same test written after the match). The
docstring says that an all-digit token is not read as a commit. The rest of the scan is unchanged:
it is an `off:` line, never a refusal.

Accepted cost: an abbreviated SHA made only of digits is not checked. About one 7-character
abbreviation in 27 is all digits; none of 40 characters in practice. See open point 2.

### Area 5: the batch-15 base case, failed on the old code

No change to `_stack_base`. Evidence only, recorded in the PR body.

The batch-15 case (retro of CR-213, point "`order after` refused on a ready CR"): CR-212 had
`after: [CR-211]`; a CR was inserted between them (`order add`, then `stack`); CR-212's recorded
base stayed CR-211's branch. Before CR-215, `_stack_base` returned `_start_base` for any CR with an
`after` (not a fix), whatever its place in the stack. CR-215 changed that, and added two scenario
checks:

- `run_scenario.py`, about line 3319: "`ship` records the stack place as base for a stacked CR
  that has an `after`";
- about line 3491: "the release's base is the CR just under it after an insertion below it, and
  the CR above the new one sits on it (`take stack`)".

The Driver, in its worktree:

1. Replaces `_stack_base` with its body from `b3cc2be^`
   (`git show b3cc2be^:skills/chantier/scripts/cli/src/chantier/commands.py`), uncommitted (after
   CR-221 merges: in `commands/facts.py`, same body).
2. Runs the scenario (`--forge github`) and keeps the output: the first of the two checks fails
   (the second may fail too). It names which ones failed.
3. Restores the file (`git checkout -- <file>`, nothing committed), and runs the scenario again:
   both pass.

If neither check fails on the old body, the scenario does not reproduce the batch-15 case: the
Driver adds a step closer to it (a CR with an `after` on the CR under it, `ready`, then a CR
inserted between them with `order add` and `stack`, then `ship` and `take stack` for the CR with
the `after`), proves it fails on the old body and passes on the current one, and says so in the
PR. If it still cannot reproduce it, the PR's Known gaps say so, with the commands tried.

## Out of scope

- Any other point of batch-16's retro (Driver context, gate lock, Inspector re-run after a
  rebase, late hand-back on a merged CR, eval kit campaign): their own inbox items.
- A change to what P10 counts or to its line's words (Area 2 documents them; open point 1).
- Detecting other `gh` extensions, or checking the extension's version.
- A change to `_stack_base` (Area 5 is evidence only).
- Uppercase SHAs in the PR body (the scan stays lowercase, as `git` prints them).
- `hooks/`, `types/` (no `just mod`), the agent files, the CI workflow, any version edit.

## Order in batch-17

This CR touches the CLI, and CR-221 (`.agents/changes/4-batch/2-actives/221-python-inline-deps/`)
moves the same functions into new modules. **It does not need to wait for CR-221**: no change here
needs CR-221's code, and no change of CR-221 needs this CR's. They share files only, which is not a
reason for `depends.json`. Whichever merges second rebases on the other:

- If CR-221 merged first, this CR's Driver applies Areas 1, 3 and 4 in the moved modules
  (`commands/permissions.py`, `commands/forge_stack.py`, `commands/delivery.py`), restores the
  old `_stack_base` in `commands/facts.py` for Area 5, and meets CR-221's targets (`just lint` in
  `just check`): the new `subprocess.run` passes `check=False` explicitly (`PLW1510`), the tries
  count is a named constant (`PLR2004`), `_rebuild` stays within 50 lines and complexity 10 (split
  the unstack loop into a helper if needed), and the PEP 723 dependencies apply to `just scenario`.
- If this CR merged first, CR-221 carries the five changes as behaviour to keep (its "Behaviour
  kept" compares with `main` at its rebase).

## Evidence

**Checks:** `just check` passes (Linux, macOS, Windows). `tests/test_structure.py` (or, after
CR-221, the split test file that holds the preflight runs) is unchanged unless a test there reads
the gh-stack folder; the detection is proved in the scenario, not by a new structure test.

**Scenario** (`just scenario`, both forges; needed since the CLI and a card change):

1. `scenario/fake_gh.py` answers `extension list` from the state's `extensions` list (one
   `name\towner/repo\tversion` line each; none by default), exit 0.
2. In the P10 steps (about `run_scenario.py` lines 549 to 571), with the fake `gh` on `PATH`:
   with `extensions` naming `github/gh-stack`, the `P10 warn` line names `gh stack view`; with none,
   it does not. A `gh-stack` folder made under the data directory, with `extensions` empty, does
   not add it (the folder no longer counts).
3. In the `forge-stack rebuild` steps (about lines 3495 to 3549): `fake_gh.py` gains a state flag
   (for instance `unstack_ignored`) under which `unstack` answers 200 and leaves the stack open.
   With it set, and a first stack that unstacks normally before the stuck one (or the stuck one
   alone, if a second stack is too costly to set up), `rebuild` exits 4; its stderr holds the
   `unstacked #<n>` line of what was done (when there was one) and
   `is still open after 5 unstack tries`. With the flag cleared, a second run completes.
4. In the stale-SHA steps (about lines 3322 to 3338): a dangling commit whose first seven
   characters are all digits (made with `git commit-tree` in a bounded loop until its SHA starts
   with seven digits, so it resolves and is outside the head's history), named in
   `work/pr-body.md` by those seven digits: `ship` does not name that line, while the line naming
   the old head with letters is still named.
5. `scenario/README.md` lists the new steps.

**By hand, in the PR body:**

- `$CHANTIER preflight` in the main checkout with the user's real settings, on Windows: the P10
  line still names `gh stack view` (the extension is installed here, now found by
  `gh extension list`), and its count, with Area 2's breakdown of the 16.
- Area 5's two scenario outputs (the old `_stack_base` failing, the current one passing), with the
  names of the failed checks.

No CI job is added or changed.

## Self-containment for the Driver

Files to change:

- `skills/chantier/scripts/cli/src/chantier/commands.py` (`_sample_groups`, the `_SAMPLES` comment,
  `_stale_body_shas`) or, after CR-221, `commands/permissions.py` and `commands/delivery.py`
- `skills/chantier/scripts/cli/src/chantier/forge_stack.py` or, after CR-221,
  `commands/forge_stack.py`
- `skills/chantier/references/hosts/claude-code.md`
- `scenario/fake_gh.py`, `scenario/run_scenario.py`, `scenario/README.md`

No change to `hooks/` or `types/`, so `just mod` is not needed. No version edit. No agent file
changes (the cards change only in `hosts/claude-code.md`, read by both hosts' agents alike).

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **P10's count: explain, not change.** Default: the count stays (commands, not rules) and the
   card explains it (Area 2); the line's words do not change. Alternative: the line also names
   how many rules to add, or the groups it checked.
2. **All-digit tokens.** Default: skipped, at the cost of not checking an abbreviated SHA made
   only of digits (about 1 in 27 at seven characters). Alternative: skip them only below some
   length (for instance keep all-digit tokens of 12 characters or more).
3. **`gh` missing or failing in P10.** Default: the `gh stack` sample simply does not apply (P9
   reports `gh` itself); no folder test is kept as a second way. Alternative: P10 says in its
   line that it could not ask `gh` about the extension.
4. **Area 5 when the case cannot be reproduced.** Default: the Driver writes a closer step, and
   if that also passes on the old code, the PR's Known gaps say so; `_stack_base` is not changed
   by this CR in any case.
