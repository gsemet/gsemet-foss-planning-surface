# Conflicts: rebase of CR-248 onto origin/main

## Commit 1 (feat(cli) ready locally ...): skills/chantier/scripts/cli/src/chantier/commands/batch_status.py, `status()`
- main: `lines = [_batch_line(...), *_autosync_lines(repo)]`, then `last_closed_text` appended, then `_cr_row(d, c, args.notes)`.
- CR-248: `_cr_row(repo, d, c, args.notes)` (takes repo for the draft state), last_closed on the batch line list.
- Choice: main's autosync line and line order, with CR-248's `_cr_row(repo, d, c, ...)` signature. Both intents kept.

## Commit 2 (docs(cards) ...): README.md, table row "it is grilled enough" / "run the P1s"
- main: "it is grilled enough" row adds the spec critic; "run the P1s" row says "a PR handed back ready is mergeable at once".
- CR-248: "run the P1s" row says "a PR ready to merge (out of draft) is mergeable at once, a PR in draft is not".
- Choice: main's "grilled enough" row (spec critic) and CR-248's "run the P1s" row.

## Gate
- `just check` (in the worktree): pass (ruff, mypy, biome, uv lock, 72 pytest, release notes). A ruff format diff on batch_status.py was line-ending only; nothing to commit.
- `just mod`: pass, 57 pass, 0 fail.
- No conflict markers remain. Not pushed; branch has diverged from origin (rebased), so the push needs a force-with-lease via the usual route.
