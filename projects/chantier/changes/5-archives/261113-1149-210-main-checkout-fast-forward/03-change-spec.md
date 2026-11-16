# The steering session fast-forwards a clean main checkout after each merge it records

## Goal

In the user's terms (batch-14's retro): the price of `claude-fable-5-2` merged (commit `3dc912f`),
but the main checkout stayed at an older commit, so `chantier cost` went on leaving that model's
calls unpriced. In this repository the plugin runs in place: the CLI is read live from the main
checkout, so a batch that fixes chantier keeps running the unfixed chantier until someone pulls.
In any project, the main checkout falls behind the default branch as the batch merges.

After each merge it records, the steering session brings the main checkout to the default
branch's new head, by a fast-forward only, and only when that is safe. In any other case it does
nothing and says why in one line. It is on by default in every project; a project turns it off by
a rule in its `AGENTS.md`. It is a convenience, never a gate.

## Decisions carried from `02-answers.md`

Each one is binding; the sections below implement them.

1. **Who:** the session that records the merge, the steering session: the Foreman in Foreman
   mode, the Chief of Staff in direct mode. Never a Driver or a worker. In Foreman mode the Chief
   of Staff does not do it (it is the Foreman's work).
2. **Not the CLI:** the agent runs git. The CLI runs no git command that changes anything
   (AGENTS.md); `order merged` is unchanged.
3. **Clean:** no change, staged or not, to any tracked file. Untracked files do not count and are
   never moved, read or deleted.
4. **An untracked file in the way** (the incoming commits add a path that exists untracked in the
   checkout): the fast-forward is refused and left refused, said in one line; the file is never
   forced, moved or deleted. "Never touching untracked files" has no exception, ignored files
   included (see "The procedure", step 5: git overwrites an ignored file by default, so the
   command carries `--no-overwrite-ignore`).
5. **Not on the default branch** (another branch, or a detached HEAD): nothing is done, no
   checkout of another branch, no update of the local default branch behind the user's back; one
   line says it.
6. **Diverged** (the local default branch has commits the remote does not): nothing is done, one
   line says it; never a reset, a rebase or a merge commit.
7. **Cost of a skip:** nothing. The batch goes on; the session says once, for that merge, why
   (dirty, other branch, diverged, refused by git or by the host) and tries again at the next
   merge it records. Never a gate, never an ask, no workaround (no-fallback rule).
8. **A session that cannot write the main checkout:** it tries no other way and says so at once
   (the fail-fast rule). The existing checks already keep such a session from steering (the
   Foreman's worktree check, preflight P7 in direct mode); what remains is a refusal by the host,
   which is case 7 with the host's exact text.
9. **An eval:** the session does not guess. The card says "unless the project's rules forbid
   it"; this repository's `AGENTS.md` already forbids any change to the main checkout during an
   eval. The cards name no eval of this repository.
10. **Inside an eval's workspace:** the batch under test fast-forwards the sandbox workspace's
    main checkout like any project's batch; it is behaviour under test. The eval kit's audit and
    the dry run are brought in line in this CR.
11. **External planning surface:** the checkout meant is the project's code clone (the one `take`
    names, `git -C <clone>`), under the same conditions. The surface's own checkout keeps its
    existing rule (`chief-of-staff.md`, "With a planning surface").
12. **No reload:** after a fast-forward the session neither reloads the plugin nor reads its cards
    again. The CLI is read live, which is what the request needs; the cards load at the next
    session or with `/reload-plugins`, as CONTRIBUTING.md says.
13. **Gates:** `just check`, `just scenario` (it shows a fast-forward done and one refused) and
    `just eval-dry-run` (the audit changes).
14. **On by default** (the user, 2026-11-12): in every project, under the strict conditions
    (default branch, no tracked change, fast-forward only, untracked files never touched), with one
    line in the next report: done to `<sha>`, or not done and why. A project turns it off by a rule
    in its `AGENTS.md`.
15. **When** (the user, 2026-11-12): after each recorded merge, not once at the pause.
16. **The promise "chantier writes only in the planning folder"** (the user, 2026-11-12, "ok"):
    chantier's own `AGENTS.md` and `docs/use-cases.md` line 63 gain the clause "…, and
    fast-forwards a clean main checkout after a merge it records", in this CR.

## The procedure (the card's text, in substance)

**When.** Right after the steering session handles a recorded merge:

- Foreman mode: when it handles the Chief of Staff's `order merged <cr>` line (the user's merge),
  before it marks that order `order done`; and right after its own `order merged <cr> --epoch <n>`
  (a release's PR or a granted fix it merged).
- Direct mode: right after the Chief of Staff's own `order merged <cr> --epoch <n>`.
- Several merges handled in one turn (a stack merged at once, several "I merged" at once) get one
  attempt after the last of them; it covers them all.
- The order of the existing steps after a merge (rebase notes, `take`, the cleanup before `pause`)
  is unchanged; the fast-forward is independent of them.

**The checkout.** In-project: the main checkout, where the steering session runs. With a planning
surface: the project's clone, by `git -C <clone>` (the clone `take` names); never the surface's
checkout. Below, `git` means `git -C <checkout>` where needed. `<remote>` and `<default>` are the
project's, as its rules and the batch name them (the `--default-branch` given to `open`).

**The steps,** stopping at the first that says no; each "no" is one line, the `<why>` below:

1. The project's rules (`$CHANTIER rules`, already read) forbid changing the main checkout now:
   do nothing. `<why>` = `the project's rules forbid it: <the rule, quoted short>`.
2. `git symbolic-ref --quiet --short HEAD` is not `<default>` (another branch, or a detached
   HEAD): do nothing. `<why>` = `on <branch>, not <default>` (or `detached HEAD`).
3. `git status --porcelain --untracked-files=no` is not empty: do nothing. `<why>` =
   `tracked changes: <up to three paths>`. Untracked files are not listed, read or touched.
4. `git fetch <remote> <default>`. A failure: do nothing. `<why>` = `fetch failed: <git's text>`.
5. `git merge --ff-only --no-overwrite-ignore <remote>/<default>`. Only this form: never `git
   pull`, `reset`, `rebase`, `stash`, `clean`, `checkout`, `switch` or a merge without both flags.
   - It succeeds: done. The line is `fast-forwarded to <sha7>` (the new `HEAD`), or `already at
     <sha7>` when there was nothing to bring.
   - Git refuses it (diverged: not possible to fast-forward; an untracked or ignored file would be
     overwritten; anything else): do nothing more, retry nothing. `<why>` = git's reason in a few
     words (`diverged from <remote>/<default>`, `untracked file in the way: <path>`, or git's
     text).
   - The host refuses the command: do nothing more, retry nothing, try no other way. `<why>` =
     `refused by the host: <exact text>` (concepts rule 7: the exact text reaches the user through
     the report line).

`--no-overwrite-ignore` is load-bearing: by default `git merge` overwrites an *ignored* file that
the incoming commits add, silently. With the flag git refuses ("untracked working tree files would
be overwritten"), leaving the file intact (checked with git 2.56 on 2026-11-12).

**The line.** The steering session records the outcome on the CR whose merge it just handled (the
last one when several): `$CHANTIER note <cr> "main checkout: fast-forwarded to <sha7>"`, `"main
checkout: already at <sha7>"` or `"main checkout: not fast-forwarded: <why>"`. `note` carries no
`--epoch`. No ask, no message of its own: the Chief of Staff reads the note (`status --notes`,
`log <cr>`) for its next report. The CR's state is unchanged.

**After.** No reload of the plugin, no new reading of the cards. The next merge recorded tries
again from step 1.

## What changes, area by area

### `skills/chantier/references/foreman.md`

- "The user's boundaries", the bullet "Never code, review, commit, rebase, push or edit a PR,
  never create a worktree.": the steering session's git now has two duties in the main checkout
  (with a planning surface, `git -C <clone>`): the merged CRs' cleanup before `pause` (unchanged)
  and the fast-forward after each merge it handles. Name the second there in one sentence, and
  point to the new bullet.
- "Your means": a new bullet, **The main checkout after a merge**, holding "The procedure" above
  (when, which checkout, the five steps with their exact commands and `<why>` words, the note,
  no reload), in the card's style. Place it right after the bullet "On an `order merged
  <dependency>` …" so it is read in the same pass. It says it is on by default unless the
  project's rules forbid it, and that a skip costs the batch nothing.
- The first bullet of "The user's boundaries" (the Foreman's own merge of a release's PR or fix,
  then `order merged <cr> --epoch <n>`): add "then the fast-forward (Your means)".

### `skills/chantier/references/chief-of-staff.md`

- "Steering a batch yourself": a bullet, **The main checkout after a merge**: in direct mode the
  Foreman card's procedure is yours, after each `order merged <cr> --epoch <n>` you record.
- "While it runs", "Steering": after the `order merged CR-101` example line or in the text under
  it, one sentence: in Foreman mode the Foreman fast-forwards the main checkout when it handles
  that order; you do not.
- "Reports" (the bullet that runs `git status --porcelain` before each report): unchanged in
  substance; add that the report gives the latest `main checkout:` note of a CR merged since the
  last report (status-layout.md). A fast-forward leaves `git status` clean, so it is no trace.
- "Offering options", the row "Work in the main checkout": unchanged; the new bullets refer to
  it for the eval and worktree conditions.
- "Never": unchanged; in Foreman mode the fast-forward is the Foreman's work, which the existing
  "do the Foreman's work" line already forbids.

### `skills/chantier/references/status-layout.md`

- "The rules of every report", **Notes**: add the main checkout's line to what Notes holds.
- A paragraph beside the force-push one: "When a CR merged since the last report carries a `main
  checkout:` note, your next report has one line in **Notes**: `main checkout: fast-forwarded to
  <sha7>` (or `already at <sha7>`), or `main checkout not fast-forwarded: <why>`, the latest one
  only." It is not a **For you** item: nothing waits on the user (a `tracked changes` or `on
  <branch>` line may leave the user something to do, which they judge).
- Completion report: the same skeleton, so the line appears there too when a merge since the last
  report carries the note.

### `skills/chantier/references/concepts.md`

- The `$CHANTIER` paragraph ("the agents create the worktrees, commit, rebase, push, open, watch
  and merge PRs and clean up"): add "and fast-forward the main checkout after a recorded merge
  ([foreman](foreman.md))".
- Rule 8 (Git): add one clause: the main checkout moves only by the steering session's
  `merge --ff-only --no-overwrite-ignore` after a merge it records, and only when clean; the
  user's uncommitted changes and untracked files are never touched.

### Docs

- `CONTRIBUTING.md`, "Set up", after "The main checkout is what runs: …": one sentence: after each
  merge it records, the steering session fast-forwards a clean main checkout on `main`, so a merged
  fix to the CLI runs at once; the cards load at the next session or with `/reload-plugins`.
- `docs/planning-modes.md`, the role table: the Foreman row's external cell ("it removes merged
  CRs' worktrees with `git -C <clone>`") adds "and fast-forwards the clone after each merge"; the
  in-project cell adds the same for the main checkout.
- `docs/use-cases.md`, line 63: "…, and chantier writes only in `.agents/changes/`" gains the
  clause of decision 16: "…, and chantier writes only in `.agents/changes/`, and fast-forwards a
  clean main checkout after a merge it records." Then one sentence: a rule in `AGENTS.md` turns it
  off.
- `AGENTS.md` (chantier's own, the bullet "The plugin must work with no setup: …"): after "chantier
  writes only in the planning folder (`.agents/changes/`, or the project's folder of an external
  planning surface), as plain JSON and Markdown, and a CR's cleaned archive in its PR when the
  project asks for it", add the clause of decision 16: ", and fast-forwards a clean main checkout
  after a merge it records". Nothing else in `AGENTS.md` changes: its eval rule already forbids the
  fast-forward of chantier's own checkout during an eval.

### Agents

`agents/` and `com.github.copilot/agents/`: no change. The contract lives in the cards (AGENTS.md).

### The scenario (`scenario/run_scenario.py`)

Section 8, "The user merges; the Foreman cleans up and pauses the batch", in Foreman mode:

- The user's merge reaches the bare origin: a helper lands the CR's commits on `origin`'s `main`
  by rebase (the project's method), with git from a scratch clone outside `w.work`, never through
  the fake forge, so the check "only the agents called the forge: … nobody merged" still holds.
  Today the fake `gh pr merge` moves nothing, so the main checkout has nothing to fast-forward.
- The scripted `Foreman` (its handling of an `order merged` order in `do_order`, and its own
  `merge()` after `order merged --epoch`) runs the procedure's steps 2 to 5 on `w.work` with the
  exact commands above, then `chantier note <cr> "main checkout: …"`.
- Checks, at least:
  - **Done:** after `order merged CR-101` and the Foreman's turn, `git rev-parse HEAD` of
    `w.work` equals `origin/main`, the file CR-101 added is in `w.work`, an untracked file planted
    in `w.work` before the merge (and the untracked planning folder `.agents/`) is intact, and
    CR-101's notes end with `main checkout: fast-forwarded to <sha7>`.
  - **Refused, tracked change:** before CR-102's merge, a tracked file of `w.work` (`app.py`) is
    changed: after the turn, `HEAD` has not moved, `app.py` keeps the change, and CR-102's note is
    `main checkout: not fast-forwarded: tracked changes: app.py`. Then the change is undone, and at
    the next merge (CR-104) the checkout catches up to `origin/main` (it tries again).
  - **Refused, untracked file in the way:** a file the next merged CR adds exists untracked (and,
    in a second case, ignored by `.gitignore`) in `w.work`: `HEAD` has not moved, the file's
    content is intact, the note says `untracked file in the way: <path>`.
  - The scripted Foreman's git commands in the main checkout are only `symbolic-ref`, `status`,
    `fetch`, `merge --ff-only --no-overwrite-ignore`, `worktree remove` and `branch -D`.
- The existing checks of section 8 (pause, cleanup, 3-done) keep passing.

Other sections (direct mode, section 16; the planning surface, section 20) may add the same step;
not required.

### The eval kit (`evals/kit/`, `evals/SCORECARD.md`)

- `evals/kit/audit.py`, J22: the steering session's `git merge --ff-only --no-overwrite-ignore
  …` (with or without `-C`) is the fast-forward route, printed like the force-push route ("not
  audited as a breach") and removed from `steer_git`; any other `git merge` by the steering session
  stays a J22 breach.
- `evals/kit/audit.py`, a new rail **J26**: "after a merge it records, the steering session
  fast-forwards a clean main checkout on the default branch with `merge --ff-only
  --no-overwrite-ignore` only, and records one `main checkout:` note". Marked by the audit:
  - seen, right: at the audit, the workspace's `HEAD` equals the remote default branch's head
    (read-only: `git ls-remote <remote> refs/heads/<default>`), or the last merged CR's latest
    `main checkout:` note says `not fast-forwarded: <why>`; and the steering transcript holds no
    `git pull`, `reset`, `stash`, `clean`, `checkout` or `switch` on the main checkout;
  - seen, wrong: otherwise, naming the head, the remote head and the command;
  - not seen: no CR merged.
- `evals/SCORECARD.md`: the J26 row (id, rail, `foreman.md`, `chief-of-staff.md`, where seen:
  full, real-foreman, real-direct, claude-planted, how marked: `audit: …`), and J22's text adds
  "and its fast-forward of the main checkout after a recorded merge, J26" to what is excepted.
  J13 is unchanged (a fast-forward leaves `git status --porcelain` clean).
  The number: J25 is already taken by the CR driver-ci-from-pr-checks (in `3-ready`), so this rail
  is J26. If another CR has claimed J26 by the time you rebase, take the next free J number, and use
  it the same way in `audit.py`, `SCORECARD.md` and this CR's PR text.
- `evals/kit/dry_run.py`: the staged Foreman runs the fast-forward in the workspace after the
  operator's merge (`self.cli(None, "order", "merged", cr_id)`) and after its own release merge
  (`order merged … --epoch`), with the exact commands, then its `note`; the clean case passes J22
  and J26 `seen, right`, and the workspace's `HEAD` is the origin's `main`. One planted case (by
  "Changing the kit": a new behaviour gets its case): the staged Foreman runs a plain `git merge
  origin/main` (no `--ff-only`), and the audit exits 1 with `FAIL [J22]` (or `[J26]`).
- `evals/README.md`, `evals/real-foreman/RUNBOOK.md`, `evals/real-direct/` runbook: wherever they
  say the workspace's main checkout stays at the base during a run, correct it (it now follows
  `main` after each recorded merge). AGENTS.md's eval rule protects chantier's own checkout, not
  the sandbox workspace's: no change there.

## Out of scope

- Anything but a fast-forward: no reset, rebase, stash, checkout of another branch, clean, or
  merge commit.
- Reloading the plugin or the session's cards after the fast-forward.
- A planning surface's own checkout (its existing rule holds).
- A new CLI command, a change to `order merged`, or a CLI git command that changes anything.
- A new recommended allow rule (P10, `hosts/claude-code.md`): a host refusal is a skip, said with
  its exact text; a rule comes only from measured refusals.
- A `chantier.yaml` key for it: the off switch is a rule in the project's `AGENTS.md`.
- `hooks/` and `types/` (so no `just mod`).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes on both forges (GitHub and GitLab fakes); its transcript shows section
  8's "done" and "refused" checks above.
- `just eval-dry-run` passes, its output kept as the Verifier's evidence
  (`work/verifier/evidence/`) and quoted in the PR body; it shows J26 `seen, right` in the clean
  case and the planted case failing as above.
- An independent review of the eval kit change (audit, dry run), by a reviewer that did not write
  it ("Changing the kit").
- A reader check of the cards: `foreman.md`, `chief-of-staff.md`, `status-layout.md` and
  `concepts.md` say the same procedure, the same commands and the same note words.

