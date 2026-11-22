# Conflicts, CR-437 rebase

Command: `git -C <worktree> rebase --onto origin/main c5af034b` (origin/main 0e36d1f8), carrying e21be689 only.
Result head: 3b3f4b1e (amended once, see below), plus one uncommitted edit (startup-core.md).

## Conflicted hunks (one file)

`skills/chantier/references/hosts/claude-code.md`, the "Every batch" row of the allow-rules table.
- main's side: the force-push route with `git [-C <checkout>] push --force-with-lease=<branch>:<sha> ...`, the `git -C * push --force-with-lease=chantier/*` rule, and "a refusal climbs the ladder of `foreman.md`".
- CR-437's side: "after the steering session's checked sync, which waits for holders", the extra rule `uv sync --locked --check --project "<checkout>"`.
- Choice: main's row kept whole; CR-437's two changes applied on top (the sync wording and the `--check` rule). No other row touched.
- Slip: the first edit failed on CRLF line endings and `rebase --continue` committed the markers; I removed them and amended the (unpushed) commit. The file keeps CRLF.

## Post-rebase fix (not a conflict)

The startup byte budget test failed by 6 bytes (chief-of-staff, copilot, reload: 12550 > 12544) because main's growth plus CR-437's added paragraph in `startup-core.md`. Tightened CR-437's added sentence there by 11 bytes (wording only). This edit is uncommitted in the worktree (I never commit).

## Fast gate

Command: `just check`. Result: lint, format passed; `just test`: 1649 passed, 20 skipped, 1 failed:
`test_triage_moves.py::test_w2_a_shell_inside_the_folder_refuses_then_lets_go` (Windows-only, expects a 1 s hold refusal). It passes alone and with its whole module (9 passed); it fails only in the full run on this machine, twice in a row. CR-437 touches nothing near it (triage, store); likely load timing, not verified on main.
