# Slim session-start.md: split by role, forge-neutral, sync card

Short name: `slim-session-start`. For the running batch batch-31. No issue.

## Goal

The owner, 2026-11-23: `skills/chantier/references/session-start.md` (29 768 bytes, read whole at
each session start by the router, the Chief of Staff and the Griller) is too big and written for
every role at once. Each role reads only what it needs, at the moment it needs it:

- section 1 (start checks) stays as it is;
- section 2 (the seat and the role) is split by role: one file each for the Chief of Staff, the
  Foreman and the Griller, the part that chooses the role staying common;
- section 3 (titles) is read by the Chief of Staff, the Foreman and the Griller only (the coders,
  the Drivers and the other workers never read it);
- section 6 (sync the checkout) becomes its own card, read only when a sync runs;
- the startup cards speak of "a forge": `gh` and `glab` live in each forge's own reference.

Nothing is lost: every moved instruction is named, with the card and the moment where it now
arrives, in a table the startup tests check, and a Fable advisor reads the split.

This CR goes first: `slim-the-startup-cards-of-the-three-roles` waits for it (it depends on this
one; slim-session-start-Q1). The Chief of Staff records that dependency; nothing in this CR's code
does.

## Decisions carried (02-answers.md)

| Question | Decision | Where in this spec |
| --- | --- | --- |
| Q1 order | This CR first; the sibling waits until it is merged in the batch | Goal |
| Q2 proof | A table naming each moved instruction, its card and its moment, checked by the existing startup tests; a Fable advisor reads the split | "The table of moves", Evidence |
| Q3 forge | `session-start.md` and the cards that come out of it speak of "a forge"; `gh` and `glab` live in each forge's reference; the other cards are a separate CR | "Forge wording", Out of scope |
| Q4 readers | Each role reads only its own file; coders, Drivers and workers read neither titles nor sync; the sync is its own card, read only when a sync runs; section 1 unchanged | "The new layout", "Who reads what" |
| Q5 | Specify for batch-31 | here |

## The new layout

All paths below are under `skills/chantier/references/` unless named otherwise.

### `session-start.md` (kept, slimmed: the common part)

Read by the router, the Chief of Staff and the Griller, as today. It keeps:

- Its header paragraph, rewritten to say who reads it and where each role's part is: "Read by the
  router, the Chief of Staff and the Griller at the start of a session and at each skill
  invocation; then the Chief of Staff reads [session-start-chief-of-staff](session-start-chief-of-staff.md),
  the Griller [session-start-griller](session-start-griller.md), both [titles](titles.md); the
  Foreman reads [session-start-foreman](session-start-foreman.md) only. A sync reads
  [sync-checkout](sync-checkout.md)." (wording the Driver's; the targets are these).
- `## 1. Start checks, first`: byte for byte unchanged (Q4), the trailing paragraph on P5, P9 and
  P10 included.
- `## 2. The seat and the role`, cut to the part that chooses the role, which the router needs
  before any role exists: the multi-project paragraph; `$CHANTIER seat` and its table; the
  message of a second session that becomes a Griller and its one option; the definitions of "a
  batch active" and "alive"; **Re-read the seat** (it applies to both roles); and one new line in
  place of the board and watcher parts: "Only the Chief of Staff starts the board and the
  watcher ([session-start-chief-of-staff](session-start-chief-of-staff.md)); a Griller, a Foreman,
  a Driver and the router before a role is chosen never start either."
- `## 4. First turn: introduce chantier` and `## 5. Reload`: kept, with the forge wording fix
  below in section 4 only. Their headings keep their numbers: `session-start.md#5. Reload` is a
  manifest reading, the four `SKILL.md` files, `hosts/claude-code.md`, `hosts/copilot.md`,
  `test_stack_shape.py` and `test_startup_manifest.py` (`FIRST_TURN`) cite them by these headings;
  renumbering is not this CR's.
- Section 3 and section 6 leave the file entirely, and so do the board and watcher parts of
  section 2.

### `session-start-chief-of-staff.md` (new)

`# Session start: the Chief of Staff`, then the Chief of Staff's part of section 2, moved with its
wording kept (only the forge words change, below), under level-2 headings that the tests name:

- `## The board`: the **The board.** paragraph; the host-without-watcher paragraph (the board
  question alone, `--forge-always`, the yes that covers a restart, a decline, a host with no
  background command); the stale-build paragraph ("Another project runs chantier from its checkout
  in plugin mode, ...", the `STALE_BUILD` text of `test_launch_modes.py`, kept once and verbatim)
  with its dev-mode parenthesis; the list of board lines (`board on <URL> over ...` to `error:
  board not started: ...`); "On a surface, `$CHANTIER serve --seat <id>` keeps the `--project`
  that `$CHANTIER` holds."
- `## The watcher`: the **The watcher.** paragraph and its lines, and "When it starts and stops:
  [chief-of-staff](chief-of-staff.md)."
- `## Stopping the board by hand`: that paragraph, and "A reload starts nothing: ...".
- `## The role changes`: the "become a griller" in the Chief of Staff bullet, introduced by "The
  user's word changes the role at any time".

### `session-start-griller.md` (new)

`# Session start: the Griller`, with:

- `## The role changes`: the "become chief of staff" / "tu es le chief of staff" in a Griller
  bullet, moved verbatim, introduced by "The user's word changes the role at any time".
- One line: a Griller never starts the board or the watcher; the Chief of Staff does.

### `session-start-foreman.md` (new)

`# Session start: the Foreman`, one section `## Startup core` (a manifest startup section must be
`file#heading`), holding the Foreman's part of sections 2 and 3:

- Your title is given in your prompt, `[<code>] ⚙️ Project · Foreman (Batch <nn>)` (the Foreman
  row of the titles table and its example `[Battle] ⚙️ Chantier · Foreman (Batch 17)`): set it
  first, by your host's means; a later Foreman of the same batch has the same title.
- You never start the board or the watcher; the Chief of Staff does (in direct mode, the Chief of
  Staff steering the batch keeps its own watcher, as `foreman.md` says).

It adds about 600 bytes to the Foreman's startup reading (7 721 bytes today on Claude Code, 7 902
on Copilot, under the manifest's limit of 12 544).

### `titles.md` (new)

`# Session titles`: section 3 moved whole and verbatim (the machine code, the icon, the project,
the batch number, the role, the separator, the table, the examples, the `seat take --title` line),
its first line saying it is read by the Chief of Staff and the Griller at the session's start and
by the Chief of Staff when it builds the Foreman's prompt. No worker, Driver or Foreman wrapper
lists it.

### `sync-checkout.md` (new)

`# Sync the checkout`: section 6 moved whole, its six steps verbatim, with only its references
fixed: "`session-start.md`'s board start" becomes "`session-start-chief-of-staff.md`'s board
start"; "`session-start.md`, "5. Reload"" stays (that heading stays). Its first line: read before
the first sync of a dev-mode session, by the session that syncs (the launch paragraph of the
`SKILL.md` files says who), at a session's start, a batch's start, and after a merge that changes
`uv.lock`. Who syncs does not change.

### `forges/github.md` and `forges/gitlab.md` (new)

One reference per forge, the place where `gh` and `glab` are named for what moved out of the
startup cards (Q3). Each holds, for its forge:

- its command-line tool, the user's own (`gh` for GitHub, `glab` for GitLab), and its word for a
  change (pull request, PR; merge request, MR: the words `board/forge_kind.py` already uses);
- what the startup cards say a forge is used for, with this tool: the surface server's forge hub
  reads the forge with it (only the PRs or MRs a running batch waits for, every 20 s while a
  client is subscribed, or always with `--forge-always`), and needs the network for that; a
  Driver opens the PR or MR and reads its CI with it.

Nothing else: the other cards' forge wording, and the rest of what a forge reference could hold,
belong to the separate CR (Q3).

## Forge wording

In `session-start.md` and in each new card above but `forges/`, no `gh` and no `glab`:

- The board paragraph's "it reads the forge every 20 s with the user's own `gh` or `glab`"
  becomes "with the user's own command-line tool for the project's forge (its reference in
  `forges/`)".
- Section 4's Drivers bullet, "with `git`, `gh` and `glab`", becomes "with `git` and the forge's
  own command-line tool (its reference in `forges/`)".
- Section 4's tracker examples "(Jira, GitHub, GitLab…)" stay: they name trackers, not a forge
  tool the session calls.

## Who reads what, and the manifest

`startup-manifest.json`:

- `actions.session-start` is replaced by two readings:
  - `session-start:chief-of-staff`: `session-start.md`, `session-start-chief-of-staff.md`,
    `titles.md`, `hosts/claude-code.md`, `hosts/copilot.md`;
  - `session-start:griller`: `session-start.md`, `session-start-griller.md`, `titles.md`,
    `hosts/claude-code.md`, `hosts/copilot.md`.
- `actions.chief-of-staff`: `session-start.md` stays, `session-start-chief-of-staff.md` and
  `titles.md` are added after it.
- `actions.board`: `["concepts.md", "session-start-chief-of-staff.md"]`.
- New `actions.sync`: `["sync-checkout.md"]`.
- `actions.route` and `actions.reload` unchanged (the router reads the common part; reload reads
  `session-start.md#5. Reload`).
- `startup_sections.foreman`: `"session-start-foreman.md#Startup core"` appended after the two
  existing readings.

The skills:

- `skills/chief-of-staff/SKILL.md`, Startup core: "At the session's start, read `session-start.md`
  and `session-start-chief-of-staff.md` (the manifest's `session-start:chief-of-staff` action)."
  Its first line (`watch: not running`) stays first.
- `skills/griller/SKILL.md`, Startup core: the same with `session-start-griller.md` and
  `session-start:griller`. Both keep the prefix "At the session's start, read `session-start.md`"
  (`SESSION` in `test_startup_manifest.py`).
- The launch paragraph, identical in the four `SKILL.md` files (`chantier`, `chief-of-staff`,
  `griller`, `status`; a test requires them equal): "by `session-start.md`, "6. Sync the
  checkout" (read it before the first sync)" becomes "by `sync-checkout.md` (the manifest's `sync`
  action; read it before the first sync)". Nothing else in that paragraph changes.
- `skills/chantier/SKILL.md`'s "(its table in `session-start.md`)" stays true.

The Foreman: `chief-of-staff.md`, step 4's prompt, "Read <skill>/references/startup-core.md,
<skill>/references/role-core.md and the named startup sections of <skill>/references/concepts.md
and <skill>/references/hosts/<host>.md now" gains "and <skill>/references/session-start-foreman.md"
after it, keeping the phrase `ABOUT_FOREMAN` of the tests whole; `foreman.md`'s two lines naming
its startup sections ("(`concepts.md`'s and your host card's)", and "Read the startup sections of
[concepts](concepts.md) and your host's reference") add `session-start-foreman.md`, keeping "At
startup read the startup core and the startup sections" (a `MOVED_IN` phrase). The `<title>`
sentence of step 4 cites [titles](titles.md), "the Foreman row", instead of session-start,
"Titles".

Coders, Drivers and the other workers: no reading of theirs changes; no manifest line of theirs
names `titles.md`, `sync-checkout.md` or any `session-start*.md`.

## Citations to update

Every link and named reference to a moved part points to its new card (a link to
`session-start.md` that means section 1, the seat table, "looks stopped", the first turn or the
reload stays):

- `chief-of-staff.md`: lines 7, 12 (read session-start: add the Chief of Staff's file), the
  table rows of lines 45 to 49 that mean the board (to `session-start-chief-of-staff.md`; "become
  a griller / chief of staff" keeps `session-start.md` for the seat, plus the two role files),
  511 ("start the surface server"), 829 (the sync, to `sync-checkout.md`), 975 (titles), 1006,
  1482 and 1509 (the watcher), 1835 ("Titles", to `titles.md`); 886 (re-read the seat) and 1570
  (the first-turn introduction) stay.
- `griller.md`: line 8 ("your seat reading and your title are in session-start": seat in
  `session-start.md`, title in `titles.md`, role change in `session-start-griller.md`); 63 and 99
  stay (the seat).
- `concepts.md`: 394 ("Titles" to `titles.md`), 752 and 755 (the watcher's start and stop rules,
  the stop command: to `session-start-chief-of-staff.md`).
- `hosts/claude-code.md` line 49 and `hosts/copilot.md` line 43 ("Run the board", `--forge-always`
  on a host that cannot run the watcher: to `session-start-chief-of-staff.md`); the Reload and
  "looks stopped" citations (claude-code 566, 768; copilot 51, 109) stay.
- `CONTRIBUTING.md` line 63 (the references list: `session-start.md` holds the start checks and the
  seat; add the three role files, `titles.md`, `sync-checkout.md` and `forges/`) and the tree at
  line 208 (add them, and "forges/ (one reference per forge: GitHub, GitLab)").
- Release notes of past versions are not edited.

## The table of moves

The Driver puts this table, completed with every moved instruction (one row each, its first words
quoted), in the PR's Deliverables. Each row has one `MOVED_IN` entry (the phrase, the new file,
its heading) and one `MOVED_OUT` entry (the phrase gone from `session-start.md`) in
`tests/test_startup_manifest.py`, the existing startup tests that check moves.

| Instruction (from) | Now in | Read when, by whom |
| --- | --- | --- |
| §2 "The board." paragraph | `session-start-chief-of-staff.md`, The board | Chief of Staff, session start (`session-start:chief-of-staff`), and before a board act (`board`) |
| §2 board question alone, host without watcher | same, The board | same |
| §2 stale-build paragraph (dev mode) | same, The board | same |
| §2 the board lines (`board on`, `board already running`, ... `writer not started`) | same, The board | same |
| §2 `serve --seat` keeps `--project` | same, The board | same |
| §2 "The watcher." and its lines | same, The watcher | same |
| §2 Stopping the board by hand; a reload starts nothing | same, Stopping the board by hand | same |
| §2 "become a griller" in the Chief of Staff | same, The role changes | same |
| §2 "become chief of staff" in a Griller | `session-start-griller.md`, The role changes | Griller, session start (`session-start:griller`) |
| §2 a Griller, a Foreman, a Driver, the router never start the board | `session-start.md` §2 (one line), and the Foreman's line in `session-start-foreman.md` | router, Chief of Staff, Griller at start; Foreman at startup |
| §3 titles, whole | `titles.md` | Chief of Staff and Griller at session start; Chief of Staff building the Foreman's prompt |
| §3 the Foreman row | `session-start-foreman.md`, Startup core | Foreman, startup (`startup_sections.foreman`) |
| §6 sync, six steps | `sync-checkout.md` | the syncing session, before its first sync (`sync`) |
| §2, §4 `gh` and `glab` | `forges/github.md`, `forges/gitlab.md` | by link, when the forge's tool matters |

Phrases the tests use (at least these, more as the Driver lists rows): "The board a watcher starts
is no background task of the session"; "I start the watcher, which starts the board if it is not
running?"; "`board: writer not started: <reason>`"; "\"become a griller\" in the Chief of Staff";
"\"become chief of staff\" / \"tu es le chief of staff\" in a Griller"; "A title tells first
whether the user talks to the session"; "`[<code>] ⚙️ Project · Foreman (Batch <nn>)`" (in the
Foreman's file); "Name the holders before syncing"; "with the user's own `gh`" style wording in
`forges/github.md` and its `glab` twin.

## Tests to update and add

All under `skills/chantier/scripts/cli/tests/`; each reads the shipped files from the repository
at the head under test (no prepared copy):

- `test_startup_manifest.py`: the `MOVED_IN` and `MOVED_OUT` rows above; `FOREMAN_SECTIONS` gains
  `"session-start-foreman.md#Startup core"`; the byte limit test keeps passing for every role and
  host (the Foreman's measure rises by the new section only).
- `test_launch_modes.py`: the `uv sync --locked --project "<plugin root>"` and
  `SYNC_SECTION_PHRASES` checks read `sync-checkout.md` whole instead of `session-start.md` section
  6; `SYNC_PARAGRAPH_PHRASES`' `'"6. Sync the checkout"'` becomes "`sync-checkout.md`"; the
  `STALE_BUILD` docs map names `session-start-chief-of-staff.md` instead of `session-start.md`
  (still exactly once); the foreign-build sentence's parametrized case names
  `session-start-chief-of-staff.md`.
- `test_command_names.py`, `test_the_blocked_sync_steps_name_the_serve_holder_and_its_stop`: reads
  `sync-checkout.md`.
- `test_plugin_files.py`, `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`: the
  card list gains `session-start-chief-of-staff`, `session-start-griller`,
  `session-start-foreman`, `titles` and `sync-checkout`.
- New, in `test_startup_manifest.py` (parametrized over the files): `session-start.md`, the three
  `session-start-*.md`, `titles.md` and `sync-checkout.md` name no `gh` and no `glab` (as a
  backticked command or a word: `\bgh\b`, `\bglab\b`); `forges/github.md` names `gh`,
  `forges/gitlab.md` names `glab`.
- New, same file: no manifest reading of a worker, a Driver role or the Foreman's wrapper names
  `titles.md` or `sync-checkout.md`, and only the Foreman's startup section names
  `session-start-foreman.md`.
- `test_stack_shape.py` (`batch:stack` in "## 5. Reload") unchanged and passing.

## Evidence

- `just check` green in the worktree at the pushed head (Linux, macOS and Windows by CI).
- The long gate `scenario` (`just scenario`, ubuntu-latest) green before the PR: the change is to
  the cards (AGENTS.md); in batch-31, the local `chantier gate <cr> scenario` when this CR is on
  top of the stack, as the rules say. Not under the CLI's `src/` or `evals/kit/`: no
  `just eval-dry-run` owed. No `hooks/` or `types/` change: no `just mod`.
- The table of moves in the PR's Deliverables, each row backed by its `MOVED_IN` and `MOVED_OUT`
  test.
- The sizes, measured and quoted in the PR (LF bytes): `session-start.md` before (29 768) and
  after, each new file, and the `startup-bytes` lines of
  `test_startup_manifest.py -k measures -s` for the router, the Chief of Staff, the Griller and the
  Foreman, before and after.
- The Fable advisor (Q2): before the push, one read-only reading on `claude-fable-5-2` of the old
  `session-start.md` (at the merge base) against the new files at head and the table, reporting
  each instruction not found, changed in meaning, or now read at another moment or by another
  role than the table says. Its report goes in the CR's `evidence/`; each finding is fixed or
  named in the PR's Known gaps. Who runs it is open question 1.
- No host or default matrix: what changes is which file holds a text and when it is read; no
  behaviour depends on the host or on a configured value.

## Out of scope

- The forge wording of every other card (`driver.md`, `chief-of-staff.md`, `foreman.md`,
  `concepts.md`, `hosts/`, `init.md`, ...) and of the CLI: a separate CR (Q3).
- Slimming the startup cards of the Chief of Staff, the Foreman and the Driver: the sibling CR
  `slim-the-startup-cards-of-the-three-roles`, which waits for this one.
- Sections 4 (first turn) and 5 (reload) beyond the forge wording; renumbering the kept headings.
- Who syncs, when a sync runs, and any change to the board, the watcher, the seat or the titles'
  rules: the text moves, the behaviour stays.
- The CLI: no code change.

## Open questions

1. **Who runs the Fable advisor.** This spec has the Driver start it before the push, as one
   read-only worker (an Inspector) on `claude-fable-5-2`. If the batch's playbook cannot start a
   worker on that model, the Driver stops and asks (no look-alike model). Or should the Chief of
   Staff run it at review, after the PR is ready, as for the spec critic?
2. **One shared `titles.md`.** Q4 says each role reads only its own file and that the titles are
   read by the three roles only. This spec keeps the titles in one shared `titles.md` (read by the
   Chief of Staff and the Griller; the Foreman gets its one row in its own file) rather than copying
   the title rules into both the Chief of Staff's and the Griller's files. Does that hold, or must
   each role's file carry its own copy?
