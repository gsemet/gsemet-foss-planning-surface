# Change Specification: the write guard reads Git Bash paths

## Goal

On Windows, an agent guarded by the plugin's write guard (a worker or a CR Driver, whose prompt
holds a `writes:` line) may write anywhere inside its folders, whatever form the path takes. Today
a path in the Git Bash drive form (`/c/Users/...`) is refused even when it is inside an allowed
folder (`C:/Users/...`): the guard compares the two as different paths. In batch-18's real eval
runs of 2026-11-15 this cost one refused call; every `/c/` path is refused the same way. The guard
maps the drive form before it judges.

Origin: verbal (the study of batch-18's two real eval runs of 2026-11-15; audits in
`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md` and
`real-direct-2026-11-15.audit.md`). No issue.

## Decisions carried from `02-answers.md`

1. The request's scope stands as written: map a Git Bash drive path to its drive form before the
   check. Planned for the next batch (parallel), before the next release.
2. No behaviour question is left open for the user; implementation detail is the agents'.

## What changes

### `hooks/register.tsx` (the only code file)

The guard's path helpers sit at the top of the file ("paths: plain strings, `/` everywhere, no
Node": `slash`, `clean`, `fold`, `isInside`) and the guard itself under "the worker write guard"
(`isAbsolute`, `judgeShell`, the `tool.call` handler).

- **The mapping.** A Git Bash drive path is a path whose first segment is one ASCII letter, either
  case: `/c`, `/c/`, `/c/Users/x`, `/D/work` (also with backslashes, which `slash` already turns
  into `/`). Its drive form is that letter, a colon, then the rest: `/c/Users/x` -> `c:/Users/x`,
  `/c` -> `c:/`. Nothing else is mapped (`/cc/x`, `/1/x`, `/mnt/c/x`, `/cygdrive/c/x`,
  `//server/share` keep their form).
- **When it applies.** Only in the guard's comparison of a path with an agent's folder, and only
  when one of the two sides is in drive form (`X:/...`): there the other side, if it is a Git
  Bash drive path, is mapped before the compare. On Linux and macOS, where no folder of a
  `writes:` line has a drive letter, nothing changes: `/c/x` stays a real POSIX path. A folder of
  the `writes:` line given in the Git Bash form (`writes: /c/Work/repo`) is judged by the same
  rule against a drive-form path (`C:/Work/repo/a.py` passes).
- **Where it applies.** Both guard branches of the `tool.call` handler:
  - Write, Edit and NotebookEdit: the `file_path` / `notebook_path` checked against
    `known.folders`.
  - Bash and PowerShell: each target `judgeShell` collects (redirections, `tee`, `sed -i`, `cp`,
    `Set-Content`, `[IO.File]::Write*` and the rest of `writtenBy`'s forms), checked against the
    folders. A Git Bash drive path is absolute (it is already, by `isAbsolute`), so it is not
    read against the agent's `cwd` and a preceding `cd` does not make it unjudged.
- **The other users of `isInside` are untouched.** The CR board pane's link and path opening
  (`isInside(root, path)` near the pane's `onOpen` and `showPath`) keeps its behaviour: the
  mapping lives in the guard's compare (a guard-only helper, or a parameter the guard alone
  passes), not in the shared `clean`, `fold` or `isInside` behaviour the pane relies on.
- **Messages unchanged.** A refusal still quotes the path as the agent wrote it (after `slash`),
  in the same two messages: `refused: <path> is outside the folders this agent may write in
  (<folder>; <folder>); write there` and `refused: a shell write to <path> is outside the folders
  this agent may write in (<folder>; <folder>); the shell follows the same rule as Write and
  Edit`. The board notes (`Write guard: could not ...`) are unchanged. No new note: a mapped path
  is judged, not left unjudged.
- **The spawn's `cwd` is unchanged.** The first folder of the `writes:` line is passed to the
  engine as written; this CR does not rewrite it.
- **A guard at fault still costs nothing**: the mapping runs inside the existing `try`, so a throw
  there lets the call pass with the existing note.

### `hooks/register.test.tsx`

In the "the worker write guard" section, beside the existing test `a Windows path in another drive
case or with backslashes is judged the same`, add cases (one parametrized test or a few short
ones, in the file's style with `guardWorld`, `spawn`, `write`, `shell`):

- An agent with `writes: C:/Work/repo.worktrees/b-CR-5; C:\Work\notes`:
  - Write to `/c/Work/repo.worktrees/b-CR-5/src/a.py` passes; so does `/C/work/notes/a.md`
    (letter and folder case) and Edit and NotebookEdit with a `/c/` path inside.
  - Write to `/d/Work/notes/a.md` is refused, with the one message quoting `/d/Work/notes/a.md`.
  - Write to `/c/Work/repo/a.py` (same drive, outside every folder) is refused.
  - Bash `echo x > /c/Work/notes/log.txt` and `cp a /c/Work/repo.worktrees/b-CR-5/b` pass;
    Bash `echo x > /c/Other/a` is refused with the shell message quoting `/c/Other/a`.
  - Bash `cd /c/Work; echo x > /c/Work/notes/a` passes with no `could not` note (an absolute
    target after a `cd` is judged).
- An agent with `writes: /c/Work/repo` (the folder in the Git Bash form): Write to
  `C:/Work/repo/a.py` passes; Write to `C:/Work/other/a.py` is refused.
- A POSIX agent, unchanged: with `writes: /work/repo` (the file's `WT`-style paths), a Write to
  `/c/work/repo/a.py` is refused (no drive form on either side: no mapping), and the existing
  tests keep passing unchanged.

### Docs and cards

- `skills/chantier/references/hosts/claude-code.md`, "The write guard": one sentence after "a
  relative path is read against the folder it runs in.": on Windows a Git Bash drive path
  (`/c/Users/...`) is read as its drive form (`C:/Users/...`), for Write, Edit, NotebookEdit and
  the shell targets alike.
- `docs/boards.md` (around its `writes:` paragraph) and `CONTRIBUTING.md` (the mod's paragraph):
  no change unless they state which path forms the guard reads; the Driver checks and aligns only
  if they do.
- `com.github.copilot/` and `agents/`: no change (Copilot has no guard).
- Release notes: an entry under the next release's notes (the release driver's usual place),
  in the project's style: the write guard reads a Git Bash drive path (`/c/...`) as `C:/...`.

## Out of scope

- WSL (`/mnt/c/...`), Cygwin (`/cygdrive/c/...`) and UNC (`//server/share`) forms.
- Any change to the CLI (`rails.py` and the rest), to `types/index.d.ts`, to the pane, or to what
  the guard covers (roles, tools, write forms).
- Rewriting the spawn's `cwd` or the paths an agent writes: the guard only judges.
- Symlinks, junctions and 8.3 short names (`C:/PROGRA~1`).

## Evidence

- `just mod` passes (the project's rule for a change to `hooks/`): `claude plugin validate .` and
  `claude plugin test .`, which run `hooks/register.test.tsx` with the new cases. A Driver that
  cannot run it stops and says so, with no workaround.
- `just check` passes on Linux, macOS and Windows.
- `just scenario (ubuntu-latest)` green at the PR's head (the change touches the plugin's hooks;
  the project's long gate). The scenario needs no new step: the guard's behaviour is proved by the
  mod's tests.
- The pane screenshot rule does not apply: the pane's drawing and `STATUS.json` are untouched.

## Open questions

None. `02-answers.md` leaves no behaviour question open; the choices above (the mapping only when
one side is in drive form, WSL and Cygwin forms out) are implementation detail within the
request's scope.
