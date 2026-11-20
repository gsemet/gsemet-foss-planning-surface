# Change Specification: a PR merged without chantier ends in the archives (Part G of seven)

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20). No tracker issue.

This CR is Part G, outside contributions, of the seven-part work the user split into seven CRs
(planning-server-Q7, 2026-11-20). Its grill is `planning-server`'s:
`../../2-backlog/P3/planning-server/02-answers.md` (Q1 to Q30). Its reference text is that CR's
`experiments/03-change-spec-all-parts.md`, "Part G. Outside contributions", with §1 to §4, the
docs map of §2 and §5 to §9 where they name Part G. It builds on three specified CRs whose
specifications and answers rank above the reference where they differ:

- Part C, the writer, `../../2-backlog/P3/planning-server/03-change-spec.md` (approved): no writer,
  no write.
- Part B, `../plan-store-interface/03-change-spec.md`: every published write of the CLI goes
  through `repo.store`, `check_publish` first.
- Part A, `../typed-journal-events/03-change-spec.md`: the journal's typed lines. Part G publishes
  no journal type.

The four points the reference left open are settled in this CR's own `./02-answers.md`
(2026-11-20, by the Chief of Staff), cited below as "this CR's answer <n>". This file is
self-contained: a Driver needs nothing else.

## 1. Goal, in the user's terms

The user, 2026-11-10: "des contributions mineures externes doivent pouvoir être faites sans
chantier, même si ce serait bien qu'elles se terminent par un rapport dans les archives."

- A minor outside contribution, a PR (GitHub) or MR (GitLab) merged on the project with no
  chantier CR, no batch and no Driver, stays possible: chantier asks nothing of its author.
- On the user's word, the Chief of Staff turns such a merged PR into a short report in the
  planning folder's archives, so the archives tell the whole story of the project, chantier's
  merges and the others.
- No new CLI tool: no measured token cost justifies one yet (AGENTS.md, "The CLI's scope"). The
  Chief of Staff writes the report with its own tools; the CLI's `validate` learns its name.

## 2. Dependencies and neighbours

| CR | What this CR needs from it |
| --- | --- |
| C, `2-backlog/P3/planning-server` (approved; this CR's `depends.json`: `{"after": ["planning-server"]}`) | the surface's writer, which commits, rebases and pushes the planning surface; the `writer:` line (`$CHANTIER sync`, `status`, `seat`, its C.9 and C.10); `SurfaceStore.check_publish` refusing a published write with no live writer, exit 2, its C.8 text; its rewrite of `chief-of-staff.md`, "With a planning surface" (its C.11), which this CR's card text sits in. |
| B, `1-inbox/plan-store-interface` (through C) | `summary set` writes `summary.json` through `repo.store` after `check_publish` (its §5.4 table, row `summary set`). Its §2 table names this CR: "its outside archive is written through `repo.store` (through Part C)". The archive's own files are written by the Chief of Staff's tools, not the CLI (§3.2); the CLI write of this CR's flow is `summary set`, already in Part B's table. |
| A, `1-inbox/typed-journal-events` (through C) | nothing: this CR appends no journal line. |

Nothing depends on this CR. The neighbours `1-inbox/forge-connectors` (a connector interface for
the hub's forge reads) and `1-inbox/explain-access` (Part F) are independent of it: here the Chief
of Staff reads the forge itself, as agents do (AGENTS.md: "The agents do the work, git and the
forge included").

## 3. What changes

### 3.1 Words

- **Outside PR:** a PR or MR merged on the project's repository without chantier: no CR of a
  batch's record names it (`4-batch/batch.json`, `5-archives/batches/batch-NN.json`).
- **Outside archive:** the folder `5-archives/<YYMMDD-HHMM>-outside-<number>-<slug>/` of the
  planning folder, the report of one outside PR. Not a CR: it went through no stage, holds no
  `01-intent.md`, no `STATUS.json`, and is never moved.
  - `<YYMMDD-HHMM>`: the PR's merge time, UTC, as a CR's archive is named for its merge time
    (`lifecycle/stages.archive_name`, so the archives keep the merge order; this CR's answer 3).
  - `<number>`: the forge's number of the PR (`#<n>` on GitHub) or MR (`!<iid>` on GitLab),
    digits only.
  - `<slug>`: the PR's title made a slug as `file` makes one (`lifecycle/filing.slugify`:
    lowercase letters and digits, runs of anything else become one hyphen, at most 40
    characters).
  - Example: `5-archives/261120-1015-outside-42-fix-typo-in-readme/`.

### 3.2 The Chief of Staff's card (`skills/chantier/references/chief-of-staff.md`)

The card says what the Chief of Staff judges; no other card changes (the Griller, the Foreman and
the Drivers never archive an outside PR).

**Entry points** table, one row, placed after the "add, drop, reorder, change a CR; "I merged
#42" ..." row:

| The user asks… | Do | Section below |
| --- | --- | --- |
| "archive <link>" (a PR or MR merged outside chantier) | read it with the forge's CLI, write its outside archive in `5-archives/`, `summary set` on it; with `writer: not running`, write nothing | With a planning surface ("Outside contributors") |

**"With a planning surface"**, right after the sentence on outside contributors who submit a CR
by a PR on the surface (the sentence stays as it is), one paragraph, "An outside PR":

- Only on the user's word, "archive <link>": never offered unprompted, never from a forge read of
  your own.
- In a planning surface, read the `writer:` line first (`$CHANTIER sync`, Part C's C.9). With
  `writer: not running`, write nothing (no folder, no file, no `summary set`), say so to the user
  in one line, and act as that line says (start the surface server, or, when it names an older
  board, ask the user to stop it), then archive. In-project mode has no writer and refuses nothing
  (Part C, C.1); the archive is written in `.agents/changes/5-archives/` as every other write of
  the planning folder there (this CR's answer 2).
- Read the PR with the forge's CLI, read-only: GitHub `gh pr view <link> --json
  number,title,url,author,state,mergedAt,files,body`; GitLab `glab mr view <link>` (title, link,
  author, merged at, description) and its changed files with `glab` as the installed version
  allows. You need: the title, the link, the author, the merge time, the files changed and the
  description.
- Write nothing, and say why in one line, when (this CR's answer 4): the PR is not merged
  (`state` is not `MERGED`, or no merge time); a CR of a batch's record names it (it is
  chantier's: `order merged` records it, not this); an outside archive of its number already
  exists in `5-archives/` (`*-outside-<number>-*`): name it.
- Write `5-archives/<YYMMDD-HHMM>-outside-<number>-<slug>/` (§3.1) with two files, UTF-8 without a
  byte-order mark:
  - `intake/request.md`: the PR's description, as received (an empty description: the PR's title
    alone, as a `# ` heading line).
  - `delivery.md`, in the shape `lifecycle/stages._delivery` gives a CR's, plus the author and
    what changed:

    ```markdown
    # Delivery

    - PR: <the PR's link>
    - Author: <the author's login>
    - Merged: <the merge time, YYYY-MM-DDTHH:MM:SSZ, UTC>
    - Archive in the PR: no

    <what changed, in a few lines: the files changed, grouped, and what the PR does>
    ```
- Then `$CHANTIER summary lint <the archive's folder>` and `$CHANTIER summary set <the archive's
  folder> --title "<the PR's title>" --summary "<one line: what it changed, by whom>"`, as for any
  folder you write ("A CR's summary"). A named archive folder is checked; the default walk leaves
  `5-archives` out (the card's existing sentence).
- The writer publishes the folder at its next cycle like any change of the planning folder;
  `$CHANTIER sync now` when the user wants it on the forge at once. When `summary set` is refused
  (the writer stopped between your check and the command: exit 2, Part C's C.8 text), the
  archive's two files stay in the working tree and the next writer commits them (Part C, C.8):
  tell the user, and run `summary set` again once the `writer:` line is back.
- Reply in one line: `archived <link> at 5-archives/<name>/`.

The card's size: the row and the paragraph, about 2,500 bytes. `chief-of-staff.md` is read by the
Chief of Staff's action (`startup-manifest.json`, `actions.chief-of-staff`), not by a startup core
or a Driver's common path: no budget of `test_startup_manifest.py` moves (the Driver checks it with
the test, unchanged).

### 3.3 `validate` (`lifecycle/layout_check.py`)

**Which check gets the rule, and why:** chantier's `validate`, not the surface's
`scripts/validate-bundles.py`:

- AGENTS.md: `validate` is "a read-only check of a planning folder that a surface would otherwise
  keep in its own drifting script"; the surface's own `AGENTS.md` says "the format of a change
  request belongs to chantier: the surface adds no schema of its own, and checks only what
  chantier does not check yet".
- The surface's script places only folders that hold a `01-intent.md`; an outside archive has none,
  so it never sees one. It is pinned to a chantier tag (`v0.11.0`) and is a surface file, committed
  by hand (planning-server-Q17): this CR does not edit it.
- Every surface and every in-project planning folder gets the rule at once with chantier's
  release.

**Today:** `validate` checks no name in `5-archives/`: `stage_crs` lists the archives, `placement`
looks for nested CRs and misplaced priority folders, `summary_findings` checks each archive's
`summary.json`'s format, and archives keep "their format only" (`tests/test_validate.py`,
`test_the_archives_and_the_trash_keep_their_format_only`). A well-named outside archive already
passes. What this CR adds is the error on an outside archive's malformed name.

**The rule** (this CR's answer 1):

- A folder directly in `5-archives/`, other than `batches`, **claims the outside form** when its
  name matches `^(?:\d{6}(?:-\d{4})?-)?outside-`: `outside-` at its start, or right after a date
  `YYMMDD-` or a stamp `YYMMDD-HHMM-`. So `261120-1015-412-outside-contributions-archive` (the
  archive of a CR whose slug starts with `outside`: this CR's own, one day) and a legacy
  `264-edit-outside-trusted-workspace` do not claim it.
- A name that claims the outside form and does not match
  `^\d{6}-\d{4}-outside-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$` is an error:
  `error 5-archives/<name>: not an outside archive's name (<YYMMDD-HHMM>-outside-<number>-<slug>) → rename it`
  (the `Finding` line, `severity path: text`; the `→` hint as the other findings give one).
- Every other name in `5-archives/` is checked as today: none. The user's surfaces hold 294
  archive folders in other forms (`projects/markdown-okf-schema-studio/changes/5-archives/`: 293,
  as `000-markdown-okf-schema-studio`, `_orchestration-2026-10-26`, `release-v1-9-2`;
  `projects/chantier`: `261116-1102-planning-surface`), none claiming the outside form (searched
  2026-11-20), and the reference says only "accepts" for the good name.
- Severity: error, as the reference says ("a malformed name (an error)"): exit 3. `validate`'s
  meaning of an error is "chantier or the board misreads the folder": a malformed outside name is
  read by `status/views.when_of` with no time, or with the wrong one, and by `lifecycle/stages.cr_slug`
  as a CR's slug.

Code: one function in `layout_check.py` (the regexes as module constants, the function at most 50
lines, the file under 400), its findings added by `placement` (it is about a folder's place and
name). `validate` and its output's head line, order and exit codes are unchanged.

The `validate` help text (`declare/validate.py`), "check the whole planning folder: stages, CR
folders, summary.json's format, missing or late summaries, broken links; ...", adds "outside
archives' names" after "CR folders".

### 3.4 What does not change, and how the rest reads an outside archive

- No CLI command, no refusal, no message changes, but the `validate` error and help text above.
  No journal type, no `STATUS` field, no board route.
- `summary set` and `summary lint` already take a folder of `5-archives/` (`commands/summary._cr_folder`,
  `cr_stage` gives `archives`); `delivery.md` and `intake/*.md` are already covered files
  (`summaries/sources.COVERED`, `INTAKE`).
- `status` (`status/views._past`) lists the outside archive among the planning folder's merged
  items, as any archive folder with no `STATUS.json`: its title from `intake/request.md`'s heading
  (`TITLE_FILES`), else the folder's name; no CR id, no batch, no cost; its time from the name's
  stamp. The board shows what `STATUS.json` holds. No change.
- `opening.archived_merged` and `board/archived._slug_of` (a `depends.json` slug met by an archive;
  a batch record's archives) read an outside archive as `outside-<number>-<slug>` or not at all:
  a `depends.json` names CRs, never an outside PR. No change.
- `close` never touches an outside archive: it renames only the `3-done` CRs of its batch
  (`commands/close_archive.archive_and_delete`).

## 4. Decisions carried from `02-answers.md` (planning-server's and this CR's)

| Decision (date) | Where it lands |
| --- | --- |
| Minor outside contributions can be made without chantier; ideally they end as a report in the archives (11-10) | §1, §3.2 |
| "No setup" is for the target project (11-10) | nothing asked of the project or the contributor: the archive is written in the planning folder only |
| The external surface is the most important point; everything in Markdown, browsable on the forge (11-10) | the archive is two Markdown files and a `summary.json`, published by the writer |
| Chantier takes the sync over: the surface server is the one writer (11-20, Q4) | §3.2: the writer publishes the archive; no hand commit |
| With no server, writes are refused; no fallback (11-20, Q5) | §3.2: with `writer: not running`, nothing written; `summary set` refused by Part C's C.8 |
| Q7: seven separate CRs; G after C (11-20) | §2, `depends.json` |
| Q10: sessions write the surface's files under the CLI's locks; only the writer commits, rebases and pushes (11-20) | §3.2: the Chief of Staff writes the files; the writer commits them |
| Q17: the writer touches only `projects/` and the root `chantier.yaml` (11-20) | the archive lies under `projects/<name>/changes/5-archives/`: a published path |
| Q26: nobody pulls or pushes the surface by hand while a writer runs (11-20) | §3.2: `sync now`, never a hand push |
| A coherent split, docs and SVGs included, in the same CR as the behaviour (11-20) | §5 |
| This CR's answer 1: only names in the outside form are checked; a malformed one is an error (exit 3); every other archive name stays unchecked (11-20) | §3.3 |
| This CR's answer 2: in-project mode too, in `.agents/changes/5-archives/`, with no writer and nothing refused (11-20) | §3.2, §6 |
| This CR's answer 3: the name's time is the PR's merge time, UTC, as a CR's archive (11-20) | §3.1 |
| This CR's answer 4: nothing written, said in one line, for a PR not merged, a PR a batch's CR names, or a PR that already has an outside archive (11-20) | §3.2 |
| This CR's answers: the rule goes in chantier's `validate`, not the surface's `scripts/validate-bundles.py`; no spec critic (11-20) | §3.3 |

The reference's Part G text, carried whole: "on 'archive <link>' ... read it with the forge's CLI
(`gh pr view`, `glab mr view`: title, link, author, merged at, the files changed and its
description), and write `5-archives/<YYMMDD-HHMM>-outside-<forge number>-<slug>/` with
`intake/request.md` (the description, as received) and `delivery.md` (the PR, its author, the
merge time, what changed in a few lines, `Archive in the PR: no`), then `summary set` on it. The
writer publishes it like any write; with no writer, nothing is written." (§3.2); "`validate`
accepts an archive named `<YYMMDD-HHMM>-outside-<number>-<slug>`" (§3.3); "Evidence:
`tests/test_validate.py` gains an outside archive (valid) and a malformed name (an error)" (§7).

## 5. Docs and diagrams

Changed, in this CR:

- `docs/planning-folder.md`, the tree: under the line
  `├── 5-archives/<YYMMDD-HHMM>-<number>-<slug>/   merged, after `close` (time of the merge, UTC)`,
  one line, aligned with it:
  `├── 5-archives/<YYMMDD-HHMM>-outside-<number>-<slug>/   a PR merged without chantier, archived on your word`.
- `docs/planning-folder.md`, the `validate` paragraph ("`chantier validate` checks the whole
  planning folder ..."): "the placement of CR folders (...)" adds "and the names of outside
  archives (`<YYMMDD-HHMM>-outside-<number>-<slug>`)", so the list of what it checks stays whole.
  (Not in the reference's docs map; the paragraph lists `validate`'s checks, which §3.3 extends.)
- `docs/planning-modes.md`, "Outside contributors": one paragraph after the existing one (on the
  surface's PRs): a PR or MR merged on the project without chantier is archived on your word
  ("archive <link>") as `5-archives/<YYMMDD-HHMM>-outside-<number>-<slug>/`, with
  `intake/request.md` and `delivery.md`; in a planning surface the writer publishes it, and with
  no writer nothing is written.
- `skills/chantier/references/concepts.md`, "Planning surface", the `validate` sentence
  ("`$CHANTIER validate` checks the whole planning folder (stages, CR folders, `summary.json`'s
  format, missing or late summaries, broken links between its Markdown files) ..."): the
  parenthesis adds "outside archives' names". (Not in the reference; same reason as the
  `validate` paragraph.)

Searched and unaffected:

- `docs/planning-modes.svg` and `docs/planning-modes-texts.md`: the "Outside contributors" line
  and the `<desc>`'s last sentence ("Outside contributors submit a CR by a pull request on the
  surface") are about the surface's contributor, whom this CR does not change; the "Archive" box
  (line 68 of the texts) is a CR's archive and stays true. No SVG, no `-texts.md`, no `<desc>`
  changes.
- `docs/cr-folder-lifecycle.svg` and its texts: an outside archive goes through no stage; a CR's
  archive name there stays true. `docs/batch-lifecycle`, `cr-lifecycle`, `cr-lifecycle-simple`,
  `how-chantier-works` (its "It writes only in the planning folder" stays true: the archive is in
  it) and their texts: about CRs and batches, unchanged.
- `docs/planning-modes.md`, "Archives, in two places": a CR's two archives; unchanged.
- `README.md`: its pointer to "outside contributors" in `docs/planning-modes.md` stays true.
- `AGENTS.md`: no CLI tool, no new write place (the archive is in the planning folder), no git
  exception: no rule changes.
- `docs/release-notes/` is history; this CR's notes are written at release time.

## 6. Host, mode and forge

No host and default matrix: the card is the same on Claude Code and Copilot (the Chief of Staff's
own steps, no host means), and nothing depends on a configured value (`Archive in the PR: no` is
written whatever `project.md` says: an outside PR carries no chantier archive). What does vary is
proved as follows:

| Case | Expected | Proof |
| --- | --- | --- |
| external mode, writer running | the folder written, `summary set` passes, the writer publishes it | Part C's `test_surface_writes.py` row `summary set` (passes with a live writer); the card's text |
| external mode, writer not running | nothing written by the card; `summary set` exit 2, Part C's C.8 text | Part C's refusal test, row `summary set` (no new test here) |
| in-project mode | the folder written in `.agents/changes/5-archives/`; `summary set` passes | the card's text; `validate` on the repo cell (§7) |
| GitHub | `gh pr view --json` gives every field §3.2 names | one real read, §7 |
| GitLab | `glab mr view` gives title, link, author, merged at, description; the changed files read with `glab` | unproved unless a real merged MR is at hand: named in the PR's Known gaps |

## 7. Evidence

- `skills/chantier/scripts/cli/tests/test_validate.py`, built as its other tests are (`build`,
  the `repo` fixture, the CLI in-process):
  - One parametrized test over names, each a folder `5-archives/<name>/` holding
    `intake/request.md` and `delivery.md`, and `summary.json` (`summary()`): the valid
    `261120-1015-outside-42-fix-typo` gives `no error, no gap (1 CRs)`, exit 0 (the reference's
    "an outside archive (valid)"); the malformed `261120-1015-outside-fix-typo` (no number),
    `outside-42-fix-typo` (no stamp), `261120-outside-42-fix-typo` (half a stamp),
    `261120-1015-outside-42-Fix_Typo` (not a slug) and `261120-1015-outside-42-` (no slug) each give
    exactly one error line, the §3.3 text with its name, exit 3 (the reference's "a malformed name
    (an error)"); the non-claiming `261120-1015-412-outside-contributions-archive` and
    `264-edit-outside-trusted-workspace` give no error.
  - `test_the_archives_and_the_trash_keep_their_format_only` keeps its `5-archives/x` and its three
    lines unchanged: a name in no form is still not checked.
  - A prepared tree is right here: `validate` reads a planning folder, which no shipped file holds.
  - Time: about 9 in-process `validate` calls on trees of three files, well under 1 s; the PR
    states the time `just test` adds, measured on the same machine before and after (AGENTS.md:
    at most 30 s above 18.5 s).
- One real, read-only forge read, by the Driver: `gh pr view <a merged PR of chantier> --json
  number,title,url,author,state,mergedAt,files,body` returns every field the card names; the
  output's field names quoted in the PR's evidence. GitLab: the same with `glab mr view` on a real
  merged MR if one is at hand; else "GitLab read unproved" in the PR's Known gaps.
- No check guards the card's text: the card is agent judgement, and the existing structure tests
  (`test_plugin_files.py`, `test_startup_manifest.py`) read the shipped cards at the head under
  test and must pass unchanged.
- The project's gates (AGENTS.md): `just check` (Linux, macOS, Windows); `just eval-dry-run` (a
  change under the CLI's `src/`); `just scenario` green on the pipeline's `just scenario
  (ubuntu-latest)` job before the PR (a change to the CLI and the cards), and locally on Windows
  (`chantier gate`) when this CR is the top of its batch's stack. No scenario step is added: the
  scenario runs no Chief of Staff's own steps, and `validate`'s rule is proved by its tests.
- No CI job is added or changed.

## 8. Rollout

- Lands after Part C (`depends.json`); the card's paragraph is written into the "With a planning
  surface" section as Part C left it (rebase onto it, keep both).
- A surface whose `5-archives/` holds a folder that claims the outside form with a bad name sees
  `validate` exit 3 after the upgrade: rename the folder. On the user's surfaces today, none does
  (searched: `projects/*/changes/5-archives/`, 2026-11-20).
- The release notes, written at release time, say: "archive <link>" turns a PR merged without
  chantier into a report in `5-archives/`; `validate` checks an outside archive's name.
- Mixed versions: an older chantier lists an outside archive as any archive and checks nothing of
  its name.

## 9. Out of scope

- A CLI command that writes the outside archive (`archive <link>` as a command): no measured
  token cost yet (the reference: "No CLI tool (no measured cost yet)").
- Finding outside PRs on its own: the hub, the board's PRs page and the forge connectors read only
  the batch's PRs; no poll lists the project's merged PRs. The Chief of Staff archives only on the
  user's word.
- Any change to the outside contributor's path on the surface (a CR submitted by a PR on the
  surface).
- The surface's `scripts/validate-bundles.py`, `AGENTS.md` and `justfile`: surface files, committed
  by hand (Q17).
- Archiving a PR of chantier's own CRs this way (`order merged` records those), and an archive in
  the outside PR itself.
- A check of an outside archive's content (`intake/request.md`, `delivery.md`): archives keep their
  format only.

## 10. Self-containment notes for the Driver

- Files: `skills/chantier/scripts/cli/src/chantier/lifecycle/layout_check.py` (`placement`,
  `stage_crs`, `Finding`), `declare/validate.py` (help text), `tests/test_validate.py`;
  `skills/chantier/references/chief-of-staff.md` ("Entry points", "With a planning surface"),
  `skills/chantier/references/concepts.md` ("Planning surface"); `docs/planning-folder.md`,
  `docs/planning-modes.md`.
- Existing shapes to follow: `lifecycle/stages._delivery` (the `delivery.md` shape),
  `lifecycle/filing.slugify` (the slug), `core/clock.stamp` (`%y%m%d-%H%M`).
- `test_code_targets.py`: files at most 400 lines, functions at most 50, no import cycle.
- Repository text in English; the card's rows stay one line each in the table.

## 11. Open questions for the user

None. The four questions of this specification's first pass are settled in `./02-answers.md`
(2026-11-20, by the Chief of Staff), each as recommended, and folded in above.
