# 133 — Read-only previews never expose the home folder or dot-directories

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/security-read-only-root-home`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "pars sur les nouveaux P1/P2" (same autonomous mode as the previous runs). List these in the PR body under "Autonomous decisions".
- Follow the item's expected behaviour. "Home folder" is `os.homedir()` after realpath; roots are `/` and drive roots on Windows.
- The dot-segment rule applies to read-only previews only; trusted workspaces are unchanged.
- Docs (security / trust section) and SwRS updated.
