---
type: change-spec
description: A working CR taken on top of a ready stack stays out of the stack's ask until the stack driver places it; take's base rule (nearest earlier CR with a PR) stands.
---

# A CR taken on top of a ready stack stays out of its ask

## Goal

From batch-24's retro (the user's word, 2026-11-18: "file all six and run them in batch-24"):
CR-342, CR-343 and CR-344 were all taken on CR-341's branch; CR-342's draft PR, on its place
but never placed by the stack driver, made `forge-stack show` fail check 2 (`missing #304`), so
the partial-stack ask for CR-338..341 waited until the Foreman reordered the record. The change:
a CR taken on top of a ready stack is kept out of that stack's ask until the stack driver places
it after it gets its PR. Its base stays the one the user set in CR-333: the nearest earlier CR of
the batch that already has a PR (`02-answers.md`, "Settled by the Chief of Staff (after the spec
critic)", A).

## What changes

### CLI (`skills/chantier/scripts/cli/src/chantier/`)

1. **`stacks.py`, a new predicate `to_come(d, c, repo) -> bool`:** true when `c` is not in the
   stack as it stands: it has no PR, or `off_place(d, c, repo)` is not None, or
   `c.status == "working" and not c.stacked` (a working CR whose PR the stack driver has not
   named in `stack <cr>…` yet). Its docstring says so in these words.
2. **`commands/forge_stack.py`, `_plan`:** the loop breaks on `to_come(data, c, repo)` instead
   of `not c.pr or off_place(data, c, repo)`; the docstring's "or a working one off its place"
   becomes "or a working one off its place or not placed by the stack driver yet". `show`,
   `create` and `rebuild` (GitHub and GitLab, which share `_plan`) so list that CR under
   `to come:`, never among the rows: check 2 does not name it as missing, and `create`/`rebuild`
   do not retarget or stack its PR.
3. **`commands/forge_stack.py`, `_no_bottom`:** when the first CR of the chain has a PR on its
   place but is working and not placed, the refusal reads `no PR placed at the bottom of the
   stack: <cr> is working and the stack driver has not placed its PR <link> yet`
   (`EXIT_PRECONDITION`), instead of the wrong `<cr> is working, no PR`.

No new command, flag or record field; one new refusal text in `_no_bottom` (item 3). `take`,
`stack`, `start_on_for`, the `start_on` record field, the `status` lines and the five checks
keep their behaviour and wording.

### Cards (`skills/chantier/references/`)

- **`concepts.md`, "Stack as it stands":** the parenthesis becomes "(a working CR whose PR is on
  another base than its place is to come until its Driver rebases; a working CR the stack driver
  has not placed yet is to come until a stack driver names it in `stack`)". "To come": "the open
  CRs of the stack with no PR yet, and those the stack as it stands leaves out". The base rule
  ("Stack", lines ~212-215, and "Dependencies", line ~313: the nearest earlier CR of the batch
  that has a PR; a branch with no PR is never a base) is unchanged.
- **`foreman.md`, the partial ask (line ~326):** "to come: the drafts on top and the CRs with no
  PR" becomes "to come: the drafts on top (the rows not ready to merge) and the CRs of
  `forge-stack show`'s `to come:` line (no PR yet, or working and not placed yet)". This CR edits
  only that "to come:" gloss in the bullet (lines ~323-326);
  `1-inbox/partial-stack-ask-windows-gate` rewrites the same bullet's form in the same batch: if
  that CR lands first, this CR rebases onto its form and keeps only the gloss change. The first
  take (line ~276) is unchanged. No new rule for the Foreman: a working CR's first PR already
  makes a later `take stack` due.
- **`driver.md`, the five checks (line ~872):** the parenthesis "drafts on top and the `to come:`
  line are no failure" adds "(a working CR not placed yet is in `to come:`)". The base rule
  (lines ~733-736) and the Ordering rule are unchanged.

Both hosts' agent files are untouched (the contract stays in the cards).

### Tests and scenario

- **`skills/chantier/scripts/cli/tests/test_stack_due.py`** (the existing test file of
  `stacks.py`; no new file): one parametrized test of `to_come` on a `BatchRecord` (repo
  stand-in: `cast(Repo, SimpleNamespace(config={"default_branch": "main"}))`), in-process, no
  git, no forge: no PR → true; working, PR on its place, `stacked` false → true; same with
  `stacked` true → false; ready, PR, `stacked` false → false; working, `stacked` true, `pr_base`
  off its place → true.
- **`scenario/run_scenario.py`:** in the GitHub `forge-stack` section, next to the check at
  ~line 5605 ("a working CR whose PR is not on its place…"), one check: a CR added by
  `order add`, `working` with a draft PR on its place and not named in `stack` → `forge-stack
  show` exits 0, its `to come:` line names it `working`, no `check 2` line names its PR. 13-bis
  (`stack_start_base`, ~line 5201) is unchanged. Any other scenario check that relied on a
  never-placed working CR being a row is updated to name it under `to come:`.
- **`scenario/README.md`:** the `forge-stack` paragraph (lines ~191-193, "`drafts on top`, `to
  come:`") adds the case "a working CR with a PR the stack driver has not placed, under `to
  come:`". Line ~155 (the start base) is unchanged.

## Out of scope

- `take`'s start base: it stays the nearest earlier CR with a PR (CR-333's rule); a CR whose
  worktree exists but has no PR is not a base.
- The conflicts of a final-order restack between CRs touching the same files.
- A `ready` CR not placed yet (the Foreman's next `take stack` places it before any ask).
- Holding a take until the CR before it has its worktree or its PR; the stack's order rules.

## Evidence

- `just check` (includes `just test`, within its time budget) and `just eval-dry-run` in the
  worktree, at the pushed head (a change under the CLI's `src/`).
- `just scenario (ubuntu-latest)` green at the PR's head (CLI and cards changed); the new
  scenario check passes and 13-bis still passes.
- The new unit test cases above, each named in the PR's Test plan.
