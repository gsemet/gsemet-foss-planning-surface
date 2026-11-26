# Evidence 3: read by the CLI after the swap

Worktree `batch-31-CR-510`, uncommitted tree (base `88d9ab40`), 2026-11-26. Commands run from the
worktree. `$W` is the worktree, `$S` the CR folder's `work/scratch`.

## The Driver table

`uv run --no-sync --project $W python $S/e3_driver_table.py` (calls
`chantier.driver_prompt.driver_table()` and `chantier.roles_data.load_roles()`), exit 0:

```text
rows: 4
`cr-driver` | `take <cr>`, a CR of kind `change` or `fix` | `cr-driver.md` | the CR folder, then the absolute archive path when `take` prints one | yes | own branch
`release-driver` | `take <cr>`, a CR of kind `release` | `release-driver.md` | none | none | own branch
`stack-driver` | `take stack` | `stack-driver.md` | none | yes | batch branches
`qa-driver` | `order qa` | `qa-driver.md` | none | none | none
cr-driver: table Card=cr-driver.md roles.yaml card=cr-driver.md equal=True
release-driver: table Card=release-driver.md roles.yaml card=release-driver.md equal=True
stack-driver: table Card=stack-driver.md roles.yaml card=stack-driver.md equal=True
qa-driver: table Card=qa-driver.md roles.yaml card=qa-driver.md equal=True
roles.yaml driver roles: ['cr-driver', 'qa-driver', 'release-driver', 'stack-driver']
table rows equal the driver roles: True
all Card cells equal: True
```

## "Change Request" (`LAYOUT_GAP`)

`git grep -n "Change Request" -- skills/chantier/references/concepts.md` (the working tree, since
nothing is committed), exit 0:

```text
skills/chantier/references/concepts.md:20:## Change Request (CR)
```

## The host rows on both hosts

`CHANTIER_HOST=claude uv run --no-sync --project $W chantier host > $S/host-claude.log`: exit 0.
`CHANTIER_HOST=copilot uv run --no-sync --project $W chantier host > $S/host-copilot.log`: exit 0.

First lines of each (the whole outputs are the two logs, 257 and 260 lines):

```text
host: claude (this session)
start-foreman: Start the Foreman's session (untested)
  `mcp__ccd_session__start_session` with `initiation: "user_asked"`, `title: "<title>"`, `context: "fresh"`, no `cwd`, no `preset`, `use_worktree: false`.
  `model: "claude-sonnet-5-5"`, `effort: "medium"`, the user's permission mode; leave the session linked.
  This path was never tried for real here.
```

```text
host: copilot (this session)
start-foreman: Start the Foreman's session (untested)
  `create_session` with `model: "claude-opus-5.5"`, `workspace` = the repository, `worktree: false`, `title: "<title>"`.
  A refused start is reported with its exact text.
  This path was never tried for real here.
```

Each output checked against its JSON file: `python -I $S/e3_host_check.py $W $S/host-claude.log
$S/host-copilot.log`, exit 0:

```text
claude: claude-code.json rows=50 printed rows=50 same order=True missing lines=0 marks in the file=['proved', 'untested']
copilot: copilot.json rows=50 printed rows=50 same order=True missing lines=0 marks in the file=['untested']
```

## Unchanged files

Byte comparison of the base's `cards-next/` file with the staged file of `references/`:
`cmp <(git show 88d9ab40:skills/chantier/cards-next/<f>) <(git show :skills/chantier/references/<f>)`.

```text
cmp index floor.md exit=0
cmp index hosts/claude-code.json exit=0
cmp index hosts/copilot.json exit=0
```

The blob ids agree too (`git ls-tree 88d9ab40` and `git ls-files -s`): `floor.md` 61da01e8,
`hosts/claude-code.json` 3f2daf79, `hosts/copilot.json` b4dec473. `git diff --quiet` on the three
paths: exit 0 (no unstaged change). On this Windows checkout (`core.autocrlf=true`) the working
files carry CRLF; with the CR bytes removed they are equal to the base too (same `cmp`, exit 0).
