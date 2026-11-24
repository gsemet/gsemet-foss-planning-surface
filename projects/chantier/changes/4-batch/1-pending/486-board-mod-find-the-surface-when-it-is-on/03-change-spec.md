# Board mod: find the surface from the project's planning pointer

Short name: `board-mod-surface`. One file of code, `hooks/register.tsx`, with its tests in
`hooks/register.test.tsx` and two lines of docs.

## Goal

In a Claude Code session whose folder is a project's checkout (markdown-okf-schema-studio, say)
and whose planning surface is only added to the session, `/chantier-board` shows that project's
board, read from the surface's `projects/<name>/changes/STATUS.json`. Today the pane is empty there.
A leftover `.agents/changes/` in the project, with no `STATUS.json`, no longer hides the surface.
The layout where the session's folder is the surface itself works as it does today.

## What the mod's engine offers (read 2026-11-25, Claude Code 2.1.330)

`$.session` answers `cwd`, `root`, `id`, `model`, `turns`, `messages`, `repo`, `surface`,
`surfaces`, `identity`, `usage`, `version`, `machine` and `info` (`transcriptPath`,
`scratchpadDir`, `promptId`, `agentType`, `configRoot`, `platform`, `isHosted`). None of them
lists the session's added working directories. `$.settings.read({ source })` reads one settings
layer, so it would see a `permissions.additionalDirectories` entry in a settings file, but never
a folder added with `--add-dir` or `/add-dir`. That is only part of the list, so this CR does not
use it (open question 1). As answer Q2 says, the means is the project's `AGENTS.md` `planning:`
pointer, matched by `git remote get-url origin` the way the session-start card
(`skills/chantier/references/session-start.md`, "Finding the surface") finds a surface.

## Today (origin/main)

- `findRoot($)` runs `git rev-parse --path-format=absolute --git-common-dir` in `$.session.cwd()`.
  The main checkout `root` is the parent of the common dir, or the cwd outside a repository.
  `findRoot` then calls `findBases($, root)`, reads the session id and calls `choose`.
- `findBases($, root)` returns `[{ name: null, dir: root/.agents/changes }]` as soon as that folder
  exists, even when it holds no `STATUS.json`. Otherwise it returns one base per
  `root/projects/<name>/changes`, and `[own]` when there is none.
- `choose` keeps the named bases whose `seat.json` or `4-batch/batch.json` names the session id,
  else all of them, with the line `No seat names this session: showing every project.`.
- `site.root` bounds the links that open in the pane (`isInside(root, …)` in `Linked`, the table
  cells and the document links). `site.common` is where `readBoardKeys` reads
  `chantier/server.json` for the Services section.

## What changes

### 1. `findBases` reads the project's pointer first (`hooks/register.tsx`)

`findBases($, root)` first reads `<root>/AGENTS.md` (`$.fs.read`). If the file is missing or
unreadable, the mod behaves as today.

- **The pointer line.** The first line that matches `- planning: <url>, projects/<name>`, with any
  leading spaces, `<url>` one token with no spaces, `<name>` one path segment and trailing spaces
  allowed. CRLF line ends are read like LF. A line that does not match is not a pointer.
- **No pointer line:** today's behaviour, unchanged. That is the project's own `.agents/changes/`,
  else `root/projects/*/changes` (the session's folder is the surface), else `[own]`.
- **A pointer line:** the project plans in the surface (the session-start card: with a pointer,
  the project's own `.agents/changes/` is not its planning folder). The mod never reads, draws or
  falls back to `root/.agents/changes`, with or without a `STATUS.json` (expected point 2). It
  looks for the surface's checkout among these candidates, in this order:
  1. the ancestors of `root`, nearest first, down to but not including the filesystem root (`/`
     or a drive's root). This covers a clone nested in the surface.
  2. the direct sub-folders of `parentOf(root)`, other than `root`, in name order
     (`localeCompare`). This covers a clone beside the surface, the usual layout of
     `projects/<name>/checkout.yml` (`repo: ../../../<clone>/`). The Studio's layout is this one.

  A candidate `S` matches when `S/projects/<name>/changes` exists (`$.fs.exists`) and
  `git remote get-url origin`, run with `cwd: S`, exits 0 with a url equal to `<url>` after
  normalisation. The mod runs git only for a candidate whose `projects/<name>/changes` exists.
- **URL normalisation** (the session-start card's rule): trim; drop a trailing `/`, then a trailing
  `.git`. `https://host/path`, `http://host/path`, `ssh://[user@]host[:port]/path` and
  `user@host:path` all become `host/path`, with the host lowercased and the path kept as written.
  Two urls match when their normal forms are equal.
- **One match `S`:** the bases are `[{ name: <name>, dir: S/projects/<name>/changes, pinned: true }]`.
  `site.root` is `S`, so the CR links and documents in the surface open in the pane.
  `site.common` is the surface's git common dir: the same `git rev-parse --path-format=absolute
  --git-common-dir`, run with `cwd: S`, so the Services section reads the surface board's
  `chantier/server.json`. If that call fails, `common` is null and the Services section shows no key.
- **No match:** no board. A one-line view through `site.error`, with the Refresh button:
  `This project plans in the surface at <url> (projects/<name>); no checkout of it was found above or beside <root>: clone it beside the project, or start the session in the surface.`
- **Several matches:** no board. A one-line view through `site.error` that names them all:
  `Several checkouts of the surface at <url> hold projects/<name>: <S1>, <S2>.`
  The mod does not pick one.

### 2. `choose` keeps a pinned base with no line

A base with `pinned: true` names its project exactly, through the pointer. `choose` returns it as
`kept` with `unseated: null`, reads no `seat.json` or `batch.json` for it, and draws no
`No seat names…` line. Its section keeps its bold project name, as a surface section does.
`rechoose` treats a site whose bases are all pinned like a project's own folder (it returns null).

Expected point 3: with the session's folder being the surface (no pointer, several
`projects/<name>`), the seat and batch records choose the project as they do today. Nothing in
that path changes.

### 3. Atom shapes and the header comment

- `Base` gains `pinned?: boolean`. Its type is stored in the `site` atom, so the tag goes from
  `site-5` to `site-6`, as the file's own rule says.
- The file's header comment and the "What it is" paragraph of `docs/boards.md` say what the mod
  reads and runs now. It reads the project's `AGENTS.md` for the `planning:` line, in addition to
  the index, the seat and batch records and `chantier/server.json`. It runs `git rev-parse` and
  `git remote get-url origin`, still read-only. `docs/boards.md` gains one sentence: with a
  `planning:` pointer, the pane reads the project's folder in the surface found above or beside
  the project's checkout, whose `origin` is the pointer's url.

### 4. When the search runs

Only in `findRoot`, so at opening (`begin`) and at each Refresh (`refresh`), as today. The 15 s
check does not search again. A Refresh after the surface is cloned finds it.

## Decisions of `02-answers.md`, carried

- Q1, go tonight: this specification is written on it.
- Q2, the four expected points stand. Point 1 is met by the pointer, matched by origin, because the
  engine lists no added working directories. Point 2: with a pointer, the own folder is never read.
  Point 3: the seat path is unchanged, and the pointer names the project in the Studio layout.
  Point 4: the tests below. Nothing falls back to a look-alike: no match, or several, is said in
  one line.
- Q3, proof: the PR carries one screenshot of the pane from a real Claude Code session in the
  Studio's layout (the Studio's checkout as the session's folder, the surface added), running the
  PR's head and captioned with the head's seven-character SHA. Until then, the PR's Known gaps
  says "no screenshot of the pane from a real session" (AGENTS.md).
- Q4, no spec critic.

## Out of scope

- Reading the session's added working directories: the engine offers no list. `$.settings.read`
  is not used (open question 1).
- A surface checkout placed neither above nor beside the project's checkout.
- The web board, the CLI, the cards (the session-start card stays as it is), Copilot (no pane) and
  the leftover `.agents/changes/` in the Studio (the mod ignores it; nothing deletes it).
- `checkout.yml`: the mod does not read it. The origin match and `projects/<name>/changes` decide.

## Evidence

Tests in `hooks/register.test.tsx`, run by `just mod` (`claude plugin test .`). AGENTS.md: a change
to `hooks/` passes `just mod` before its PR, run by the agent itself, which stops and says so if it
cannot run it. `just check` passes as well. The `world` fake answers `process.run` with one stdout
for every call today. It is extended to answer by `argv` and `cwd`: `rev-parse --git-common-dir`
per folder, `remote get-url origin` per folder, and an exit code per folder. The existing tests'
answers stay the same. The existing first-call assertion (`calls.run[0].argv` is the `rev-parse`)
still holds.

New tests, each one `test(...)`, parametrized where the list says so:

1. **The Studio layout (beside).** The cwd is `/work/studio` (common dir `/work/studio/.git`).
   `/work/studio/AGENTS.md` holds `- planning: https://github.com/o/surface, projects/studio`
   among other lines. `/work/studio/.agents/changes/` exists with no `STATUS.json`. `/work` lists
   `studio`, `surface` and `unrelated`. `/work/surface/projects/studio/changes/STATUS.json` has
   1 live and `/work/surface/projects/other/changes/STATUS.json` has 4 live. The origin of
   `/work/surface` is answered in each form, parametrized: `git@github.com:o/surface.git`,
   `https://github.com/o/surface.git`, `ssh://git@GitHub.com/o/surface`. Expected: `1 live` drawn,
   `4 live` not drawn, the `studio` name drawn, no `No seat names` line, no stat of
   `/work/studio/.agents/changes/STATUS.json` and none of the surface's `seat.json`, and a CR link
   under `/work/surface/projects/studio/changes/` that opens its sheet when pressed (inside
   `site.root`).
2. **A pointer hides an own folder even with a status.** As test 1, but
   `/work/studio/.agents/changes/STATUS.json` exists (7 live). Expected: `1 live`, never `7 live`.
3. **Nested layout.** The clone is `/work/surface/repos/studio`, and its ancestor `/work/surface`
   matches. Expected: the studio board.
4. **No match.** A sibling holds `projects/studio/changes`, but its origin is
   `https://github.com/o/elsewhere`. A second run has no candidate at all. Expected: the one line
   `This project plans in the surface at https://github.com/o/surface (projects/studio); no checkout of it was found above or beside /work/studio: …`,
   the Refresh button, and no board, even with an own `.agents/changes/STATUS.json`. Then the
   surface appears, a press of Refresh is simulated, and the board is drawn.
5. **Several matches.** `/work/surface` and `/work/surface-copy` both match. Expected: the
   `Several checkouts…` line naming both, and no board.
6. **No pointer line.** An `AGENTS.md` with no `planning:` line, parametrized with a missing
   `AGENTS.md`: today's own-folder behaviour (`INDEX` is read), and no `remote get-url` call.
7. **The surface's keys.** In the Studio layout, an index with `services.server`, and
   `/work/surface/.git/chantier/server.json` holding a key. Expected: the Services section's board
   link carries that key, read from the surface's common dir (the `rev-parse` run with
   `cwd: /work/surface`).
8. **A Windows drive path.** Test 1 with the cwd `C:/work/studio` and a pointer line ending in
   CRLF. Expected: the same board (the fake's `n()` maps the drive form).

The existing surface tests (cwd = the surface, the seat and batch matches, `MATCHES`) and the
own-folder tests pass unchanged. That is expected point 3.

The PR also carries the screenshot of Q3. The scenario (`just scenario`) does not run the mod. The
long gate is still owed by AGENTS.md's rule for a change outside the docs.

## Open questions

1. **A surface not placed above or beside the project's checkout.** This CR only finds the surface
   among the project's ancestors and the project's siblings, the two placements `checkout.yml`
   uses. A surface checkout elsewhere, added with `/add-dir`, is not found, and the pane says so
   in one line. Should the pane also try the `permissions.additionalDirectories` entries of the
   settings files (`$.settings.read`)? That would cover a folder added in settings, but never one
   added with `/add-dir` or `--add-dir`. This specification says no.
