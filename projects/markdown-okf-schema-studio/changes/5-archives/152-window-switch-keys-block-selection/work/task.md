# Task T1 — Keyboard block selection after a window switch

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-152` on branch
`change-requests/152-window-switch-keys-block-selection` (from fresh `origin/main`, `node_modules`
symlinked to the main checkout, read-only).

## Definition of done

- Root cause identified (bisect `6df062d3` against `00f40bd1` if needed) and stated in the report.
- A test that fails on the unchanged code (unit or webview where possible, in addition to the
  integration step that already fails), and the heavy integration step passes.
- No weakened or retried assertion; existing paste-URL behaviour (CR 145) keeps its tests green.

## Requirements traceability (mandatory, checked by the reviewer)

- Every behaviour changed has its SwRS requirement updated; a "Known issue" line added if a
  limitation remains. `@implements_req <ID>` at the implementation and `@tests_req <ID>` at each
  test for every touched leaf requirement. `just requirements-update` and a dated entry in the
  bundle's `tiers/log.md`.

## Gates (foreground, in the worktree)

- `just check` with `STUDIO_OKFREQ='env UV_NO_CONFIG=1 uvx --from okf-schema==0.13.0 okfreq'`.
- Heavy CI on the branch: `gh workflow run ci.yml --ref <branch> -f heavy=true` (integration job
  must pass; stress ignored). Real-window suites locally only under `WINDOW-TESTS.lock` with
  `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`.
