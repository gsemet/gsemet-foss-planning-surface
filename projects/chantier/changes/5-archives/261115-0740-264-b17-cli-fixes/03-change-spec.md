# Change Specification: batch-17 CLI fixes

Origin: the batch-17 retro (`5-archives/batches/batch-17.md`, Retro, lines 61, 63, 65, 68, 81),
filed on the user's word (ID-Q1, A). No tracker issue.

Sources: `intake/request.md` (the four points and the evening finding) and drafts 3, 5, 7 and 10 of
`.agents/changes/batch-17-issue-drafts.md`. There is no `02-answers.md`: the intake's lines are the
decisions. The card-only points of the same retro are the sibling CR `b17-card-fixes`; this CR
changes a card only where the CLI's new behaviour would make it wrong.

## Goal

Four things the batch-17 night paid for in round trips, hand-written notes and failed commands, in
the user's terms:

1. A Driver that handed back `blocked` and is still the CR's recorded Driver can hand back `ready`
   once the block is gone, with no `take --note` round trip through the Foreman.
2. `forge-stack create` builds the stack from the CRs that are ready and leaves the others for a
   later `rebuild` (already true at main, see Part B).
3. In chantier's own checkout on Windows, no `$CHANTIER` command fails with os error 32 because the
   board or a gate holds `.venv\Scripts\chantier.exe`, and no command runs on a stale `.venv`: the
   environment is synced at named moments only, and every command runs with `--no-sync`.
   Every start of the CLI in chantier's own checkout, the board included, uses `uv run --project`,
   never `uvx --from <checkout>` (it served a stale cached build of the board).
4. `take`, `handoff` and `ship` print a stacked CR's real base, the one its PR has on the forge,
   instead of `base origin/main`.

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless they start with a
top-level folder.

## Part A: a blocked CR's ready hand-back (draft 3)

Today `handback` calls `live_cr` (`commands/driver_checks.py`), which refuses any CR that is not
`working`: a `blocked` CR answers `<cr> is blocked: no Driver holds it until the steering session
takes it back (take <cr> --note "<why>"), then hand back again`.

The change, in `commands/driver.py` `handback` and `commands/driver_checks.py` `live_cr`:

- `handback <cr> ready <link>` on a CR whose status is `blocked` **and** whose `agent` is recorded
  (`CrEntry.agent` not empty: the Driver that blocked was not cleared with `agents set <cr> -`) is
  accepted. "The recorded Driver" is this condition: the CLI cannot tell who calls it, and a
  Driver replaced after `blocked context:` has its agent cleared before the new `take`.
- Every refusal of a ready hand-back still applies, unchanged and in the same order: the release
  rules, `ready means a PR recorded (chantier ship)`, and `handback_refusals` (the worktree's head
  is the shipped head, clean, pushed, the long gate passed or `--no-gate`, a verdict `VERIFIED` at
  that head).
- On acceptance, the hand-back carries a note of the block it leaves:
  - the CR's notes get `ready after blocked: <the blocked_reason it had>`;
  - the `handback` event gets `from_blocked: "<the blocked_reason>"`;
  - `blocked_reason` is cleared and the status becomes `ready`, as for a working CR;
  - the printed lines are those of a ready hand-back (`_ready_lines`), with the second line
    followed by `; it was blocked: <the blocked_reason>` so the Foreman sees what was resolved.
- Still refused, with today's text naming `take <cr> --note`:
  - a blocked CR with no agent recorded;
  - `handback <cr> blocked …` on a CR already `blocked` (the scenario's check at
    `scenario/run_scenario.py` l.3818-3822 stays);
  - a `ready` CR handed back again (unchanged);
  - a release CR (`kind == "release"`) that is blocked: it keeps the `take --note` round trip,
    because a release's ready hand-back with no PR marks it released and merged, and its take back
    re-checks the stack under it (`check_take`, `unmet`) and its pending fixes (see open question 2).
- A blocked CR holds no slot and a ready one holds none (`rails.py` `held`): no slot check.

Cards, so they agree with the CLI:

- `skills/chantier/references/driver.md` l.313-316 ("A hand-back refused with `<cr> is ready` or
  `<cr> is blocked`…"): a Driver still recorded on a CR it handed back `blocked` (a `waits:` that
  landed, a `question:` answered to it, an `infra:` that cleared) hands back `ready` directly when
  its checks hold; a refusal naming `take --note` keeps today's route.
- `skills/chantier/references/foreman.md` l.81-82 and l.366: a `[driver <cr>→foreman] hand-back
  ready … it was blocked: …` from a blocked CR needs no `take`; the Foreman handles it as any ready
  hand-back. `agents/` and `com.github.copilot/agents/` are unchanged (the contract is in the cards).

## Part B: `forge-stack create` from the ready CRs (draft 5)

At main this is already the behaviour, from CR-244 (PR #180, merged in batch-17 after the event the
retro names): `commands/forge_stack.py` `_plan` takes the CRs from the bottom while each has a PR
and stops at the first with none; the CRs above are printed `to come:`, and the stack driver adds
them with `forge-stack rebuild` as each joins (`driver.md` l.517-540). The stack driver orders the
ready CRs first with `stack <cr>…` (readiness order, `driver.md` l.486). The scenario proves it
(`forge_stack_cli`, l.4319-4354 and l.4427-4455: two ready PRs and a release with none, `to come:`,
no PR at the bottom refused with the CR named).

What this CR does: no code change. The Driver runs those scenario checks at the CR's head and
quotes them in the evidence as the proof of point 5. A CR with no PR at the bottom of the record's
order (`stack` not yet run) is still refused, `no PR at the bottom of the stack: <cr> is <status>,
no PR`, by CR-244's design (a CLI that orders the stack by itself is out of its scope and this
one's): see open question 1.

## Part C: sync once, then `--no-sync`, in chantier's own checkout (draft 7 and the evening finding)

### The run line

- `plugin_files.py` `cli_command`: in the dev mode (`is_dev_checkout()`), the line becomes
  `uv run --no-sync --project "<plugin root>" chantier` (with a surface, plus `--project
  "<folder>"` after `chantier`, unchanged). The plugin mode (`uvx --from "<plugin root>" chantier
  --skill "<skill folder>"`) is unchanged. The line is the same on every system: one method, as
  AGENTS.md asks; only preflight's text is Windows-only.
- A new function next to it, `sync_command()`, returns the dev mode's sync line,
  `uv sync --locked --project "<plugin root>"`, and `None` in the plugin mode. `cli_command`'s
  docstring names both.

### Who syncs, and when

Only the steering session (the Chief of Staff, or a Griller session for its own start) runs the
sync, and only in the dev mode. A Foreman, a Driver or a worker never syncs: it runs `$CHANTIER` as
its prompt gives it, `--no-sync`. That is what keeps a running gate or the board from colliding
with a sync started by another agent.

1. **At the session's start, before the first `$CHANTIER` command** (so before preflight and before
   the board): `skills/chantier/SKILL.md` (the router's `$CHANTIER` paragraph, l.16),
   `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md` and `skills/status/SKILL.md` (each
   carries the same dev-mode sentence) say: in the dev mode, run `uv sync --locked --project
   "<plugin root>"` once, then `$CHANTIER` is `uv run --no-sync --project "<plugin root>" chantier`.
   A sync that fails (os error 32 because another session's board or gate runs, or any uv error) is
   one line to the user with uv's text, and the session goes on: nothing is installed that was not
   there.
2. **At a batch's start:** `skills/chantier/references/chief-of-staff.md`, at the go, before
   `$CHANTIER preflight`: in the dev mode, the sync, with the board stopped first and started again
   after (the host's stop of a background shell; then `$CHANTIER board --seat <id>` as
   `session-start.md` says). No gate runs then: no batch is running.
3. **After a merge that changes `uv.lock`:** `skills/chantier/references/foreman.md`, the
   fast-forward steps (l.325-347): note `HEAD` before step 5; after a fast-forward, when
   `git diff --quiet <before> HEAD -- uv.lock` says it changed, the note becomes `main checkout:
   fast-forwarded to <sha7>; uv.lock changed: sync pending`. In the direct mode the Chief of Staff
   does the same fast-forward itself (`chief-of-staff.md` l.894). The Chief of Staff, on that note,
   syncs when `$CHANTIER status` shows no gate running, with the board stopped and started again
   around it; until then it says `sync pending` in its report's Notes (`status-layout.md` l.95,
   the `main checkout:` line). See open question 3.

### Preflight says so on Windows

`commands/preflight.py` `_check_tools` (P5): in the dev mode on Windows (`os.name == "nt"`), the
P5 line, passed or failed, ends with `; dev mode on Windows: $CHANTIER runs --no-sync; sync with
<sync_command()> only when no chantier process runs (the board, a gate): os error 32 otherwise`.
It is text, not a check, and no new P line (the report stays within ten lines). Nothing changes on
Linux and macOS.

### The permission rules

- `commands/permissions.py`: the dev row becomes `uv run --no-sync --project /checkout chantier
  status` / `uv run --no-sync --project * chantier *`, and a new dev row `uv sync --locked --project
  /checkout` / `uv sync --locked --project *` under the `batch` capability, so P10 names both.
- `skills/chantier/references/hosts/claude-code.md`: the rows and rule lists that name `uv run
  --locked --project * chantier *` (l.142, 191, 230-231, 289, 347, 371) name the new forms, and the
  sync rule with them.

### The words in the repository

- `AGENTS.md` l.40-41 (the one method that runs the CLI): in chantier's own checkout, `uv sync
  --locked --project` once at the moments above, then `uv run --no-sync --project`, the local code,
  live; never `uvx --from <checkout>`. See open question 4.
- `CONTRIBUTING.md` l.71-73 and l.175-176: the same, with the reason in one sentence: uv caches a
  local source by its version, so `uvx --from <checkout>` (even with `--refresh`) can serve an older
  build; on 2026-11-14 it served a board with no Triage view and no `js/i18n/fr-write.js`, both on
  main at ce00ec3.
- `docs/web-board.md`, "By hand" (l.137-140): one more sentence: in chantier's own checkout, start
  it with `uv run --no-sync --project <checkout> chantier board` after a sync; never `uvx --from
  <checkout>`.
- `skills/chantier/references/concepts.md` l.273 (`$CHANTIER`): the dev form.
- A search of the cards, `skills/*/SKILL.md`, `README.md`, `CONTRIBUTING.md` and `docs/` for
  `uvx --from` with a local path and for `--refresh` next to `uvx` found no line that tells anyone
  to run chantier's own checkout through `uvx` today; the Driver runs it again at its head and fixes
  any it finds. Past release notes under `docs/release-notes/` are history and stay.
- Not changed: `scripts/docs_screenshots.py` (a one-shot script, `uv run --locked`, run by hand)
  and the eval kit (`evals/`: an eval's workspace uses the user's own install).

## Part D: a stacked CR's base from its PR (draft 10)

Today `take` and `handoff` print `worktree: … base <ref>` from `start_base` (`commands/facts.py`
`_base_of`): for a CR of a stack with no `after`, that is `origin/<default>`, though the stack
driver has retargeted its PR onto the CR below. `ship` prints and logs `stack_base(d, c, repo)`
with `planned=False` (`commands/delivery.py` l.137-143), which is the start base too until `stack`
marks the CR. Drivers needed a hand-written BASE note.

The change:

- A "stacked CR" here is a CR of a batch in `stack` mode that is in `chain(d)` (`stacks.py`): not
  ended, not a fix. A release in a stack is one too. Other modes (parallel, series) and fix CRs are
  unchanged and make no forge call.
- **When such a CR has a PR recorded** (`c.pr`), `take` and `handoff` (both through `cr_facts`'s
  `worktree:` line) read the PR's base from the forge and print it, formatted by `_ref` (the
  default branch as `<remote>/<default>`, another branch by its name). With no PR, the line is
  today's.
- **`ship <cr> <link>`** on a stacked CR reads the base of the PR named by `<link>` (the one it
  records) and prints `recorded <link> (base <forge base>, head <sha7>, …)`; the `ship` event's
  `base` is that value.
- **The read:** GitHub, `gh api repos/<owner>/<repo>/pulls/<n>`, field `base.ref`; GitLab, `glab
  api projects/<path>/merge_requests/<iid>`, field `target_branch`. The forge is read from the
  link's shape, as `forge-stack` does: reuse `forge_stack._pr_parts`, `forge_stack._gh` and
  `forge_stack_gitlab.glab` (move what is shared into `commands/forge_stack_shared.py` or a small
  module both import; no second copy of the calls). One read per command, no retry.
- **A read that fails** (no `gh`/`glab` on PATH, the forge refuses, no network, a link of neither
  shape): the command does not fail and records what it records today; the base reads
  `base ? (not read from <link>: <the forge's text, one line>)`, and `ship`'s event keeps `base`
  empty. It prints no other base in its place (no fallback). See open question 5.
- `take stack` and `stack` (`facts.stack_lines`, `_stack_ref`) keep the record's planned base:
  they are the stack driver's plan, not a PR's state.
- `driver.md` l.449-450 and l.458 ("`take` prints the base as another CR's branch"): unchanged in
  meaning; one clause says that for a stacked CR with a PR the base `take` prints is the PR's base
  on the forge.

## Decisions carried from the intake

- Point 3: `handback ready` from the recorded Driver of a blocked CR is accepted with a note
  (Part A).
- Point 5: `forge-stack create` builds from the ready CRs and leaves the queued ones to a later
  `rebuild` (Part B: met at main).
- Point 7: chantier's own-checkout run line syncs once at batch start, before the board starts and
  after any merge that changes `uv.lock`, then runs with `--no-sync`; preflight says so on Windows
  (Part C).
- Point 10: `take`, `handoff` and `ship` take a stacked CR's base from its PR's base when a PR
  exists (Part D).
- The evening finding: in chantier's own checkout every start of the CLI, the board included, uses
  `uv run --project`, never `uvx --from <checkout>`; the cards and docs that say otherwise are fixed
  (Part C, "The words in the repository").

## Out of scope

- The retro's card-only points (drafts 1, 2, 6, 8, 9, 11 to 15): `b17-card-fixes` and the CRs the
  drafts name.
- A CLI that orders the stack by itself, or builds a stack that skips a CR with no PR at its bottom.
- A sync run by the CLI itself (it runs from the `.venv` it would rewrite), or any check that the
  `.venv` is in sync.
- The plugin mode's `uvx --from` line; the eval kit; `scripts/docs_screenshots.py`.
- The base printed by `take stack` and `stack`; bases in parallel and series batches.
- No change under `hooks/` or `types/` (no `just mod`), none to the `STATUS.json` fields the pane
  shows (no pane screenshot), no CI job added or changed.

## Evidence

- `just check` at the PR's head (Linux, macOS and Windows through CI; Windows locally), then `just
  scenario` on the user's Windows machine, GitHub and GitLab: a CLI, card and scenario change
  (AGENTS.md).
- pytest (`skills/chantier/scripts/cli/tests/test_plugin_files.py` l.300 and l.307): the dev line is
  `uv run --no-sync --project "<root>" chantier`; `sync_command()` gives `uv sync --locked
  --project "<root>"` in the dev mode and `None` in the plugin mode.
- Scenario (`scenario/run_scenario.py`), new or changed checks:
  - Part A, beside l.3816-3822: with an agent recorded (`agents set <cr> drv-x`), `handback <cr>
    blocked question: x`, then the gate and the verdict at the head, then `handback <cr> ready
    <link>`: exit 0, status `ready`, `blocked_reason` empty, a note `ready after blocked: question:
    x`, the event's `from_blocked`, and the printed `it was blocked: question: x`. The same with
    the agent cleared (`agents set <cr> -`): refused, naming `take <cr> --note`. A ready hand-back
    from a blocked CR with no verdict at its head: refused with `no verdict VERIFIED`, the CR still
    `blocked`. A blocked release: refused as today. The existing second-`blocked` refusal stays.
  - Part C: l.668's check reads `cli: uv run --no-sync --project `; preflight's P5 line holds the
    sync sentence when the scenario runs on Windows, and does not elsewhere.
  - Part D, in a stack case with the fake forge (`scenario/fake_gh.py` answers `GET
    repos/…/pulls/<n>` with a `base`; `scenario/fake_glab.py` `GET merge_requests/<iid>` with a
    `target_branch`): a stacked CR whose PR's base on the fake forge is the branch of the CR under
    it prints that branch on `handoff`'s and `take --note`'s `worktree:` line and in `ship`'s
    `recorded … (base …)`, and the `ship` event's `base` is it; a stacked CR with no PR prints
    today's line and makes no `pulls` call (the fake forge's log); a CR of a parallel batch with a
    PR makes no `pulls` call; a fake forge that answers an error prints `base ? (not read from
    <link>: …)` and the command exits 0. GitHub and GitLab both.
  - Part B: the existing `forge_stack_cli` checks (l.4319-4354, l.4427-4455) pass; quoted.
- On the user's Windows machine, once, in chantier's own checkout, recorded in `evidence/`: with
  `$CHANTIER board` running from the PR's head, a second session's `uv run --no-sync --project
  <worktree> chantier status` runs; `uv sync --locked --project <worktree>` with the board running
  fails with os error 32 only when it has something to reinstall (the transcript says which).

## Risks

- Every `$CHANTIER` line changes form, so the user's allow rule `uv run --locked --project *
  chantier *` no longer matches: until the new rules are in `~/.claude/settings.json` (P10 names
  them; the Chief of Staff adds them on the user's yes), each command may ask, and an unattended
  batch may stop at the first one.
- Between a merge that changes `uv.lock` and the sync, the code is newer than the `.venv`: a new
  dependency fails to import. The sync waits for no gate to run, so the window can last a gate's
  length (open question 3).
- Part D adds forge reads to `take`, `handoff` and `ship`, which read none today; AGENTS.md says the
  CLI needs no network once uv's cache holds its packages. The reads are only for stacked CRs with a
  PR, which already live on the forge, and a failed read does not stop the command.
- A blocked CR handed back ready skips the Foreman's look at the block; the note and the printed
  `it was blocked:` are what it sees.

## Open questions

1. **Point 5 is met at main** by CR-244 (merged in batch-17): `forge-stack create` stacks the
   bottom CRs with a PR and lists the rest as `to come`, once the stack driver has put the ready
   ones first with `stack`. Keep point 5 as proof only (no code), or do you want `create` to build
   from the ready CRs even when one with no PR sits at the bottom of the order, without the stack
   driver reordering first (which CR-244 left out on purpose)?
2. **A blocked release.** Should a release's Driver also hand back `ready` straight from `blocked`?
   The spec says no: a release keeps `take --note`, because a ready hand-back with no PR marks it
   released, and the take back re-checks the stack under it and its pending fixes.
3. **The sync after a merge that changes `uv.lock`, on Windows.** It cannot run while a gate or the
   board runs from the `.venv`. The spec has the Chief of Staff wait until no gate runs, stop the
   board, sync, start the board again, and say `sync pending` in its reports meanwhile. Is waiting
   for the gates right, or should the sync happen at once and a gate that was running be rerun?
4. **AGENTS.md.** The run line is written in your project rules (AGENTS.md l.40-41, "One method
   runs it ... `uv run --locked --project`"). The spec changes that sentence to the sync-then-
   `--no-sync` form. Agreed, or do you prefer to edit AGENTS.md yourself?
5. **A forge read that fails in `take`, `handoff` or `ship`** (offline, `gh` missing, a refusal):
   the spec prints `base ? (not read from <link>: …)` and goes on, showing no other base. Or should
   the command fail (exit 4) as `forge-stack` does, or show the record's base marked as not
   checked?
