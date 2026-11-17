# Fix plan — approved Deep UX findings (Markdown OKF-Schema Studio)

**If you were pointed at this folder, you are the orchestrator.** Read this file to the end, then
[`STATE.md`](STATE.md), then follow [Resume procedure](#resume-procedure). Do not start coding
yourself: implementation is delegated to Sonnet subagents, and every task is reviewed by a separate
reviewer subagent before it is committed.

## What this plan does

It fixes the findings the user approved (`[x]`) in
[`../00-index.md`](../00-index.md), without breaking any feature listed in
[`protected-features.md`](protected-features.md). Findings that the user did **not** approve are
out of scope, and three of them are explicitly **frozen** (desired behaviour, must not change):

| Frozen | Behaviour to keep |
| --- | --- |
| UX-22 | `project-relative` x-okf-links resolve from the workspace/Git root unless `frontmatter.projectRoot` is set |
| UX-24 | The properties table shows values with YAML syntax (`- item`, `[]`, `null`, `(unknown)`) |
| UX-34 | The sticky heading band shows `#`/`##`/`###` markers, one heading per line |

All part-2 findings (UX-35 … UX-48) are out of scope. A task may incidentally improve one of them,
but must never make one worse, and must not claim to fix it.

## First launch only (T00 still `todo`)

Before starting T00, ask the user once, in a single question, to confirm:

1. that they have read [`decisions.md`](decisions.md) and filled any Override;
2. that local per-task commits on the current branch are fine (D-11);
3. that the extension working tree may be required clean. Show them
   `git status --porcelain -- src/markdown-okf-schema-studio`.

Log the answers in `journal.md`. Do not ask again on later resumes.

## Finding → task map

| Finding | Tasks | | Finding | Tasks |
| --- | --- | --- | --- | --- |
| QA-01 | T01 (+T04–T06) | | UX-15 | T19 |
| QA-02 | T02 (+ an RI scenario in each fix) | | UX-16 | T05, T06 |
| QA-03 | T03, T40 | | UX-17 | T07 |
| UX-01 | T08 | | UX-18 | T20 |
| UX-02 | T09 | | UX-19 | T21, T22 |
| UX-03 | T10 | | UX-20 | T23 |
| UX-04 | T11 | | UX-21 | T24, T25 |
| UX-05 | T12 | | UX-23 | T26 |
| UX-06 | T14 | | UX-25 | T13 |
| UX-07, UX-08 | T15 | | UX-26 | T35 |
| UX-09 | T16 | | UX-27 | T39 |
| UX-10 | T27, T28 | | UX-28 | T29, T30, T33, T34 |
| UX-11 | T32 | | UX-29 | T31 |
| UX-12 | T04 | | UX-30 | T36 |
| UX-13 | T17 | | UX-31, UX-32 | T37 |
| UX-14 | T18 | | UX-33 | T38 |

## Files in this folder

| File | Purpose | Who writes it |
| --- | --- | --- |
| `README.md` | This entry point and the orchestration protocol | Plan author only |
| `STATE.md` | Task tracker: status, base SHA, commit SHA, duration, review rounds. **Single source of truth.** | Orchestrator |
| `journal.md` | Append-only log of every orchestration step, with timestamps | Orchestrator |
| `decisions.md` | Product decisions with the default that tasks apply | User may override |
| `protected-features.md` | Features that must keep working, with the tests that cover them | Plan author; reviewers read it |
| `conventions.md` | Codebase pitfalls every implementer must know | Plan author |
| `review-checklist.md` | What a reviewer checks, and the verdict format | Plan author |
| `visual-review.md` | Agent screenshot review protocol (QA-03), used by T40 | Plan author |
| `prompts/implementer.md` | Prompt template for the implementer (Sonnet, see D-12) | Plan author |
| `prompts/reviewer.md` | Prompt template for the reviewer | Plan author |
| `scripts/gate.sh` | Runs test gates and writes logs to `logs/` | — |
| `scripts/diff.sh` | Prints the task diff restricted to the extension | — |
| `tasks/Txx-*.md` | One self-contained task per file | Plan author |
| `reports/Txx-implementation-rN.md` | Implementer report, round N | Implementer |
| `reviews/Txx-review-rN.md` | Review verdict, round N | Reviewer |
| `logs/` | Gate logs | `gate.sh` |
| `followups.md` | Non-blocking review findings deferred for later | Orchestrator |
| `RESULTS.md` | Final per-finding status with evidence (written by T40) | T40 implementer |

`.agents/changes/` is git-ignored: this folder is never committed. Code changes are committed task
by task (see [Commits](#commits)).

## Orchestration protocol

Run the tasks **strictly in the order of `STATE.md`**, one at a time. Never run two implementers in
parallel: most tasks touch `src/webview/scrollSync.ts` or `src/extension.ts`.

For each task `Txx`:

1. **Pre-flight.**
   - `git status --porcelain -- src/markdown-okf-schema-studio AGENTS.md` must be empty. If it is
     not, stop and ask the user: the user also edits this repository, and their uncommitted work
     must never be mixed into a task.
   - **One exception:** untracked directories under `test/integration/fixtures/`
     whose names match a test prefix (`real-input-*`, `checkbox-e2e-*`, `frontmatter-edit-*`, or
     another `mkdtemp` prefix used by a test) are leftovers of a crashed test run. Inspect them,
     delete them, and log it in `journal.md`.
   - Record `base = $(git rev-parse HEAD)` in `STATE.md` and set the status to `implementing`.
   - Append a line to `journal.md`.
   - If the task lists **Depends on** tasks, check that they are `done`.
   - If it references decisions, read them in `decisions.md`; an `Override` value from the user
     wins over the default.
2. **Implement.** Spawn the implementer with the Agent tool:
   - `model: "sonnet"`, no `effort` (the agent's normal effort), `subagent_type: "general-purpose"`,
     `run_in_background: false` (see decision D-12; T00–T06 ran with `haiku`).
   - Prompt: the text of [`prompts/implementer.md`](prompts/implementer.md) below its `---` line,
     with these placeholders filled:
     - `{TASK}` = `Txx`;
     - `{ROUND}` = 1;
     - `{TASK_FILE}` = `tasks/Txx-….md`;
     - `{OVERRIDES}` = the Override cells of the referenced decisions, or "none";
     - `{FEEDBACK}` = "none".

   The implementer writes `reports/Txx-implementation-r1.md` and never commits.
3. **Gate.** Run `scripts/gate.sh Txx <levels>` yourself, using the levels listed in the task's
   **Gate** line. Record the one-line summary of each level in `STATE.md`.
   - **The implementer reports a STOP:** set the status to `blocked` and ask the user. Do not
     review or gate.
   - **A gate fails:** go straight to step 5 with the gate log as the finding. No review is needed
     yet.
4. **Review.** Spawn the reviewer with the Agent tool:
   - `model: "opus"`, `effort: "low"` (see decision D-12; the user asked for this effort level),
     `subagent_type: "general-purpose"`, `run_in_background: false`.
   - Prompt: the text of [`prompts/reviewer.md`](prompts/reviewer.md) below its `---` line, with
     `{TASK}`, `{ROUND}`, `{BASE}`, `{TASK_FILE}`, `{OVERRIDES}`, and `{GATE_SUMMARY}` (the gate
     lines printed in step 3) filled in.

   The reviewer writes `reviews/Txx-review-rN.md`, ending with `VERDICT: PASS` or
   `VERDICT: CHANGES REQUESTED`.
5. **Fix rounds.** On `CHANGES REQUESTED` or a failed gate, spawn a new implementer with
   `{ROUND}` = N+1 and `{FEEDBACK}` = the paths of the review file and/or the failing gate logs.
   Then repeat steps 3 and 4.
   At most **two** fix rounds (three implementation rounds in total). If round 3 still fails, set
   the status to `blocked`, summarise the open findings in `STATE.md`, and ask the user.
   - **User decision (2026-10-10, during T29):** "Note pour plus tard si ça plante encore et
     continue si besoin". When round 3 fails, do not stop the run to ask:
     1. set the status to `blocked`;
     2. write the open findings to `STATE.md` and `followups.md` (section "Blocked tasks");
     3. save the task's uncommitted work as `logs/Txx-blocked.patch` (`git diff` plus the untracked
        task files), check it with `git apply --check -R`, then restore **only that task's files**,
        so the next pre-flight is clean;
     4. continue with the next task that does not functionally need the blocked one. Skip and mark
        `blocked` any task that does, for example T30, which builds on T29's readiness and counter.

     Report every blocked task to the user at the end.
   - Do not switch the implementer to a stronger model without the user's consent.
   - Do not fix the code yourself.
6. **Commit.** On `PASS` with all gates green:
   - Stage **only** the paths listed in the task's **Allowed files** and in the implementation
     report, with `git add <path> …`. Never use `git add -A` or `git add .`: the repository holds
     unrelated user changes, for example in `book/`.
   - Commit with the message given in the task (Conventional Commits). Follow the session's commit
     attribution instructions.
   - Record the SHA in `STATE.md`, set the status to `done`, and log non-blocking findings in
     `followups.md`.
   - **Duration.** `scripts/state.py set Txx status=done …` fills the `Duration` column
     automatically: wall-clock time from the task's `pre-flight` journal line to now. Check the
     printed row. If the task included a wait that was not work (locked screen, a question to the
     user, a rate limit, an interrupted session), rerun `scripts/state.py duration Txx "incl.
     <time> <reason>"` after the commit line is in `journal.md`. It recomputes from the journal
     and names the wait in parentheses. Never leave a `done` row without a duration.
7. **Checkpoint.** At the end of each phase (the `— Phase n —` rows of `STATE.md`):
   - run `scripts/gate.sh PHASEn full visual`;
   - if anything fails that passed in the T00 baseline, stop and ask the user before continuing.

Keep your own context small. Read the task file, the report summary and the review verdict, not the
full diffs. The reviewer does the deep reading.

## Resume procedure

When starting (or restarting after an interruption):

1. Read `STATE.md` and the last 20 lines of `journal.md`.
2. Run `git log --oneline -15` and
   `git status --porcelain -- src/markdown-okf-schema-studio AGENTS.md`.
3. Reconcile the first task that is not `done`:

| Status in `STATE.md` | Working tree | Action |
| --- | --- | --- |
| `todo` | clean | Start it at step 1 |
| `implementing` | any | If `reports/Txx-implementation-rN.md` exists, continue at step 3. Otherwise spawn the implementer for the same round and tell it that partial changes may exist and must be inspected first. |
| `gating` / `reviewing` | dirty | Continue at step 3 or 4 for the recorded round |
| `changes-requested` | dirty | Continue at step 5 |
| `done` but no commit SHA | dirty | Check that the diff matches the task, commit (step 6), record the SHA |
| `done` with SHA | clean | Next task |
| `blocked` | any | Ask the user; never skip a blocked task silently |

If the working tree contains extension changes that no in-progress task explains, stop and ask the
user. Never run `git reset --hard`, `git checkout -- .`, `git clean` or `git stash` without explicit
user approval.

## Commits

One local commit per task on the current branch (`dev/gsemet`), never pushed (decision D-11). The
plan starts from commit `1a5f8d8` ("feat: checkbox support …"), which already contains the
checkbox feature and the QA skill. If the user disallows commits, stop and ask how to proceed: the
review protocol needs a stable base per task.

## Environment notes

- Run everything from the repository root; `gate.sh` changes directory itself.
- Node comes from `fnm` (`.nvmrc` pins 24). The integration suites start real VS Code windows.
  Do not use the machine while they run, and never run two suites at the same time.
- The VS Code test host refuses to start when it inherits `VSCODE_*` / `ELECTRON_*` variables
  (error: `Code: bad option: --user-data-dir`). `gate.sh` unsets them.
- `gate.sh … visual` never leaves regenerated screenshots in the tree: it copies them to
  `logs/visual-<label>/`, restores the tracked `test/visual/screenshots/` folder, and fails only on
  failure lines missing from `logs/visual-baseline-failures.txt` (compared with every number replaced by `#`, so a known failure whose measured coordinates move stays known) (37 scenarios already fail on
  HEAD, mostly sticky-band checks; UX-34 is frozen, so they stay). Never add lines to that
  baseline without the user's approval. At each phase checkpoint, remove the lines that now pass
  (this only makes the gate stricter); `logs/visual-baseline-failures.T00.txt` keeps the original. Refreshing the tracked screenshots is a separate, final commit.
- **User approval (2026-10-10, standing):** when an interrupted visual run leaves
  `test/visual/screenshots/` dirty, the orchestrator restores that folder only (`git restore` plus
  deleting untracked files in it), exactly as `gate.sh` does, and logs it. Implementers never do it.
- **Implementers never swap sources** (added after T25): no copying, moving or temporarily editing
  source files to reproduce the old behaviour for a red-first run. A T25 implementer started a
  background command that would have overwritten `scrollSync.ts` with a stale temp copy. Its shell
  then sat for 8 h 45 min at an interactive `cp -i` prompt (zsh aliases `cp` to `cp -i`). It
  changed nothing, and the orchestrator stopped it on 2026-10-11 during T35. The risk is losing
  the task's work. Every implementer prompt repeats this rule in its environment notes.
  - Before gating, check that no implementer process is still running, with untruncated command
    lines: `rtk proxy /bin/ps -A -ww -o pid,etime,args | rtk proxy rg -e 'gate\.sh|run-tests|capture\.py|eval .cd '`.
  - A plain `ps` is rewritten by rtk and truncates long commands. That is why the T25 shell was
    missed until T35.
- The exploratory QA harness used to find these bugs is the skill
  [`markdown-studio-exploratory-qa-claude`](../../../../skills/markdown-studio-exploratory-qa-claude/SKILL.md).
  T40 reuses it to replay every approved bug sheet.
