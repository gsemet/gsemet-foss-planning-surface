# chantier's merge route works for a PR of a native GitHub stack

## Goal

When chantier merges a PR itself (the steering session, under the user's grant: a release PR, a
fix PR), the route the cards give must work when that PR is in a native GitHub stack. Today the
cards and `permissions.py` name only `gh pr merge`, and GitHub refuses it for every PR of a native
stack (batch-18's real-foreman run 2, 2026-11-15, through the eval kit's merge script):

```text
GraphQL: This pull request is part of a stack and must be merged using the asynchronous merge REST API. For more information, see https://docs.github.com/rest/pulls/pulls#merge-a-pull-request-asynchronously (mergePullRequest)
```

A release PR on top of a stack batch is in that stack, so a granted release merge in a stack
batch hits this refusal. The eval kit already uses the route that works (PR #224, merged:
`evals/kit/sandbox.py`, `merged_with` and `merge_async`). This CR puts the same route in the
cards and the allow rules, and proves it or says what stays unproved.

## Decisions carried from `02-answers.md`

1. The request's scope stands as written: the cards and the allow rules get the route for a PR in
   a native stack, proved on a real stacked PR or with what stays unproved said.
2. Planned for the next batch, parallel, before the next release. No behaviour question was left
   open by the user; implementation detail is the agents'.

## The route (what the cards say)

GitHub only. GitLab has no native stack (`concepts.md`, "Batch", Stack): `glab mr merge` stays as
it is. The user's own merges (GitHub's page, one action from a stack's top or one PR at a time
from the bottom) do not change.

For every merge the steering session runs on GitHub (a release PR or a fix PR, under the grant,
after `$CHANTIER release go <cr> --note "merge <pr>"` says `go`, exactly as today):

1. **Read the PR's stack first**, one command:
   `gh api -X GET repos/<owner>/<repo>/stacks -F per_page=100`. Find an open stack (`open: true`)
   whose `pull_requests` holds the PR among its open ones (the same reading as `merged_with` in
   `evals/kit/sandbox.py`).
2. **No open stack holds it:** merge as today, `gh pr merge <pr> --<the project's method>
   --match-head-commit <the PR's head SHA>` (head read with `gh pr view <pr> --json headRefOid`).
3. **An open stack holds it and an open PR sits below it in that stack:** do not merge. GitHub's
   asynchronous merge of a stacked PR merges every open PR below it in the same action, and the
   steering session never merges a stack that holds the release (`concepts.md`, "Words", the paragraph
   of "PR in draft": "the steering session merges it only under the grant, and never a stack that
   holds it"). It is a stop: the Foreman sends the Chief of Staff an ask (`[foreman→chief-of-staff]
   release <cr>: PR <pr> is in a stack above open PRs <numbers>; not merged`), in direct mode the
   Chief of Staff tells the user. Nothing is merged.
4. **An open stack holds it and it is the lowest open PR there** (the others below are merged):
   merge through GitHub's asynchronous merge, one command:
   `gh api -X PUT repos/<owner>/<repo>/pulls/<pr>/merge-async -f merge_method=<the project's
   method: rebase, squash or merge> -f merge_action=direct_merge -f sha=<the PR's head SHA>`.
   The answer's `status`:
   - `merged`: the merge is done; go on as after any merge (`order merged`, the fast-forward of
     the main checkout, `foreman.md` "Your means").
   - `pending`: read its result once more after one bounded wait (see "Rule 8" below), with
     `gh api -X GET repos/<owner>/<repo>/pulls/<pr>/merge-async/<the answer's details.uuid>`.
     `merged` then: as above. Still `pending`: no new `PUT`, no further read loop; record
     `$CHANTIER note <cr> "merge: <pr> pending on GitHub's asynchronous merge after <s> s"` and
     ask the Chief of Staff (`[foreman→chief-of-staff] release <cr>: merge of PR <pr> still
     pending on GitHub`); before any later merge attempt, the PR's state is read first
     (`gh pr view <pr> --json state,mergedAt`): a PR already merged is recorded, never merged
     again.
   - anything else (or a refused call): a stop, reported with its exact text (concepts rule 7):
     nothing more, no other route, no `gh pr merge` attempt.

The head SHA in both forms (`--match-head-commit`, `sha=`) is the guard that the merged head is
the one judged: a PR whose head moved after the hand-back is not merged.

### Rule 8

`concepts.md` rule 8 says "No `sleep`, no polling loop", with one named exception (the bounded
wait before a second CI look, `driver.md`, `CI:`). This CR adds a second named exception, written
the same way: after a `PUT .../merge-async` whose answer is `pending`, one bounded wait, once (a
single `sleep` of at most 30 seconds), then one `GET` of the result; never a loop, at most once per
merge. (Open question 1 below.)

## What changes, area by area

### Cards (`skills/chantier/references/`)

- `foreman.md`, the bullet of "A release PR is never yours to merge ... You merge a fix only under
  the grant ... with the forge's CLI by the project's method" (around line 105-110): name the
  route above for GitHub, steps 1 to 4, in a few lines (or point to one place that holds them, for
  instance a short paragraph in "Your means" next to the fast-forward, and refer to it from the
  bullet). The steering session in direct mode is the Chief of Staff: the Chief of Staff's card
  reaches the same text through what it already reads for direct-mode steering; where
  `chief-of-staff.md` speaks of the grant's merge ("auto", around line 1552), it does not repeat
  the commands, only refers to the route.
- `concepts.md`:
  - rule 8: the second named exception ("Rule 8" above);
  - rule 6 ("The Foreman alone merges, and only a release's PR or fix ...") is unchanged; the
    "Release CR" paragraph (grant) is unchanged.
  - The "Words" sentence "the steering session merges it only under the grant, and never a stack
    that holds it" stays; add after it, in a few words, that on GitHub a PR in a native stack is
    merged through the asynchronous merge, which takes every open PR below it, so the steering
    session merges it only when nothing open sits below it.
- `driver.md`, the Release driver's section: unchanged in substance (the Release driver never
  merges; it hands back `ready <pr link>: waits for the merge`); no edit needed unless a sentence
  names `gh pr merge` (none does today).
- `hosts/claude-code.md`, "Capabilities and their commands":
  - row "A release on its own": the commands column names the asynchronous merge (`gh api -X PUT
    repos/<owner>/<repo>/pulls/<pr>/merge-async ...`, its result `gh api -X GET
    .../merge-async/<uuid>`) and the stack read (`gh api -X GET repos/<owner>/<repo>/stacks ...`)
    next to `gh pr merge`; the rules column adds the three rules below; the trial column says the
    asynchronous merge has no harmless form ("no trial, P10's rule check only"); the mark says
    the risk ("any asynchronous merge of any PR `gh` can reach, which merges every open PR below
    it in its stack").
  - row "Fixes on a grant": the same three rules and the same words.
  - "Auto mode", the bullet that lists the commands with no harmless form (`gh release create`,
    `gh pr merge`, `gh pr edit --base`, `SendMessage`): add `gh api -X PUT .../merge-async`.
- `hosts/copilot.md`: no permission table there; nothing to change. The route on a Copilot host is
  **unproved** (say so where the route is written, in one clause).
- `agents/` and `com.github.copilot/agents/`: unchanged (no role's body changes).

### Allow rules (`skills/chantier/scripts/cli/src/chantier/commands/permissions.py`)

Add to `SAMPLES`, for each of the capabilities `release` and `fixes`, forge `github`, after the
`gh pr merge` sample of that capability and in the order of the host card's table (the test
`test_cli_runs.py` compares them):

| Sample command | Rule |
| --- | --- |
| `gh api -X GET repos/o/r/stacks -F per_page=100` | `gh api -X GET repos/*/stacks*` |
| `gh api -X PUT repos/o/r/pulls/12/merge-async -f merge_method=rebase -f merge_action=direct_merge -f sha=<_SHA>` | `gh api -X PUT repos/*/pulls/*/merge-async*` |
| `gh api -X GET repos/o/r/pulls/12/merge-async/<a uuid>` | `gh api -X GET repos/*/pulls/*/merge-async/*` |

(`o/r` and the uuid are realistic placeholders; `_SHA` is the module's constant.) The rules stay
out of `RECOMMENDED_ALLOW` (the pasteable block): like `gh pr merge*`, they are offered only
under a grant (`GRANT_ALLOW`), and P10 names them in its release and fixes warnings. The `gh pr
merge*` rule stays (a PR outside a stack still merges with it).

No other CLI change: the CLI runs no merge and no forge command beyond `forge-stack`
(`concepts.md`, `$CHANTIER`; `AGENTS.md`, the CLI's scope); the steering session runs these
commands itself.

### Docs and eval kit

- `evals/kit/sandbox.py`: unchanged (it already uses the route, PR #224).
- No `docs/` page names `gh pr merge` today; nothing to change there.

## Out of scope

- The user's own merges of a stack, and the stack's one-action merge on GitHub's page.
- GitLab (no native stack; `glab mr merge` unchanged).
- A CLI command that merges (would breach the CLI's scope in `AGENTS.md`).
- Any change to when the steering session may merge (grant, `release go`, "every other CR merged
  or cancelled and its base is the default branch").
- The kit's judge reading a head the forge's restack replaced (run 2's finding 5): another item.

## Evidence

- `just check` green (Linux, macOS, Windows), with:
  - `test_cli_runs.py`'s existing table test (line 245-258) passing on the new samples: each new
    sample matched by its own rule in both forms (`Bash`, `PowerShell`), and the host card's table
    holding exactly `SAMPLES`' rules per capability;
  - the release assertion (line 337) extended: the P10 warning for `--autonomous-releases 1` on a
    GitHub remote names `gh api -X PUT repos/*/pulls/*/merge-async*` next to `gh pr merge*`; and
    the same for `--grant-fixes` (one parametrized test, kept fast, `AGENTS.md`'s test budget);
  - `RECOMMENDED_ALLOW` holds none of the three new rules (asserted next to the existing
    `release create` assertion, line 250).
- `just scenario` (the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head, the
  project's long gate; this CR changes the CLI and the cards): the step at `scenario/run_scenario.py`
  line 792-796 (`preflight --autonomous-releases 1`) also checks the merge-async rule in the P10
  release line.
- The route on GitHub, proof by use:
  - **proved by the kit:** the two calls themselves (`PUT .../merge-async` with `merge_method=rebase`,
    `merge_action=direct_merge`, `sha=`, then `GET .../merge-async/<uuid>` until not pending) merged
    the five stacked PRs of batch-18's real-foreman run 2 (PRs 8, 6, 7, 9, 10 of the eval sandbox,
    one at a time from the bottom, "merged"; audit
    `C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md`, findings 2 and 3),
    run by the operator through `evals/kit/sandbox.py merge`, not by an agent under the host's
    permission check. The PR cites this, with the audit's words, in its Deliverables.
  - **unproved until a real run:** the steering session running the route itself (the host's
    allow rules and auto mode's classifier on `gh api -X PUT ...merge-async`, a granted release
    merge of a release PR in a native stack), and a `pending` answer handled by the bounded wait.
    The PR's Known gaps names it, and the card marks the route **unproved** by an agent until it
    is (the mark the host card already uses), unless open question 2 is answered with a live
    trial.

## Open questions for the user

1. **The bounded wait.** After a `pending` answer, the route allows one bounded wait (at most
   30 s) then one read, as a second named exception to rule 8 ("no `sleep`, no polling loop"),
   and a still-pending merge becomes an ask. Is this exception acceptable, or should a `pending`
   answer go straight to an ask with no wait?
2. **A live proof on a real stacked PR.** The request asks to prove the route on a real stacked
   PR, or say what stays unproved. The kit proved the two API calls (operator, run 2); proving the
   cards' route by an agent means an agent merges a PR. May the batch's Driver (or a Verifier)
   build a two-PR native stack in the eval sandbox (`gsemet/chantier-eval-sandbox`, reset after
   with `sandbox.py reset --yes`) and merge it through the route, on your word given now? With no
   such word, the route ships marked **unproved** by an agent, and the next stack eval with a
   release grant proves it.
