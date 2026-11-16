# Change Specification: each CR carries a condensed JSON summary, kept fresh by a linter

## Goal

The user's words (`intake/request.md`, `01-intent.md`, and `visualization-backend/02-answers.md`):
the agents keep writing Markdown, and the board's server stays deterministic and reads JSON. So
each CR folder gets a condensed JSON: its title, a short summary of the CR's current state, where
the request came from (a Jira, GitHub or GitLab issue, or a verbal request in the chat), its labels
and its group. A checksum of the CR's Markdown files tells when the summary is late. A summary is
a judgment, so an agent writes it, never the CLI: the CLI lists the gaps, stores what it is given
and records the checksums. The agent that edits a CR's Markdown runs the linter and closes its
gaps; the Chief of Staff does it at worst.

This CR is the CLI and the cards. Its CLI part stands alone: it draws nothing on the board. The
board's display of these fields (the origin icon, the late-summary clock, the labels and their
filter, the summary as a card's text) lands in `board-read-views` and `board-backlog-edit`, which
read the data this CR writes (see "The board: what this CR gives, and where the display lands").

It waits for `python-inline-deps` (`depends.json`): the code is written in that CR's package
layout, with its libraries and under its measured targets.

## Decisions carried from the answers

| Decision (`visualization-backend/02-answers.md`, unless named) | Where this spec carries it |
| --- | --- |
| "Markdown for the agents, JSON for the server": a refresh turns the Markdown into JSON | "The record", "The commands" |
| The JSON holds condensed fields, not the Markdown's text: the title, and a summary of the CR's current state | "The record" |
| A summary is a judgment: the agent writes it; the CLI computes the gaps, stores what it is given, records each file's checksum, writes no summary | "The commands", "What the CLI never does" |
| The refresh is a loop the agent starts: the CLI lists every gap, the agent reads what changed and calls the commands that set the fields | `summary lint`, `summary set` |
| No frontmatter forced: the Markdown stays free text; the condensed fields live in the JSON only | "The record", "What the CLI never does" |
| Who refreshes: the agent that changed a file runs the linter, which says which gaps and which command for each; at worst the Chief of Staff | "The cards" |
| Scope: CRs only, every CR whatever its stage, each with its title and summary; no batch or project summary | "Which folders", "Out of scope" |
| The checksum covers `intake/*.md`, `01-intent.md`, `02-answers.md`, `03-change-spec.md` and an archive's `delivery.md`; not `STATUS.md`, `work/` or `evidence/` | "The covered files" |
| A late summary shows as a small icon on the card, nothing more | "The board" (the `late` flag); the icon is drawn by `board-read-views` |
| "Where a request comes from": each card carries the origin (Jira, GitHub or GitLab issue, verbal), a field of the JSON the agent refreshes; read from the `issue:` line in the prototype; a tracker badge shows `#41` or `CHT-118`, verbal an icon only | "The origin" |
| "Labels and groups": a label system links tickets, with a filter at the top; groups are kept; both in the CRs' JSON, so on every device and pushed by the autosync | "The record", `summary label`, `summary group` |
| The "refresh summary" button that asks the Chief of Staff is removed from the prototype (cleaned to the first version) | "Out of scope" |
| Split: the CLI part stands alone; the board's display comes after `board-read-views` | "The board: what this CR gives, and where the display lands" |
| "The same thing at the end": the specification names the views and `v6-xx` screenshots, the PR shows them, a final QA on PC and phone | "The prototype's views and screenshots" |
| Technology: PEP 723 dependencies after `python-inline-deps`; very clean, standard, modular code | "Code layout and standards" |

## The record: `summary.json`

Each CR folder may hold one file, `summary.json`, beside `01-intent.md`. It is written by the CLI
only (`$CHANTIER summary …`), never by hand, and it is published with the rest of the CR's folder:
it is not in the planning folder's `.gitignore` (the `IGNORED` list does not change), so the
surface's git and its autosync carry it to every device.

```json
{
  "schema": 1,
  "title": "Each CR carries a condensed JSON summary",
  "summary": "Grilled and specified; the CLI part (linter, commands, cards) stands alone.",
  "origin": {"kind": "github", "ref": "#41", "url": "https://github.com/owner/repo/issues/41"},
  "labels": ["board", "cli"],
  "group": "board v1",
  "sources": {
    "01-intent.md": "<sha256, hex>",
    "02-answers.md": "<sha256, hex>",
    "intake/request.md": "<sha256, hex>"
  },
  "summarized": "2026-11-13T17:46:00Z"
}
```

- `schema`: `1`.
- `title`: one line, at most 120 characters, the agent's.
- `summary`: one line of plain text, at most 300 characters, the agent's: what the CR means now
  (its state of grill or delivery, not its progress in a batch, which comes from the record).
- `origin`: `{"kind": "verbal"}`, or `{"kind": "github"|"gitlab"|"jira", "ref": …, "url": …}`
  (see "The origin").
- `labels`: a sorted list of distinct labels, each matching `[a-z0-9][a-z0-9-]{0,23}`; absent or
  `[]` when none.
- `group`: the group's name, one line, at most 60 characters; absent when none. A group is the
  set of CRs of the project whose `group` is that exact name; it has no file of its own.
- `sources`: each covered file present when the summary was last set or confirmed, by its path
  relative to the CR folder (forward slashes), with its checksum.
- `summarized`: the time the summary was last set or confirmed, in the CLI's time format (`now()`,
  as in `events.jsonl`).

A file with only `labels` or `group` (written by `summary label` or `summary group` before any
summary) is valid: its CR still has the "no summary" gap.

Written as UTF-8 without a byte-order mark, `indent=2`, `ensure_ascii=False`, keys in the model's
order, one newline at the end, through the atomic `write_json` of `core/files.py`. A key this
version does not declare survives a read and a write (the model's `extra="allow"`, as every record
model of `python-inline-deps`); an absent optional key stays absent (`exclude_unset`).

### The covered files

For a CR folder, the covered files are, when present: every `intake/*.md` (the top level of
`intake/` only), `01-intent.md`, `02-answers.md`, `03-change-spec.md` and `delivery.md`. Nothing
else: not `STATUS.md`, `STATUS.json`, `summary.json`, `depends.json`, `work/`, `evidence/`,
`retro.md`, nor any other file.

The checksum is SHA-256 of the file's text after two normalisations, so that a checkout on another
system does not make a summary late: a leading UTF-8 byte-order mark is dropped, and `\r\n` becomes
`\n`. A file that is not valid UTF-8 is hashed as bytes, with the same `\r\n` rule.

### The gaps

For one CR folder, in this order (one gap per folder, the first that applies):

1. **unreadable**: `summary.json` exists but is not valid JSON or does not match the model; the
   error is named.
2. **no summary**: no `summary.json`, or one with no `title` or no `summary`.
3. **late**: the covered files differ from `sources`: a file changed, a new covered file, or a
   recorded one gone. The gap names each file and how (`changed`, `new`, `gone`).

A folder with no covered file at all (for instance a `5-archives` folder that holds only a batch's
`retro.md`) is not a CR for this check: no gap, not counted.

### Which folders

`summary lint` with no folder walks every CR folder of the planning folder, stage by stage, in
the lifecycle's order: `1-inbox/*`, `2-backlog/P1…P4/*`, `3-ready/*`, `4-batch/1-pending/*`,
`4-batch/2-actives/*`, `4-batch/3-done/*`, `5-archives/*`; each stage sorted by name. `6-trash/`
is left out: a dropped CR is not shown. On a planning surface, one project per call, by
`--project` as every command. The folder moves (`triage`, `open`, `take`, `order merged`, `close`,
`abandon`, `restore`) carry `summary.json` with the folder, since a folder moves whole; none of
them changes.

### The origin

The origin comes from the CR's `issue:` line, the one `skills/chantier/references/concepts.md`,
"Tracker issue", already defines: the first line matching `^issue:\s*(\S+)` in `01-intent.md`, else
in `03-change-spec.md`. `summary set` reads it each time it runs, so the origin is refreshed with
the summary; both files are covered, so a new or changed `issue:` line makes the summary late.

- No `issue:` line: `{"kind": "verbal"}`.
- An `issue:` URL: the kind from the URL, by these rules in order: a path `/browse/<KEY>-<n>`
  gives `jira`, ref `<KEY>-<n>`; a path holding `/-/issues/<n>`, or a host holding `gitlab`, gives
  `gitlab`, ref `#<n>`; the host `github.com` (or one ending in `.github.com`), or a path
  `/issues/<n>` on a host holding `github`, gives `github`, ref `#<n>`.
- A URL these rules do not place (a self-hosted tracker): `summary set` refuses (exit 1) with
  "the issue: line's tracker is not known from its URL: add --tracker github|gitlab|jira". With
  `--tracker`, the kind is the one given and the ref is taken as above for that kind
  (`#<last number of the path>`, or the Jira key).
- `--tracker` with no `issue:` line is refused (exit 1): the line is the CR's origin, as concepts
  says; the agent writes the line first.

The four kinds are the user's: no other kind (a QA finding, a Markdown file) is added.

## The commands

One new command, `summary`, with four actions. Each takes CR folders as `triage` does: a path
read by `repo.planning_path` (relative to the planning folder, or the older `.agents/changes/…`
form), which must be a CR folder of a stage of "Which folders" (else exit 1, "not a CR folder:
<path>"; a `6-trash/` folder: exit 1, "a dropped CR keeps its summary as it is: restore it
first"). Every write happens under `changes_lock(repo)`, reading the file again inside the lock,
so that the board, a Griller and the Chief of Staff can write the same file without losing a
field. Paths in the output are shown as `triage` shows them (`_shown`). The CLI names no role in
any output.

### `summary lint [<folder> …]`

Lists the gaps, without writing anything. With folders, only those; with none, every CR folder of
"Which folders".

- First line: `no gap (<n> CRs)` and exit 0, or `<k> gap(s) in <n> CRs` and exit 2.
- Then one line per gap, in the walk's order, each with the command that closes it:
  - `<path>: no summary → summary set <path> --title "<title>" --summary "<the CR's state now>"`
  - `<path>: summary late (02-answers.md changed, intake/02-x.md new) → read them, then summary set <path> --summary "<…>" or --unchanged`
  - `<path>: summary.json unreadable (<error>) → repair or remove it, then summary set <path> …`
- Not in `FULL_OUTPUT`: the ten-line cap of `cli.main` applies (`… N more lines`). The first line
  carries the count, so the cap never hides it; the agent closes what it sees and runs it again.

### `summary set <folder> [--title T] [--summary S | --unchanged] [--tracker K]`

Stores what the agent gives, refreshes the origin, and records the checksums.

- `--title`: one line, at most 120 characters, not empty. Required when the file has no title yet.
- `--summary`: one line of plain text, at most 300 characters, not empty. Required when the file
  has no summary yet.
- `--unchanged`: the agent read the changed files and the summary still holds; refused when the
  file has no summary yet. Exclusive with `--summary`.
- `--tracker github|gitlab|jira`: see "The origin".
- At least one of `--title`, `--summary`, `--unchanged` (else exit 1).
- With `--summary` or `--unchanged`: `sources` becomes the covered files as they are now and
  `summarized` the time. With `--title` alone, neither changes, so a late summary stays late.
- The origin is refreshed at every `set`.
- Refused, exit 1, nothing written: a value with a newline or another control character, or over
  its limit (the message names the field and the limit). Refused, exit 2, nothing written: an
  unreadable `summary.json` (the message says to repair or remove it).
- Output, one line: `summary set <path> (origin <kind> [<ref>]; <n> files)`.

### `summary label <folder> … (--add L[,L…] | --remove L[,L…])`

Adds or removes labels on one or more CR folders, at once, under one lock. A label is lowercased
then checked against `[a-z0-9][a-z0-9-]{0,23}` (exit 1 otherwise, nothing written). Adding a label
a CR has, or removing one it lacks, is not an error. `sources` and `summarized` do not change: a
label never makes a summary fresh or late. Creates `summary.json` when absent. Output: one line per
folder, `labels <path>: board, cli` (or `labels <path>: none`).

### `summary group <folder> … (--name G | --clear)`

Puts one or more CR folders in the group `G` (one line, at most 60 characters, not empty, kept as
given), or takes them out of their group. A CR is in one group at most: `--name` replaces its
group. Like `label`: one lock, `sources` untouched, the file created when absent. Output: one line
per folder, `group <path>: <name>` or `group <path>: none`.

### `--help`

The `summary` parser's help: "the CR's condensed JSON (title, summary, origin, labels, group):
lint lists what is missing or late, set stores what an agent wrote, label and group link CRs".

## What the CLI never does

- Write a title or a summary of its own, from the Markdown or anywhere else. (`file` does not
  write `summary.json`: a new inbox item has the "no summary" gap until an agent sets it.)
- Change, add a frontmatter to, or rewrite any Markdown file.
- Run `summary lint` from another command. No command refuses because of a gap: a late summary
  is shown, never a blocker.
- Change `STATUS.md`, `STATUS.json` or the dashboard: the STATUS files stay byte-identical with
  or without `summary.json` (so the pane draws the same thing, and `AGENTS.md`'s screenshot rule
  is not triggered).

## The board: what this CR gives, and where the display lands

This CR adds one read function for the board's server, in `summaries/view.py`:
`summary_view(folder: Path) -> SummaryView | None`, a pydantic model (or frozen dataclass) with
`title`, `summary`, `origin`, `labels`, `group` and `late: bool` (any gap of kind "late"; `None`
when the folder has no `summary.json`; an unreadable file gives `late=True` and empty fields, and
is logged by the caller, not raised). It reads one JSON and hashes at most a few small files, so
the server stays deterministic and needs no agent.

The display lands in the later CRs (the default the split implies; see open point 1):

- **`board-read-views`**: the read API's per-CR fields and the Kanban view: the origin icon and
  badge (`#41`, `CHT-118`; verbal an icon only), the clock beside it when `late`, the labels on
  the cards, the label filter at the top of Kanban, the summary as the card's two-line text (the
  prototype's `firstPara`, replaced), the title from `summary.json`, falling back to the folder's
  slug.
- **`board-backlog-edit`**: the Triage view: the same icons and labels on the post-its, the label
  filter at the top of Triage, the "Label…" action on a selection (`summary label`), the groups
  (`summary group`: "Grouper", a drop on a post-it, "défaire", a group moved whole).

## The prototype's views and screenshots

The reference is `visualization-backend/prototype/index.html` (served with its `data.js`) and
`visualization-backend/evidence/prototype/`. The fields of this CR are what these screenshots
show; their drawing is reproduced by the CRs named above, and their data comes from here:

| Screenshot | What it shows that comes from `summary.json` | Drawn by |
| --- | --- | --- |
| `v6-18-source-icon-kanban.jpg` | the origin icon and badge on Kanban cards | `board-read-views` |
| `v6-19-source-icon-triage.png` | the origin icon on Triage post-its | `board-backlog-edit` |
| `v6-22-kanban-labels-pc.jpg` | labels on cards, the label filter, the clock on two cards, the summary text | `board-read-views` |
| `v6-23-home-written-by-board.png` | none of this CR (the journal "Écrit par le board" is `board-backlog-edit`'s) | |
| `v6-24-triage-labels-phone.jpg` | labels on post-its and the filter, on a phone | `board-backlog-edit` |

This CR draws nothing, so its PR shows no screenshot and needs no PC or phone QA of its own.
What it gives the final QA instead is the prototype's simulated data made real, so the later CRs
can reproduce those screenshots from real records (evidence E4): the three tracker examples of
the prototype's `DEMO_SRC` (`docs-sphinx-rtd` GitHub `#41`, `landing-page` GitLab `#12`,
`epoch-required-everywhere` Jira `CHT-118`), the two late items of `DEMO_LATE`
(`visualization-backend`, `audit-force-upstream-exemption`), and the labels of its `T0().lab`
(`board`, `cli`, `docs`). The final QA, ordered by the Chief of Staff after the five CRs, compares
those views with the prototype, view by view, on PC (1400x860) and phone (375x812); this CR's
share of it is that every icon, badge, clock and label in them is read from `summary.json`.

## The cards

A role's contract lives in the cards; the CLI knows no role. Both hosts read the same cards, so no
file of `agents/` or `com.github.copilot/agents/` changes.

- **`concepts.md`**
  - The CR folder's tree (under "Change Request (CR)") gains the line
    `├── summary.json  ← title, summary, origin, labels, group; through $CHANTIER summary, never by hand`.
  - Rule 1 ("State changes only through `$CHANTIER`"): a CR's `summary.json` joins the files never
    edited by hand.
  - A new word, **A CR's summary**: what `summary.json` holds, the covered files, the rule: "An
    agent that writes a covered file of a CR (`intake/*.md`, `01-intent.md`, `02-answers.md`,
    `03-change-spec.md`, `delivery.md`) runs `$CHANTIER summary lint <the CR's folder>` before it
    ends its turn, reads what the gap names, and closes it with `summary set` (a title and a
    summary it writes itself, one line each, plain text; `--unchanged` when the summary still
    holds). The Chief of Staff closes what is left (its card says when). Labels and groups are
    the user's: an agent sets them on the user's word only."
- **`chief-of-staff.md`, "Backlog and grill"**: the commands block gains
  `$CHANTIER summary lint [<folder>]`, `summary set <folder> --title "…" --summary "…"`,
  `summary label <folders> --add|--remove <labels>` and `summary group <folders> --name "…"|--clear`
  with one comment each. The rule of concepts applies to the Chief of Staff's own writes
  (`01-intent.md`, `02-answers.md`, the ticket summary's records). The sweep: `summary lint` with no
  folder, and its gaps closed, when it re-reads the backlog's folders (before proposing a batch,
  on "status?", when the user says a Griller has finished), after placing a Griller's files from a
  worktree, after a `restore` (which appends to `01-intent.md`), and after `close --yes` (the
  archives' `delivery.md`). Run past the cap again until the first line says `no gap`.
- **`chief-of-staff.md`, "Steering a batch yourself"**: in "What you accept while you steer",
  "Backlog work" names the summary commands among the backlog's files.
- **`griller.md`**: "What you do" gains the rule (concepts' word); "In a worktree": no `summary`
  command there (the planning folder is the main checkout's); the Chief of Staff runs it on
  placing the files.
- **`spec-writer.md`**: "Output" becomes `03-change-spec.md` in the CR's folder and its summary
  refreshed (`$CHANTIER summary lint <folder>`, then `summary set`), nothing else written
  anywhere; "End" unchanged.
- **`driver.md`, `foreman.md`, `worker.md`**: unchanged. A Driver writes no covered file of the
  planning folder (its cleaned archive is a copy in the worktree); `delivery.md` written by
  `order merged` is closed by the Chief of Staff's sweep after `close --yes`.

The host references' allow rules already cover the command (`uv run --script *chantier.py *`):
no change there or in `commands/permissions.py`'s samples.

## Code layout and standards

The user: "juste assure toi que le code soit hyper propre avec de beau standard et modularité pour
facilite la maintenance". Every new or changed file meets `python-inline-deps`' targets, enforced
by `just lint` inside `just check`: at most 400 lines per file, 50 per function, complexity 10, 5
arguments, ruff with its rule families clean, `mypy --strict` clean, no import cycle, no import
inside a function except the declared lazy ones. Each module has one responsibility, stated in its
docstring, and imports only from its layer or below.

| Layer | Module | Responsibility |
| --- | --- | --- |
| 0 | `core/records.py` (or `core/records/summary.py` if `records` is a package) | the pydantic models `CrSummary` and `Origin`, `schema: 1`, `extra="allow"`, the limits as named constants |
| 2 | `summaries/__init__.py` | the package's docstring only |
| 2 | `summaries/sources.py` | `COVERED` (the covered files' rule), `covered_files(folder)`, `checksum(path)` with the two normalisations, `diff(recorded, now) -> list[Change]` |
| 2 | `summaries/origin.py` | `issue_url(folder)` (the `issue:` line), `origin_of(url, tracker)` and its rules, the refusal |
| 2 | `summaries/store.py` | `read(folder) -> CrSummary | None` (raises a `ChantierError` naming the file when unreadable), `write(folder, summary)` |
| 2 | `summaries/gaps.py` | `Gap` (kind, folder, changes, error), `gap_of(folder)`, `walk(paths)`: the CR folders of "Which folders" |
| 2 | `summaries/view.py` | `SummaryView`, `summary_view(folder)` for the board |
| 2 | `lifecycle/stages.py` | gains `cr_folders(paths)`, the walk's order, if the stage list belongs there (it does today: `stage_layout`) |
| 3 | `commands/summary.py` | `register(sub)` (a nested subparser per action) and the four handlers, each a short function that parses, locks, calls layer 2 and formats lines |

The lines of the output are built in `commands/summary.py` only; layer 2 returns data. The limits,
the label pattern and the kinds are constants, never repeated literals (`PLR2004`).
`commands/summary.py` must stay under 400 lines; if it does not, `lint` and `set` go in one module
and `label` and `group` in another.

## Out of scope

- Every board change: the API fields, the icons, the clock, the labels, the filters, the groups'
  drag-and-drop (`board-read-views`, `board-backlog-edit`). The server itself (`visualization-backend`).
- The "refresh summary" button: removed from the prototype by the user's cleaning.
- A batch or project summary; a summary of a `6-trash` CR.
- Frontmatter in any Markdown file.
- `triage` or any move clearing a CR's group when it leaves its group's column: the prototype's
  rule ("a group lives where its post-its are") is `board-backlog-edit`'s, through `summary group`.
- `summary.json` in the cleaned archive a Driver commits in its PR (`driver.md`'s list unchanged).
- Merge conflicts on `summary.json` between two devices: the surface's sync handles them as for
  any file.
- The docs' SVG diagrams and their `-texts.md` (`cr-folder-lifecycle*`).
- `hooks/`, `types/` (so no `just mod`), `.github/workflows/ci.yml`, a version bump.

## Docs

- `docs/planning-folder.md`: under the tree, one paragraph on `summary.json`: what it holds, that
  the agents keep it fresh through `chantier summary lint` and `summary set`, that it is published
  with the CR, and that the board reads it.
- `CONTRIBUTING.md`: nothing beyond what `python-inline-deps` writes.

## CI

No job changes. `just check` (with `lint` and the tests) runs on `ubuntu-latest`, `macos-15-intel`
and `windows-latest`; `just scenario` on `ubuntu-latest`. The new code fetches no new dependency
(`pydantic` comes from `python-inline-deps`; `hashlib` and `re` are standard), so nothing here
differs from what that CR's first CI run proves.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`; the PR body quotes them.

- **E1. `just check`** passes on the Windows machine and in CI on the three systems: 0 ruff
  findings, 0 mypy errors, `test_code_targets.py` passing with the new modules. No structure test
  is added (`AGENTS.md`: few and fast); a test that lists the cards' `$CHANTIER` commands, if one
  exists, passes with `summary`.
- **E2. `just scenario`** passes on both forges, with a new section, `## 21. A CR's summary: the
  linter and its commands`, checking:
  1. A filed item: `summary lint` exits 2, first line `1 gap(s) in 1 CRs`, then the "no summary"
     line with its `summary set` command.
  2. `summary set --title --summary`: exit 0; `summary.json` has `schema` 1, `origin` verbal, and
     `sources` holding exactly `intake/request.md`; `lint` exits 0 (`no gap (1 CRs)`).
  3. Writing `02-answers.md` and a new `intake/02-more.md`: `late`, naming `02-answers.md new` and
     `intake/02-more.md new`; a change in `work/` or `evidence/` or `STATUS.md` gives no gap; the
     same `01-intent.md` rewritten with `\r\n` and a byte-order mark gives no gap.
  4. `--unchanged` closes the gap and leaves `summary` as it was; `--title` alone leaves it late.
  5. Origins: an `issue:` line `https://github.com/o/r/issues/41` gives `github #41`;
     `https://gitlab.com/o/r/-/issues/12` gives `gitlab #12`;
     `https://example.atlassian.net/browse/CHT-118` gives `jira CHT-118`;
     `https://tracker.example.org/t/7` is refused (exit 1) without `--tracker` and accepted with
     `--tracker gitlab` (`#7`); `--tracker` with no `issue:` line is refused (exit 1).
  6. `summary label a b --add Board,cli`: both carry `board, cli`; `--remove cli`; `--add "no
     way"` is refused (exit 1, nothing written); labels and groups never change `sources`; a label
     on an item with no summary creates the file and `lint` still says "no summary".
  7. `summary group a b --name "board v1"`, then `--clear` on one.
  8. Refusals: a summary with a newline, a 301-character summary, a `6-trash/` folder, a path that
     is not a CR folder (`STATUS.md`), `--unchanged` on a new item; each with its exit code and
     nothing written.
  9. An unreadable `summary.json`: `lint` names it; `set` exits 2 and leaves it as it was.
  10. The file travels: `triage --priority P2`, `triage --ready`, `open`, `take`, `order merged`,
      `close --yes` keep `summary.json` with the folder; after `close --yes`, the archive's new
      `delivery.md` makes it `late`.
  11. The STATUS files (index, batch, CR) are byte-identical in two copies of the same planning
      folder, one with `summary.json` files and one without.
  12. More than ten gaps: the first line holds the count, the output ends with `… N more lines`.
  13. In the external surface section (`## 20`): `summary set` and `lint` with `--project` write
      and read the surface's project, and `summary.json` is not ignored by its `.gitignore`
      (`git check-ignore` exits 1).
- **E3. On this repository's own planning folder**, on the Windows machine, from a copy outside
  the repository (the main checkout does not change): `summary lint` on the copy, its first line
  and run time quoted (today 2 inbox, 18 backlog and 103 archived CRs).
- **E4. The prototype's data made real.** A fixture planning folder in the scenario (or a copy of
  the planning folder from E3) holding the prototype's cases, written through the commands: the
  three tracker origins of `DEMO_SRC`, the two late items of `DEMO_LATE`, the labels `board`,
  `cli`, `docs` on the items of `T0().lab`. Their `summary_view` output is quoted in the PR body
  beside the prototype's simulated values, one row per item: the later CRs reproduce `v6-18`,
  `v6-19`, `v6-22` and `v6-24` from these records.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **Where the display lands.** Default: in `board-read-views` (Kanban, the API fields) and
   `board-backlog-edit` (Triage, labels and groups editing), not here, so this CR's CLI part runs
   at once after `python-inline-deps`. Their `depends.json` should then add `cr-summaries`
   (`board-read-views`: `["visualization-backend", "cr-summaries"]`; `board-backlog-edit`: the
   same plus `board-read-views`); this spec does not write them.
2. **The file's name**: `summary.json`, from the intent's title. Alternative: `cr.json`.
3. **The origin comes from the `issue:` line**, read by `summary set` at each refresh, with
   `--tracker` only for a URL the rules cannot place; no free `--origin` option, so the JSON never
   disagrees with the line concepts already defines. Alternative: the agent passes the origin.
4. **Archives count.** Default: every CR, archives included, as the user said ("every CR, whatever
   its stage"); `6-trash` left out. In this repository the first sweep finds about 123 gaps, 103
   of them archives, each a summary an agent writes (a real token cost, once). Alternatives:
   leave `5-archives` out of the default walk (named folders still checked), or sweep them in a
   separate, user-ordered pass.
5. **Limits**: title 120 characters, summary 300, a label `[a-z0-9][a-z0-9-]{0,23}` lowercased
   (the prototype lowercases), a group name 60 characters.
6. **`file` writes no `summary.json`**: a new item (the board's "New" included) shows its slug and
   the "no summary" state until an agent sets it. Alternative: `file` stores the request's first
   line as the title (deterministic) and leaves the summary to the agent.
7. **`delivery.md` written by `order merged`**: closed by the Chief of Staff's sweep after `close
   --yes`; the Foreman's and a direct steering session's loop do not lint. Alternative: the
   steering session lints after each `order merged`.
8. **Line endings**: the checksum ignores a byte-order mark and `\r\n` versus `\n`, so a Windows
   and a Linux checkout agree.
9. **Exit code of `lint`**: 2 when a gap exists, as `preflight` failing.
10. **Labels and groups are the user's**: an agent sets them on the user's word only; the board
    sets them on the user's click. Alternative: an agent may propose labels when it files a CR.
11. **The cost line**: a `summary set` in a turn that writes a covered file is counted with that
    turn (`grill and specifications with the user` for the Chief of Staff); a sweep in a turn of
    its own while the Chief of Staff steers a direct batch counts on the steering row. No change to
    `cost`'s attribution.

## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **Archives: apart.** The default walk leaves `5-archives` out (a named folder is still checked); a separate pass, on the user's order, summarises the archives later.
- The other open points stay at the specification's defaults.
