# Make two flaky tests deterministic

## Goal
`just check` stops failing at random on `test_the_refusals_of_several_boards[only-two|only-one]`
and on `test_w2_a_shell_inside_the_folder_refuses_then_lets_go`, so `main` is green for v0.15.0.

## Behaviour
- `chantier live --once` with `--only <id>` that no board serves always exits 2 (usage) with the
  `--only` sentence once every board has given its first answer, whatever the order in which the
  reader threads finish. Never exit 0 with a printed screen in that case.
- The cause of `test_w2_...` is found and removed in the code or the test (no sleep added to
  hide it, no retry, no skip).

## Out of scope
Any other behaviour of `live` or of the folder lock; any other test.

## Evidence
- The race shown: a test or a forced interleaving that failed before the fix and passes after
  (for `live`: make the main loop see the last model complete before the reader's error is
  appended).
- `just check` green on Linux, macOS and Windows at the PR's head; the two tests run 50 times in
  a loop locally with no failure (`pytest --count` or a shell loop), output quoted in the PR.
