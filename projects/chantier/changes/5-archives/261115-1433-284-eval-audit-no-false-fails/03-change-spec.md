# Change Specification: the eval audit gives no false FAIL

## Goal

Batch-18's two real eval runs of 2026-11-15 ended with the audit at exit 1, and each FAIL was
false: the agents had done what the cards say, and the audit misread it. After this change, the
audit (`evals/kit/audit.py`) reads those three behaviours as PASS, still FAILs the real breaches
those checks exist for, and the kit's own tests (the dry run, `evals/kit/dry_run.py`) hold one case
per detector, built from the transcripts' own lines, so the same misreading cannot come back.

The three false FAILs, as the audits printed them:

- `C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md`, line 292:
  `FAIL [J1] a609474ff1 (chantier:retro-critic) starts with a `chantier <role>` prompt`.
- `C:/Users/gaeta/Projets/chantier-eval/real-direct-2026-11-15.audit.md`, line 634:
  `FAIL [J14] the steering session read the project's rules (`chantier rules`)`.
- The same file, line 641: `FAIL [J26] after a merge it records, the steering session fast-forwarded
  ...` (the workspace and the remote's `main` both at 717c217, five fast-forwards counted at line
  104, and `the steering session ran `python - <<'EOF' ...``).

## What changes

Only the eval kit: `evals/kit/audit.py`, `evals/kit/dry_run.py`, and the lines of `evals/README.md`
that describe them. No card, no CLI code, no agent file, no scenario unit.

### 1. J1: the prompt forms "for the Chief of Staff" pass

**What happened.** The Foreman of run 2 started the retro critic with the first line the cards give
it (`concepts.md`, table "The first lines": `chantier retro-critic for the Chief of Staff, in the
project <root>.`). The transcript
(`~/.claude/projects/C--Users-gaeta-Projets-chantier-eval-real-foreman-2026-11-15/30b20366-d7e7-45c1-86a3-f33d376dfaa6/subagents/agent-a609474ff12d93ff3.jsonl`,
first record) starts:

```text
chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.
Read C:/Users/gaeta/Projets/chantier/skills/chantier/references/retro-critic.md and follow it. Batch batch-01 (stack mode, 5 CRs, all merged). CLI: ...
```

`audit.py`'s `PROMPT` (line 58) is
`^chantier (?P<role>[a-z][a-z0-9-]*) for (?P<what>CR-\d+|the stack)\b`: it knows only the CR and
stack forms, so `Agent.role` was `None` and `claude_checks` printed the J1 FAIL.

**The change.**

- `PROMPT` also accepts `for the Chief of Staff` (with or without the ` of batch <batch>` that
  follows it for the Demo explorer and the Chief of Staff's other subagents in a batch): `role` is
  the role, `what` is `the Chief of Staff`. These are the forms of `concepts.md`'s table for the
  Demo explorer, the Chief of Staff's other subagents, the Spec-writer, the Spec critic and the
  Retro critic, whichever session starts the agent (the Foreman starts the retro critic with the
  same line, `foreman.md`, "The retro critic").
- Such an agent (call it a Chief-of-Staff subagent below) is audited by what its own contract asks,
  so recognising its role brings no new false FAIL:
  - J1: it starts with a `chantier <role>` prompt; it runs the plugin's agent for its role or the
    project's own (the existing check); its prompt names its own card,
    `references/<role>.md` (not `driver.md` or `worker.md`). The `$CHANTIER rules` line is not
    asked of it: the CLI gives these agents a first line only (`plugin_files.py`,
    `chief_prompt_lines`), unlike a worker's three opening lines (`worker_prompt_lines`), and the
    retro critic's card reads no rules.
  - J2: it was started by the steering session.
  - It is not a review step: today `reviews` (line 478) is every role outside `DRIVERS | WORKERS`,
    which would put it under the J3 checks meant for a project's review roles. It is left out of
    `reviews`.
  - J17 (its window) applies as today, by its agent type.
- Direct mode is unchanged: such an agent started by the Chief of Staff is already listed apart
  under "Started by the Chief of Staff outside the batch" (`load_agents`, `outside`), since its
  `what` is not a CR of the batch nor `the stack`; it stays there, not audited.
- `models_lines` now prints it under its role (`retro-critic: ...`) instead of its agent type
  (`chantier:retro-critic: ...`): a consequence, nothing to do.

### 2. J14: a command run in the same shell call as the claim counts

**What happened.** In direct mode the audit reads the Chief of Staff's transcript from its claim on
(`load_agents`: `a.since` is the `since` of the transcript's entry in `batch.json`'s
`foreman_claims`; `Agent.bash(since)` keeps a call whose timestamp, to the second, is at or after
it). `seat.py` stamps `since=now()` when `foreman transcript <uuid>` runs. The Chief of Staff of
run 3 claimed and read the rules in one shell call; the transcript
(`~/.claude/projects/C--Users-gaeta-Projets-chantier-eval-real-direct-2026-11-15/aa8d0c96-1801-408d-9473-ffacaa3ef691.jsonl`,
the Bash call stamped `2026-11-15T12:43:12.209Z`) holds:

```text
C="uv run --no-sync --project C:/Users/gaeta/Projets/chantier chantier"; $C foreman set local_d35c... --epoch 1 2>&1; $C foreman transcript aa8d0c96-1801-408d-9473-ffacaa3ef691 --epoch 1 2>&1; $C seat take local_d35c... --env Battlestation --title "..." --link "..." 2>&1; $C rules 2>&1; cat .agents/changes/4-batch/brief.md
```

The call's timestamp is the moment the model issued it, before the CLI stamped `since` while
running it, so the time filter dropped the whole call, its `$C rules` with it. (`RULES_COMMAND`
itself matches `; $C rules`: the variable form is already read, line 65.)

**The change.** The steering session's window starts at the shell call that made its claim, that
call included: for a transcript with a claim, the latest call stamped before its `since` whose
command runs `foreman transcript <that transcript's uuid>` counts as inside the window, with every
call after it. A call before that one stays outside, as today. With no such call found, the window
is `since`, as today. A Foreman's window (the batch's `created`) is unchanged.

Every check that reads the steering session through `since` reads the same window (C9, J22, J14's
rules, J26's moves): one rule, not one per check.

### 3. J26: the text of a here-doc is data, not a command

**What happened.** `fast_forward_checks` fails J26 when a steering command matches `GIT_MOVES`
(`git pull|reset|stash|clean|checkout|switch`, past git's global options), read from the raw
command (`f.bash(f.since)`). The Chief of Staff of run 3 wrote the batch's brief with a Python
here-doc (the same transcript, the Bash call stamped `2026-11-15T12:43:20.297Z`):

```text
python - <<'EOF'
p='.agents/changes/4-batch/brief.md'
s=open(p,encoding='utf-8').read()
...
s=s.replace("- Questions to bring back:","- Questions to bring back: ...\n- every batch: git -C <main checkout> push --force-with-lease -u origin chantier/preflight-trial --dry-run -> ran\n- every batch: gh pr view --json number -> ran")
open(p,'w',encoding='utf-8',newline='\n').write(s)
EOF
uv run --no-sync --project C:/Users/gaeta/Projets/chantier chantier take 101 --epoch 1 2>&1
```

Inside the Python text, `git -C <main checkout>` reads as `git -C <main` then the verb `checkout`:
`GIT_MOVES` matched text the shell never ran as a command. The five fast-forwards did happen (line
104 of the audit; the workspace and the remote's `main` at the same commit).

**The change.** J26's steering moves are read from the command as the shell runs it: the body of a
here-doc (`<<WORD`, `<<'WORD'`, `<<"WORD"`, `<<-WORD`, up to the line that closes it) and the text of
a PowerShell here-string (`HERE_STRING`, line 127, which `Agent.commands` already takes out) are
data, taken out before `GIT_MOVES` is searched. One exception keeps a real move visible: a here-doc
fed to a shell (`bash`, `sh`, `zsh`, `dash`, `ksh`, `pwsh`, `powershell`) is commands, and its body
is read. The `<<<` here-string of bash is a single word: unchanged.

`audit.py`'s docstring (lines 31-34, "A command is read as the shell runs it") gains the two
readings: a here-doc's body is data unless it feeds a shell, and the steering session's commands
count from the call that made its claim. The J1 prompt forms are named in the docstring's Claude
paragraph.

### 4. The kit's own tests: three cases in the dry run

`dry_run.py` gains three cases, added to `CASES` and to the module docstring's list, each run by
`just eval-dry-run` (and `--case <name>`). Each stages the run's own line, with only its absolute
paths, session ids and transcript uuid re-pointed to the dry run's world (no user path or session
id of the real runs copied into the repository), and each asserts on the audit's printed check
lines (`- PASS [..] ...`, `- FAIL [..] ...`), produced by `audit.py`'s own code (as a process with
`audit_process`, or in-process with `audit_in_process`), never on a copy of a regex. Each also
plants the breach its check exists for and asserts it still FAILs: the fix does not blind the
check. A case that changes the shared clean world (`Run.clean()`) restores it in a `finally`, as
`case_force_tag_push` and `case_plain_merge` do, so the cases stay independent.

| Case | Staged from | Must hold |
| --- | --- | --- |
| `audit-cos-prompt` | The Foreman spawns a `retro-critic` (agent type `chantier:retro-critic`) whose prompt is the two lines of item 1 (`chantier retro-critic for the Chief of Staff, in the project <ws>.` / `Read <skill>/references/retro-critic.md and follow it. ...`) | No `FAIL [J1]` and no `FAIL [J2]` names that agent; it shows in the agents table with role `retro-critic`, for `the Chief of Staff`, parent `steering`. Planted: the same agent whose prompt starts `chantier retro-critic about the retro` (no recognised form) gets `FAIL [J1] ... starts with a `chantier <role>` prompt`; and one whose prompt does not name `references/retro-critic.md` gets the J1 card FAIL |
| `audit-claim-call` | A direct-mode steering session (`steering: direct`, a `foreman_claims` entry for its transcript), whose one shell call holds, in item 2's order, `C="<the CLI>"; $C foreman set <session> --epoch 1 2>&1; $C foreman transcript <its uuid> --epoch 1 2>&1; $C seat take ...; $C rules 2>&1; cat .agents/changes/4-batch/brief.md`, stamped before the claim's `since` | `PASS [J14] the steering session read the project's rules`. Planted: the `$C rules` moved alone to a call stamped before the claim call (and removed from the claim call) gets `FAIL [J14] ... rules` |
| `audit-heredoc` | The steering session runs item 3's call: the `python - <<'EOF' ... EOF` here-doc whose body holds `git -C <main checkout> push --force-with-lease ...`, then the CLI's `take` line | `PASS [J26]` and no `FAIL [J22]`. Planted: `git checkout main` as a command (outside any here-doc) gets `FAIL [J26]`; and the same move inside a here-doc fed to `bash` (`bash <<'EOF'` / `git reset --hard origin/main` / `EOF`) gets `FAIL [J26]` |

How the direct-mode steering session of `audit-claim-call` is staged (a separate world, or the
clean world's `batch.json` edited and restored) is the Driver's choice; the clean case
(`case_clean`) still passes unchanged after the three cases run.

`evals/README.md`, the `kit/dry_run.py` row of the kit table (line 276), adds the three audit cases
to its list of planted faults.

## Decisions carried from `02-answers.md`

- The request's scope stands as written: the three detectors (J1, J14, J26), each with a case in
  the kit's own tests built from the transcripts' lines. Items 1 to 4 above are that scope and
  nothing more.
- No behaviour question was left open for the user; implementation detail is the agents'.
- Planned in the next batch (parallel), before the next release (`01-intent.md`); short name
  `audit-fails`.

Two readings this specification takes within the request, so that the fix makes no new false FAIL
nor a false PASS (named here so a reviewer can see them):

- A Chief-of-Staff subagent is audited by its own card (item 1), with no `$CHANTIER rules` line
  asked of it and outside the review-step checks: recognising its role under the old worker
  checks would trade the one false FAIL for three (card, rules, parent).
- A here-doc fed to a shell keeps its body as commands (item 3): a move run that way is a real
  move.

## Out of scope

- Any other detector or rail of the audit, and the other checks' reading of here-docs (J22, C9
  and the Drivers' checks read the commands as today; only the shared window of item 2 reaches
  them).
- The QA driver's first line (`chantier qa-driver for <folder> of batch <batch>, ...`), which
  `PROMPT` does not accept either: no run has shown it (see the open question).
- Re-auditing the two runs of 2026-11-15: both batches are closed (no `4-batch/batch.json` in
  either workspace) and `audit.py` runs only before `close --yes`; the dry-run cases are the proof.
- The cards, the CLI, the agent files, the scorecard's rows (`evals/SCORECARD.md` names the rails;
  their wording holds), the operator's notes in the two audit files.
- The Copilot audit (not written yet).

## Evidence that proves it

- `just eval-dry-run` passes on the PR's head, every case `as expected`, the three new ones
  included, with their PASS lines and their planted FAIL lines; its output is the Verifier's
  evidence (`work/verifier/evidence/`), quoted in the PR body (`evals/README.md`, "Changing the
  kit"). It is also the CI job `just eval-dry-run (ubuntu-latest)`, unchanged in its steps (no CI
  job is added or changed, so no cold-cache run is owed).
- `just check` passes (Linux, macOS, Windows in CI; locally on Windows). The kit is outside `ruff`
  and `mypy`'s paths (`justfile`'s `lint` reads `skills/`); the change still follows the
  surrounding style.
- A change to the eval kit alone owes no `just scenario` (AGENTS.md); none is run for this CR.
- `evals/README.md` asks an independent review of the whole campaign path (setup, a run, the audit,
  the judge) before the merge, by a reviewer that did not write the change: the Driver's review
  step covers it.

## Open questions for the user

1. The QA driver's first line (`chantier qa-driver for <folder> of batch <batch>, in the project
   <root>.`) would also fail J1 today, with the same cause as the retro critic's; no run has shown
   it yet. Fix it in this CR too, or leave it to an inbox item?
