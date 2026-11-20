# retro v0.14.0: just tag refuses in the main checkout still on the previous version

From CR-388's release Driver retro (2026-11-19). After the user merged the version PR #356, the
main checkout was still at v0.13.0: `just tag`'s check-tag reads the local version and refused,
so the Driver ran it from the release worktree instead.

Change: make check-tag read the version at `origin/main` (after a fetch), or have the release
procedure fast-forward the main checkout before `just tag`, so the step runs from the main
checkout as CONTRIBUTING.md "Release" says.
