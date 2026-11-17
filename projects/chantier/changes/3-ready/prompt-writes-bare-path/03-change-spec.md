# Change Specification: workers get a bare `writes:` line to copy, and Verifiers a scratch folder inside `work/`

## Goal

Batch-23 retro (`5-archives/batches/batch-23.md`, the last retro point): in CR-317, round 6, a
Coder could not write its round file because the `writes:` line of its prompt carried a
parenthetical; in CR-315 a Verifier wrote a scratch project to `C:/cvscratch`, outside its
`writes:` folders, and could not delete it afterwards (CR-315 `work/verify.md`: "I could not remove
the scratch folder `C:/cvscratch` (outside my `writes:`)").

As filed (02-answers.md, carry-Q7): the prompt skeleton the Driver works from prints `writes:` as a
bare path (no parenthetical), and it names a scratch folder inside `work/` for Verifiers.

## Why it happens today

- The write guard (`hooks/register.tsx`, `writesOf`) splits the first `^writes:` line of a prompt on
  `;` and trims each entry. Each entry must be absolute and nothing else. An entry such as
  `C:/.../101-one (work/, evidence/)` is still absolute to `isAbsolute`, so the guard accepts it as a
  folder, and then no real path is inside it: every Write to the CR folder is refused.
- No command prints a worker's `writes:` line. The Driver writes it by hand from the `worktree:`
  and `folder:` lines that `take`, `round` and `handoff` print (`driver.md`, "Children", and the
  checklist under "Every worker's prompt"). Both lines carry text after the path:
  - `folder: <path> (work/, evidence/)` (`commands/facts.py`, `cr_facts`);
  - `worktree: <path> branch <b> base <ref>[; not created yet: a Driver creates it first]`.
  A Driver that copies a value whole copies the trailing text too.
- The template in `concepts.md`, "Starting an agent", prints the line as
  `writes: <worktree>; <CR folder>   (a worker's prompt: worktree first; ...)`: the explanation sits
  on the line itself, in parentheses.
- The CR Driver's own `writes:` line is already printed bare by `take` (`driver_prompt.py`,
  `driver_prompt_lines`, value from `_cr_driver_block` in `commands/driver.py`). It does not change.
- The Verifier's card sends scratch projects outside its folders: `verifier.md` "Ground rules" says a
  probe of the board's write paths points at "a fresh temporary folder, or one under the worktree's
  test fixtures", and its capture paragraph allows "a scratch folder at a neutral location". On
  Claude Code the guard then refuses the Verifier's writes or deletes there (a visible shell
  `Remove-Item`/`rm` included), and the folder is left behind.

## What changes

### 1. The CLI prints the worker's `writes:` line, bare (`commands/facts.py`)

`cr_facts` (behind `take <cr>`, `round` and `handoff`) prints, after the worker opening lines
(`worker_prompt_lines`), one heading line and one indented line:

```text
worker writes line (copy it unchanged, without the two leading spaces, into each worker's prompt):
  writes: <worktree>; <CR folder>
```

- `<worktree>` is the CR's worktree path (`c.worktree`) and `<CR folder>` is `cr_directory(repo, c)`.
  Both are absolute and printed with forward slashes (`as_posix()`), the way the Driver's own line
  prints its folder. Nothing follows either path on that line: no parenthetical, no `branch`, no
  `base`, no "not created yet", no trailing `/`.
- The line is indented by two spaces, the same as the opening lines. When `take <cr>` puts the facts
  inside the CR Driver's skeleton (`DriverBlock.middle`), the line ends up indented by four. Once the
  Driver copies its prompt without the first two spaces, the line is still indented, so the guard's
  `^writes:` (column 0) does not read it in the Driver's own prompt. In every Driver's prompt the
  Driver's own `writes:` line stays the only one at column 0.
- A release CR prints the line too (`cr_facts` serves every kind). The release Driver starts no
  workers that need it, and the line is harmless there because it is indented.

### 2. The CLI prints the Verifier's scratch folder (`commands/facts.py`)

`cr_facts` prints one more fact line, directly after `folder:`:

```text
scratch: <CR folder>/work/scratch
```

The value is absolute, uses forward slashes and has nothing after it. The folder lies inside the
worker's `writes:` folders (the CR folder), so the guard allows the Verifier to write it and to
delete it. The CLI does not create it. Like any sub-folder of a CR, it is created when first written
(`concepts.md`, "A CR's folder").

### 3. The planning folder's `.gitignore` ignores `work/scratch/` (`core/files.py`)

- Add `work/scratch/` to `IGNORED` in `core/files.py`, next to `work/gates/`.
- `ensure_gitignore` already appends any missing entry to an existing `.gitignore`, so a planning
  folder created before this change gets the entry the next time the CLI writes there. No migration
  is needed.
- A scratch project the Verifier failed to remove (one with a nested `.git` included) is therefore
  never pushed with the planning surface or the project.
- `concepts.md`, "Planning folder": the list of what the `.gitignore` keeps out of git
  ("the detailed logs (`work/gates/`, `*.log`)") also names the Verifier's scratch folder
  (`work/scratch/`). In "A CR's folder", wherever `work/gates/` is named as not published,
  `work/scratch/` is named beside it.

### 4. A scratch project is its own repository, and every call there names it

`work/scratch` sits inside a git repository: the project's own (in-project mode, under
`.agents/changes/`) or the planning surface's clone (external mode). The CLI finds its project with
`Repo.find` (`core/repo.py`, lines 96-126):

- with `--project`, it uses that project folder;
- without it, `CHANTIER_ROOT`, or else the current folder, is resolved by
  `git rev-parse --git-common-dir`.

Because of that, a CLI or `board` call made under `work/scratch` without its own repository would
resolve to the enclosing repository and reach the live planning folder. So would a call that reuses
the `$CHANTIER` line from the Verifier's prompt, which carries the live project's `--project` in
external mode. The rule for the cards (02-answers.md, "Spec questions, round 2"):

- A scratch project under `work/scratch` is its own git repository. The Verifier runs
  `git init <scratch project>` before anything else there, and that runs before any chantier command.
- Every `chantier` or `chantier board` call aimed at the scratch project names it explicitly. Either
  `--project <scratch project's folder>` is given (for a scratch planning surface), or the call runs
  with the scratch repository as its working folder and no `--project` and no `CHANTIER_ROOT` that
  points elsewhere. It is never the `$CHANTIER` line of the prompt as printed: that line names the
  live project.
- The CLI's code does not change for this. It is a rule in the Verifier's card, proved by a check
  (Evidence).

### 5. The cards

- `concepts.md`, "Starting an agent", the template block: the `writes:` template line holds only
  `writes: <worktree>; <CR folder>`. Its explanation (a worker's prompt: worktree first; a Driver's:
  "A Driver's prompt"; a CR Driver: its CR folder, then the absolute archive path) moves into prose
  under the block. The prose also says that every entry on a `writes:` line is a bare absolute path
  with nothing after it, and that a worker's line is copied from the `worker writes line` that
  `take`, `round` or `handoff` printed. The other template lines with an inline parenthetical
  (`Steering:`, `Team:`, `Needs:`, the `Read <role>.md` line) keep it: they are not paths the guard
  reads. The `(...)` on the `writes:` line is the only one this CR moves.
- `concepts.md`, "A Driver's prompt": the bullet "Every path on a `writes:` line is absolute" also
  says that each path is bare (nothing after it), for every `writes:` line.
- `driver.md`, "Children" (the sentence "Every worker's prompt holds `writes: <worktree>; <CR
  folder>`, the two absolute paths as `take`, `round` or `handoff` printed them (`worktree:` and
  `folder:`)"): the worker's line is the `worker writes line` as printed, copied unchanged. It is
  never put together from `worktree:` or `folder:`, whose values carry text after the path.
- `driver.md`, the checklist under "Every worker's prompt": the `writes:` item becomes "the `writes:`
  line of the `worker writes line`, copied unchanged".
- `driver.md`, lines 559-560 ("A CR that touches the board's write paths carries the scratch-folder
  rule of [coder](coder.md) (the same in [verifier](verifier.md)) in each Coder's and Verifier's
  brief, and the evidence plan names the scratch folder its runs use"): name each card's own rule and
  drop "(the same in [verifier](verifier.md))". The sentence becomes, in substance:
  - each Coder's brief carries the scratch-folder rule of [coder](coder.md);
  - each Verifier's brief carries the `scratch:` folder and the rule of [verifier](verifier.md) for
    it (its own repository, every call naming it);
  - the evidence plan names the scratch folder each role's runs use.
- `driver.md`, the capture paragraph (about line 338, "a scratch folder at a neutral location"):
  the same change as in `verifier.md`, below, so that the two cards agree.
- `verifier.md`, "Ground rules":
  - The bullet on the board's write paths, reworded. It keeps its scope: a test, smoke run or probe
    of the board's write paths never points at the live planning folder. The difference is where
    each kind of folder goes:
    - the project's own tests (the suite, its fixtures, the `tmp` folders they make) keep their
      fixtures and tmp folders as they are;
    - only a throwaway the Verifier makes itself (a scratch planning folder, a probe project, a
      hand-run smoke run) goes under the `scratch:` folder the Driver's brief gives
      (`<CR folder>/work/scratch`), never a temporary folder or any other path outside the prompt's
      `writes:` folders.
    The bullet carries the rule of section 4: the scratch project is `git init`ed first, and every
    `$CHANTIER`/`board` call there names it explicitly, never with the prompt's `$CHANTIER` line as
    printed. The Verifier still removes the scratch project at its end, as today. It can do so
    because the folder is inside its writes.
  - A path under the scratch folder that is too long for Windows (a write, a `git` command or a
    tool failing on the path's length) is a stop. The Verifier reports it to its Driver with the
    exact error text, as for any refusal: no shorter folder outside its `writes:` folders, no other
    workaround. The claim that needed the scratch project is then not proved, and the verdict
    follows the card's existing rule for evidence that cannot be captured.
- `verifier.md`, the capture paragraph ("how you get it is yours (a scratch folder at a neutral
  location, a made-up folder name, `~`, `user`)"): "a scratch folder at a neutral location" is
  dropped, because a neutral location outside `writes:` is what CR-315 hit. The scratch project
  lives under `work/scratch`, which sits under the user's home folder, so a capture of it shows the
  user's paths. The Verifier rewrites them to made-up paths in the capture (for example in a text
  output before rendering it, or with `~` or `user`). A capture it cannot rewrite that way is not
  kept, and `before-after.md` names it with why, as the paragraph already says.
- The Driver's brief to a Verifier carries the `scratch:` line, along with "the other lines `take`,
  `round` or `handoff` printed" (`concepts.md` template), which already covers it. No new template
  line.

### 6. Hosts and agent files

- `hosts/claude-code.md`, "The write guard": one sentence saying that an entry is a bare absolute
  path. The guard reads anything after it as part of the folder's name, so every write is refused.
  The guard's code does not change (see Out of scope).
- `agents/` and `com.github.copilot/agents/`: no change unless a Verifier or Driver agent file
  repeats the card text touched above. Both hosts change together, with identical bodies (AGENTS.md).
- Copilot has no guard. The printed lines are the same on both hosts.

## Decisions carried from 02-answers.md

- batch-Q8: this CR joins the next batch, with the other five retro points of batch-23 and the four
  board CRs of 2026-11-17. (Batch membership is the Chief of Staff's job. Nothing in this spec
  depends on it.)
- carry-Q7, as filed: (a) the printed skeleton gives `writes:` as a bare path with no parenthetical:
  section 1, and the template fix in section 5; (b) it names a scratch folder inside `work/` for
  Verifiers: section 2 and the `verifier.md` changes in section 5.
- Spec questions (settled 2026-11-17):
  - the planning folder's `.gitignore` ignores `work/scratch/`: section 3;
  - the "neutral location" scratch option goes, and Verifiers use `work/scratch` and rewrite the
    user's paths in a capture or do not keep it: section 5, `verifier.md` and `driver.md` capture
    paragraphs;
  - a path too long on Windows is a stop the Verifier reports: section 5, `verifier.md` "Ground
    rules".
- Spec questions, round 2 (settled 2026-11-17, after the spec critic):
  - a scratch project is its own git repository, `git init` first, and every `$CHANTIER` or `board`
    call there names it explicitly, proved by a test or scenario check: section 4, `verifier.md`, and
    Evidence;
  - only throwaways the Verifier makes itself go under `work/scratch`, and the project's own tests
    keep their fixtures and tmp folders: section 5, `verifier.md` "Ground rules";
  - `driver.md` lines 559-560 name each card's own scratch rule: section 5.

## Out of scope

- The guard's parsing (`hooks/register.tsx`): no refusal, note or trimming for an entry that carries
  text after the path. A change to `hooks/` would need `just mod` (AGENTS.md) and was not asked for.
- The text of the `folder:` and `worktree:` lines. They keep their trailing text, because other
  readers split on it (the scenario's `check_driver_skeleton`, the tests). The cards stop sending
  anyone to compose `writes:` from them.
- A change to `Repo.find`'s resolution order. The isolation in section 4 is a rule of the card,
  proved by a check.
- A scratch folder for Coders, Debuggers and Investigators. `coder.md` and `debugger.md` keep their
  scratch-planning-folder wording. Only Verifiers were asked for.
- The CR Driver's own `writes:` line, and the release, stack and QA Drivers having none.

## Evidence

- Tests (`skills/chantier/scripts/cli/tests/`, parametrized, in-process, kept few):
  - `test_driver_prompt.py`: extend
    `test_the_commands_print_each_drivers_prompt_skeleton_without_a_writes_line_for_most`. For
    `take <cr>` of kind `change`, the output has the `worker writes line` heading followed by exactly
    one `  writes: <worktree>; <folder>` line. Its two entries are absolute, contain no space-then-`(`
    and equal the worktree path (posix) and the `folder:` path without its `(work/, evidence/)`. In
    the CR Driver's skeleton, once the two leading spaces are stripped, exactly one line starts with
    `writes:` at column 0 (the Driver's own). For `round` and `handoff`, the same worker line.
  - The same test, or one beside it: `scratch: <folder>/work/scratch` is printed right after
    `folder:`, absolute, with nothing after it, and inside the folder named on the worker's
    `writes:` line.
  - `test_cli_runs.py`, `_the_cr_drivers_writes_hold_the_folder_then_the_absolute_archive`: it
    takes the first line starting with `"  writes: "`, which after this change would be the worker
    line printed in the facts. Point it at the Driver's skeleton (the line after its heading, as
    `_skeleton` does) so it still checks the Driver's line.
  - A structure test that the `concepts.md` template's `writes:` line holds no `(`.
  - The planning folder's `.gitignore` holds `work/scratch/` after the CLI writes there. Use an
    existing `.gitignore` test if one checks `IGNORED`; otherwise add one case. A file under a CR's
    `work/scratch/` shows as ignored (`git check-ignore`) in a prepared repository.
  - Scratch isolation (a test, or the scenario step below; one of the two is enough), on a prepared
    repository with an open batch, in-project. Under a CR's `work/scratch/`, `git init` a scratch
    project, then run, from its folder, a CLI command that writes in its planning folder (for
    example the inbox `new` or an `inbox` add the board uses). The command lands in the scratch
    project's own `.agents/changes/`, and the live planning folder is unchanged: its file list and
    its batch record are byte-identical before and after. A command passed the scratch project's
    explicit `--project` (external form) holds the same.
- Scenario (`scenario/run_scenario.py`): `check_driver_skeleton` keeps passing. Its
  `startswith("  writes:")` inside the Driver block does not match the worker line, which is indented
  by four there. Add one check after a `take <cr>` and a `round`: the printed worker `writes:` line
  is bare, both paths are absolute, and the worktree comes first. When the scratch isolation is
  proved here rather than in a test, add a step doing the probe above in the scenario's world, and
  check that the live planning folder is unchanged.
- Gates: `just check` on the three systems, and `just scenario (ubuntu-latest)` green at the PR's
  head (the CLI, the cards and the scenario change). `just test` stays within its time budget.
- No CI job is added or changed.

## Open questions

None: the questions were settled in 02-answers.md, "Spec questions" and "Spec questions, round 2".
