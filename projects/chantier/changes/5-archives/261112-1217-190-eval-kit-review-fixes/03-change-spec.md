# Fix the eval kit's review findings before the first sandbox campaign

## Goal

CR-188 eval-sandbox-app and CR-189 reproducible-evals (both merged, `main` at d72df44) delivered
the sandbox campaigns. A read-only review of that kit (`evidence/00-fable-review.md`) found that
`full` will not end clean and that the quick campaigns run with avoidable risks. This CR fixes
what it found, in one PR from `main`, so the first paid campaign measures chantier, not the kit:

1. a correct `full` run passes the audit (the merged release PR is the batch's, and gets J5);
2. `sandbox.py reset --yes` ends clean from the second campaign on (GitHub keeps `refs/pull/*`);
3. the operator merges through one reviewed kit command that refuses what the user would not
   merge, and the workspace allows exactly what a run needs and the user's settings may lack;
4. the release PR does not go red on a stale `uv.lock`;
5. the docs say what the code does, and what the operator does at the limits (messages, budget).

No tracker issue. The criteria of CR-189 (`.agents/changes/4-batch/3-done/189-reproducible-evals/
02-answers.md`) stay; where this specification and CR-189's differ, this one wins (named below).

## Decisions carried from the answers and the intent

- The user's go (2026-11-12): one follow-up PR from `main`, left unmerged ("130 est mergé. Fait une
  PR en plus si besoin"), in autonomy ("Fait en autonomie maintenant plus de question"): the Chief
  of Staff decided the five points of `01-intent.md`, "What changes"; the points this
  specification settles further are listed in "Decisions taken here", at the end.
- A1: the audit counts the merged release PR (and a fix's) from what the batch recorded (the
  `ship` events, the `merged:` note) and runs J5 on it.
- A2: the reset compares only `refs/heads/*` and `refs/tags/*`, in its survey and its verification.
- A3, B4, B6: `sandbox.py merge <pr>`, sandbox only; refuses a PR not open, a title without the
  run's prefix, checks not all green at its head; merges by rebase. Runbooks and `evals/README.md`
  use it and say why the operator merges. `setup.py` writes the workspace's
  `.claude/settings.local.json` with only: that merge command, the Release driver's tag push to the
  sandbox, `gh release create` on the sandbox, each as narrow as the rule form allows.
- A4: the two frozen release CRs name `uv.lock` in their files and their steps; the sandbox's
  `RELEASING.md` is unchanged (it would change the base).
- Docs: batch 1 has 8 feature CRs plus the release; the merge command, not the forge, refuses a
  red PR; the quick runbooks get `full`'s 10-message-limit fallback (B3); every sandbox runbook
  says what the operator does on a `budget:` ask (one raise, a finding; a second drops the CR,
  B1); `full` says a `ping` may be needed more than once and the report counts each (B2).

## What changes

Everything is under `evals/`. The plugin, the cards, the CLI, `hooks/`, `types/`, the scenario,
`evals/kit/sandbox/` and `evals/kit/sandbox.json` are untouched. Read the kit from `main` (the
files named below are those of d72df44).

### 1. A1: the audit counts the release's PRs (`evals/kit/audit.py`)

Why it fails today: `rails.py` `release_merged` (the CLI, unchanged) appends the note
`merged: <link>` to the release CR and sets its `pr` to `None`; `sandbox_checks` builds `ours` and
the J5 loop only from CRs that still have a `pr`, so the merged release PR, whose title carries
the prefix, is a stray merge (C12 FAIL, exit 1) and gets no J5.

- **New function** `batch_prs(data: dict, events: list[dict]) -> dict[str, list[str]]`: for each
  CR id of `data["crs"]`, every PR link the batch recorded for it, in this order and without
  duplicates (two links with the same PR number, `pr_number()`, are one): the `pr` of each `ship`
  event of that CR (`e["kind"] == "ship"`, `e["cr"]`), in log order; then each of the CR's
  `notes` that starts with `merged: ` and whose rest holds `://` (the rest, stripped, is the
  link; `merged: None` is skipped); then the CR's current `pr`, if any. A CR with none maps to
  `[]`.
- **`sandbox_checks(data, events, run, check)`** uses it:
  - **J5** runs on every link of every CR (not only the current `pr`), one check line per PR,
    labelled as today (`<CR id> PR <n>: …`). The "checks green at its head" part is required
    unless the CR is `cancelled` (as today) or the PR's `state` is `CLOSED` (closed without a
    merge: a release attempt the procedure started again). The other parts are unchanged.
  - The returned `views` stays keyed by CR id, holding the view of the CR's **last** link (so
    `judge_rows` keeps working, and a release whose `pr` is `None` has a view).
  - **C12, strays:** `ours` is the PR numbers of every link of `batch_prs`, every CR included.
  - **C12, the release's merges:** `want` counts the links of release and fix CRs whose view is
    `MERGED` (every link, not one per CR); the check's text and its `seen=bool(want)` stay.
- **`judge_rows`**: the PR column of a release CR shows the numbers of its links joined by `, `
  (`-` when none); a feature CR's column is unchanged. `main()` passes what it needs (the links,
  or `batch_prs`'s result) from `sandbox_checks`'s caller.
- Nothing else in the audit changes; the staged path (`claude-planted`) does not call
  `batch_prs`.

### 2. A2: the reset compares branches and tags only (`evals/kit/sandbox.py`, `evals/kit/setup.py`)

Why it fails today: `remote_refs()` keeps every ref but `HEAD` and peeled tags, and `verify()`
demands that the whole map be `{"refs/heads/main": base}`; GitHub keeps `refs/pull/<n>/head` (and
`refs/pull/<n>/merge`) forever, and no push can delete them.

- **New pure function** `parse_refs(text: str) -> dict[str, str]`: the `git ls-remote` output
  parsed into `{ref: sha}`, keeping only the refs that start with `refs/heads/` or `refs/tags/`,
  without `HEAD` and without peeled entries (`^{}`).
- **`remote_refs(url: str = URL)`** returns `parse_refs` of `git ls-remote <url>`. The parameter
  exists for the evidence (a local bare repository); no command-line argument or variable sets
  it: the module's sentence "The repository is a constant: no argument or variable changes it"
  stays true of the command line.
- **New pure function** `ref_problems(refs: dict, base: str) -> list[str]`: what keeps the refs
  from being the base, in these words (setup's today): `main is at <sha or None>, not <base>`;
  `branches other than main: <names, sorted, comma-separated>`; `tags: <names>`. Empty when only
  `refs/heads/main` is there, at `base`.
- **`verify(base)`** = `ref_problems(remote_refs(), base)` plus, as today, `a PR is still open`
  and `a release is still there`; same `Stop(EXTERNAL, "verification failed: …")`.
- **`cmd_reset`**'s survey (the printed lines and the plan) keeps its output; it reads the same
  filtered `remote_refs()`, so nothing under `refs/pull/` ever appears in it.
- **`setup.py` `survey()`** uses `sandbox.ref_problems(sandbox.remote_refs(), base)` instead of its
  own inline comparison, then adds the open PRs and the releases as today: one rule for the
  reset's survey, its verification and setup's precondition.

### 3. A3, B4, B6: `sandbox.py merge` and the workspace's allow rules

#### 3a. The command (`evals/kit/sandbox.py`)

```text
uv run --no-project python <checkout>/evals/kit/sandbox.py merge <pr> [--workspace <dir>]
```

- `<pr>`: a PR number, or the sandbox PR link `https://github.com/gsemet/chantier-eval-sandbox/pull/<n>`
  (an optional trailing `/`). A `github.com` PR link of any other repository: exit 2,
  `merge works on gsemet/chantier-eval-sandbox only: <pr>`. Anything else: exit 1 (usage).
- `--workspace`: the sandbox workspace, default the current folder (the operator runs it from the
  workspace, like `$CHANTIER`). Its run record `<workspace>.run.json` (written by `setup.py`)
  gives the run's prefix. No record, unreadable JSON or no `prefix`: exit 2, `not a sandbox
  workspace: no <name>.run.json next to <workspace>`. A record whose `repository` is not `REPO`:
  exit 2, `the run record names <repository>, not gsemet/chantier-eval-sandbox`.
- It reads the PR, read-only: `gh pr view <n> --repo gsemet/chantier-eval-sandbox --json
  number,state,title,headRefOid,statusCheckRollup`. A failure: exit 4 with gh's text (nothing
  merged).
- **New pure function** `merge_refusal(view: dict, prefix: str) -> str | None`, the refusals in
  this order (the first that holds is returned; `None` merges):
  1. `state` is not `OPEN`: `PR #<n> is <state, lower case>, not open`;
  2. the title does not start with `<prefix> ` (the prefix and one space): `PR #<n>'s title does
     not start with the run's prefix <prefix>`;
  3. the checks at its head are not all green, by `checks_green(rollup)` (below): `PR #<n>'s
     checks are not all green at its head <sha7>: <name>=<result>, …` (each check that is not
     green, `name` or `context` for its name, `conclusion` or `state` for its result, `pending`
     when neither), or, with no check at all, `PR #<n> has no check at its head <sha7>`.
  A refusal prints `sandbox.py: refused: <text>; nothing merged` on stderr and exits 2; no
  `gh pr merge` is run.
- **New function** `checks_green(rollup: list[dict]) -> bool`, the rule `audit.py` `green()` has
  today: not empty, and every entry's `conclusion` (else `state`) is `SUCCESS`; a skipped,
  neutral, pending or failed check is not green. `audit.py` imports `sandbox` and its `green`
  calls `sandbox.checks_green` (one rule for the audit's J5 and the merge).
- It merges: `gh pr merge <n> --repo gsemet/chantier-eval-sandbox --rebase --match-head-commit
  <headRefOid>`, alone (the head checked green is the head merged; a head that moved makes gh
  refuse). No `--delete-branch`, no `--admin`, no `--auto`. A failure (a conflict, a moved head):
  exit 4 with gh's text, `nothing merged`.
- Success: `merged PR #<n> at <sha7> into main by rebase`, exit 0. The operator then runs
  `$CHANTIER order merged CR-<n>` itself: the command knows no CR and writes nothing.
- `merge` runs no `check_preconditions()` (it needs no `workflow` scope) and never pushes.
- The module docstring gains the usage line and one sentence: `merge` is how the operator, who
  plays the user, merges a run's PR; it is the kit's only merge, and `reset` stays the only force
  push. `main()` gets the `merge` sub-parser (`pr`, `--workspace`) and dispatches to `cmd_merge`.

#### 3b. The allow rules (`evals/kit/setup.py`)

CR-189 said setup writes no `.claude/settings.local.json` for a sandbox campaign; this replaces
it. For a sandbox campaign whose `host` is `claude` (`full`, `real-foreman`, `real-direct`; not
`copilot`), setup writes `<workspace>/.claude/settings.local.json` (the sandbox's `.gitignore`
already ignores it, so the workspace's git stays clean and the base is unchanged), after `init`
and `uv sync --locked` and before placing the CRs, inside the same clean-up-on-failure block. If
the file already exists at that point: exit 2, `<path> already exists`, the workspace removed as
for any failure there. UTF-8 without a byte-order mark, LF, `indent=2`, and **nothing but**:

```json
{
  "permissions": {
    "allow": [ "…the rules below, in this order…" ]
  }
}
```

- **New function** `merge_command() -> str`: `uv run --no-project python <script> merge`, where
  `<script>` is `(HERE / "sandbox.py").as_posix()`, wrapped in double quotes only when it holds a
  space.
- **New function** `allow_rules(spec: dict) -> list[str]`, each rule in its `Bash(…)` form then its
  `PowerShell(…)` form (the host reference's convention):
  1. the merge, every campaign: `Bash(<merge_command()> *)`, `PowerShell(<merge_command()> *)`;
  2. per release CR of the campaign (`release-v<a>-<b>-<c>` gives the tag `v<a>.<b>.<c>`; `full`:
     `v0.2.0`, `v0.3.0`; the quick campaigns: none), the tag push of `RELEASING.md` step 6, exact,
     with no wildcard: `Bash(git push origin <tag>)`, `PowerShell(git push origin <tag>)`, and its
     `-C` form (the host matches `git -C <dir> push …` only with its own rule):
     `Bash(git -C * push origin <tag>)`, `PowerShell(git -C * push origin <tag>)`;
  3. per release CR, `RELEASING.md` step 7: `Bash(gh release create <tag> *)`,
     `PowerShell(gh release create <tag> *)`.
  Nothing else: no `env`, no other permission, no deny or ask rule.
- Setup's summary prints one more line, `merge     <merge_command()> <pr>   (run from the
  workspace)`, and, on Claude, `allowed   <n> rules in .claude/settings.local.json`.
- The module docstring says so (the sandbox paragraph: setup writes the workspace's ignored
  settings file with the merge and the release's tag push and GitHub release, nothing else).

### 4. A4: `uv.lock` in the frozen release CRs

In `evals/kit/sandbox-crs/release-v0-2-0/03-change-spec.md` and `…/release-v0-3-0/03-change-spec.md`:

- "Change" gains a bullet after "Procedure": ``- The version bump changes `uv.lock` (it records the
  project's own version): after setting the version, run `uv lock` and commit `uv.lock` with the
  release commit, or the long gate (`uv run --locked pytest -q`) fails on the release PR.``
- "Files" gains `` - `uv.lock` (the bump changes it) `` after `CHANGELOG.md`.
- "Done when" is unchanged.

`evals/kit/sandbox/RELEASING.md` is unchanged. In `evals/full/RUNBOOK.md`, the paragraph after
batch 1's turns (the warning on `uv.lock` that reached only the operator) becomes: the release is
made by the sandbox's `RELEASING.md`; its step 3 does not name `uv.lock`, so the frozen release CRs
do.

### 5. Docs and runbooks

**`evals/README.md`**:

- The campaigns table, `full` row: `8 feature CRs plus a release, a 9th feature CR injected while
  they run (the batch's 10th CR), then 2 feature CRs plus a release` instead of `9 feature CRs
  plus a release, a 10th injected while they run, …`.
- "A sandbox campaign", **A merge** bullet, rewritten:
  - Why the operator merges: it plays the user, and the merge is the user's;
    `chief-of-staff.md`'s "Never merge" is about the real user's PRs, which an eval has none of.
    The Foreman still merges the release PR itself, as the card says.
  - How: `uv run --no-project python <this checkout>/evals/kit/sandbox.py merge <n>` (the line
    `setup.py` prints), from the workspace, alone, never chained; never a raw `gh pr merge`.
  - What refuses: the sandbox's `main` is not protected, so the forge refuses only a conflict;
    the merge command refuses a PR that is not open, whose title lacks the run's prefix, or whose
    checks are not all green at its head (a pending check included), and merges nothing then. A
    refused merge is reported as it is; the steering session sees the PR not merged, as usual.
  - Then `$CHANTIER order merged CR-<n>` and its line, and the merge order by mode, unchanged.
- A new bullet after **A CR stuck**, **A `budget:` ask** (`ask blocked CR-<n> budget: …`, or
  `status` says the budget is spent): the first in a batch, the operator raises the budget once,
  `$CHANTIER order budget --note <the opening budget × 1.5, rounded up to whole dollars>`, sends
  its line, and the report records it as a finding (the cost of the kit's CRs is part of what a run
  measures). Any later `budget:` ask in the same batch: `$CHANTIER order drop CR-<n>` for the CR
  that asked, its line; the report says why. No other raise.
- **The 10-message limit** bullet: a quick campaign aims to stay under it; if a send is refused
  anyway, the campaign's runbook says how to go on (`full`'s way).
- "Before you start": one sentence that on Claude, for a sandbox campaign, `setup.py` writes the
  workspace's `.claude/settings.local.json` (ignored by the sandbox's git) with the merge
  command's rule and, for `full`, the release's tag push and `gh release create` for its versions:
  rules the user's own settings may lack. Nothing else is allowed there.
- "The kit" table: the `kit/sandbox.py` row adds `merge` (the operator's merge of a run's PR, with
  its refusals); the `kit/setup.py` row adds the settings file; the `kit/merge.py` row says
  `claude-planted`'s merge, on the local forge.
- "The sandbox" section: one line on `merge` next to `build` and `reset`.

**`evals/full/RUNBOOK.md`**:

- Turn 3: the merge with `sandbox.py merge <n>` (as the README says), alone.
- A new turn before `final`: a `budget:` ask, as the README says: here the raise is to `$60` in
  batch 1 and `$23` in batch 2.
- The `uv.lock` paragraph as in section 4.
- "Living with the 10-message limit", its last paragraph: if the Foreman's heartbeat has ended
  (`status` says `heartbeat stopped`) while an order waits, the user types one line, `ping`, in
  the Foreman's session; this may be needed more than once; each `ping` is a human step, and the
  report counts them (the only human steps a `full` run may have). "Report" says it names each
  human step and gives their count, instead of "the human step, if there was one".

**`evals/real-foreman/RUNBOOK.md`**:

- Turn 2: the merge with `sandbox.py merge <n>`, alone, then `order merged` as today.
- Turn 3: a question, a stuck CR or a `budget:` ask, as the README says (raise to `$30`).
- A section "If the 10-message limit is reached" (B3), `full`'s fallback adapted: the quick
  campaign aims to stay under it; past it, the operator follows the host's notes of each of the
  Foreman's turns and `$CHANTIER status` / `$CHANTIER asks`, records every order with `$CHANTIER`
  before sending, sends at most one message per wave; a refused send is reported (J15) and never
  sent another way; the Foreman reads the recorded order at its next heartbeat wake; if its
  heartbeat has ended while an order waits, the user types `ping` in the Foreman's session, as
  many times as needed, and the report counts each as a human step.

**`evals/real-direct/RUNBOOK.md`**:

- It says that the merge, the question, the stuck CR and the `budget:` ask (raise to `$30`) are
  real-foreman's; its "The host's limits" keeps that the 10-message limit does not apply (no
  Foreman session) and adds: should a send between sessions be refused anyway, report it as
  `full` and real-foreman say, never send another way.

**`evals/copilot/RUNBOOK.md`**:

- Turn 2: the merge with `sandbox.py merge <pr>`, alone, then `order merged`.
- A `budget:` ask, as the README says (raise to `$5`). It names no 10-message limit (a Claude
  Desktop limit) and gets no settings file (setup writes none on Copilot).

## Out of scope

- The judge's strictness on contiguous text (B5).
- The base commit and the sandbox itself: `evals/kit/sandbox/` (its `RELEASING.md` included),
  `sandbox.json`; no reset, no push, no PR on the sandbox in this CR.
- The plugin, the cards (`chief-of-staff.md`'s "Never merge" stays as written), the CLI
  (`release_merged` keeps clearing `pr`), `hooks/`, `types/`, the scenario.
- An allow rule for the Foreman's own merge of the release PR, for `$CHANTIER`, or for anything
  else the intent does not name: a host refusal there is reported, as the cards say, and the
  report records it.
- A new structure test (AGENTS.md: few and fast; the evidence below runs the new code instead).
- `claude-planted`, `kit/forge.py`, `kit/merge.py`, the frozen feature CRs and the hidden tests.

## Evidence

The change is the eval kit and its docs alone: AGENTS.md asks for no `just scenario` and no
`just mod`. No paid campaign runs; nothing is written on the sandbox (no `reset --yes`, no PR, no
push, no merge there). Every scratch folder and script is outside this repository and never
committed; the main checkout does not change. Each item quotes its commands with their output, at
the pushed head.

1. **`just check` passes.**
2. **A1, the audit, unit level.** A scratch script loads `evals/kit/audit.py` from the worktree by
   its path, replaces `audit.forge_view` and `audit.run_cmd` with canned answers (no network), and
   runs `sandbox_checks` on a made-up batch read from a scratch folder (`batch.json`,
   `events.jsonl`, a run record with the prefix `[eval 9 2026-11-14 full]`): `created`
   `2026-11-14T10:00:00`; CR-1, a feature, `merged`, `pr` `…/pull/11`; CR-2, the release
   `release-v0-2-0`, `kind` `release`, `pr` `None`, its notes holding
   `merged: https://github.com/gsemet/chantier-eval-sandbox/pull/12`, a `ship` event of CR-2 with
   that link, an `order merged` event with `actor` `foreman`. The canned `gh pr list` gives #11 and
   #12 (both prefixed, merged after `created`) and an older #5; the canned views are `MERGED`,
   green, base `main`, prefixed.
   - With `audit.py` of d72df44 (`git show d72df44:evals/kit/audit.py` into the scratch folder):
     C12 FAIL naming `#12`, and no J5 line for PR 12.
   - With the head's: J5 PASS for `CR-2 PR 12`, the strays check PASS, the release's merges check
     PASS and seen; `batch_prs` printed for both CRs.
   - One more case at the head: CR-2 with a first `ship` link #12 `CLOSED` and red, then #13
     `MERGED` green: J5 PASS for both (the red check of a closed attempt is not required green).
3. **A2, the reset's refs.**
   - `parse_refs` on a fake `git ls-remote` text holding `HEAD`, `refs/heads/main`,
     `refs/pull/7/head`, `refs/pull/7/merge`, `refs/tags/v0.2.0` and `refs/tags/v0.2.0^{}`:
     returns `refs/heads/main` and `refs/tags/v0.2.0` only; `ref_problems` of it says `tags:
     v0.2.0`, and of `{"refs/heads/main": base}` says nothing.
   - A local bare repository in a scratch folder, `main` pushed at the commit `sandbox.py build
     <tmp>/ref` makes, plus `git update-ref refs/pull/1/head <sha>` in it: `remote_refs(<bare>)`
     is `{"refs/heads/main": <base>}` and `ref_problems` is empty; the same with d72df44's
     `verify` logic (its whole-map comparison) reports `refs/pull/1/head`.
4. **A3, the merge command, with no write on the sandbox.**
   - `merge_refusal` on canned views: `MERGED`, `CLOSED`, a title without the prefix, a failed
     check, a pending check, no check, and an open, prefixed, green PR: the six refusals' texts
     and `None` for the last.
   - `cmd_merge` end to end with `sandbox.gh` replaced by a recorder that answers `pr view` from
     canned JSON: on each refusal, exit 2 and no `pr merge` call recorded; on the green PR, exit 0
     and exactly one call, `pr merge <n> --repo gsemet/chantier-eval-sandbox --rebase
     --match-head-commit <sha>`.
   - From the command line, in a scratch folder with a made-up `<ws>.run.json`: `merge abc`
     exits 1; `merge https://github.com/other/repo/pull/3` exits 2 (sandbox only); `merge 3
     --workspace <a folder with no run record>` exits 2 (not a sandbox workspace). None reaches
     `gh`.
   - `allow_rules` and `merge_command` printed for `full`, `real-foreman`, `real-direct`: the merge
     pair for each; for `full` also the four tag-push rules and the two `gh release create` rules
     for `v0.2.0` and `v0.3.0`; nothing for `copilot` (no file written).
   - If `sandbox.py reset` (the plan only, which changes nothing) says the sandbox is at its base,
     `setup.py full <scratch>/full` and `setup.py real-foreman <scratch>/rf` are run (they clone,
     read-only): the settings file's content is quoted, and `git -C <scratch>/full status
     --porcelain -uall` does not list it. If the sandbox is not at its base, this item says so and
     is not run: no reset in this CR. The workspaces are deleted afterwards.
5. **A4, `uv.lock`.** In a scratch repository made by `sandbox.py build <tmp>/ref`: set `0.2.0` in
   `pyproject.toml` and `src/shelf/__init__.py`; `uv run --locked pytest -q` fails (the lock is
   out of date); `uv lock`, then it passes, and `git status --porcelain` lists `uv.lock`. The two
   release specifications' new "Change" bullet and "Files" line are quoted.
6. **Docs.** `git diff --stat` at the head lists only files under `evals/`. A search of the four
   sandbox runbooks and `evals/README.md` for `gh pr merge` finds no instruction to the operator to
   run it (only the README's sentence that the operator never uses it raw); the matches left
   elsewhere (`claude-planted`, `kit/forge.py`, `kit/merge.py`, `kit/sandbox/AGENTS.md`, the merge
   command's own call) are listed.
7. **Not run, said in the PR:** the host's acceptance of the new allow rules, the merge command
   on a real PR, and `reset --yes` against real `refs/pull/*`: the first paid campaign proves
   them and its report records it.

The PR body's Deliverables quote items 2 to 5.

## Decisions taken here (under the user's autonomy, for the Chief of Staff to note)

1. `merge` reads the prefix from `<workspace>.run.json`, the workspace being `--workspace` or the
   current folder; it takes a number or the sandbox PR link; it uses `--match-head-commit` so the
   head merged is the head checked; it deletes no branch and records nothing in chantier.
2. Refusals are exactly the three named (plus "sandbox only" and the missing run record); a draft
   or a PR on another base is left to `gh` and the forge, whose error is passed on (exit 4).
3. "All green" is the audit's existing rule (`SUCCESS` only; pending, skipped, neutral and no
   check at all are refusals), now one function shared by the audit and the merge.
4. The allow rules are exact where the command is fixed (the tag pushes name each version of the
   campaign), with `*` only where an argument varies (the PR number, the notes file); the quick
   campaigns get only the merge rule; Copilot gets no file; each rule in its Bash and PowerShell
   forms, and the tag push also in its `git -C` form.
5. A release attempt's PR closed without a merge is not required green by J5; every other J5 part
   still applies to it.
6. The budget raise is the opening budget × 1.5, rounded up ($60, $23, $30, $5), once per batch;
   any later `budget:` ask drops the CR that asked.
7. B3 goes in `real-foreman`; `real-direct`, with no Foreman session, keeps "does not apply" and
   only says how to report a refused send; `copilot` gets no limit text.
8. B2 replaces CR-189's "one human step" (Q8): each `ping` is a human step, counted.
9. No new structure test; the evidence runs the new functions directly.

No open question.
