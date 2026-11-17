# `just check` rejects a byte-order mark; the worker cards repeat the rule

## Goal

A UTF-8 byte-order mark (BOM) written by an agent is caught in the round that wrote it, not one
round later at review. Two retros measured the fault: in batch-14, CR-191's round 3 Coder wrote a
BOM into `evals/kit/dry_run.py` on Windows and a whole round existed only to strip it; in
real-direct run 1 (2026-11-12, PR 137) conflict resolutions twice left a BOM in files of the
sandbox. So:

1. In this repository, `just check` is red when a tracked file starts with the UTF-8 BOM, on
   Linux, macOS and Windows, and names every such file in one run.
2. In every project chantier runs in, the worker card repeats the no-BOM rule where the fault
   happens: the Coder's and the Conflict resolver's sections.

The CR has no tracker issue.

## Today

- `skills/chantier/references/concepts.md`, rule 9 (end of the "Rules" section), is the one full
  statement: "Every file you write, a PR body included, is UTF-8 without a byte-order mark (on
  Windows PowerShell 5.1, `Out-File` and `Set-Content -Encoding utf8` add one)."
- `justfile`: `check: test release-notes`; `test` runs `uv run --group dev pytest -q` in
  `skills/chantier/scripts/cli`.
- `skills/chantier/scripts/cli/tests/test_structure.py` has one BOM check, inside
  `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter` (line ~120): an agent file
  of either host must not start with `b"\xef\xbb\xbf"`, with the comment "a BOM hides the
  frontmatter from a host". Any other file passes with a BOM.
- `test_a_byte_order_mark_from_windows_powershell_is_read_through` writes BOMs into files of a
  temporary repository to prove the CLI reads through them. Those files are not tracked by this
  repository; that test is unchanged.
- No tracked file carries a BOM (checked on 2026-11-12: 291 tracked files, 0 with `EF BB BF` at
  the head), so the check can be strict from its first day.

## What changes

### 1. The check, in `tests/test_structure.py`

Add one structure test to `skills/chantier/scripts/cli/tests/test_structure.py` (it then runs in
`just test`, hence in `just check`, on the three systems in CI and in every Driver's fast gate; no
new recipe, no change to the `justfile`):

- **Which files:** every file git tracks in this repository, listed with `git ls-files` run at
  `PLUGIN_ROOT` (the repository's root, from `conftest.py`). Tracked files only: no untracked and
  no ignored file is read. No list of exceptions, no filter by extension: a binary file is read
  the same way (no binary format here starts with those bytes, and an exception list is where the
  next BOM would hide).
- **What is red:** a file whose first three bytes are `EF BB BF`. Nothing else: no UTF-16 or
  UTF-32 mark, no check that the content is valid UTF-8, no line-ending check. Read the first
  three bytes only, so the test stays fast.
- **The message:** one run names every file with a BOM (collect them all, then assert the list is
  empty), and says each must be UTF-8 without a byte-order mark. For example:
  `files with a UTF-8 byte-order mark (write them as UTF-8 without one): evals/kit/dry_run.py, ...`.
- **Portability:** the test uses the standard library and `subprocess` only, like the rest of the
  file; paths from `git ls-files` are joined to `PLUGIN_ROOT` so they resolve on Windows too. A
  tracked path absent from the working tree (deleted, not yet committed) has no bytes to check and
  is not red. A failure of `git ls-files` itself fails the test (no fallback that would pass
  silently).
- **Consequence to know:** a file a Coder creates is untracked until the Driver commits it, so the
  round's fast gate does not see it; the long gate (`$CHANTIER gate` runs on a clean, committed
  tree) and CI do. A file the Coder modifies is tracked and is checked at once.

The existing agent-file check: the Driver chooses to keep it or to drop it in favour of the
general test, provided an agent file with a BOM stays red and the reason (a BOM hides the
frontmatter from a host) stays written in the test file.

### 2. The worker card, `skills/chantier/references/worker.md`

One short line in each of two sections; `concepts.md` rule 9 stays the one full statement and is
not changed.

- **`## Coder`:** never add a byte-order mark to a file: on Windows PowerShell 5.1, `Out-File`
  and `Set-Content -Encoding utf8` add one ([concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), rule 9). A file of the
  project that already has a BOM keeps it: the rule is "add none", not "strip all".
- **`## Conflict resolver`:** the same rule, plus a check before the rebase continues: each
  resolved file starts as it did before the conflict (the base's encoding, so no new BOM, and a
  BOM the file already had is kept) before `git rebase --continue`.

Wording is the Driver's, in the card's style (short sentences, no host tool named beyond the
PowerShell cmdlets already named in rule 9; `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`
must stay green).

Nothing else changes: no agent file (`agents/`, `com.github.copilot/agents/`), no other card, no
CLI code.

## Decisions carried from `02-answers.md`

| Question | Decision |
| --- | --- |
| Which files does the gate check? | Every tracked file, no exceptions; red when its first three bytes are the UTF-8 BOM. |
| Untracked or ignored files? | No: tracked files only. |
| Part of `just check` or a separate recipe? | Part of `just check` (via the structure tests), on the three systems; it stays fast. |
| What does a red result say? | Every file with a BOM, in one run, and that it must be UTF-8 without a byte-order mark. |
| UTF-16, UTF-32, invalid UTF-8? | No: the UTF-8 BOM only. |
| Does the CLI (`gate`, `ship`) refuse a BOM in a user's project? | No: a project's own gate decides; the cards carry the rule. |
| Which cards repeat the rule? | `worker.md`, Coder and Conflict resolver sections, one short line each, with the Windows cause and a pointer to `concepts.md` rule 9. |
| A user's file that already has a BOM? | Left as found: "add none", not "strip all"; a resolved conflict or an edit keeps the base's encoding. |
| Does the Conflict resolver check before continuing? | Yes: a resolved file starts as it did before the conflict, before the rebase continues. |
| The existing agent-file BOM test? | The Driver's choice, as long as an agent file with a BOM stays red and its reason stays written. |
| Which gates? | `just check` and `just scenario`; no `just mod`. |

## Out of scope

- A CLI refusal of a BOM (`gate`, `ship`, or any other command) in a user's project.
- UTF-16 and UTF-32 marks, UTF-8 validity, line endings, any other content check.
- Stripping BOMs from existing files, here or in a user's project.
- The agent files of either host, and every card other than `worker.md`; `concepts.md` rule 9
  is not edited.
- Untracked and ignored files.

## Evidence

Each run at the pushed head, with its output:

1. `just check` passes on Linux, macOS and Windows (CI), with the new test collected and green.
2. The test is red on a BOM, and names every file: in the worktree, prepend `EF BB BF` to two
   tracked files (for example `README.md` and `evals/kit/dry_run.py`, with a byte write, not an
   editor), run `just test`, keep the output showing the new test failed and naming both files and
   the "UTF-8 without a byte-order mark" text; then restore both files (`git checkout -- <path>`)
   and show `just test` green again. Keep the red output as evidence in the CR's `evidence/`.
3. An agent file with a BOM is still red (whichever test holds the check after the Driver's
   choice): same technique on `agents/coder.md`, output kept.
4. An untracked file with a BOM is not red: create one untracked file with a BOM, run `just test`
   green, delete it.
5. `just scenario` passes (the CR changes a card).
6. The diff of `skills/chantier/references/worker.md` shows the line in `## Coder` and the line
   in `## Conflict resolver` (with the check before the rebase continues), and no other card or
   agent file in the diff.

## Open questions

None.
