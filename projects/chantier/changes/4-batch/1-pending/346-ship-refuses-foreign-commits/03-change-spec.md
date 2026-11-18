# Change Specification: ship refuses a main-based PR that carries another CR's commits

## Goal

In batch-24 the user merged PR 297 (CR-337) right after its force push. Its PR was on main and
out of draft, but its head carried CR-336 under it, so CR-336 landed through CR-337's PR and the
partial stack (#299: PR 295 + 296) dissolved with CR-335 still unmerged. Three things change:

1. `ship` refuses to record a PR that is on the default branch, out of draft, and whose head
   carries the commits of another CR of the batch not recorded merged. The CR then cannot be
   handed back ready at that head.
2. The refusal makes putting the PR back to draft the first step, always: draft, then `ship`
   again (which records the PR in draft, so the CR reads "PR in draft" and its earlier ready line
   no longer reads mergeable), then rebase if needed. A refused `ship` itself still records
   nothing.
3. The `stack-ready-to-merge` ask names the one PR to merge, and the Chief of Staff tells the user
   that PR first; while the stack stands, the only other PR of the batch the user is told to merge
   is a CR outside the stack order (a fix CR) whose latest readiness ask names it.

Proof that the refusal would have fired: batch-24's `events.jsonl` holds two `ship` events of
CR-337, at 22:43:02 and 22:47:28, both with base main, draft false and head 5f5bb5a, which carries
CR-336's head 2a514cb (the 22:43:02 carry base); both come before the merge at 22:49:05/07.

Source: `intake/request.md`; decisions: `02-answers.md` (W1 to W8, and S1 to S9 settled after
the spec critic).

## What changes

### 1. CLI: `ship` refuses foreign commits (`skills/chantier/scripts/cli/src/chantier/commands/delivery.py`)

Add a read-only helper in `delivery.py`:

```python
def _foreign_crs(repo: Repo, d: BatchRecord, c: CrEntry, wt: Path, head: str) -> list[CrEntry]:
    """The other CRs of the batch whose commits the head carries: not recorded merged, with a PR
    recorded, whose recorded head or remote branch tip is an ancestor of the head and not of the
    remote default branch. Read-only git."""
```

Rule, for each `o` in `d.crs` with `o.id != c.id`, `o.status != "merged"` and `o.pr` set (a
`cancelled` CR counts too: merging would bring in dropped work):

- candidate refs: `o.head` (when set) and `<remote>/<o.branch>` (when `git rev-parse --verify
  --quiet` reads it), `<remote>` being `repo.config["remote"]`;
- a ref counts when `git merge-base --is-ancestor <ref> <head>` holds and, when
  `<remote>/<default_branch>` can be read, `git merge-base --is-ancestor <ref>
  <remote>/<default_branch>` does not (a ref git cannot read is skipped, never an error);
- `o` is returned when one of its refs counts.

Reuse `carry._ancestor` (import it, or move it to a shared spot in `commands/carry.py`'s public
names) rather than a second `subprocess` call shape.

In `ship`, right after `base, draft, shown = read_state(args.pr)` and **before**
`RenderedBatch` (so nothing is written), when `base == repo.config["default_branch"]` and
`draft is False`:

```python
foreign = _foreign_crs(repo, d, c, wt, head)
if foreign:
    raise ChantierError(
        f"{c.id}: {args.pr} is on {base} and out of draft, but its head {short} carries "
        + ", ".join(f"{o.id} ({o.pr})" for o in foreign)
        + ": merging it would merge them too. First put the PR back to draft and ship again "
        "(it then reads PR in draft); then, if it is to stay on "
        f"{base}, rebase it onto {base} without their commits, push, and ship again. "
        "If " + ", ".join(o.id for o in foreign) + " is already merged on the forge, ship "
        "again once `status` shows it merged",
        EXIT_PRECONDITION,
    )
```

- A failed forge read (`base` or `draft` is `None`) refuses nothing (W2).
- A draft PR is never refused (W3); a PR on another base (a CR's branch) is never refused. So the
  `ship` that follows putting the PR to draft passes and records the draft state.
- `--conflict` does not bypass it (W6).
- Update `ship`'s docstring: it now also refuses that case.

No change to `rails.py` (the check needs git, which `rails.py` does not run), to `handback`
(its existing "the worktree's head … is not the head ship recorded" refusal already holds such a
CR back), to `readiness_key` or to the board.

### 2. Cards (`skills/chantier/references/`)

- `driver.md`, the `$CHANTIER ship` paragraph (around line 315-329): add after the existing
  sentences: "`ship` refuses, and records nothing, a PR on the default branch and out of draft
  whose head carries the head of another CR of the batch not recorded merged and with a PR
  (`… carries CR-x (<link>): merging it would merge them too …`). The first step is always the
  same: put the PR back to draft (`gh pr ready --undo`, `glab mr update --draft`) and `ship`
  again, which records the PR in draft so the CR no longer reads mergeable; then, if the PR is to
  stay on the default branch, rebase it onto it without those commits, push, and `ship` again. If
  the CR named is already merged on the forge, `ship` again once `status` shows it merged. For the
  stack driver it means a PR moved without first going to draft, as the stack driver section
  asks."
- `foreman.md`, the two `stack-ready-to-merge` ask forms (around lines 323-328): insert
  `merge <cr> <link>` right after `mergeable below <sha7>`, naming the highest PR of the mergeable
  part (the PR whose head is `<sha7>`). Written composed with the local-gate clause that
  `1-inbox/partial-stack-ask-windows-gate` adds, the forms are:
  - partial: `stack-ready-to-merge <stack link> partial stack mergeable below <sha7> merge <cr>
    <link> <cr>=<link> gaps: …… [local gate <cr> at <sha7>: passed] to come: <cr> <cr>…`;
  - complete: `stack-ready-to-merge <stack link> mergeable below <sha7> merge <cr> <link>
    <cr>=<link>…`.
  The asks format list near line 405 becomes `… mergeable below <sha7> merge <cr> <link>
  <cr>=<link>[ gaps: …]…[ local gate <cr> at <sha7>: passed|failed|not run] [to come: …]`.
- `chief-of-staff.md`, the stack-batch bullet (around lines 1061-1081): on a
  `stack-ready-to-merge` ask, partial or complete, tell the user first the one PR to merge, by the
  ask's `merge <cr> <link>` (its number and link): on GitHub, merging that PR merges those under it
  in one action; one PR at a time from the bottom stays their choice, as today. Add: tell the user
  that no other PR of the batch is to be merged while the stack stands, except the PR of a CR that
  is not in the stack order (a fix CR) whose latest readiness ask names it; a PR of a draft on top,
  of a CR to come, or of a CR in the stack order handed back on its own is not to be merged; a
  merge they make anyway is recorded as any merge. The GitLab sentence (one MR at a time from the
  bottom up to the MR of the commit named) names that same MR by the `merge` part.

Overlap with the same batch: `1-inbox/partial-stack-ask-windows-gate` edits the same ask forms,
the format list and `chief-of-staff.md` around lines 1062-1068, and
`1-inbox/stack-top-cr-out-of-ask` rewrites the partial ask's "to come:" parenthesis (around line
326). The forms above are the composed target. Whichever CR merges second rebases its edit onto
the other's wording, keeping both clauses.

The Copilot and Claude Code agent files do not change (a role's contract lives in the cards).

### 3. Test (`skills/chantier/scripts/cli/tests/test_carry_ship.py`)

One parametrized test on the existing `stack` fixture: A commits, its remote branch and `main`
set (`remote(...)`), `chantier("ship", A, PR_A)` records A's PR and head (the fixture's
`read_state` returns `("main", False, "")`; A carries nothing foreign); B is rebased onto A's tip.
Then, after A's `ship`, `read_state` is monkeypatched per case and `chantier("ship", B, PR)` runs:

| case | `read_state` | expected |
| --- | --- | --- |
| out of draft on main | `("main", False, "")` | exit `EXIT_PRECONDITION`, stderr names A and its PR, no new `ship` event, B's recorded `pr`/`head` unchanged |
| draft on main | `("main", True, "")` | exit 0, recorded |
| on A's branch | `(A's branch, False, "")` | exit 0, recorded |
| A recorded merged | `("main", False, "")` | exit 0, recorded |

For "A recorded merged", prepare the state by editing the record directly, as the other tests
prepare state by writing the batch's files: set A's `status` to `merged` in the batch record that
`batch_helpers.record` reads, write it back as UTF-8 JSON, then ship B. No `handback` or
`order merged` is run.

The existing first test (B shipped onto A while A has no PR) must still pass unchanged: A has no
PR there. Keep the test in-process and fast (`just test` budget in AGENTS.md).

## Out of scope

- A head that carries only part of another CR's commits, a cherry-pick, or commits of a CR of
  another batch.
- `stack --out-of-draft` and the forge's `gh pr ready` are not checked; the stack driver turns a
  PR ready only after `forge-stack rebuild` and the five checks, as `driver.md` already says.
- Any forge write or retarget by the CLI; any new CLI command; a refusal event in the record.
- A scenario step, the eval scorecard (`evals/SCORECARD.md` C8), the docs pages, the board.
- Changing the stack driver's restack order (it already puts moved PRs to draft).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI); `just test` stays within its budget.
- The new parametrized test above passes, its four cases each asserted.
- `just eval-dry-run` in the worktree (a change under the CLI's `src/`).
- `just scenario (ubuntu-latest)` green at the PR's head (a CLI and cards change), and, as the top
  CR of the batch when it is, `chantier gate` locally per AGENTS.md.
- By reading: the three card edits match this specification word for word in substance; `grep`
  shows `merge <cr> <link>` in both `foreman.md` ask forms and its format list, and in
  `chief-of-staff.md`; the refusal text and `driver.md` both put "draft, then ship" first.
- Forge note: the refusal rests on `read_state`'s draft read, proved on GitHub; on GitLab the
  `draft` field stays unproved, as `driver.md` already says (no new trial owed by this CR).
