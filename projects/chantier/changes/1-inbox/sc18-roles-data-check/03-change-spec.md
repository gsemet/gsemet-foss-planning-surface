# SC18: Role data in `roles.yaml` and a `just roles` check of the wrappers

Child 18 of 28 of the program `simplify-cards-and-prompts`. The program's `03-change-spec.md`, its
`02-answers.md` (answers 17-22) and its `work/study-*.md` rank above this specification. F9, Q3 and
the other short ids are the program's findings and questions, carried as the program settled them
(answer 22). The owner's confirmation of answer 22 at wake is pending; this child does not depend
on anything beyond it.

## Goal

The roles become one data file that the CLI and a check read, instead of tables spread through the
code and the tests. `skills/chantier/roles.yaml` holds the 18 roles: each one's name, kind, who
starts it, its tools per host, what it writes, its reply format, its card, its first line, its
description and its host specifics. `brief` (child 10) and `help --for` (child 7) read this file in
place of their current tables, and their output does not change. A new `just roles` target checks
that the hand-written wrappers of both hosts agree with the data and that their bodies are
identical. The wrappers stay hand-written (Q3). Loading a project's own roles is a later CR with its
own grill (F9).

This child only adds things to the plugin. No card, wrapper or AGENTS.md text changes, and no role
is added, removed or renamed.

## Place in the chain

- **Base: child 17's branch** (`launcher`), in the single stack batch. Rebase on it before the
  first push.
- **Reads what children 7 and 10 built** (both are below it in the stack):
  - child 10's `src/brief_roles.py` (the `RoleData` dataclass and the `ROLES` tuple of 18 roles,
    with `name`, `card`, `wrapper`, `first`, `unit`, `writes`, `rows`). Child 10's spec says child
    18 replaces it, keeping `brief`'s bytes per role;
  - child 7's `src/commands/help.py`, whose `--for <role>` checks the role against the manifest's
    `roles` map (`references/startup-manifest.json`), and child 7's test that each topic's roles
    are in that map.

  If either file is not in the stack at this child's base, the Driver stops and says so. There is
  no fallback and no hand-made copy.
- **Relies on child 9's AGENTS.md wording**: "the CLI knows roles only as data
  (`skills/chantier/roles.yaml`, read by `brief`, `help --for` and `msg steering`)". That is why
  this child adds no AGENTS.md line (see open question 1 on `msg steering`).
- **Depended on by:**
  - children 19 to 23, which write the unloaded `cards-next/` set and run
    `brief <role> --cards skills/chantier/cards-next`. `brief` reads the role table from
    `roles.yaml` from here on, and `--cards` still changes only where the cards and the floor are
    read from;
  - child 24 (the swap), whose wrapper bodies change "only where a role's first line or card path
    changed, by hand, identical on both hosts, checked by `just roles`". Child 24 edits
    `roles.yaml` (`card`, `first`, `reply`) together with the wrappers, and `just roles` proves
    the two agree;
  - child 26, whose card gates are pytest gates. It may read `roles.yaml` for each role's card,
    but this child adds no budget or history lint (those are child 26's).

## Decisions carried

| Source | Decision | Where here |
| --- | --- | --- |
| Answer 12 (Q12) | Outside roles may be review steps, critics or workers that write in the worktree, never a steering role. This program keeps only the role kinds in its data | the `kind` field, with five values |
| Answer 22, F9 | Child 18 keeps `roles.yaml`, the lint and the wrapper check as a `just` target. Project roles are a later CR | the `just roles` target and `scripts/roles_check.py`; no `roles:` key in a project's `chantier.yaml` |
| Answer 22, Q3 | Wrappers stay hand-written; `roles build` becomes a check | `--write` prints the expected wrapper and writes nothing |
| Program, child 18 | `brief` and `help --for` read the data, with the same output | sections 3 and 4; the byte evidence |
| Program, child 18 | It replaces the "bodies identical" half of `tests/test_plugin_files.py` | section 6 |
| Program, Must not | No `roles:` key in a project's `chantier.yaml` (it collides with `src/playbook/config.py`'s `ROLES_MOVED`, line 35), no written wrappers, no role added, removed or renamed | Out of scope |
| Program, Risk | The long gate is owed. No AGENTS.md change | Gates; AGENTS.md change |
| Program, rules for every child | State the seconds added to `just test`; mark unproved claims; no version edited by hand | Acceptance evidence |

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/` and
`tests/` is `skills/chantier/scripts/cli/tests/`.

### 1. `skills/chantier/roles.yaml` (new)

The file is YAML, UTF-8, with LF line endings. It has a short header comment saying what reads it
(`brief`, `help --for`, `scripts/roles_check.py`), that the wrappers are hand-written and checked
against it, and that it lists the plugin's roles only. Its shape:

```yaml
version: 1
roles:
  - name: coder
    kind: worker              # steering | driver | worker | review-step | critic
    started_by: [driver]      # role names, a kind (any role of that kind), user, surface-server
    writes: worktree          # none | worktree | cr-folder
    reply: coder.md#Your part # <file>[#<heading>] under references/, or none
    card: coder.md            # path relative to skills/chantier/references/
    first: 'chantier coder for <cr> "<title>" of batch <batch>, in the project <root>.'
    description: 'Implements one round of one chantier CR in its worktree; never commits. Started by a Driver.'
    unit: cr                  # cr | order | stack | folder | none (brief's unit, from child 10)
    rows: [ending]            # child 8's capability ids that brief prints (from child 10)
    hosts:
      claude:
        wrapper: agents/coder.md
        tools: [Bash, PowerShell, Read, Edit, Write, Grep, Glob]
      copilot:
        wrapper: com.github.copilot/agents/chantier-coder.agent.md
        tools: [execute, read, edit, search]
```

What each field means:

- **`name`**: the role id. It is the agent type for the 15 roles with a wrapper, and
  `chief-of-staff`, `griller` or `foreman` for the three without.
- **`kind`**: one of the five values, as the program names them. Nothing in this child acts on
  `kind`: it is data, kept for the later project-roles CR (answer 12).
- **`started_by`**: who starts the role, taken from the wrapper description's "Started by…"
  sentence. For the three roles without a wrapper, it comes from the cards. Each token is a role
  name of the file, a kind name (meaning any role of that kind), `user` or `surface-server`.
- **`writes`**: the value child 10's `RoleData.writes` holds for the role, unchanged.
- **`reply`**: where the role's card states its reply format. A role that answers only the user
  (the three steering roles) has `none`.
- **`card`**: child 10's `RoleData.card`, unchanged. It is relative to `skills/chantier/references/`,
  so the two skill roles keep `../../chief-of-staff/SKILL.md` and `../../griller/SKILL.md`.
- **`first`**: the wrapper's `Prompt starts with:` text, the same on both hosts. It is `null` for
  the three roles without a wrapper.
- **`description`**: the wrapper's `description` cut before ` Prompt starts with:`. This is the
  cut `plugin_files.plugin_role_descriptions` already makes. For the three roles without a
  wrapper, it is one plain sentence, which nothing compares with a file.
- **`unit`** and **`rows`**: child 10's `RoleData.unit` and `RoleData.rows`, unchanged. They are
  carried here so that `brief` keeps no table of its own.
- **`hosts`**: the host specifics. For each of `claude` and `copilot`, `wrapper` is the
  repository path of the agent file (`null` for the three roles without one) and `tools` is the
  frontmatter's tool list, in the file's order. Tools are given per host because the two hosts
  name them differently (`Bash` against `execute`). A role without a wrapper has `tools: []`.

**How to fill the file.** Every value that child 10's `brief_roles.py` or a shipped wrapper already
holds is copied from there, never retyped from memory. The table below is the expected result at
`origin/main`'s wrappers and cards. Where it differs from `brief_roles.py` at the base or from a
wrapper, the shipped file wins and the PR names the difference.

| name | kind | started_by | writes | card | reply | unit |
| --- | --- | --- | --- | --- | --- | --- |
| chief-of-staff | steering | user | (child 10) | `../../chief-of-staff/SKILL.md` | none | none |
| griller | steering | user | (child 10) | `../../griller/SKILL.md` | none | none |
| foreman | steering | chief-of-staff | (child 10) | `foreman.md` | none | none |
| cr-driver | driver | foreman, chief-of-staff | cr-folder | `driver.md` | `driver.md#Means: your end` | cr |
| release-driver | driver | foreman, chief-of-staff | none | `driver.md` | `release-driver-end.md#Release driver: the end` | cr |
| stack-driver | driver | foreman, chief-of-staff | none | `driver.md` | `driver.md#Means: your end` | stack |
| qa-driver | driver | foreman, chief-of-staff | none | `driver.md` | `driver.md#Means: your end` | order |
| investigator | worker | driver | worktree | `investigator.md` | `investigator.md#Your part` | cr |
| coder | worker | driver | worktree | `coder.md` | `coder.md#Your part` | cr |
| debugger | worker | driver | worktree | `debugger.md` | `debugger.md#Your part` | cr |
| conflict-resolver | worker | driver | worktree | `conflict-resolver.md` | `conflict-resolver.md#Your part` | cr |
| verifier | worker | driver | worktree | `verifier.md` | `verifier.md#Your part` | cr |
| inspector | review-step | driver | worktree | `inspector.md` | `inspector.md#Your part` | cr |
| demo-explorer | worker | chief-of-staff | (child 10) | `demo-explorer.md` | `demo-explorer.md#Your part` | none |
| spec-writer | worker | chief-of-staff | (child 10) | `spec-writer.md` | `spec-writer.md#End` | folder |
| spec-critic | critic | chief-of-staff, griller | (child 10) | `spec-critic.md` | `spec-critic.md#Reply` | folder |
| retro-critic | critic | foreman, chief-of-staff | (child 10) | `retro-critic.md` | `retro-critic.md#Reply` | none |
| board-griller | worker | surface-server | (child 10) | `griller.md` | `griller.md#Started from the board` | folder |

The roles are listed in the file in this order. `rows` and every "(child 10)" cell are copied from
`brief_roles.py`. The `kind` column is this specification's reading of each wrapper's description,
and open question 2 asks the owner to confirm it.

### 2. `src/roles_data.py` (new): the one reader

- A frozen dataclass `Role` with the fields above (`hosts` as a mapping from host to a small frozen
  `HostSpec(wrapper: str | None, tools: tuple[str, ...])`).
- `load_roles(path: Path | None = None) -> tuple[Role, ...]` reads
  `plugin_files.skill_dir() / "roles.yaml"` with `ruamel.yaml` (`YAML(typ="safe", pure=True)`, as
  `plugin_files.plugin_role_descriptions` does). The `path` argument is for the tests' prepared
  cases. The result is cached per path.
- The loader checks the file's shape and raises `ChantierError(..., EXIT_PRECONDITION)` naming the
  role and the field when the check fails. The rules:
  - `version` is 1;
  - every field is present;
  - `kind`, `writes` and `unit` hold allowed values;
  - names are unique;
  - each `started_by` token is a name, a kind, `user` or `surface-server`;
  - `first` and both `wrapper` values are either all set or all `null`.

  The message ends "the plugin files are out of step", the wording `driver_prompt.driver_row` uses.
- `role(name) -> Role | None` and `names() -> tuple[str, ...]`, in the file's order.
- The module knows no role by name. Its docstring says the roles are data read from `roles.yaml`
  (child 9's wording).

### 3. `brief` reads `roles.yaml`

- `src/brief_roles.py` is removed. Every caller of its `ROLES` or `RoleData` (child 10's
  `src/commands/brief.py` and `tests/test_brief.py`) reads `roles_data.load_roles()` instead. The
  fields keep their names and meaning: `wrapper` becomes `role.hosts[host].wrapper is not None`.
- Child 10's unknown-role refusal (`unknown role '<x>'; roles: <list>`) lists `roles_data.names()`.
  It is the same 18 names in the same order: the file's order is child 10's `ROLES` order, and the
  Driver keeps it so.
- What the Drivers take from `driver_prompt.driver_table()` (team, rewrites, and the
  `concepts.md` table that `take` reads) stays read from there, as child 10 does. `roles.yaml`
  does not replace the `concepts.md` table: `take` still reads that table until child 24.
- No byte of a brief file or of a short prompt changes, for any role, unit or host (evidence 2).

### 4. `help --for` reads `roles.yaml`

- In child 7's `src/commands/help.py`, the role check of `--for <role>` reads `roles_data.names()`
  instead of the manifest's `roles` map. The refusal becomes
  `no role <role>; roles: <the 18 names>`.
- The output is unchanged for each of the 18 roles: its topics, or the line
  `no topic for <role>; help lists them all`. `help` with no argument and `help <topic>` are
  unchanged.
- The one visible difference: the manifest's map also holds `router` and `status`, two skills that
  are not roles. `help --for router` and `help --for status` now refuse, where they printed "no
  topic for …" before. Open question 3 asks the owner to confirm this.
- Child 7's test "each topic's role is in the manifest's `roles` map" checks against
  `roles_data.names()` instead.

### 5. `scripts/roles_check.py` (new) and `just roles`

- **Recipe**, in `justfile`, beside `journal-schemas`:

  ```
  # Check the hand-written agent files of both hosts against skills/chantier/roles.yaml (writes nothing)
  roles *args:
      {{run-cli}} scripts/roles_check.py {{args}}
  ```

  `run-cli` is `uv run --locked python`, so the script imports `chantier.roles_data` from the
  locked project: one parser for the CLI and the check. The recipe is not added to `check`,
  because `tests/test_roles_data.py` already runs the same checks on the shipped files in
  `just test`, which `just check` and CI run on the three systems.
- **Not a CLI command.** The script writes nothing anywhere: no file in the plugin, no planning
  folder, no git. It reads only files under `--root <dir>`, which defaults to the repository root
  found from the script's own path. The tests pass a prepared copy.
- **The checks.** Each failure prints one line: `roles: <role> (<host>): <what>`. The checks are:
  1. `load_roles()` on `<root>/skills/chantier/roles.yaml` passes its shape check.
  2. **Wrapper set.** Each host folder (`agents/`, `com.github.copilot/agents/`) holds exactly the
     wrapper paths the data names for that host: no file without an entry, no entry without its
     file.
  3. **Frontmatter**, per role and host, read with `ruamel.yaml` from the block between the first
     two `---` lines:
     - `name` is the role (claude) or `chantier-<role>` (copilot);
     - `description` equals `<description> Prompt starts with: \`<first>\``;
     - the tools equal `hosts.<host>.tools` in order: on claude, the comma list split on `, `; on
       copilot, the YAML list.
  4. **First line in the body.** The body holds ``My prompt must start with `<first>` `` and the
     text ``does not start with `chantier <role>`` (a prefix: the coder's body closes the backtick
     there, the board-griller's goes on with `` for the board` ``).
  5. **Card in the body.** When the body has a line `Your card is \`<x>\``, `<x>` is the
     basename of `card`. This is the "card path changed" guard that child 24 counts on.
  6. **Bodies identical.** For each role, the bytes after the frontmatter are identical on the two
     hosts.
  7. **Card exists.** `<root>/skills/chantier/references/<card>` is a file.
  8. **Reply format exists.** When `reply` is not `none`, its file exists under `references/`.
     With `#<heading>`, a line `# <heading>` or `## <heading>` exists in it, with the same text.
- **Output.** On success: `roles: 18 roles, 15 wrappers on 2 hosts agree` (the counts come from
  the data), exit 0. On failure: every problem line, then `roles: <n> problem(s)`, exit 1. A
  missing or unreadable `roles.yaml` exits 1 with one line naming it.
- **`--write <role> [--host claude|copilot]`.** Prints the wrapper the data expects, for one host or
  for both (each preceded by `=== <path>`), and writes nothing. The expected wrapper is:
  - the committed frontmatter, with `name`, `description` and the tools rewritten from the data in
    the file's own syntax, and every other key (`model`, `model-policy`, `background`,
    `autoCompactWindow`, `strict-tools-list`, `user-invocable`) kept as committed;
  - then the claude host's committed body, with the first-line texts of check 4 and the card name
    of check 5 replaced by the data's values.

  When everything agrees, the output equals the committed bytes. An unknown role exits 1, and so
  does a role without a wrapper (with the line `<role> has no wrapper`). This is the "`roles build`
  as a check" of Q3: a person editing a wrapper by hand copies from it, and nothing writes for them.
- The script is covered by `ruff` (`just lint` runs on `scripts`). It follows the repository's
  script style (`scripts/journal_schemas.py`): a module docstring, `main(argv) -> int`, and
  `if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))`.

### 6. `tests/test_plugin_files.py`: the "bodies identical" half leaves

- `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter` drops what `just roles`
  now checks:
  - the body identity;
  - the `name` and `description` equalities;
  - the `Prompt starts with:` and `My prompt must start with` assertions.

  It keeps the BOM check, the two refusal sentences ("a message to me gets this same answer…",
  "Any later message…"), the models, `model-policy`, `user-invocable`, `strict-tools-list`, the
  `Agent`/`agent` tool rule and `background`. It is renamed
  `test_each_host_gives_a_role_its_own_frontmatter`.
- `test_the_board_griller_has_the_same_body_on_both_hosts_and_refuses_another_prompt` drops the
  body identity, the name, the description and the first-line assertion. It keeps the models,
  `model-policy`, `user-invocable`, the tools rule and `## Started from the board`.
- The tuples `DRIVERS`, `WORKERS`, `CHIEF_ROLES`, `ROLES` and `ALL_ROLES` stay. Other tests in the
  file use them, and replacing them is not in this child's scope.

### 7. `tests/test_roles_data.py` (new)

Described under Acceptance evidence, item 1.

### 8. Docstrings

Child 9 left this rewording to children 10 and 18: the docstrings that say "the CLI knows no
role" in `src/plugin_files.py` (`plugin_roles`, `worker_prompt_lines`, `agent_problems`),
`src/driver_prompt.py` (`driver_prompt_lines`) and `src/commands/__init__.py` (line 14) now say
that the CLI reads roles only as data: the agent files, or `roles.yaml` for `brief` and `help`.
Only comments change; no code changes.

## Out of scope

- A `roles:` key, or any project role, in a project's `chantier.yaml` (F9; the key collides with
  `src/playbook/config.py`'s `ROLES_MOVED`). The later project-roles CR has its own grill.
- Writing or generating a wrapper (Q3). `--write` only prints.
- Adding, removing or renaming a role (program, answer 1), and any change to a wrapper, a card,
  `startup-manifest.json`, `concepts.md`'s Driver table or a `SKILL.md`.
- Other readers of the wrappers, which keep reading the agent files: `plugin_files.plugin_roles`,
  `plugin_role_descriptions`, `chief_prompt_lines`, `worker_prompt_lines`, `agent_problems`,
  `driver_prompt.driver_row`, the playbook's role lists (`playbook/edit.py`, `layers`, `timing`,
  `limits`) and `rules`. Moving them to `roles.yaml` is not asked. Their output must not change.
- `msg steering` (child 13): it reads no role table, and this child gives it none (open question 1).
- The models, `model-policy`, `background` and the other frontmatter keys that the data does not
  hold: they stay checked by `test_plugin_files.py`.
- `roles lint`, card budgets, the history lint and rule ids (child 26).
- A CLI command: `just roles` is a script only.

## Acceptance evidence

Every check reads the shipped files from the repository at the head under test:
`skills/chantier/roles.yaml`, `agents/`, `com.github.copilot/agents/`, `skills/chantier/references/`.
A prepared copy is used only for the refusals, which the shipped files cannot hold, and each
refusal case is paired with the passing case on the shipped files.

1. **`tests/test_roles_data.py` (new)**, calling `scripts/roles_check.py` in-process through
   `conftest.load_script` and `chantier.roles_data` directly:
   - **The shipped files agree**: `main(["--root", PLUGIN_ROOT])` returns 0 and prints the
     `18 roles, 15 wrappers on 2 hosts agree` line.
   - **The data's frame**: `load_roles()` gives 18 roles; their names are those of child 10's
     brief tests (the 15 wrapper roles plus `chief-of-staff`, `griller`, `foreman`); every `kind`
     is one of the five; every `writes` is one of the three; the 15 wrapper roles on each host are
     exactly the files `test_each_host_ships_one_agent_per_role_and_nothing_else` lists.
   - **Prepared mismatches** (parametrized; each copies `agents/`, `com.github.copilot/agents/`,
     `skills/chantier/roles.yaml` and `skills/chantier/references/` into `tmp_path`, then changes
     one thing). Each returns 1 and prints the expected `roles: <role> (<host>): …` line:
     - a description word changed on one host;
     - a tool removed on copilot only;
     - the bodies differ by one character;
     - the first line changed in the data only;
     - a `Your card is` name that disagrees with `card`;
     - `card` naming a missing file;
     - `reply` naming a missing heading;
     - an extra wrapper file with no entry;
     - an entry whose wrapper file is missing;
     - a `kind` outside the five (the loader's refusal, exit 1, naming the role and the field).
   - **`--write` writes nothing**: a snapshot of the repository's tracked files under `agents/`,
     `com.github.copilot/agents/` and `skills/chantier/` (names and bytes) is unchanged after
     `--write coder`. For every wrapper role and both hosts, `--write <role> --host <h>` prints the
     committed file's bytes after its `=== <path>` line. `--write foreman` exits 1 with
     `foreman has no wrapper`.
   - **No CLI command**: `chantier --help` lists no `roles` command (in-process, `chantier.cli`).
2. **`brief`'s bytes are unchanged for each role.** At the base (child 17's head, before any edit)
   and again at the PR's head, the Driver runs a throwaway script kept in its scratch folder, not
   committed. It calls the CLI in-process on child 10's test fixture (`world` / `stack_world`) and
   records the sha256 of the brief file and of the short prompt:
   - for each of the 18 roles × 2 hosts (`CHANTIER_HOST` `claude` and `copilot`);
   - with the unit child 10's tests use, and without it for the roles that have one;
   - and once with a configured generic agent for one worker.

   The same script records `help --for <role>` for the 18 roles, `help`, and `help --for router`
   (expected to change, section 4). The two lists are identical except the `router` line. The PR
   gives both lists, or their one-line digest, and states the exception. Child 10's
   `tests/test_brief.py` and child 7's help tests pass unchanged, apart from the import switch.
3. **The removed half is covered**: the PR lists the assertions dropped from
   `test_plugin_files.py` (section 6) and names, for each, the `roles_check` check that now makes
   it (checks 3, 4 and 6).
4. **`just roles`** passes on the committed wrappers. Its output is quoted in the PR. A
   hand-made mismatch also makes it fail, shown by running it on a scratch copy and quoted in
   the PR; the committed tree stays untouched.
5. **`just test` seconds** (F20): measured before and after on the same machine, and both numbers
   stated under Deliverables. Expected: about +1 s for `test_roles_data.py` (about 12 cases, each
   a copy of about 100 small files and a parse). The trimmed `test_plugin_files.py` takes a
   little less. The budget is 30 s above 18.5 s (AGENTS.md); the ceiling is still open
   (`2-backlog/P2/test-ceiling-decision`).
6. **Host and default matrix**, one line per cell:
   - claude, shipped defaults: `just roles` on `agents/`; `brief` and `help --for` bytes on the
     claude host (evidence 2).
   - copilot, shipped defaults: `just roles` on `com.github.copilot/agents/`; `brief` bytes on
     the copilot host. These are file checks only; no real Copilot session runs (unproved in a
     real session, as the program says for all Copilot rows).
   - claude, a project's role configured as a generic agent: the worker's brief carries its
     contract lines, with bytes unchanged (evidence 2). `roles.yaml` holds no model or agent, so
     the configuration's path is untouched.
   - copilot, configured: the same, file checks only, unproved in a real session.
7. **Gates**:
   - `just check` passes;
   - `just eval-dry-run` passes (a change under `src/`; child 6's quiz calls `brief`);
   - the long gate `just scenario (ubuntu-latest)` is green at the PR's head (a CLI change);
   - the local `chantier gate <cr> scenario` is owed only if this child is the stack's top when it
     is called ready, per AGENTS.md's stack rule.

   No scenario step is added: `just roles` is not a CLI command, and `brief` and `help` keep the
   steps children 10 and 7 added. `just mod` is not owed, since nothing under `hooks/` or `types/`
   changes.

## AGENTS.md change

None. The wrappers stay hand-written, so the rule "`agents/` … are hand-written, one file per role
and host … their bodies must stay identical" stays true word for word. Child 9 already names
`skills/chantier/roles.yaml` and its readers.

## Open questions

1. **`msg steering` and the AGENTS.md sentence.** Child 9's binding wording says `roles.yaml` is
   "read by `brief`, `help --for` and `msg steering`". The program gives this child only `brief`
   and `help --for`, and child 13's `msg steering` reads no role data: its target is fixed, and its
   audience is the steering session's key or `role:steering`. Once this child lands, AGENTS.md
   overstates by one reader. Default here: leave `msg steering` and AGENTS.md as they are, and name
   the gap in the PR's Known gaps. Should child 9's sentence drop `msg steering` instead (an
   AGENTS.md edit this child would then make), or should `msg steering` read something from
   `roles.yaml`?
2. **The role kinds.** The five kinds are the program's, but the program does not assign them to
   the 18 roles. Default here:
   - steering: Chief of Staff, Griller, Foreman;
   - driver: the four Drivers;
   - review-step: Inspector;
   - critic: Spec critic, Retro critic;
   - worker: every other role, the Verifier, the Spec-writer, the Demo explorer and the board
     Griller included.

   Nothing reads `kind` in this program, but the later project-roles CR will (answer 12: an outside
   role is a review step, a critic or a worker, never steering). Confirm, or move a role, for
   instance the Verifier to `review-step`.
3. **`help --for router` and `--for status`.** Today child 7 accepts every name of the manifest's
   map, including the two skills `router` and `status`, and prints "no topic for …". Read from
   `roles.yaml`, they refuse with the 18 role names. Default here: refuse (they are not roles; the
   program counts 18). Confirm, or keep them accepted, which would put two non-roles in
   `roles.yaml`.
