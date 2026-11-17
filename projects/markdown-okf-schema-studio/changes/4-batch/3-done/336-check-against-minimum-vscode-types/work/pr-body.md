## Summary

The extension declares `engines.vscode ^1.95.0`, but the lock file resolves `@types/vscode` to 1.140.0, so a change could call an API added after 1.95 and no check would fail. `just check` now type-checks `src/` against the 1.95 typings as well.

## Deliverables

A new `just check-min-vscode` step, run by `just check` (and so by the CI static job):

```text
tsconfig.vscode-min.json   maps "vscode" -> node_modules/@types/vscode-min (npm:@types/vscode@1.95.0)
package.json               devDependency "@types/vscode-min": "npm:@types/vscode@1.95.0"
                           script check:min-vscode = tsc --noEmit -p tsconfig.vscode-min.json
```

Why an alias: the main build needs the newer `@types/vscode` (1.140.0), which stays as is, while the check needs the 1.95 typings at the same time. npm cannot install two versions under one package name, so the 1.95 typings are installed under a second name, `@types/vscode-min`, as an exact-pinned alias of the same registry package. The two sit side by side in `node_modules/@types/`, and only `tsconfig.vscode-min.json` points `vscode` at the alias.

The main build keeps `@types/vscode` 1.140.0. Proof: the step passes on the current `src/`, and fails with TS2339 when `src/extension.ts` uses `vscode.lm.registerMcpServerDefinitionProvider` (an API from 1.101) while the main type-check accepts it; the probe was removed.

## Blast radius

Grade: **1**. Development tooling only; `git revert` restores the previous state.

## Autonomous decisions

- The 1.95 typings come from an exact-pinned npm alias (`@types/vscode-min`) of the existing registry, so the main `@types/vscode` is untouched.
- No requirements (SwRS) entry: this is tooling, not product behaviour.
- `@types/vscode-min` is added to the `--reject` list of `just update` so it is not bumped past the minimum.

## Known gaps

- The unit test `tableBreakout` ("Auto measures a table again on a real resize while a cell is edited", `test/page/tableBreakout.test.ts`) fails on Windows, identically on the base commit, so not because of this change; the long gate was not run locally and Linux CI is the check. A follow-up change request covers it.

<details>
<summary>Details</summary>

## Changes

- `tsconfig.vscode-min.json` (new), `package.json`, `package-lock.json`, `justfile` (recipe `check-min-vscode`, added to `check`; `update` rejects the alias), `CONTRIBUTING.md` (describes the step and says to raise the alias with `engines.vscode`).

## Impacts

Contributors: a use of an API newer than 1.95 now fails `just check` locally and in CI. No visual or runtime change.

## Test plan

- [x] New or changed tests: No behaviour change (a tooling check; proven by the failing probe above)
- [x] Local gates at `5f828f0`: `just check-min-vscode`, `just format` pass
- [x] Evidence: none, no visible change
- [x] Review: approved at `5f828f0`
- [x] Verified at `5f828f0`
- [x] CI green at `5f828f0` (static, static-windows, visual)

## Internal references

- CR-336 (nothing protects the engines.vscode minimum); follow-up CR-339 (Windows `tableBreakout` failure). The archive is not in this PR (`.agents/changes/` is not in git).

</details>
