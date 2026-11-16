# Change Specification: `verdict VERIFIED` refuses a verify note that does not name the head

## Goal

A Verifier that records `VERIFIED` without having written its proof note at the head it judged
is stopped by the CLI inside its own run, and corrects itself there, before it replies. The
Driver no longer finds out after the fact, restarts a worker or runs `verdict` itself. The
refusal is role-free (the CLI knows no role) and works the same on both hosts (Claude Code,
GitHub Copilot) and both forges (GitHub, GitLab): it reads one file in the planning folder and
one git head, and touches no host or forge.

## What the record shows (the check the request asked for first)

The question: did the workers started after CR-256's merge read the old card text? CR-256
(`9a63cf2`, "Coder, Inspector and Verifier reply in an exact template...") reached the main
checkout at 2026-11-14 23:34:59Z (`git reflog main`: "merge origin/main: Fast-forward" at
00:34:59 +0100). A worker's prompt names the card in the plugin's skill folder, which is the main
checkout (`plugin_files.skill_dir()`; the plugin runs in place). The text "run `$CHANTIER verdict`
before you reply" and the `Head: <sha>` line were already in `worker.md` before `9a63cf2`
(`git show 9a63cf2^:skills/chantier/references/worker.md`).

Survey of the 44 Verifier transcripts started after 23:35Z in batch-18 (the subagent transcripts
under the user's Claude Code project folder, read-only):

- 7 read `worker.md` in the main checkout: the new text.
- 3 read `worker.md` in their CR's worktree (`chantier.worktrees/batch-18-CR-257`, `-CR-267`, and
  a relative path in CR-263's worktree): the CR branch's copy, which is the new text only when
  the branch holds `9a63cf2`.
- 34 read no `worker.md` at all: they acted on their prompt alone. Example: the Verifier for
  CR-254 started at 00:52:15Z (a restart) read no card, wrote `work/verify.md`, ran no `verdict`,
  and replied `VERIFIED` with prose under it.

So the workers did not read the old card text: most read no card at all, and those that read one
read the new text. The decision of `02-answers.md` that is conditional on "they read the old card
text" therefore does not apply; the change is still the CLI refusal the request names, with the
card lines that state it (below). A card rewording cannot reach a worker that does not read the
card; the refusal reaches it at the moment it runs `verdict`. The record cannot tell who ran a
`verdict` (`commands/delivery.py` logs every verdict with `actor="driver"`), which is why the
survey is from the transcripts. Two Driver notes confirm Drivers ran `verdict` from a reply
(CR-262 at 02:48:38Z: "the verifier did not record its verdict, so I ran verdict CR-262 VERIFIED
from its reply").

The survey also shows where `verify.md` lands: `work/verify.md` (most), `work/verifier/verify.md`
(the card's `Proof:` line), the CR folder's root, `evidence/` and `verifier/`. The Drivers' notes
and briefs name `work/verify.md` ("verifier left no work/verify.md", "verify.md left in evidence/
not work/"). This spec uses `work/verify.md`, the request's path (see Open questions, 1).

## What changes

### 1. The CLI: `verdict` (`skills/chantier/scripts/cli/src/chantier/commands/delivery.py`)

In `verdict(args)`, after the clean-tree check and `head = git("rev-parse", "HEAD", cwd=wt)`, and
only when `result == "VERIFIED"`:

- Read `work(repo, c) / "verify.md"` (the CR's work folder, `<CR folder>/work/verify.md`; `work`
  is already imported from `chantier.commands.crs`), with `chantier.core.files.read_text` (UTF-8,
  a byte-order mark tolerated as `read_text` does today).
- A `Head:` line is a line that, once its leading whitespace is stripped, starts with `Head:`.
  Its value is the first whitespace-separated token after `Head:`, with surrounding backticks
  removed. Text after that token is allowed (the record holds lines like
  `Head: bc46f8c...f264 (worktree HEAD, pushed; PR 213)`).
- The note names the head when one `Head:` line's value is exactly the full 40-character SHA the
  verdict binds to (`head`, the worktree's `HEAD`), compared case-insensitively. A short SHA
  does not match: the card asks for the full SHA, and a short one is the format error this CR
  closes.
- Refused (exit 2, `EXIT_PRECONDITION`, nothing logged, the record untouched) when the file is
  absent, holds no `Head:` line, or no `Head:` line names that head. One message, its last part
  naming what was found:

  ```text
  CR-123: verdict VERIFIED needs <CR folder>/work/verify.md with a line "Head: <full SHA>" for the head abc1234 it records: <reason>
  ```

  where `<CR folder>` is printed as the absolute path, POSIX slashes (`.as_posix()`), and
  `<reason>` is one of `no such file`, `no Head: line`, or `its Head: line names def5678` (the
  first `Head:` value found, cut to seven characters). The message names the full SHA to write
  nowhere else: the Verifier gets it from `git rev-parse HEAD` as its card says.
- `NOT VERIFIED` is never refused for this: a Verifier, or a Driver, can always record a failure.
- The order of the checks stays: the verdict word (exit 1), the CR (exit 2), the worktree (exit
  2), the clean tree (exit 2), then the note (exit 2). The docstring says it reads the note at
  `work/verify.md` and still names no role.
- Function size: `verdict` stays under the project's function limit; the note check goes in its
  own small function in `delivery.py` (for instance `_verify_note_names(path, head) -> str | None`
  returning the reason or `None`).

The existing behaviour is kept: the last verdict at a head decides, `handback ready` still needs a
`VERIFIED` at the head (`last_verdict` in `commands/crs.py` is unchanged), and the budget never
refuses `verdict` (`concepts.md` line 254).

### 2. The cards (`skills/chantier/references/`, shared by both hosts)

- `worker.md`, section "Verifier":
  - The output sentence (line 137) names the place: `<work folder>/verify.md` (the work folder's
    root, the one file the CLI reads), with its `Head: <full SHA>` line, the full SHA of
    `git rev-parse HEAD` in the worktree.
  - The `verdict` sentence (lines 140-142) adds: `verdict <cr> VERIFIED` is refused (exit 2)
    until `<work folder>/verify.md` has a `Head:` line naming that full SHA; on the refusal, write
    or fix the note and run `verdict` again, in the same run, before you reply.
  - The reply template's `Proof:` line (line 195) becomes `Proof: <work folder>/verify.md`.
  - The line at the top that sends a role's notes to `<work folder>/<role>/` (line 14) names the
    one exception: the Verifier's `verify.md` is at `<work folder>/verify.md`; its before/after
    evidence stays in `<work folder>/verifier/evidence/`.
- `driver.md`, the Verifier bullet of "A reply out of format" (lines 83-89): `verify.md` is named
  `work/verify.md`, and the bullet adds that the CLI refuses `verdict VERIFIED` without a
  `Head:` line naming the head there, so a `VERIFIED` in `$CHANTIER handoff <cr>` at the head is
  proof the note exists at that head.
- `concepts.md`, the paragraph on `verdict` (lines 351-353): `verdict <cr> VERIFIED` is refused
  (exit 2) unless `work/verify.md` in the CR's folder has a `Head:` line naming the full SHA of
  the head it records; `NOT VERIFIED` is not.

No `unproved` mark: the refusal is one code path, the same on both hosts and both forges (no host
tool, no forge call), proved by the tests and the scenario below on the local machine and in CI
on Linux, macOS and Windows. The card lines state only the refusal, never that a Verifier then
corrects itself; that is the expected effect, read in the next batch's retro, not a claim.

`agents/verifier.md` and `com.github.copilot/agents/verifier.md` are not changed (a role's
contract lives in the cards).

### 3. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- A helper, beside `World.ready`, writes `<CR folder>/work/verify.md` with
  `Head: <git -C <worktree> rev-parse HEAD>` (UTF-8, no byte-order mark) before each
  `verdict ... VERIFIED` the scenario runs. `World.ready` (line 268) calls it before its
  `verdict`; every direct `w.chantier("verdict", <cr>, "VERIFIED")` (lines 3464, 3474, 3504, 3558,
  3583, 3662, 3690, 3708, 3719, 3735, 3860, 3876, 3925, 5624, and any other the Driver finds) gets
  it too, written at the head in force at that call.
- In `handback_proofs` (line 3431), before the first `verdict ... VERIFIED`, three checks:
  - with no `work/verify.md`: `verdict <cr> VERIFIED` exits 2, its stderr holds `work/verify.md`
    and `no such file`, and `events.jsonl` holds no new `verdict` event;
  - with a `verify.md` whose `Head:` line names the previous commit's full SHA: exit 2, stderr
    holds `its Head: line names <that sha7>`, no event;
  - `verdict <cr> "NOT VERIFIED"` with no note is accepted (exit 0, one event).
  Then the helper writes the right note and the existing checks run as today. The check count of
  `log_events("verdict")` at line 3477 is adjusted for the added `NOT VERIFIED`.
- The `gates` unit's time budget (`UNITS["gates"]`, 400 s) is kept; the added calls are a few
  CLI runs.
- `scenario/README.md`, "Coverage": the bullet that covers `handback_proofs` (unit `gates`) names
  the refusal: "`verdict VERIFIED` refused without `work/verify.md` naming the head (no file, a
  stale `Head:`), `NOT VERIFIED` accepted without it", with the pytest marker below.

### 4. Tests (`skills/chantier/scripts/cli/tests/`)

One parametrized test, in `test_rail_refusals.py` (or a new `test_verdict_note.py` if the Driver
finds that file at its size limit), on a prepared state built as `test_gate_refusals.py`'s `gated`
fixture does (`open_batch`, `take --epoch 1`, the worktree added with `git worktree add`), calling
the CLI in-process:

- cases (label, the note's text or no file, the expected code, a part of stderr):
  - no file: 2, `no such file`;
  - a note with no `Head:` line: 2, `no Head: line`;
  - a `Head:` with a seven-character SHA of the head: 2, `its Head: line names`;
  - a `Head:` with another commit's full SHA: 2, `its Head: line names`;
  - a `Head:` with the full head and trailing text, indented, in backticks: 0;
- for each refusal: no `verdict` event added to `events.jsonl`;
- one more case: `NOT VERIFIED` with no file: 0.

The test keeps `just test` within its budget (one fixture, one parametrized function).

### 5. The eval kit (`evals/`)

- `evals/kit/dry_run.py` line 408: the dry run writes `<CR folder>/work/verify.md` with the
  worktree's head before `self.cli(driver, "verdict", cr_id, "VERIFIED")`, as the Verifier does.
- `evals/SCORECARD.md`, row C6: its text adds "and `VERIFIED` is refused unless `work/verify.md`
  names the head"; its other cells are unchanged.

## Decisions carried from `02-answers.md`

- Source and choice: the request's fix is the user's ("oui les 6", then "lance le tout dans le
  batch actuel"); the CR joins batch-18, switched to a stack. Carried: the change is the request's
  refusal, nothing else in the CLI.
- Generality: the same on both hosts and both forges; a path not proved on Copilot or a real
  GitLab carries the mark "unproved" in its card line. Carried: the refusal has no host- or
  forge-specific path, so no card line carries the mark (section 2).
- Place in the stack: last. Carried: the Driver bases the branch on the CR below it in batch-18's
  stack; the scenario edits are written against that base.
- If the workers after CR-256's merge read the old card text, the spec says so and keeps only the
  CLI refusal. Carried: the record shows they did not read the old text (most read no card); the
  spec says so, and keeps the refusal with only the card lines that state it and the one place of
  `verify.md` it needs (section 2).

## Out of scope

- Any refusal of a role ("a Driver may not run `verdict`"): the CLI knows no role.
- Checking the claims inside `verify.md` (their commands, outputs and SHAs): the Driver's
  format check stays a judgement.
- Comparing `verify.md`'s head with the shipped head (`c.head` from `ship`) when it differs from
  the worktree's head (Open questions, 2).
- The Inspector's JSON and the conflict-resolver's reply (the other out-of-format replies of the
  retro): not this CR.
- Recording who ran a verdict (the `actor` of the event).
- Moving the `verify.md` files of closed or archived CRs.
- `agents/*.md` and `com.github.copilot/agents/*.md`.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI), with the new parametrized test.
- `just scenario` passes, with the three new checks in `handback_proofs` and every existing
  `verdict VERIFIED` preceded by its note.
- `just eval-dry-run` passes with the note written in `dry_run.py`.
- By hand, in the PR's evidence, at the PR's head, on a scratch batch outside the repository: the
  three refusals (no file, no `Head:` line, a stale `Head:`) with their exit code and message, the
  accepted `VERIFIED` once the note names the head, and `NOT VERIFIED` accepted with no note;
  `events.jsonl` before and after each refusal shows no new event.
- `git diff --stat` at the head touches only: `commands/delivery.py`, the new or extended test
  file, `scenario/run_scenario.py`, `scenario/README.md`, `skills/chantier/references/worker.md`,
  `driver.md`, `concepts.md`, `evals/kit/dry_run.py`, `evals/SCORECARD.md`.
- Not a change to `hooks/` or `types/`: no `just mod`. Not a change to the pane: no screenshot.

## Open questions

1. The note's place. The request says `work/verify.md`; `worker.md` says
   `<work folder>/verifier/verify.md` (its `Proof:` line); batch-18's Drivers and Verifiers mostly
   used `work/verify.md`. This spec takes the request's `work/verify.md` and aligns `worker.md` to
   it. Should the CLI read `work/verifier/verify.md` instead (and the Drivers' briefs follow the
   card)? Reading both is not offered (no fallback).
2. "The CR's recorded head". This spec compares the note with the head the verdict itself records
   (the worktree's `HEAD`, the one `handback ready` checks). Once the CR is shipped at that head
   it is also the recorded `head` of the CR. Should the refusal also require the CR's shipped head
   (`ship`'s `head`) to equal it, which would refuse a `VERIFIED` before `ship` (the scenario runs
   several)?
