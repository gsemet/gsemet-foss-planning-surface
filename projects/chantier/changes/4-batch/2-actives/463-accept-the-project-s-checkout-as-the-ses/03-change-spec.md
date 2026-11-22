# Accept the project's checkout as the session folder beside the surface

Short name: `session-folder`. Destination: the running batch batch-31, released right after with
no eval (`02-answers.md`, 3). No critic.

## Goal

chantier serves any project, in two layouts: in-project (`<project>/.agents/changes/`), or a
planning surface that serves n projects (`<surface>/projects/<name>/changes/`, the project's clone
placed by `projects/<name>/checkout.yml`: a gitignored subfolder of the surface, `repo: .repo`, or
beside it, `repo: ../../../<name>/`). A session may hold both the project's clone and the surface,
and its cwd may be either. Today a session whose cwd is the project's clone fails preflight P6 and
P7 (P7 with a false "linked worktree" message), so no batch opens and a Foreman it starts (no
`cwd`, it lands in the same folder) cannot pass its own preflight. After this CR:

- P6 and P7 pass when the cwd is the surface's main checkout or the project's main checkout (its
  clone), whichever comes first in the session; a real linked worktree, of the surface or of the
  project, still fails P7, and any other folder fails P6, each with its own exact message
  (`02-answers.md`, Q1: option A).
- The surface is found by the Chief of Staff from the project's `AGENTS.md` pointer line and the
  folders present, then kept for the session; every git read of the CLI that concerns the surface
  runs on the surface, and every one that concerns the project runs on the project's code
  repository, whatever the cwd (`02-answers.md`, Q2: option A).
- The cards say what the code does.

## What changes

### 1. `core/repo.py`: which checkout the session folder is

Add to `Repo` one read, `session_checkout(cwd: Path | None = None) -> SessionCheckout`
(`cwd` defaults to `os.getcwd()`, never `CHANTIER_ROOT`: it is the process's real folder that the
host runs the session in). `SessionCheckout` is a `NamedTuple` in the same module:

- `top: Path | None`: the cwd's `--show-toplevel`, resolved; None when the cwd is in no git
  repository;
- `linked: bool`: the cwd's `--git-dir` differs from its `--git-common-dir` (both resolved);
- `owner`: one of `"surface"`, `"clone"`, `"project"`, `"other"`, `"none"`:
  - in-project (`not repo.external`): `"project"` when the cwd's common dir equals
    `repo.git_dir`;
  - external: `"surface"` when the cwd's common dir equals `repo.git_dir` (the surface's);
    `"clone"` when it equals the clone's common dir (`git rev-parse --path-format=absolute
    --git-common-dir`, `cwd=repo.clone`, only when `repo.clone` is a folder);
  - `"other"`: any other repository; `"none"`: no git repository.
- `main: Path`: the main checkout of that owner, the one the session must be in: `repo.root`
  (in-project), `repo.surface_root` (surface), `repo.clone` (clone); for `"other"`/`"none"`,
  `repo.session_root`.

The cwd is read with one git process: `git rev-parse --path-format=absolute --show-toplevel
--git-dir --git-common-dir` (`cwd=` the folder, `check=False`), three lines. Paths are compared
resolved (`Path.resolve()`), as `_check_checkout` does today. The clone's common dir is read with
the exact argument list the test fixture caches (`rev-parse --path-format=absolute
--git-common-dir`). A nested clone (`projects/<name>/.repo`) is its own repository, so a cwd inside
it is `"clone"` and a cwd anywhere else in the surface (`projects/<name>/` included) is
`"surface"`.

`Repo.session_root` keeps its meaning (`self.surface or self.root`); its docstring says it is the
surface's checkout in external mode, and that the session may run in the project's clone too
(`session_checkout`).

### 2. `commands/preflight.py`: P6, P7, P11

`_check_checkout(r, repo)` uses `repo.session_checkout()`:

- **P6** passes when `owner` is `"project"`, `"surface"` or `"clone"` and `top == main`.
  - ok, in-project: `in the main checkout of <root.name>` (unchanged);
  - ok, surface: `in the main checkout of the surface <surface.name>`;
  - ok, clone: `in the project's main checkout <clone>; the plan is in the surface <surface>`;
  - FAIL, in-project: `session folder <top or cwd> is not the repository root <root>` (unchanged);
  - FAIL, external: `session folder <top or cwd> is neither the surface's checkout <surface> nor
    the project's clone <clone>: start the session in one of them`.
- **P7** passes when `not linked` (a folder in no repository is no linked worktree: ok).
  - ok: `not a linked worktree` (unchanged);
  - FAIL, owner `"project"`: `session folder <top> is a linked worktree of <root>: the Foreman
    must start in the main checkout`;
  - FAIL, owner `"surface"`: `session folder <top> is a linked worktree of the surface
    <surface>: the Foreman must start in the surface's main checkout or the project's clone`;
  - FAIL, owner `"clone"`: `session folder <top> is a linked worktree of the project's clone
    <clone>: the Foreman must start in the surface's main checkout or the project's clone`;
  - FAIL, owner `"other"`: `session folder <top> is a linked worktree of another repository`.

  The old text `this session runs in a linked worktree: ...` is gone: it was printed for a main
  checkout that is not the surface's.

Paths in messages are printed as `Path` prints them today (no change of style).

**P11** (`_check_surface`): `git branch --show-current` runs with `cwd=repo.surface_root`, not the
process's cwd. Today, from the project's clone, it reads the clone's branch and judges the surface
by it. Messages unchanged.

### 3. The audit: git reads of the CLI that depend on the cwd

Every `git(...)`, `default_branch`, `branch_exists`, `refusal`, `is_ancestor` and `subprocess`
git call under `skills/chantier/scripts/cli/src/chantier/` was read. Those with no `cwd` (they read
the process's cwd) and what each concerns:

| Call | Concerns | Change |
| --- | --- | --- |
| `preflight._check_checkout`, `--show-toplevel` and `--git-dir` | the session folder itself | replaced by `session_checkout` (section 2): reading the cwd is its point |
| `preflight._check_surface`, `branch --show-current` | the surface | `cwd=repo.surface_root` (section 2) |
| `intake.init`, `--git-dir` compared with `repo.git_dir` (the "preflight's P7" refusal) | the session folder | `repo.session_checkout()`: refuse only when `linked`, with P7's exact text for the owner (section 2) as the refusal, exit `EXIT_PRECONDITION`; today `init --project <folder>` from the project's clone is refused as a linked worktree |
| `permissions.commands_not_allowed`, `git remote` | the project's forge (the remote the batch's PRs go to) | `cwd=repo.root` when `repo` is given (the clone in external mode), else the process's cwd |
| `permissions._forges`, `git remote get-url <remote>` | the project's forge | same: `cwd=repo.root` when `repo` is given |
| `crs.py`, `git version` | git itself | none |

Today, from the surface's checkout, `git remote` reads the surface's remote, so P10 picks the
forge rows of the surface's forge, not the project's: a GitHub surface serving a GitLab project
gets the wrong samples. That is the same cwd fault and is fixed with it.

Every other git call already passes `cwd=` (the clone, a worktree, `repo.git_dir`,
`repo.surface_root`). The surface server's writer runs in the surface's checkout by its own paths
and is unchanged.

One read that is not git depends on the session folder in the same way: P10's settings files,
`permissions._settings_rules`, read `repo.session_root / ".claude" / "settings.json"` and
`settings.local.json`. The host loads a project's settings from the session's folder, so from the
project's clone it loads the clone's. Change: read them from `repo.session_checkout().top` when
it is not None, else `repo.session_root` (as today). Transcript lookups through
`repo.session_root` (`costs/transcripts.transcript_path`) already fall back to finding the session
id in any project folder, and the display helpers (`playbook/layers.display`,
`lifecycle/filing.shown`) fall back to absolute paths: no change.

### 4. The cards

**`skills/chantier/references/session-start.md`, section 1**, the bullet "With a planning
surface, ...", rewritten to say:

- With a planning surface, the session's folder is a main checkout, of the surface (on its default
  branch) or of the project (its clone, nested in the surface or beside it, as `checkout.yml`
  places it); the other folder is added to the session. P6 and P7 accept both and refuse a linked
  worktree of either.
- Finding the surface, once per session, before `$CHANTIER` runs: read the project's `AGENTS.md`
  pointer line (`- planning: <url>, projects/<name>`). With no pointer line and a
  `.agents/changes/` in the checkout, the project plans in itself (in-project layout): no
  `--project`. With one, the surface is the session folder (cwd or added working directory) whose
  `git remote get-url origin` names that url (compare without a trailing `.git`, and the same
  host and path over https or ssh) and that holds `projects/<name>/`; when the cwd is the surface
  itself, its own `projects/` names the project. `$CHANTIER` is then the skill's command plus
  `--project <absolute surface folder>/projects/<name>` for the whole session.
- Once found, the session keeps it: the plan's writes go through `$CHANTIER` (by absolute paths),
  and the session's own git reads run with `git -C <surface>` for the plan and `git -C <clone>`
  for the project's code, never with a bare `git` that reads whichever folder the cwd is.
- A session whose project `AGENTS.md` holds the pointer line and that has no folder matching it
  says, first, "this project plans in the surface at <url>; add its checkout to this session, or
  start the session there", and plans nothing in the project (replaces "start the session there").
- The project's clone hosts the session when it is the cwd; its linked worktrees (the CRs') never
  do.

**`skills/chantier/references/hosts/claude-code.md`**: the row "Session in a planning surface"
of the sessions table and the paragraph "The rule: starting a session from Remote Control" keep
their two setups and add that preflight P6 and P7 accept both main checkouts (the surface's, the
project's clone) and refuse a linked worktree of either; a Foreman started with no `cwd` lands in
the same folder and its preflight passes the same way. Nothing proved is rewritten; no new proof
is claimed.

**`skills/chantier/references/hosts/copilot.md`**: the row "A session in a planning surface ..."
adds, in the same words, that the session's folder may be the surface's main checkout or the
project's clone (P6 and P7 accept both), still unproved on that host.

**`skills/chantier/references/chief-of-staff.md`**: in "The project", one short paragraph after
the first: the surface is found as `session-start.md`, section 1, says, and kept for the session
(`--project` on every `$CHANTIER`, `git -C` for its own git reads). In "Starting a batch", step 1,
the preflight list reads "P6 (the session folder is a main checkout: the repository's, or with a
surface the surface's or the project's clone), P7 (not a linked worktree)".

**`skills/chantier/references/foreman.md`**: the worktree check before the epoch claim
(`git rev-parse --git-dir --git-common-dir`) is unchanged; add "(the surface's checkout or the
project's clone both pass)" after "If they differ, this session is in a worktree", so a Foreman
landing in the clone does not stop.

No agent file changes (`agents/`, `com.github.copilot/agents/`), no hook, no type: `just mod` is not
owed.

## Out of scope

- The CLI does not read the `AGENTS.md` pointer line: the Chief of Staff finds the surface and
  passes `--project <absolute folder>` (the open question below asks whether the CLI should also
  refuse a run without it).
- A bare `--project <name>` from the project's clone (it resolves under the clone's top and fails
  as today, "no project folder ... in a planning surface"); the cards already ask for an absolute
  folder.
- The write guard hook and what the host lets a session write outside its folder (the host
  references keep those rows unproved).
- Any change to the board, the writer, the hub, `lease`, `take` or the Driver's start folder.

## Evidence

Tests, in-process with the `chantier` fixture, in one new file
`skills/chantier/scripts/cli/tests/test_session_folder.py`, parametrized, set up with
`CHANTIER_HOST=claude` and `CLAUDE_CODE_ENTRYPOINT=claude-desktop` (as `test_allow_rules.py`), each
running `chantier --project <absolute project folder> preflight` and reading the P6, P7, P11 and
P10 lines:

1. **The session folders** (one test, parametrized over layout x folder):
   - layouts: `nested` (the `surface` fixture as is: `projects/demo/.repo`) and `beside`
     (`checkout.yml` rewritten to `repo: ../../../proj` and `worktrees: ../../../wt`, the `repo`
     fixture's folder, with `.repo` removed);
   - folders: `surface` (cwd the surface root) and `clone` (cwd the clone) expect P6 ok with the
     exact ok text of section 2 and `P7 ok   not a linked worktree`, and the run's exit code 0
     (the other checks pass on these fixtures, as `test_external_archive.py` shows from the
     surface); `surface-worktree` (`git worktree add <tmp>/swt -b s` in the surface, cwd there) and
     `clone-worktree` (`git worktree add <tmp>/cwt -b c` in the clone, cwd there) expect P7 FAIL
     with the exact text for that owner and exit `EXIT_PRECONDITION`; `other` (a fresh `git init`
     folder in `tmp_path`) expects the external P6 FAIL text and `P7 ok`.
   - The `clone` cell is the regression of this CR: it fails today with
     `P6 FAIL session folder ... is not the repository root ...` and
     `P7 FAIL this session runs in a linked worktree ...`.
2. **In-project** (one test, two cells): cwd the `repo` fixture expects P6 and P7 ok as today; a
   linked worktree of it expects `P7 FAIL session folder <wt> is a linked worktree of <root>: the
   Foreman must start in the main checkout`.
3. **P11 reads the surface** (one test, two cells, cwd the clone): the surface gets
   `refs/remotes/origin/main` (`git update-ref`) and `refs/remotes/origin/HEAD` pointing at it
   (`git symbolic-ref`); cell `surface-off-main`: the surface checked out on a branch `side`, the
   clone on `main`, expects `P11 warn the surface is on side, its default branch is main: ...`;
   cell `clone-off-main`: the surface on `main`, the clone on a branch `feature`, expects
   `P11 ok   the surface is on its default branch (main)`. Both fail today (they read the clone's
   branch).
4. **P10 reads the session folder's settings and the project's remote** (one test, cwd the
   clone): `.claude/settings.local.json` with `filled_allow()` written in the clone only expects a
   `P10 ok` line; today P10 reads the surface's (absent) settings and warns. A second cell writes
   the same file in the surface only, with cwd the surface, and expects `P10 ok` (unchanged
   behaviour).
5. **`init` from the clone** (one cell in test 1's file): `chantier --project <folder> init` with
   cwd the clone is not refused; with cwd the clone's linked worktree it exits
   `EXIT_PRECONDITION` with P7's clone text.

The tests build their linked worktrees with real git (`git worktree add`), as `conftest.py` says a
test that makes a worktree does; keep it to the cells above so `just test` stays within its budget.
No check here guards a shipped file's content.

Before the push, as `AGENTS.md` asks for a change under the CLI's `src/`: `just check` and `just
eval-dry-run` in the worktree at the rebased head. The long gate `just scenario` is not run locally:
the user's word, 2026-11-23 ("pas de porte longue", `02-answers.md`, 4); the PR's CI runs what it
runs, and the steering session merges only on a green CI. Nothing depends on the host or on a
shipped default versus a configured value: no host matrix.

By hand, once merged, in the Studio's session that filed this CR (cwd its main checkout, the
surface added): `$CHANTIER preflight --direct` prints `P6 ok   in the project's main checkout ...`
and `P7 ok   not a linked worktree`.

## Open questions

None left. Question 1 below was answered by the Chief of Staff, the user being asleep and having
asked for a small fix: no for this CR, filed as an inbox item (`02-answers.md`, 5).

1. Should the CLI also refuse a command run without `--project` in a checkout that has no
   `.agents/changes/` and whose `AGENTS.md` holds the pointer line (one line: "this project plans
   in the surface at <url> (projects/<name>): pass --project <surface folder>/projects/<name>"),
   instead of taking the project as in-project and writing its planning `.gitignore` there? It
   would guard a session that forgot the switch. Recommended: no for this CR (the user asked for a
   small fix released now); file it as an inbox item.
