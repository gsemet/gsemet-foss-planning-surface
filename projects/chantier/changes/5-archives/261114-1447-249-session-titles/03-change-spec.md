# New session titles

## Goal

The user (2026-11-14) wants the chantier session titles redesigned so that a phone, which shows
about 25 characters of a title (`intake/phone-session-list.png`), tells first whether the user
talks to the session, then the project and the role, with the machine still recognisable
(answers 5 to 7 and 12). The chosen design: the machine's short code first, in brackets, then an
icon (💬 a session the user talks to, ⚙️ one they do not), the project, the batch's number when
there is one, and the role, joined by ` · `.

This CR changes what the cards and docs tell a session to call itself. Nothing else changes:
not when a session renames itself, not the CLI, not the seat.

## The new forms (answers 7 to 12)

The parts:

- **Icon:** `💬` (U+1F4AC) for the Chief of Staff and a Griller; `⚙️` (U+2699 U+FE0F) for the
  Foreman.
- **Project:** as today (session-start section 3): the repository's folder name, or the project's
  folder in a surface, capitalised (`Chantier`).
- **Batch number:** only for a session that steers a batch (the Foreman, the Chief of Staff in
  direct mode), after the project with a space, on two digits as in the batch's id (answer 10):
  `Chantier 17`, `Chantier 06`.
- **Role:** `CoS` for the Chief of Staff, `Griller`, `Foreman`. A Griller adds its subject once
  known, after the role: a few of the user's words, not a slug (`landing page`).
- **Machine code (answer 8):** the machine's name (the first label of `hostname`, as today) as it
  is when it has 6 letters or fewer (`Mac`), else its first 6 letters (`Battlestation` gives
  `Battle`), its first letter uppercase (answers 8 and 11). A user's word renames the machine for the session only, as today. In a cloud session
  (the host's reference says how to tell) the code is `Remote` (answer 9).
- **Order (answer 12):** `[<code>]` first, then a space and the icon, a space and the project.
- **Separator:** ` · ` (space, U+00B7, space) between the project (with its batch number), the
  role and a Griller's subject; the batch number joins the project with a plain space.

| Session | Today | New |
| --- | --- | --- |
| Chief of Staff | `[env] Project [Chief of Staff]` | `[<code>] 💬 Project · CoS` |
| Chief of Staff steering a direct batch, from `open --direct` (or from the hand-over) until the batch is closed | `[env] Project [Chief of Staff - Batch <nn> - Direct]` | `[<code>] 💬 Project <nn> · CoS` |
| Griller | `[env] Project [Griller]` | `[<code>] 💬 Project · Griller` |
| Griller, once its subject is known | `[env] Project [Griller] <subject>` | `[<code>] 💬 Project · Griller · <subject>` |
| Foreman (given in its prompt by the Chief of Staff) | `[env] Project [Foreman - Batch <nn>]` | `[<code>] ⚙️ Project <nn> · Foreman` |

Examples to use in the cards: `[Battle] 💬 Chantier · CoS`, `[Battle] 💬 Chantier 17 · CoS`,
`[Battle] 💬 Chantier · Griller`, `[Battle] 💬 Chantier · Griller · landing page`,
`[Battle] ⚙️ Chantier 17 · Foreman`, `[Mac] ⚙️ Chantier 06 · Foreman`, `[Remote] 💬 Chantier · CoS`.

After `close --yes` the direct Chief of Staff goes back to `[<code>] 💬 Project · CoS`. A later
Foreman of the same batch, and a reused Foreman of the previous batch, take the title its prompt
gives, as today. The words "Chief of Staff" in the cards' prose and the CLI's messages do not
change; `CoS` is the title's word only.

### The first 25 characters (answers 5, 7 and 12)

Counted in characters as displayed, an icon as one:

| Form | Length | First 25 characters | Cut |
| --- | --- | --- | --- |
| `[Battle] 💬 Chantier · CoS` | 25 | whole | nothing |
| `[Mac] 💬 Chantier · CoS` | 22 | whole | nothing |
| `[Remote] 💬 Chantier · CoS` | 25 | whole | nothing |
| `[Battle] 💬 Chantier 17 · CoS` | 28 | `[Battle] 💬 Chantier 17 · ` | the role |
| `[Battle] 💬 Chantier · Griller` | 29 | `[Battle] 💬 Chantier · Gri` | the role's end |
| `[Battle] 💬 Chantier · Griller · landing page` | 44 | `[Battle] 💬 Chantier · Gri` | the role's end and the subject |
| `[Battle] ⚙️ Chantier 17 · Foreman` | 32 | `[Battle] ⚙️ Chantier 17 · ` | the role |

Every form shows, within its first 25 characters, the machine, the icon (whether the user talks to
the session) and the project. With `Chantier` and a 6-letter code, the role is whole only in the
Chief of Staff's plain form; the direct Chief of Staff and the Foreman lose it (their icon still
tells them apart), the Griller keeps `Gri`. A shorter code (`Mac`) gives back 3 characters; a
project name longer than `Chantier` cuts further. The forms stay as answered (answer 12; the
user's word on long project names).

### When sessions take the new titles

As today: a session renames itself as soon as its role is set and whenever it changes
(session-start section 3), and a reload changes no title unless the seat changed the role
(section 5). A session already running when this lands keeps its old title until its next role
change (or, for a Foreman, its next prompt); nothing renames it earlier. No migration, no CLI
check of the form.

## What changes, file by file

### Cards (`skills/chantier/references/`)

- `session-start.md`, section "3. Titles" (lines 97-113): replace the four form bullets by the
  parts and the table above (icon, project, batch number, role, machine code, separator), the
  examples, and one line with the reason (a phone shows about 25 characters: who the user talks
  to, then the project and the role, the machine's code in front). Keep the opening paragraph (rename by the host's means, nothing
  where the host cannot) and the `seat take --title` bullet as they are.
- `chief-of-staff.md`:
  - "Starting a batch", step 4, the paragraph after the Foreman's prompt (lines 460-463):
    `<title>` is `[<code>] ⚙️ Project <nn> · Foreman` ([session-start](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/session-start.md),
    "Titles"), e.g. `[Battle] ⚙️ Chantier 17 · Foreman`; a later Foreman of the same batch has the same
    title. The prompt's line `Your session title: <title>. Set it on yourself first.` (line 450)
    stays.
  - "Steering a batch yourself", "Your title" (lines 785-787): at `open --direct`, rename yourself
    `[<code>] 💬 Project <nn> · CoS`; after `close --yes`, back to `[<code>] 💬 Project · CoS`.
  - "Reusing the last Foreman" (line 475) and the hand-over (line 902): no change (they name no
    form).
- `concepts.md`, "Session title" (line 195): `[<code>] 💬 Project · <role>` for a session the user
  talks to, `[<code>] ⚙️ Project <nn> · Foreman` for the Foreman ([session-start](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/session-start.md),
  "Titles").
- `foreman.md` (lines 7-8, 339): no change; it sets the title its prompt gives.
- `griller.md` (line 7): no change; it points to session-start.
- `hosts/claude-code.md`: no change. Lines 18-20 (`title: "<title>"`, `set_session_title`), 448
  ("for `Remote` in the title", still true) and 522 (a reused Foreman renames itself) name no form.
- `hosts/copilot.md`: no change. Lines 15, 16 and 32 name no form.

### Docs and eval kit

- `docs/use-cases.md`, line 105: "in the form `[env] Project [role]`" becomes the new form, with
  `[Battle] 💬 Chantier · CoS` and `[Battle] 💬 Chantier · Griller` as examples and one clause on the icon
  (💬 a session you talk to, ⚙️ the Foreman).
- `evals/real-direct/RUNBOOK.md`, line 37: "renames itself `[<code>] 💬 Project <nn> · CoS`".
- `docs/*.svg`: no change; no diagram holds a session title (their `<title>` elements are SVG
  titles).
- `CONTRIBUTING.md` line 62 ("the session titles" in session-start): no change.

### Agent files

- `agents/*.md` and `com.github.copilot/agents/*.md`: no change. Their `"<title>"` is the CR's
  title in a worker's prompt, not a session title.

### CLI, tests and scenario

- The CLI stores the title as free text: `seat take --title` (`commands/seat.py` line 181, help
  "take: the session's current title") and prints it in the `seat` line (line 88). Its streams
  are already UTF-8 (`cli.py` lines 95-96, `stream.reconfigure(encoding="utf-8")`), so a title
  with an icon and `·` passes. No code or help change.
- Fixtures, so the examples match the cards and the round-trip of a non-ASCII title is checked on
  every platform `just check` runs on. The line numbers are main's at ff701a9; the earlier CRs of
  batch-17's stack move them (CR-224 and CR-229 move the seat test from `test_cli_runs.py` to
  `tests/test_structure.py`, CR-222 and CR-225 shift the scenario's lines), so find each by its
  text, `[Mac] Proj [Chief of Staff]` and `[remote] proj [Chief of Staff]`, on the branch's base:
  - the seat test (`skills/chantier/scripts/cli/tests/test_cli_runs.py` lines 41 and 52 on main,
    or `tests/test_structure.py` once moved): `[Mac] Proj [Chief of Staff]` becomes
    `[Mac] 💬 Proj · CoS` in both places, the `seat` line's expected text included;
  - `scenario/run_scenario.py` (lines 1096 and 1253 on main): `[remote] proj [Chief of Staff]`
    becomes `[Remote] 💬 Proj · CoS`. `[remote] surface` (line 5423 on main) stays.

### The board, the pane and the STATUS files

Checked for a session title shown or matched, on main and in batch-17's CRs CR-222 to CR-228:

- **The pane** (`hooks/register.tsx`): shows no session title. Its `TITLE = 'CR board'` (line 17)
  is the pane's own name; its rows show CR titles, and the Foreman only as the words
  `Foreman silent for <n> min` (line 886). No change; `just mod` is not needed, and no pane
  screenshot is owed (the pane's drawing and the `STATUS.json` fields it shows do not change).
- **The STATUS files and `status` output** (`status/words.py` line 95, `status/markdown.py` line
  94, `status/views.py`): name the steering as words (`direct (the Chief of Staff)`, `Foreman`,
  `steered by a Foreman`), never a session title. No change.
- **The board on main** (`board/collect.py`, `board/server.py`): reads the seat's session id only
  (`--seat`, `_seat_gone`), never its title. No change.
- **CR-222 (visualization-backend), active**: the board's project state gains `seat` with `title`
  and `env` (its spec, "A project's state"; `board/state.py`'s `_seat` on its branch). The title
  passes through as the free text `seat take --title` stored, so a new-form title shows as the
  session wrote it. No change to the board; once CR-222 is on the base, the Driver checks that
  the state's JSON carries the icon and `·` unescaped or correctly escaped (the scenario's board
  step with the `[Remote] 💬 Proj · CoS` fixture above).
- **CR-225 (board-read-views), active**: its pages (`board/web/` on its branch) show no seat and
  no session title. No change. Its `work/qa/proto/snapshot.py` reads the seat's `title` for a
  prototype only.
- **CR-226 (board-backlog-edit), CR-227 (surface-autosync)**: name the seat's session id
  (`seat.json`), not its title. No change.
- **CR-228 (board-docs-screenshots), pending**: writes a demo record ("the seat if the server
  reads it", `docs/demo/`). If its merged demo holds a `seat.json`, its `title` takes the new form
  (`[Mac] 💬 Shop-api · CoS`, with the demo's project name), so the screenshots match.
- **CR-223, CR-224**: no session title beyond the seat test fixture above.

## Decisions carried from the answers

1-3, 6. Replaced by answer 7 (the forms of answers 1 to 3 and 6 are not used).
4. The CR goes at the end of batch-17's stack, after every other CR.
5. The intent: the start tells a session the user talks to from one they do not, and the title
   stays short for a phone.
7. Icon, project, batch number when there is one, role, joined by ` · `;
   💬 talked to, ⚙️ not; `CoS`, `Griller`, `Foreman`; the Griller's subject after its role.
8. Machine code: the name as is at 6 letters or fewer, else a short form (made precise by 11).
10. The batch number on two digits.
11. Machine code: else its first 6 letters (`Battlestation` gives `Battle`); first letter uppercase.
9. `Remote` in the code's place in a cloud session.
12. The machine's code first, in brackets: `[Battle] 💬 Chantier · CoS`, `[Remote] 💬 Chantier · CoS`
    (replaces answer 7's code last).

From the coordinator's word on the spec's first open questions: a Griller's subject is a few of the
user's words; long project names keep the forms.

## Out of scope

- When a session renames itself, the reload rule, the hand-over, the seat and its file.
- Renaming sessions already running: they change at their next role change only.
- Any CLI check or construction of the title or of the machine code; a code in `chantier.yaml`.
- How the project's name is computed.
- PR titles, CR titles and the pane's `CR board` title.

## Evidence

- `just check` passes on Linux, macOS and Windows, with the `[Mac] 💬 Proj · CoS` fixture of
  `test_cli_runs.py` (the title goes in through `seat take --title` and comes back unchanged in
  the `seat` line).
- `just scenario` passes (a card and the scenario change).
- A search of the repository outside `.agents/` finds none of the old forms:
  `\[Chief of Staff\]`, `\[Chief of Staff - Batch`, `Foreman - Batch`, `\[Griller\]`,
  `Project \[role\]`, `- Direct\]`, `\[env\] Project`.
- Once CR-222 is on the base: the board's project state for the scenario's project shows the seat's `title` as `[Remote] 💬 Proj · CoS`.
- If CR-228's demo holds a `seat.json`: its `title` is in the new form.
- The examples of "The new forms" appear in `session-start.md`, and the Foreman's and the direct
  Chief of Staff's in `chief-of-staff.md`.
