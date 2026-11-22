# Conflicts: rebase of 280c01d onto origin/main (56f753e6)

One conflicted file: skills/chantier/scripts/cli/tests/test_launch_modes.py (one hunk, both sides appended at the end of the file).

- HEAD side (main): `_flat`, the sync phrase tuples and two tests (the four skills' checked sync; the cards and hosts' exception).
- CR side: the parametrized test `test_the_cards_tell_the_chief_of_staff_to_pass_on_a_foreign_build`.
- Choice: keep both, main's block first, then the CR's test, two blank lines between. No marker left, no BOM (file still starts with `"""`).

Rebase finished: branch is 1 commit ahead of origin/main. Nothing pushed.

Fast gate: `just check` in the worktree: 1744 passed, 20 skipped; release-notes check ok.
