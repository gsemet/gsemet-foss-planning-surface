# Change Specification: the CR board pane shows the session's own project on a planning surface

## Goal

In a session whose main checkout is a planning surface (`<surface>/projects/<name>/changes/`),
the CR board pane (`/chantier-board`, `hooks/register.tsx`) shows the project this session steers,
not every project of the surface. Today Studio's Chief of Staff sees "No chantier status here:
.../projects/agentic-planning-surface/changes/STATUS.json not found." then chantier's batch-24
before its own batch: the pane picks its projects from the session's folder alone
(`findRoot`, `:173-184`; `findBases`, `:155-171`), while the CLI refuses that ambiguity
(`core/repo.py:116-118`, `SurfaceChoice`).

The session's project is the one whose seat names it (`changes/seat.json`, by either form of id),
or whose current batch's record names it as its Foreman or its Chief of Staff
(`4-batch/batch.json`). When several projects name it, the pane shows each of them. With none, the
pane shows every project, as today, under one line saying so.

## What changes

### `hooks/register.tsx`

1. **This session's id.** The pane reads it with `$.session.id()`, where it already calls
   `$.session.cwd()` (`findRoot`). That call is unproved in this repository: `just mod`'s
   `claude plugin validate` must accept it; a Driver whose validate refuses it stops and says so
   (no workaround). A call that is refused or fails at run time is not swallowed: the pane treats
   the session as matched by no project (point 3) and the line of point 4 names the error
   (`This session's id cannot be read (<error>): showing every project.`).

2. **Which ids match (settled).** A project matches when this session's id equals any of these
   fields, on either form of id the records hold:
   - `projects/<name>/changes/seat.json`: `session` (the id passed to `seat take`) and
     `transcript` (written by `commands/seat.py` `_take`);
   - `projects/<name>/changes/4-batch/batch.json`: `foreman`, `foreman_transcript`, each entry of
     `foreman_transcripts`, `chief_transcript` and each entry of `chief_transcripts` (so a Chief of
     Staff known only by the batch record, with no seat, sees its own project). Fields as in
     `core/records.py:178-182`. A batch is current (running or paused) while
     `4-batch/batch.json` exists (as `Repo.batch_folders`, `core/repo.py:227-229`).
   The comparison is exact string equality. A missing file, a file that does not parse, or a field
   that is absent or not a string (or, for `foreman_transcripts` and `chief_transcripts`, not a
   list of strings) matches nothing; none of these is an error line.

3. **The choice, on a surface root only.** `findBases` keeps its two cases:
   - `<root>/.agents/changes` exists: the in-project base, unchanged (no id read, no seat read).
     The stale in-project folder in Studio's repo is the user's to remove; this CR does not touch
     it.
   - A surface root: it lists every `projects/<name>/changes` as today (`bases`). The pane then
     keeps, among all `bases`, every project matched by point 2, in name order (settled: two that
     match are both shown). With none matched, it keeps them all, in name order, as today, and the
     site carries the line of point 4.
   The choice is made at opening (`begin`), at each periodic check (every 15 s) and at Refresh
   (`refresh`); each time it chooses again among all `bases`, so a seat taken or a batch record
   written after the pane opened (the Chief of Staff's skill opens the pane before it takes its
   seat) is followed within one check. A choice that changes the kept projects updates
   `feed.views` the way `refresh` does today (a view still kept keeps its state, a new one gets
   `newView`, a dropped one goes). The periodic check reads the files of point 2 (one `seat.json`
   and at most one `batch.json` per project) by stat and modification time, as `checkIndex` does:
   a file is read and parsed again only when its mtime changed, so an unchanged surface costs one
   stat per file per check. It does not run `git rev-parse` again; the session id is read at
   opening and again at Refresh.

4. **The no-seat line.** With no project matched on a surface root, the pane draws one dim line:
   `No seat names this session: showing every project.` (or the error form of point 1), once,
   above the project sections (under the Refresh bar), and also on the single-view `Alone`
   returns (`register.tsx:803-807`: a fatal schema, or "No chantier status here"). It is drawn in
   the board view only, not over a CR page. With one or more matched, no line.

5. **The site atom.** `site` keeps every project of the surface (`bases`) and gains the line
   (`unseated: string | null`); the kept projects are `feed.views`. Its shape tag goes from
   `site-2` to `site-3` (the file's rule: a shape change changes the tag).

6. The file's header comment (`:1-3`) says the pane shows, in a surface, the projects whose seat or
   current batch names this session, else one section per project.

### `types/index.d.ts`

`PluginState.chantier.site` becomes
`{ root: string | null; bases: { name: string | null; dir: string }[]; error: string | null; unseated: string | null }`.

### `hooks/register.test.tsx`

`world()` answers `session.id` (as it answers `session.cwd`, `:110`) with a settable id, and a
way to refuse it. New or changed tests, few and parametrized where they can be:
- a surface with `demo` and `other`, the id in one field of point 2 (parametrized over
  `seat.json`'s `session` and `transcript`, `batch.json`'s `foreman`, `foreman_transcript`, an
  entry of `foreman_transcripts`, `chief_transcript`, and an entry of `chief_transcripts`): only
  that project is drawn, and no `seat.json`/`batch.json` content of the other is used to draw; no
  no-seat line;
- the id in `demo`'s seat and in `other`'s batch: both drawn, no line;
- no match (the existing test `a planning surface shows one section per project`, `:250`): both
  projects drawn, and the no-seat line;
- `session.id` refused: both projects, and the line with the error;
- a single project with no `STATUS.json` and no match: the `Alone` "No chantier status here" view
  carries the no-seat line;
- a seat written after opening: the next periodic check (mocked clock, 15 s) keeps only that
  project; a check with no mtime change re-reads no file;
- the in-project case (`.agents/changes` present) reads no `seat.json` and draws no line.

### `docs/boards.md`

"What it is" (`:9-10`): "one section per project in a surface" becomes: in a surface, the
projects whose seat or current batch (as its Foreman or Chief of Staff) names this session, else
every project under a line saying no seat names it. "How to read it" (`:27`): the 15 s check and
Refresh also look again at which projects name this session.

## Out of scope

- The CLI's resolution of the planning folder (`core/repo.py`, `SurfaceChoice`) and the stale
  `.agents/changes/` in Studio's repository: the user removes it.
- A session in a code repository whose AGENTS.md names an external surface (`planning:`): the
  pane still does not follow that line; a separate inbox item.
- Any `STATUS.json` field: the pane reads `seat.json` and `batch.json` itself, the CLI is
  unchanged.
- Any change to what `seat take`, `foreman set` or the batch record write.
- The web board (`chantier board`).
- Plain sessions (a Griller does not open the pane): no seat or batch names them, they see every
  project with the line.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just mod` passes (a `hooks/` and `types/` change; AGENTS.md): `claude plugin validate` accepts
  `$.session.id`, `claude plugin test` runs the tests above. A Driver that cannot run it, or whose
  validate refuses `$.session.id`, stops and says so.
- No `just scenario` and no `just eval-dry-run`: no CLI, card or scenario change.
- A real-session screenshot (AGENTS.md, pane change): in the PR's Deliverables, the pane in a
  real Claude Code session running the PR's head, in a session seated on a surface project
  (only that project drawn), captioned with the head's SHA (seven characters). Until it is there,
  the PR's Known gaps says "no screenshot of the pane from a real session". The Driver notes in
  the PR which field the real session's id matched.

## Working choices (settled by the Spec-writer on the Chief of Staff's brief)

- The session id is read at opening and at Refresh, not at each 15 s check: it does not change
  within a session.

## Open questions

None.
