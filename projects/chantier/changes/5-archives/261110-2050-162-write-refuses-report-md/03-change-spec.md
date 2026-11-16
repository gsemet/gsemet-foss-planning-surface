# Change Specification: subagents can write every file chantier asks them to write

## Goal

Claude Code has a built-in guard: a subagent's Write of a "report file" is refused before any
permission check, with the text "Subagents should return findings as text, not write report
files. Include this content in your final response instead." It refused the Coder of CR-159
status-command when it created the card `skills/chantier/references/report.md` (2026-11-10T15:26:13Z);
the Coder then wrote the card through PowerShell. The card is chantier's source (the shape of
the reports), not a report returned to a caller: the guard blocked it because of its name.

chantier cannot lift the guard. So:

1. the card gets a name that does not look like a report, every link to it follows, and a
   subagent proves it can write the new name;
2. every file name a chantier subagent writes is tried with a subagent, and only the names the
   guard refuses are renamed, with the proof;
3. the guard is recorded in the host's reference, and the Chief of Staff's study subagents are
   told to avoid a report-like file name.

The cause is known (02-answers.md, item 2): not a chantier rule, a setting, a hook, the
read-before-write rule, a path outside the session's folders, or the Coder's tools. The guard's
exact matching rule is not known: `progress-report.md` was written by an agent the same day with
no error. This CR does not need the rule; it needs each name tried.

## What changes

### 1. The card's new name

- `git mv skills/chantier/references/report.md skills/chantier/references/report-format.md`.
  Its content is unchanged (its title "# The reports" may stay).
- `report-format.md` is the name: the user chose it (02-answers.md, "The specification's open
  questions", item 1). If the probe (section 3) shows the guard refuses it, stop and hand back
  `blocked question:` with the probe's output; the user picks another name.
- Every link and mention of the card follows. In the current main checkout these are:
  - `skills/status/SKILL.md` line 20: `[report](../chantier/references/report.md)` becomes
    `[report-format](../chantier/references/report-format.md)`; line 30: "in the shape
    `report.md` gives" becomes `report-format.md`.
  - `skills/chantier/references/chief-of-staff.md` lines 247, 249, 280, 299 and 433: each
    `report.md` names the card and becomes `report-format.md`.
  - `skills/chantier/scripts/cli/tests/test_structure.py` line 188: `"report"` in the card list of
    `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` becomes `"report-format"`.
  - `README.md` line 385 ("it loads report.md") and line 389 (the `report` entry of the
    references list) become `report-format.md` and `report-format`.
  - `CONTRIBUTING.md` line 15: `` `report.md` `` in the list of cards becomes
    `` `report-format.md` ``.
- Search again before committing (`rg -n "report\.md|references/report|\"report\"" --glob
  "!.agents/**"`): the only hits left must be the release CR's `report.md` below.

### 2. What stays: the Chief of Staff's own `report.md`

The Chief of Staff is the main session, not a subagent; the guard does not apply to it, and the
user said it keeps writing `report.md` when it archives (02-answers.md, "Grilled enough"). These
mentions name that file, not the card, and are **not** changed:

- `skills/chantier/references/chief-of-staff.md` line 468 (`report.md` and `conversation.md` in
  the release CR's folder);
- `skills/chantier/references/driver.md` line 178 (the Release driver reads them; it never
  writes them);
- `skills/chantier/references/release-template.md` line 38;
- `docs/release-process.md` lines 62 and 133.

Historical files (`.agents/changes/4-batch/3-done/…`, `5-archives/…`,
`docs/release-notes/2026-11-07-v0.8.0/report.png`) are not touched.

### 3. Every name a chantier subagent writes, tried

The subagents are the Drivers and workers (`agents/*.md`, `com.github.copilot/agents/*.agent.md`)
and the Spec-writer. The Foreman and the Chief of Staff are sessions, not subagents: out of the
list. The fixed names the cards give them, from the current main checkout:

| Role | File, relative to its folder | Card |
|---|---|---|
| Spec-writer | `03-change-spec.md` | spec-writer.md |
| Investigator | `work/investigator/investigation.md` | worker.md |
| Coder | `work/coder/r1.md` (`r<n>.md`) | worker.md |
| Debugger | `work/debugger/diagnosis.md` | worker.md |
| Verifier | `work/verifier/verify.md`, `work/verifier/evidence/before-after.md` | worker.md |
| Conflict resolver | `work/conflict-resolver/conflicts.md` | worker.md |
| Demo explorer | `4-batch/demo/demo.md` | worker.md |
| CR driver | `work/pr-body.md` | driver.md, pr-template.md |
| CR driver (archive in the PR) | `intake/request.md`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `delivery.md`, `STATUS.md` | driver.md |
| QA driver | `findings.md` (in its inbox work folder) | driver.md |
| Release driver | `work/release/release-notes.md`, `work/release/tweet.md`, `work/retro.md`, `work/fix-1.md` (`fix-<n>.md`) | driver.md, release-template.md |
| Any Coder of this repository | `skills/chantier/references/report-format.md` (the renamed card) | this CR |

The probe, on Claude Code (the guard is Claude Code's; Copilot is not tried):

- A chantier subagent (started with `subagent_type: chantier:<role>`, the Verifier at the pushed
  head is enough) calls the **Write tool** on each path of the table, mirrored under a fresh
  temporary folder outside the repository (`<tmp>/work/verifier/verify.md`, …), with a one-line
  content, then removes the folder.
- A **control** first: the same subagent's Write of `<tmp>/report.md`. It must be refused with
  the guard's text above; if it is not, the probe proves nothing: say so, no verdict on the names.
- For the renamed card, the proof is a Write or Edit by a subagent of
  `skills/chantier/references/report-format.md` in the CR's worktree that the tool accepts (the
  Coder's edit of the card in its round is enough, if its notes record the tool result).
- Each result is kept with the tool's exact text in `evidence/name-probe.md` in the CR's folder
  (a name with no "report" in it).
- A name the guard refuses is renamed in the card that gives it and in every link to it, the same
  way as section 1, and probed again. A name it accepts stays. With the current matching unknown,
  the expected outcome is that no other name is refused; that is a finding, not an assumption.

### 4. The guard, recorded in the host's reference

The user chose to record it (02-answers.md, "The specification's open questions", item 2).
`skills/chantier/references/hosts/claude-code.md` gets one line, in "Configuration", section
"What stays refused" (no allow rule lifts it): the guard refuses a subagent's Write of a file
named like a report, before any permission check; its exact text (above); the names the probe of
section 3 proved refused (at least the control `report.md`) and accepted (`report-format.md` and
the table's names), marked **proved** with the date of the probe; its exact matching rule
**unproved** (`progress-report.md` was written the same day with no error).

### 5. A project file the guard refuses: rule 7 unchanged

The user chose "stop and report" (02-answers.md, "The specification's open questions", item 3).
When a CR in a user's project needs a file the guard refuses (for example `docs/report.md`), the
agent stops and reports the refusal with its exact text, as concepts rule 7 already says
("Refusals are reported, never worked around"); the user decides. No card changes for this:
`concepts.md` rule 7 stays as it is. The line of section 4 is what tells an agent the refusal is
this guard.

### 6. Study subagents avoid a report-like name

The user chose one line (02-answers.md, "The specification's open questions", item 4).
`skills/chantier/references/concepts.md`, "Starting an agent", the paragraph on a subagent of the
Chief of Staff (lines 179 to 183, "Its result is a report or a study."): add one sentence telling
it to give the files it writes a name that does not look like a report (for example `study.md`,
not `report.md`), since the host may refuse a subagent's Write of a report-like file
(`hosts/claude-code.md`). The card names no host tool (the structure test checks it): the
sentence points to the host's reference, it does not name the guard's tool.

### 7. Both hosts

The agent files carry no card or file name touched here (`agents/`, `com.github.copilot/agents/`
need no change). If a rename in section 3 reaches an agent file, change both hosts together and
keep their bodies identical (AGENTS.md).

## Out of scope

- The Chief of Staff's own writes, `report.md` and `conversation.md` in a release CR's folder
  included.
- The Foreman's session and what the CLI writes (`brief.md`, the STATUS files): not subagents'
  Writes.
- Lifting or bypassing the guard: chantier cannot, and rule 2 forbids a workaround.
- Any change to concepts rule 7 (section 5).
- Names chosen freely at run time (a Debugger's probe scripts, a `note --draft` path): there is
  no fixed name to try; for a study of a Chief of Staff's subagent, the line of section 6 is the
  whole change.
- Finding the guard's exact matching rule.
- Any version change (`just version` only, not in this CR).

## Evidence

- `rg -n "report\.md|references/report|\"report\"" --glob "!.agents/**"` at the pushed head:
  only the lines of section 2 remain, plus the guard's line of section 4 and the example of
  section 6, which name `report.md` as the refused name.
- `skills/chantier/references/report-format.md` exists, `skills/chantier/references/report.md`
  does not; the content is the same (`git diff -M --stat <base>` shows a rename at 100%, or close
  to it if a renamed card name inside it changed).
- `hosts/claude-code.md` holds the guard's line of section 4, with its text, the proved names and
  the probe's date; `concepts.md` "Starting an agent" holds the sentence of section 6; rule 7 is
  unchanged (`git diff` shows no change to it).
- `just check` passes (it runs `tests/test_structure.py`, whose card list now names
  `report-format`).
- `just scenario` passes (the CR changes the cards; AGENTS.md requires it before the PR).
- `/chantier:status` still loads its card: the link in `skills/status/SKILL.md` resolves to an
  existing file.
- `evidence/name-probe.md`: the control refused with the guard's text, then each name of the
  table with the tool's result, and the renamed card's Write or Edit accepted.
