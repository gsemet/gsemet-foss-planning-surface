# `ship` always reads the PR's base and draft state from the forge

## Goal

The record must not drift from the forge. In batch-18, `ship` recorded "base main" for PRs
stacked by hand on another branch (CR-264, CR-266), and CR-266's record kept a stale base and
"PR in draft, waits on cr-265" while the forge had the PR ready on another branch. It recurs from
batch-17. Today `ship` reads the forge's base only for a CR of a recorded stack (CR-264's
`is_stacked` condition), takes the draft state from the Driver's `--draft` flag, and the words
the record derives (`ready to merge`, `PR in draft … waits for …`) use a base computed from the
record, never the forge's.

After this CR, `ship` reads, for every CR it records a PR or MR for, in every batch mode, both
the PR's base and its draft state from the forge, in one read, on GitHub (`gh`) and GitLab
(`glab`) alike, and records both on the CR. The ready word and what a PR in draft waits for read
the recorded forge base. A Driver runs `ship` after any change of base or draft on the forge, so
the record follows the forge.

## Decisions carried from `02-answers.md`

1. Source: batch-18's retro, kept by the retro critic and by a Fable review; the request's fix
   is the user's choice. It joins batch-18, switched to a stack.
2. Generality: the change works the same on both hosts (Claude Code, GitHub Copilot) and both
   forges (GitHub, GitLab). A path not proved on Copilot or on a real GitLab carries the mark
   "unproved" in its card line (see "Cards" below).
3. Place in the stack: third, before the early-conflict CR (stacking on a conflict needs true
   bases).
4. A forge read that fails keeps the existing `base ? (not read from <link>: <why>)` line; no
   retry, no fallback.
5. `ship --draft` goes: the forge is the only source of the draft state.
6. `ship` records the forge's base on the CR, and `ready_word` and `draft_waits` read it: the
   stale "waits on cr-265" text is the drift the retro named.
7. A failed read prints `draft not read` in place of the draft state.

## What changes

### Record: a new CR field

File: `skills/chantier/scripts/cli/src/chantier/core/records.py`, class `CrEntry`.

- Add `pr_base: str | None = None`, beside `pr_draft`, with the comment "the PR's base branch
  on the forge, as `ship` last read it; None when never read or the last read failed".
- Old records load unchanged (the default is None): they read as today until their next `ship`.
- `rails_release.py` `release_merged` (line 33 today), which clears `pr=None` for the next
  attempt, clears `pr_base=None` and `pr_draft=None` with it, so the next PR starts unread.
- The field lives in `batch.json` only. No `STATUS.json` field is added or renamed, and no
  `types/` or `hooks/` file changes (`pr_draft` itself is not in either today).

### CLI: `forge_base.py`

File: `skills/chantier/scripts/cli/src/chantier/commands/forge_base.py`.

- `pr_base(link)` becomes a read of both fields from the same single API call it makes today
  (no second call): the base and the draft state. Rename it (for instance `pr_state`) if the
  old name would mislead; the Driver chooses.
  - GitHub: `gh api -X GET repos/<owner>/<name>/pulls/<n>`; base `["base"]["ref"]`, draft
    `["draft"]` (a boolean in GitHub's documented REST answer).
  - GitLab: `glab api projects/<path>/merge_requests/<iid>`; base `["target_branch"]`, draft
    `["draft"]` (GitLab's documented field; unproved on a real instance, see "Proof only a real
    run gives").
  - A missing or non-boolean draft field is a failed read (the `KeyError` / `TypeError` path
    `read_base` already catches), never a guess.
- `read_base(link)` returns the base and the draft state on success, and on failure `None` for
  both plus the unchanged `UNREAD` text: `base ? (not read from {link}: {why})`. One read, no
  retry.
- `is_stacked` and `stacked_read` stay, for `take` and `handoff` (`facts.py` `_base_of`), which
  this CR does not change (see "Out of scope").

### CLI: `ship` in `delivery.py`

File: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py`, function `ship`.

- Drop the `if is_stacked(d, c):` condition (line 144 today): `ship` always reads the forge for
  the link it records (`args.pr`), whatever the batch mode (parallel, series, stack), whether or
  not the CR is in a recorded stack, a release CR and a fix CR included. The unused `is_stacked`
  import goes.
- On a successful read:
  - the CR records `pr_base=<the forge's base>` and `pr_draft=<True|False>`;
  - the `ship` event logs `base` (the forge's base) and `draft` (the forge's state);
  - the line prints `recorded <link> (base <branch>, head <sha7>, draft|out of draft)`, as today.
- On a failed read (the forge refuses, `gh` / `glab` missing from PATH, a link of neither
  shape, a field missing):
  - the line keeps today's form for the base: `recorded <link> (base ? (not read from <link>:
    <why>), head <sha7>, draft not read)`, exit 0;
  - the CR records `pr_base=None` and `pr_draft=None` (a stale value read earlier is cleared, never
    kept); the event logs `base` `""` (as today for a stacked CR) and `draft` `null`;
  - `ready_word` already reads a PR with no recorded draft state as `PR in draft` ("never ahead of
    the forge"), so the record never leads the forge;
  - no retry, and no fallback: no flag of the Driver stands in for what the forge did not answer.
- The rest of `ship` is unchanged: the link check (`://`), the head, the `off:` lines (dirty
  tree, head not pushed, no long gate passed, archive missing, stale PR-body SHAs), the lock. The
  forge read stays outside the `RenderedBatch` lock, as today.

### CLI: `ship --draft` goes

Files: `skills/chantier/scripts/cli/src/chantier/declare/delivery.py` (the `ship` command's
arguments) and `delivery.py` `ship` (`draft = bool(args.draft)`).

- Remove `--draft` from `ship`; argparse refuses it as an unknown argument (exit 2), nothing
  recorded.
- The `ship` command's help line becomes "record the PR the Driver opened or updated, with its
  base and draft state read from the forge; say what is off".
- The `--draft` and `--out-of-draft` options of `stack` (the stack driver's record of a PR turned
  ready or back to a draft) are not touched.

### CLI: the derived words read the recorded forge base

File: `skills/chantier/scripts/cli/src/chantier/stacks.py`.

- A helper, for instance `pr_base_of(d, c, repo)`: the CR's `pr_base` when recorded, else
  `stack_base(d, c, repo)`. `stack_base` and `start_base` themselves are not changed: they say
  where a CR's branch starts and where the stack driver places a PR, which `take`, `handoff`,
  `stack` and the long gate queue read.
  - With `pr_base` None (no PR shipped yet, a record from before this CR, or the last read
    failed) the words read as they do today. That is today's rule for a PR whose base is not
    known, not a stand-in for a read: after a failed read `pr_draft` is None too, so the CR
    already reads `PR in draft` and never leads the forge.
- `ready_word`, the CR outside the chain (parallel, series, a fix): `READY_TO_MERGE` when the PR
  is out of draft and `pr_base_of(...)` is the default branch; else `PR in draft`. A PR stacked by
  hand on another CR's branch in a parallel batch therefore reads `PR in draft`, even once out of
  draft on the forge, as long as its forge base is not the default branch.
- `ready_word`, a CR in the chain: unchanged (out of draft, and every CR under it in the chain
  out of draft). It is the stricter rule and cannot lead the forge.
- `draft_waits`:
  1. When `pr_base` is recorded and is not the default branch: the CR whose branch is that
     base, when that CR is not out of draft (by `_out_of_draft`), is what the PR waits for. This
     is CR-266's case: it names the CR the forge stacks it on, not the record's planned
     neighbour.
  2. Else, for a CR in the chain: the CR under it in the chain not yet out of draft, as today.
  3. Else, the CR whose branch is `pr_base_of(...)` when that is not the default branch (or the
     branch name when no CR has it), as today with `stack_base`.
  4. Else `its turn out of draft`.
- `skills/chantier/scripts/cli/src/chantier/status/words.py` `notify` (line 154 today): the
  `PR in draft: <pr> on <base>` text reads `pr_base_of(...)` in place of `stack_base(...)`.
- `skills/chantier/scripts/cli/src/chantier/commands/driver.py` `_ready_lines` (line 233 today):
  the `it waits on <base>` / `the release PR <pr> waits on <base>` text reads `pr_base_of(...)`.
- Every reader of `ready_word` / `draft_waits` (`status/views.py`, `status/words.py`
  `state_label`, `board/crs.py`, `commands/driver.py`) follows with no change of its own.

### Scenario fakes

- `scenario/fake_gh.py`: the single-pull GET (`repos/<o>/<r>/pulls/<n>`) answers a `draft`
  field too, from the state's `drafts` list (the list the stacks branch already reads): `{"number":
  n, "base": {"ref": …}, "draft": n in drafts}`. Whether `pr create --draft` adds the new number
  to `drafts`, or every scripted PR starts out of draft, is the Driver's choice, as long as each
  check below holds. A helper beside `forge_base(w, link, base)` in `run_scenario.py`, for instance
  `forge_draft(w, link, draft)`, sets a PR's or MR's draft state on the fake forge.
- `scenario/fake_glab.py`: the MR GET already answers `draft` from `mrs[iid]`; `forge_draft` sets
  `mrs[iid]["draft"]`. `pull_read_refused` already covers both fakes.

### Cards

All in `skills/chantier/references/` (one copy, read on both hosts; no file under `agents/` or
`com.github.copilot/agents/` changes).

- `driver.md`, the `ship` bullet (lines 267-276 today): `$CHANTIER ship <cr> <pr link>`, with
  `[--draft]` and its parenthesis replaced by: the CLI reads the PR's base and draft state from
  the forge and records them; a failed read prints `base ? (not read from <link>: …)` and `draft
  not read`, and the CR reads `PR in draft` until a `ship` reads the forge.
- `driver.md`, one new line, in or right after that bullet: "Any change of a PR's base or draft
  state on the forge (`gh pr ready`, `gh pr ready --undo`, `glab mr update --ready`, `glab mr
  update --draft`, a retarget) is followed by `ship <cr> <link>`, so the record follows the forge
  (GitLab's `draft` field unproved on a real instance; trial: one `ship` of a draft MR and of a
  ready MR on a GitLab project, the recorded draft state matching the forge; on GitHub Copilot
  unproved; trial: one Driver on Copilot that turns its PR ready and runs `ship`, the CR reading
  `ready to merge`)."
- `driver.md`, the other uses of `ship --draft`:
  - line 205: `ship <cr> <link> --draft` becomes `ship <cr> <link>`;
  - line 208: "then `ship` without `--draft`" becomes "then `ship`";
  - lines 406-407: "runs `ship <cr> <link>` again without `--draft` (a PR turned back to a draft is
    shipped again with `--draft`)" becomes "runs `ship <cr> <link>` again (as after any change of
    draft state)";
  - line 610: `ship --draft` becomes `ship`.
- `concepts.md`, "Ready to merge" (line 13): "the CLI records it: `ship` without `--draft`,
  `stack --out-of-draft`, never ahead of the forge) and, in a stack batch, …; outside a stack its
  PR's base is the default branch" becomes "the CLI records it: `ship` reads it from the forge,
  `stack --out-of-draft`, never ahead of the forge) and, in a stack batch, …; outside a stack its
  PR's base on the forge, as `ship` last read it, is the default branch".
- `concepts.md`, "PR in draft" (line 24 onward): what it waits for names, first, the CR whose
  branch its PR's base is on the forge, as `ship` last read it.
- The CLI's messages carry no role name; the cards carry the roles.

### Docs

- `scenario/README.md` line 155: "`ship` and `ship --draft`" becomes "`ship` reading the draft
  state from the forge"; the line on section 13b (`take`, `handoff` and `ship` print a stacked
  CR's base) says `ship` reads and records every CR's base, `take` and `handoff` a stacked CR's.

## Out of scope

- `take` and `handoff` (`facts.py` `_base_of`, `stacked_read`): they keep reading the forge only
  for a stacked CR with a PR; a CR of a parallel or series batch still prints the base it starts
  on, with no forge call. They do not read `pr_base`.
- `stack_base`, `start_base`, the `stack` command, `forge-stack` and the long gate queue: they
  keep the record's plan. A stack driver's retarget is followed by `ship` (the card already says
  so, lines 780 and 803), which records the new forge base.
- `stack --out-of-draft` / `stack --draft`, and every forge write: the CLI keeps no forge write;
  `ship` stays read-only toward the forge.
- No retry, no cache, no second call for the draft field.
- No new `STATUS.json` field, and no change to the pane's code (`hooks/register.tsx`) or to the
  fields of `status.py` it shows: only where the values of `readiness` and the label come from
  changes, for a CR whose forge base differs from the record's plan. So no `just mod`, and no
  pane screenshot.

## Evidence

Checks before the hand-back: `just check` (Linux, macOS, Windows via CI), and `just scenario`
(a CLI, card and scenario change), on both forges as the scenario runs them (`ARGS.forge`
`github` and `gitlab`).

Scenario steps, in `scenario/run_scenario.py`:

1. Section 13b (`base_from_pr`, around lines 4149-4223), the stacked case: the existing checks
   still pass (one read, the CR below's branch printed and in the event). Add: the CR's `pr_base`
   is that branch.
2. Same section, the refused read: the existing check (`base ? (not read from <link>: …)`, exit
   0, the event's `base` empty) still passes. Add: the line says `draft not read`; `pr_base` and
   `pr_draft` are `None` after having held values from the previous `ship`; the CR, handed back
   ready, reads `PR in draft`.
3. Same section, its parallel-batch tail: the check "a CR of a parallel batch with a PR makes no
   forge read: `handoff` and `ship` print the record's base" becomes: `handoff` makes no forge
   read and prints `base origin/main`; `ship` makes exactly one read, prints `(base main, head …`
   and records `pr_base` `main`. The section title becomes "`take` and `handoff` print a stacked
   CR's base, `ship` reads and records any CR's base, as its PR has it on the forge".
4. New, in that section (the batch-18 case), a parallel batch with two CRs `p` and `q`, both
   with a PR: the fake forge puts `q`'s PR on `p`'s branch and marks it out of draft; `ship q`
   prints `(base <p's branch>, head …, out of draft)`, records `pr_base` `<p's branch>` and
   `pr_draft` `False`, and the event's `base` is that branch. With `p` a draft on the forge (and
   shipped), `q` handed back ready reads `PR in draft` (not `ready to merge`: its forge base is
   not the default branch), its hand-back line says it waits on `<p's branch>`, and its STATUS
   label and `notify` text name `p` as what it waits for and `<p's branch>` as its base. The
   forge then puts `q` on `main`; `ship q` records `pr_base` `main`, and `q` reads `ready to
   merge`.
5. New, a stack batch `a`, `b`, `c` (it can reuse section 13b "Ready locally, PR in draft, ready
   to merge", `ready_words`): the fake forge puts `c`'s PR on `a`'s branch (not `b`'s, the chain's
   neighbour); with `a` and `b` drafts, `ship c` and `c` handed back ready: `draft_waits` names
   `a` (the CR its forge base is on), not `b`. With `a` out of draft and `b` still a draft,
   `draft_waits` names `b` (the chain's rule), and `c` reads `PR in draft` (the chain's
   `ready_word` is unchanged).
6. Section `ready_words`, step 1 (line 5715 today) becomes "`ship` records the draft state the
   forge holds": the fake forge holds `b`'s PR as a draft, `ship` with no flag records `pr_draft`
   `True` and prints `draft)`; `a` and `c`, out of draft on the forge, record `False`. Add: the
   forge turns `b` ready, `ship` records `False` and prints `out of draft`; the forge turns it back
   to a draft, `ship` records `True`.
7. `ship <cr> <link> --draft` exits 2 (argparse refuses the unknown option) and records nothing.
8. A release whose PR is merged (`release_merged`) leaves `pr_base` and `pr_draft` `None` with
   `pr` cleared.
9. Every other `ship` call of the scenario (sections 3, 12b-12f, 13, 14, 14d, 22, and the release
   ship at line 5822 today, whose `--draft` goes, its forge PR held as a draft instead) passes with
   the forge read. A link of neither shape (`https://example.invalid/pr/0`, sections 18b and 19)
   now prints `base ? (not read from …)` and `draft not read`; the checks there look at the `off:`
   lines only and still pass, and those steps are left as is.
10. Section 22 (GitLab path): `ship` of the MR records `pr_base` `main` and `pr_draft` from the
    fake glab's `draft` field; the check "only the Driver called the forge, to create the merge
    request: nobody merged or edited it" still holds (a GET is no edit).

No test in `tests/` is required: the change is no refusal. If the Driver adds one, it stays
in-process, parametrized over the two forges, and within the 30 s budget.

## Proof only a real run gives

- GitLab's `draft` field on a real instance (the fake glab serves the documented name).
- A Driver on GitHub Copilot following the new card line.

Both carry "unproved" with a trial in the card line, as decision 2 asks.

## Open questions

None: points 1 to 3 of the first draft are answered in `02-answers.md` (decisions 5 to 7 above).
