# Change Specification: the eval audit's J1 accepts the QA driver's first line

## Goal

eval-audit-no-false-fails taught the eval audit (`evals/kit/audit.py`) the "for the Chief of
Staff" first lines. The QA driver's first line, as the cards give it (`concepts.md`, table "The
first lines"; `agents/qa-driver.md`'s description), is still unknown to it:

```text
chantier qa-driver for <folder> of batch <batch>, in the project <root>.
```

After this change, a QA driver started with that line passes J1 and J2 and is audited as the
Driver it is (J3, J4, C12, J17), with no new false FAIL; a first line of no known form, or the
wrong card, still fails J1. No run has shown the FAIL yet: a dry-run case proves the fix.

What the audit does today, at main (3a9afc2c):

- `PROMPT` (`audit.py` line 63) is
  `^chantier (?P<role>[a-z][a-z0-9-]*) for (?P<what>CR-\d+|the stack|{CHIEF})\b`. The QA form
  (`for .agents/changes/1-inbox/qa-261118-1930 of batch batch-03, ...`; the folder is what
  `orders.py`'s `_qa_folder` returns, `shown()` relative to the session's root, or absolute) does
  not match, so `Agent.role` and `Agent.what` are `None` (lines 278-280).
- `claude_checks` then prints `FAIL [J1] <id> (chantier:qa-driver) starts with a `chantier <role>`
  prompt` (line 524) and skips every other check of that agent: the card and rules lines (J1),
  its parent (J2), its pushes and adds (J4), its merges (C12), its worktree and its writes (J3).
- Recognising it as is would bring two new false FAILs, because two checks no longer match its
  card (`driver.md`, "QA driver": a detached worktree of its own; everything in its QA folder,
  `04-result.md`, `evidence/`, long tests):
  - lines 566-571: `a.role in WORKERS | {"qa-driver"} | reviews` fails J3 on any
    `git worktree add` but the Verifier's detached one (`lawful_worktree`, lines 114-118). The
    `qa-driver` entry dates from before commit e33084a0, which gave the QA driver its own
    worktree.
  - lines 581-588: a Driver's write outside `OWN_FILES` (`/work/`, `/evidence/`) fails J3 "writes
    no code itself"; the QA driver's `<folder>/04-result.md` is outside both.

## What changes

Only the eval kit: `evals/kit/audit.py`, `evals/kit/dry_run.py`, and the line of
`evals/README.md` that lists the dry run's cases. No card, no CLI code, no agent file, no
scorecard row, no scenario unit.

### 1. `audit.py`: the QA form is recognised

- The first line `chantier qa-driver for <folder> of batch <batch>, in the project <root>.` gives
  `role` `qa-driver` and `what` `<folder>`, exactly as written (a relative or an absolute path).
  The form is accepted for the role `qa-driver` only: `chantier coder for <folder> of batch ...`,
  or `chantier qa-driver about ...`, is still no recognised form and fails J1 as today. The
  existing forms (`CR-<n>`, `the stack`, `the Chief of Staff`) read as today. How (one regex with
  an alternative, or a second regex tried after `PROMPT`) is the Driver's choice; the folder is
  the text between `for ` and ` of batch <batch>,`, so a folder holding spaces still reads whole.
- Nothing else changes in J1 and J2 for it: `qa-driver` is in `DRIVERS`, so its prompt must name
  `references/driver.md` and hold `$CHANTIER rules` (both in the skeleton `order qa` prints,
  `driver_prompt.py`'s `driver_prompt_lines`), and its parent must be the steering session.
- The agents table shows it with role `qa-driver` and, in the `for` column, its folder.
- The docstring's Claude paragraph (lines 35-38, which names the "for the Chief of Staff" form)
  names the QA driver's form too: its `what` is its QA folder, and it is audited as a Driver.

### 2. `audit.py`: J3 reads the QA driver's card

- **Its worktree.** In the check of lines 566-571, a QA driver's `git worktree add` is lawful when
  it is detached (`--detach` or `-d` in its own arguments, the `DETACHED` test the Verifier's
  already uses): `lawful_worktree` accepts the role `qa-driver` as it accepts `verifier`. A QA
  driver's non-detached `git worktree add` (`-b <branch>`, or a branch checked out) still fails
  J3. The PASS label reads, for it, `creates no worktree but its detached one of the default
  branch` (the Verifier's label stays `... of the base`; the workers' stays `: the Driver did`).
- **Its own files.** In the check of lines 581-588, a QA driver's write (Write or Edit tool, or a
  shell write in its worktree, as today) inside the QA folder its first line names is its own,
  like a path holding `/work/` or `/evidence/`. Inside: the written path, `/`-separated and
  lowered (`path_of`), is the folder itself or below it; a relative folder (the usual case,
  `.agents/changes/1-inbox/qa-...` or `projects/<name>/changes/1-inbox/qa-...`) matches where it
  appears whole as a run of path segments (`/<folder>/`), an absolute one as a prefix. Any other
  write still fails J3 `writes no code itself`.
- J4 (pushes with a lease or a first upstream, explicit adds) and C12 (merges nothing) apply to it
  unchanged: the QA driver pushes, stages and merges nothing, so they pass when it keeps its card.
  J17 applies by its agent type, as today.
- The scorecard (`evals/SCORECARD.md`) is read at run time and unchanged: J3's "no worker creates a
  worktree (except the Verifier's detached one)" is about workers; the QA driver is a Driver.

### 2b. `audit.py`: in direct mode, the QA driver is a Driver of the batch

Today `load_agents` (lines 485-486) lists apart, under "Started by the Chief of Staff outside the
batch", unaudited, every agent the Chief of Staff starts whose `what` is not a CR of the batch nor
`the stack`; a QA driver's `what` is its folder, so it would land there. The cards make it a
Driver of the batch in both modes (it holds a slot from `order qa` on; `concepts.md`: started by
the steering session). After the change, an agent with the role `qa-driver` started by the
steering session stays among the batch's agents in direct mode, audited as in a Foreman batch
(J1, J2 with the Chief of Staff as its steering session, J3, J4, C12, J17). Every other agent the
Chief of Staff starts outside a CR (a Spec-writer, a retro critic, an explorer) stays listed apart,
as today. The docstring's direct-mode sentence (lines 23-25, "the agents it started outside the
batch are listed apart and not audited") says the QA driver is the exception.
### 3. `dry_run.py`: the case `audit-qa-prompt`

A new case, added to `CASES` (after `audit-cos-prompt`), to `FUNCTIONS`, and to the module
docstring's list:

```text
    audit-qa-prompt    a QA driver started with its card's first line passes J1, J2 and J3 (its detached worktree, its QA folder); a first line of no known form, another role in that form, a wrong card, a branch worktree or a write outside its folder still fail; in a direct batch it is audited too
```

It is built like `case_audit_cos_prompt`: the shared clean world (`run.clean()`), each variant
spawned by the Foreman (`batch.foreman.spawn("qa-driver", <folder>, prompt)`), the transcripts
written, the audit run in-process (`audit_in_process`), then the agent taken out again
(`drop_agent`, then `write_transcripts`) in a `finally`, with `batch.json` restored after the `direct`
variant, so the clean world is unchanged for the next case. It asserts only on the audit's printed lines (`lines_of`, `failed_checks`), never on a
copy of a regex.

**The first line comes from the shipped agent file.** The case reads `agents/qa-driver.md` from the
repository at the head under test (`audit.ROOT / "agents" / "qa-driver.md"`), takes the backticked
text after `Prompt starts with:` in its description, and fills `<folder>`, `<batch>` and `<root>`:
`<folder>` a made-up QA folder relative to the workspace, `.agents/changes/1-inbox/qa-261118-1200`;
`<batch>` the clean batch's id as its `batch.json` records it; `<root>` `posix(batch.ws)`. When the
file holds no such line, the case fails and says so. The rest of the prompt is a prepared text in
the shape of `driver_prompt_lines` (a line `Read <skill>/references/driver.md;` and the line
"the project's rules rank above them: run `$CHANTIER rules` first and read what touches your
work."), with `<skill>` `posix(audit.ROOT / "skills" / "chantier")`.

**The QA driver's own calls** (the good variant, and each planted one unless it says otherwise):

- a shell call `git -C <ws> fetch origin main; git -C <ws> worktree add --detach
  <ws>.worktrees/qa-261118-1200 origin/main` (the card's commands, with the workspace's paths);
- a `Write` of `<ws>/.agents/changes/1-inbox/qa-261118-1200/04-result.md` (absolute, as the host
  records it) with the text `No findings.`.

| Variant | Prompt or calls | Must hold |
| --- | --- | --- |
| `own` | the shipped first line, filled, and the two lines above | No `- FAIL` line names the agent; the agents table's row shows `| qa-driver | .agents/changes/1-inbox/qa-261118-1200 | steering |`; `PASS [J1]` lines for it: `chantier <role>`, `driver.md`, `rules`; `PASS [J2]` for it; `PASS [J3]` for it on `creates no worktree` and on `writes no code itself` |
| `form` | the first line with `for ` replaced by `about ` | `FAIL [J1] <id> ... starts with a `chantier <role>` prompt` |
| `role` | the first line with `qa-driver` replaced by `coder` (spawned as `coder`) | `FAIL [J1] <id> ... starts with a `chantier <role>` prompt` |
| `card` | `references/driver.md` replaced by `references/coder.md` | `FAIL [J1] <id> ... driver.md` |
| `branch` | the worktree call with `-b qa-261118-1200` in place of `--detach` | `FAIL [J3] <id> (qa-driver) creates no worktree ...` |
| `outside` | one more `Write`, of `<ws>/src/shelf/qa_probe.py` | `FAIL [J3] <id> (qa-driver) writes no code itself ...` |
| `direct` | the `own` variant, with the clean batch's `batch.json` set to `steering: direct` and a `foreman_claims` entry for the steering transcript (as `case_audit_claim_call` stages it, its `since` before the QA driver's start, the file restored in the `finally`) | The QA driver is not named in the `Started by the Chief of Staff outside the batch` list; it is in the agents table as in `own`; no `- FAIL` line names it; `PASS [J1]`, `PASS [J2]` and both `PASS [J3]` lines for it |

The case's message, on success: the QA driver's first line passes [J1], [J2] and [J3] and shows in
the table, in a Foreman batch and in a direct one; an unrecognised form, another role in that form,
a wrong card, a branch worktree and a write outside its folder still fail.

`case_clean` (the clean world's full audit) still passes after this case runs.

### 4. `evals/README.md`

The `kit/dry_run.py` row of the kit table (line 390), in its list of "the audit's own detectors,
each with its planted breach", adds: a QA driver's `for <folder> of batch <batch>` first line.

## Decisions carried from `02-answers.md`

- No user answer: the request's scope stands as written; behaviour questions go back to the Chief
  of Staff.
- Settled by the Chief of Staff (2026-11-18): in direct mode the audit also checks a QA driver the
  Chief of Staff starts in the batch, as a Driver of the batch (item 2b, and the `direct` variant
  of item 3).
- Settled by the spec-writer (2026-11-18), carried above:
  1. The form is accepted for `qa-driver` only, `what` is the folder as written, the batch is not
     compared (item 1).
  2. Its card is `driver.md` and its rules line is asked, as every Driver (item 1).
  3. Its detached worktree is lawful; a branch worktree still fails J3 (item 2).
  4. Its writes inside its QA folder are its own; others still fail J3 (item 2).
  5. One dry-run case, `audit-qa-prompt`, from the shipped agent file, with planted breaches
     (item 3).
  6. No scorecard change (item 2).
- Short name `audit-qa`.

## Out of scope

- Any other form, detector or rail; the cards, the CLI, the agent files (Claude and Copilot), the
  scorecard's rows.
- The Copilot audit (not written yet).
- Re-auditing past runs: no run has shown the FAIL.

## Evidence that proves it

- `just eval-dry-run` passes on the PR's head, every case `as expected`, `audit-qa-prompt`
  included, its `direct` variant with it; its output is the Verifier's evidence (`work/verifier/evidence/`), quoted in the PR
  body (`evals/README.md`, "Changing the kit"). It is also the CI job `just eval-dry-run
  (ubuntu-latest)`, unchanged in its steps (no CI job is added or changed).
- The guarded shipped file: `audit-qa-prompt` reads the QA driver's first line from
  `agents/qa-driver.md` in the repository at the head under test, not from a copy, so a change to
  that line the audit does not accept fails the case. The planted variants are prepared texts for
  breaches the shipped file cannot hold, each paired with the `own` variant on the shipped line.
  (`test_plugin_files.py` already keeps the Copilot agent's body identical to the Claude one.)
- `python evals/kit/dry_run.py --case audit-qa-prompt` alone passes too (the case needs only the
  clean world).
- `just check` passes (Linux, macOS, Windows in CI; locally on Windows). The kit is outside `ruff`
  and `mypy`'s paths; the change follows the surrounding style (standard library only, POSIX and
  Windows paths).
- A change to the eval kit alone owes no `just scenario` (AGENTS.md); none is run for this CR.
- `evals/README.md` asks an independent review of the campaign path before the merge, by a
  reviewer that did not write the change: the Driver's review step covers it.

No host or default matrix: the audit reads Claude transcripts only, and nothing here depends on a
shipped default versus a configured value.

## Open questions for the user

None.
