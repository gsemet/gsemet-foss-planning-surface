# Slim session-start.md: split by role, forge-neutral, sync card

Short name: `slim-session-start`. For the running batch batch-31. No issue.

## Goal

The owner, 2026-11-23: `skills/chantier/references/session-start.md` (29 768 bytes at v0.15.1,
read whole at each session start by the router, the Chief of Staff and the Griller) is too big and
written for every role at once. Each role reads only what it needs, at the moment it needs it:

- section 1 (start checks) stays as it is;
- section 2 (the seat and the role) keeps in common what chooses and changes the role; the Chief
  of Staff's and the Griller's own parts go to one file each;
- section 3 (titles) becomes `titles.md`, read by the Chief of Staff and the Griller (the Foreman
  row stays in it, for the Chief of Staff that builds the Foreman's prompt); the coders, the
  Drivers and the other workers never read it;
- section 6 (sync the checkout) becomes its own card, read only when a sync runs;
- the startup cards speak of "a forge": `gh` and `glab` live in each forge's own reference.

Nothing is lost: every moved instruction is named, with the card and the moment where it now
arrives, in a table the startup tests check, and a Fable Inspector reads the split before the push.

This CR goes first: `slim-the-startup-cards-of-the-three-roles` waits for it (Q1). The Chief of
Staff records that dependency; nothing in this CR's code does.

## Decisions carried (02-answers.md)

| Question | Decision | Where in this spec |
| --- | --- | --- |
| Q1 order | This CR first; the sibling waits until it is merged in the batch | Goal |
| Q2 proof | A table of moves checked by the startup tests; a Fable advisor reads the split | "The table of moves", "Tests", Evidence |
| Q3 forge | The startup cards speak of "a forge"; `gh` and `glab` in each forge's reference; the other cards are a separate CR | "Forge wording", "The forge cards", Out of scope |
| Q4 readers | Each role reads only its own file; coders, Drivers, workers read neither titles nor sync; sync its own card, read only when a sync runs; section 1 unchanged | "The new layout", "Who reads what" |
| Q5 | Specify for batch-31 | here |
| Q6 advisor | The Driver, before the push, starts a read-only Fable Inspector | Evidence |
| Q7 titles | One shared `titles.md`; the Foreman has its own row in it | `titles.md` |
| Q8 limit | Keep 12 544 bytes; one `session-start` action; a SKILL.md sentence as short as today; the common header sends each role to its file | "The byte budget", "Who reads what" |
| Q9 role change | The role-change paragraph stays in the common `session-start.md`; the rule "read the file of the role the seat gives you, again when the role changes" is written there and in the skills | `session-start.md`, the skills |
| Q10 Foreman | No Foreman file; the Foreman's startup does not change; `titles.md` keeps the Foreman row (supersedes Q4's Foreman file) | `titles.md`, Out of scope |
| Q11 forge cards | `forges/github.md`, `forges/gitlab.md`; "Adding a connector" gains the step "add its `forges/<name>.md`"; cite `docs/forge-connectors.md` | "The forge cards" |

## The new layout

Paths are under `skills/chantier/references/` unless named otherwise. "Before" is
`session-start.md` at the merge base of the CR's rebased head with `main` (it then holds what
CR-467 and CR-468 of this batch added, if they merged first; see "Kept in common").

### `session-start.md` (kept, slimmed: the common part)

Read by the router, the Chief of Staff and the Griller, as today, through the one `session-start`
action. It holds:

- **Its header**, rewritten to send each role to its file, in substance: "Read by the router, the
  Chief of Staff and the Griller at the start of a session and at each skill invocation. Then
  read the file of the role the seat gives you, again when the role changes: the Chief of Staff
  [session-start-chief-of-staff](session-start-chief-of-staff.md), the Griller
  [session-start-griller](session-start-griller.md); both read [titles](titles.md). A sync reads
  [sync-checkout](sync-checkout.md)." The rule's words "read the file of the role the seat gives
  you, again when the role changes" are verbatim (Q9). The host-means sentence and the
  language sentence stay.
- **`## 1. Start checks, first`**: unchanged, byte for byte (Q4), its trailing paragraph on P5,
  P9 and P10 included.
- **`## 2. The seat and the role`**, the part that chooses and changes the role, which the router
  needs before any role exists:
  - the opening multi-project paragraph;
  - **kept in common, by name:** the paragraph CR-467 adds after that opening paragraph ("A
    session's CRs are its own project's (the one its `--project` names; for the Chief of Staff,
    the seat's) ...", the "waits for that project's own Chief of Staff or Griller" rule), and the
    lines CR-468 adds where the session reads `seat` (the arrivals no watcher has told, said in
    the session's first report, one line each, no action). Whichever of this CR and those two
    merges second carries the other's text into its own layout: when this CR is rebased onto
    them, they stay in common section 2, unchanged;
  - `$CHANTIER seat`, its table, the message of a second session that becomes a Griller and its
    one option, the definitions of "a batch active" and "alive";
  - **the role-change paragraph** ("The user's word changes the role at any time, both ways", its
    two bullets "become chief of staff" in a Griller and "become a griller" in the Chief of Staff),
    unchanged (Q9), followed by the rule "read the file of the role the seat gives you, again when
    the role changes";
  - **Re-read the seat**, unchanged;
  - one line in place of the board and watcher parts: "Only the Chief of Staff starts the board and
    the watcher ([session-start-chief-of-staff](session-start-chief-of-staff.md)); a Griller, a
    Foreman, a Driver and the router before a role is chosen never start either."
- **`## 4. First turn: introduce chantier`** and **`## 5. Reload`**: kept, with only the forge
  wording fix below in section 4. Their headings keep their numbers: `session-start.md#5. Reload`
  is a manifest reading, and the four `SKILL.md` files, `hosts/claude-code.md`, `hosts/copilot.md`,
  `test_stack_shape.py` and `test_startup_manifest.py` (`FIRST_TURN`) cite them by heading.
- Sections 3 and 6, and the board and watcher parts of section 2, leave the file.

### `session-start-chief-of-staff.md` (new)

`# Session start: the Chief of Staff`, then the Chief of Staff's part of section 2, moved with its
wording kept (only the forge words change, below), under level-2 headings the tests name:

- `## The board`: the **The board.** paragraph; the host-without-watcher paragraph (the board
  question alone, `--forge-always`, the yes that covers a restart, a decline, a host with no
  background command); the stale-build paragraph ("Another project runs chantier from its checkout
  in plugin mode, ...", `STALE_BUILD` in `test_launch_modes.py`, kept once and verbatim) with its
  dev-mode parenthesis; the list of board lines (`board on <URL> over ...` to `error: board not
  started: ...`); "On a surface, `$CHANTIER serve --seat <id>` keeps the `--project` that
  `$CHANTIER` holds."
- `## The watcher`: the **The watcher.** paragraph and its lines, and "When it starts and stops:
  [chief-of-staff](chief-of-staff.md)." In the `no seat` line, "only when the session is the Chief
  of Staff by the role rules above" becomes "by the seat table of
  [session-start](session-start.md), "2. The seat and the role"" (the rules are no longer above).
- `## Stopping the board by hand`: that paragraph, and "A reload starts nothing: ...".

### `session-start-griller.md` (new)

`# Session start: the Griller`, holding the Griller's part of section 2: a Griller never starts the
board or the watcher (the sentences of the board's and the watcher's paragraphs that name the
Griller among those that never start them), and the lines of the board and the watcher it may meet
are the Chief of Staff's. It is short; see open question 1.

### `titles.md` (new)

`# Session titles`: section 3 moved whole and verbatim (the machine code, the icon, the project,
the batch number, the role, the separator, the table with its Foreman row, the examples, the
`seat take --title` line), its first line saying it is read by the Chief of Staff and the Griller
at the session's start and by the Chief of Staff when it builds the Foreman's prompt (Q7, Q10).

### `sync-checkout.md` (new)

`# Sync the checkout`: section 6 moved whole, its six steps verbatim, with only its references
fixed: "`session-start.md`'s board start" becomes "`session-start-chief-of-staff.md`'s board
start"; "`session-start.md`, "5. Reload"" stays. Its first line: read before the first sync of a
dev-mode session, by the session that syncs (the `SKILL.md` launch paragraph says who), at a
session's start, a batch's start, and after a merge that changes `uv.lock`. Who syncs does not
change.

### The forge cards (new): `forges/github.md`, `forges/gitlab.md`

One reference per forge, where `gh` and `glab` are named for what leaves the startup cards (Q3,
Q11). Each holds, for its forge, and cites [docs/forge-connectors.md](../../../docs/forge-connectors.md)
(the relative link from `references/forges/` the Driver checks):

- its command-line tool, the user's own (`gh` for GitHub, `glab` for GitLab), the `program` of its
  connector (`connectors/github.py`, `connectors/gitlab.py`), and its word for a change (PR, MR:
  the connector's `word`);
- what the startup cards say a forge is used for, with this tool: the surface server's forge hub
  reads the forge with it (only the PRs or MRs a running batch waits for, every 20 s while a
  client is subscribed, or always with `--forge-always`), and needs the network for that; a
  Driver opens the PR or MR and reads its CI with it.

Nothing else: the other cards' forge wording belongs to the separate CR (Q3).

`docs/forge-connectors.md`, "Adding a connector": a fourth step, "Add its
`skills/chantier/references/forges/<name>.md`, the forge's reference: its command-line tool and its
word, as `forges/github.md` does." The intro sentence's list ("one module ..., one line in a table,
a fake forge for the tests and a row in Supported hosts") gains "and its forge reference".

## Forge wording

In `session-start.md`, `session-start-chief-of-staff.md`, `session-start-griller.md`, `titles.md`
and `sync-checkout.md`, no `gh` and no `glab`:

- The board paragraph's "it reads the forge every 20 s with the user's own `gh` or `glab`"
  becomes "with the user's own command-line tool for the project's forge (its reference in
  `forges/`)".
- Section 4's Drivers bullet, "with `git`, `gh` and `glab`", becomes "with `git` and the forge's
  own command-line tool (its reference in `forges/`)".
- Section 4's tracker examples "(Jira, GitHub, GitLab…)" stay: they name trackers, not a tool the
  session calls.

## Who reads what, and the manifest

`startup-manifest.json`:

- `actions.session-start` stays one action (Q8): `session-start.md`, `hosts/claude-code.md`,
  `hosts/copilot.md`, as today. The role files and `titles.md` are reached by the common header's
  rule, each role reading its own.
- `actions.chief-of-staff`: `session-start-chief-of-staff.md` and `titles.md` added after
  `session-start.md`.
- `actions.board`: `["concepts.md", "session-start-chief-of-staff.md"]`.
- New `actions.sync`: `["sync-checkout.md"]`.
- `actions.route`, `actions.reload` and every `startup_sections` entry unchanged; the Foreman's
  startup does not change (Q10).

The skills:

- `skills/chief-of-staff/SKILL.md` and `skills/griller/SKILL.md`, Startup core: the sentence keeps
  the prefix "At the session's start, read `session-start.md`" (`SESSION` in the tests) and says,
  in no more bytes than today's sentence ("At the session's start, read `session-start.md` (the
  manifest's `session-start` action)."), that the session then reads the file of the role the seat
  gives it, again when the role changes (Q8, Q9). The Chief of Staff's first Startup core line
  (`watch: not running`) stays first.
- `skills/chantier/SKILL.md` (router): its "(its table in `session-start.md`)" stays; the router
  loads the chosen skill, which carries the rule.
- The launch paragraph, identical in the four `SKILL.md` files (a test requires them equal): "by
  `session-start.md`, "6. Sync the checkout" (read it before the first sync)" becomes "by
  `sync-checkout.md` (read it before the first sync)". Nothing else in it changes.

`chief-of-staff.md`, step 4's `<title>` sentence cites [titles](titles.md), the Foreman row,
instead of session-start, "Titles". The Foreman's prompt and `foreman.md` do not change.

Coders, Drivers and the other workers: no reading of theirs changes; no manifest line of theirs
names `titles.md`, `sync-checkout.md` or a `session-start*.md`.

## The byte budget

The manifest's limit stays 12 544 bytes (Q8), for each role and host, startup and reload. The
whole `SKILL.md` counts in a skill role's startup. Measured at v0.15.1 (`pytest
test_startup_manifest.py -k measures -s`, `startup-bytes` lines), startup / reload:

| Role | Claude Code | Copilot |
| --- | --- | --- |
| chief-of-staff | 11 623 / 12 515 | 11 629 / 12 521 |
| griller | 11 184 / 12 076 | 11 190 / 12 082 |
| status | 11 390 / 12 282 | 11 396 / 12 288 |
| router | 11 140 / 12 032 | 11 146 / 12 038 |
| foreman | 7 721 / 8 613 | 7 902 / 8 794 |

The Chief of Staff's reload on Copilot has 23 bytes left. So: the four skills' launch paragraph
change shortens each by about 23 bytes, and the Startup core sentence of the Chief of Staff and
the Griller may grow by no more than that saving; the PR quotes the lines before and after, every
role at or under its v0.15.1 figure plus that net, and all under 12 544. The Foreman's figures do
not change.

## Citations to update

Each link to a moved part points to its new card; a link to section 1, the seat table, the role
change, "looks stopped", the first turn or the reload stays on `session-start.md`:

- `chief-of-staff.md`: lines 7 and 12 (read session-start: add the role file), the rows of lines
  45 to 49 that mean the board (to `session-start-chief-of-staff.md`; "become a griller / chief of
  staff" stays on `session-start.md`), 511 (start the surface server), 829 (the sync, to
  `sync-checkout.md`), 975 and 1835 (titles, to `titles.md`), 1006, 1482 and 1509 (the watcher);
  886 and 1570 stay.
- `griller.md` line 8 ("your seat reading and your title are in session-start": the seat in
  `session-start.md`, the title in `titles.md`); 63 and 99 stay.
- `concepts.md` 394 (titles, to `titles.md`); 752 and 755 (the watcher's start and stop rules and
  the stop command, to `session-start-chief-of-staff.md`).
- `hosts/claude-code.md` line 49 and `hosts/copilot.md` lines 43 and 47 (the board with
  `--forge-always`; the watcher's "asks the board question alone, as `session-start.md` says"): to
  `session-start-chief-of-staff.md`. The Reload and "looks stopped" citations (claude-code 566,
  768; copilot 51, 109) stay.
- `CONTRIBUTING.md` line 63 (the references list: `session-start.md` holds the start checks, the
  seat and the role change; add the two role files, `titles.md`, `sync-checkout.md` and
  `forges/`) and the tree near line 208 (the same, and "forges/ (one reference per forge: GitHub,
  GitLab)").
- Release notes of past versions are not edited.

## The table of moves

The Driver puts this table, completed with every moved instruction (one row each, its first words
quoted), in the PR's Deliverables. Each row is backed by tests (below).

| Instruction (from, before) | Now in | Read when, by whom (the reading) |
| --- | --- | --- |
| §2 "The board." paragraph | `session-start-chief-of-staff.md`, The board | Chief of Staff, session start (common header), `chief-of-staff` and `board` actions |
| §2 board question alone, host without watcher | same, The board | same |
| §2 stale-build paragraph | same, The board | same |
| §2 the board lines | same, The board | same |
| §2 `serve --seat` keeps `--project` | same, The board | same |
| §2 "The watcher." and its lines | same, The watcher | same |
| §2 stopping the board by hand; a reload starts nothing | same, Stopping the board by hand | same |
| §2 a Griller never starts the board or the watcher | `session-start-griller.md` | Griller, session start (common header) |
| §3 titles, whole, the Foreman row included | `titles.md` | Chief of Staff and Griller, session start (common header); `chief-of-staff` action |
| §6 sync, six steps | `sync-checkout.md` | the syncing session, before its first sync (`sync` action) |
| §2 and §4 `gh`, `glab` | `forges/github.md`, `forges/gitlab.md` | by link, when the forge's tool matters |

Kept in common section 2 (no row, checked as kept): the role-change paragraph, re-read the seat,
the seat table, CR-467's paragraph and CR-468's seat lines once merged.

## Tests

All under `skills/chantier/scripts/cli/tests/`; each reads the shipped files from the repository
at the head under test, never a prepared copy. No test file may pass `MAX_FILE_LINES` (400,
`test_code_targets.py`); `test_startup_manifest.py` has 391 lines, so the new rows and checks go
in a new file, `test_session_start_split.py`, reusing `_text` and `_lf_bytes` from
`test_startup_manifest.py` (imported, not copied).

`test_session_start_split.py`:

- `MOVED_IN`-style rows, one per table row: the phrase is in the new file (and heading). At least:
  "The board a watcher starts is no background task of the session"; "I start the watcher, which
  starts the board if it is not running?"; "`board: writer not started: <reason>`"; "A title
  tells first whether the user talks to the session"; "`[<code>] ⚙️ Project · Foreman (Batch
  <nn>)`" (in `titles.md`); "Name the holders before syncing"; `gh` in `forges/github.md`,
  `glab` in `forges/gitlab.md`.
- `MOVED_OUT`-style rows: each moved phrase is gone from `session-start.md`; no `## 3. Titles`
  and no `## 6. Sync the checkout` there.
- Kept: `session-start.md` section 2 still holds "become chief of staff", "become a griller",
  "Re-read the seat" and the rule "read the file of the role the seat gives you, again when the
  role changes"; both `skills/chief-of-staff/SKILL.md` and `skills/griller/SKILL.md` Startup
  cores hold that rule's words or a pointer to it (Q9: the Driver keeps one exact phrase both
  share and asserts it).
- The reading check: for each row, its card is a reading of what the row names: a row naming a
  manifest action has its card in that action's readings; a row naming the common header has its
  card linked in `session-start.md`'s text before `## 1.`.
- No `\bgh\b` and no `\bglab\b` in `session-start.md`, the two `session-start-*.md`, `titles.md`
  and `sync-checkout.md`; `docs/forge-connectors.md`'s "Adding a connector" names
  `forges/<name>.md`; each connector in `CONNECTORS` has its `forges/<name>.md`.
- No worker, Driver or Foreman reading in the manifest (`actions` of those roles,
  `startup_sections`) names `titles.md`, `sync-checkout.md` or a `session-start*.md`.

Updated in place:

- `test_launch_modes.py`: the `uv sync --locked --project "<plugin root>"` and
  `SYNC_SECTION_PHRASES` checks read `sync-checkout.md` whole; `SYNC_PARAGRAPH_PHRASES`'
  `'"6. Sync the checkout"'` becomes "`sync-checkout.md`"; the `STALE_BUILD` docs map names
  `session-start-chief-of-staff.md` (still exactly once); the foreign-build sentence's case names
  `session-start-chief-of-staff.md`.
- `test_command_names.py`, `test_the_blocked_sync_steps_name_the_serve_holder_and_its_stop`: reads
  `sync-checkout.md`.
- `test_plugin_files.py`, the no-host-tool card list: add `session-start-chief-of-staff`,
  `session-start-griller`, `titles`, `sync-checkout`.
- `test_startup_manifest.py`: unchanged but passing (its `MOVED_IN` rows on section 5 and section
  4 and the `SESSION` prefix still hold; the byte limits hold).
- `test_stack_shape.py`: unchanged and passing.

## Evidence

- `just check` green in the worktree at the pushed head (Linux, macOS and Windows by CI).
- The long gate `scenario` (`just scenario`, ubuntu-latest) green before the PR (cards change);
  in batch-31, the local `chantier gate <cr> scenario` when this CR is on top of the stack. No
  change under `src/` or `evals/kit/`: no `just eval-dry-run`. No `hooks/` or `types/` change: no
  `just mod`.
- Section 1 unchanged: the PR quotes an empty diff between section 1 of `session-start.md` at the
  merge base (`git show <merge-base>:skills/chantier/references/session-start.md`) and at head,
  from `## 1. Start checks, first` up to `## 2.`.
- The table of moves in the PR's Deliverables, each row backed by its tests.
- Sizes in LF bytes, quoted in the PR: `session-start.md` at the merge base and at head, each new
  file, and the `startup-bytes` lines before and after for every role in "The byte budget".
- The Fable Inspector (Q6): before the push, the Driver starts one read-only Inspector on
  `claude-fable-5-2`, briefed with `session-start.md` at the merge base, the new files at head and
  the table, to report each instruction not found, changed in meaning, or now read at another
  moment or by another role than the table says. Its report goes in the CR's `evidence/`; each
  finding is fixed or named in the PR's Known gaps. If the Driver cannot start a worker on that
  model, it stops and asks: no look-alike model.
- No host or default matrix: which file holds a text and when it is read does not depend on the
  host or on a configured value.

## Out of scope

- The forge wording of every other card (`driver.md`, `chief-of-staff.md`, `foreman.md`,
  `concepts.md`, `hosts/`, `init.md`, ...) and of the CLI: a separate CR (Q3).
- A Foreman file, and any change to the Foreman's startup or prompt (Q10).
- Slimming the startup cards of the three roles: the sibling CR, which waits for this one.
- Sections 4 and 5 beyond the forge wording; renumbering the kept headings.
- Who syncs, when a sync runs, and any change to the board, the watcher, the seat, the role
  change or the titles' rules: the text moves, the behaviour stays.
- The CLI: no code change (the tests and `docs/forge-connectors.md` aside).

## Open questions

1. **The Griller's file is short.** With the role change kept in common (Q9), the Griller's own
   part of section 2 is only that it never starts the board or the watcher, which the common
   section's one line already says. Keep `session-start-griller.md` with those sentences (this
   spec, after Q4), or drop it and let the Griller read the common file and `titles.md` only?
