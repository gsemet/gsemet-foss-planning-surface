## Summary

The extension declares `engines.vscode ^1.95.0`, but the lock file resolves `@types/vscode` to 1.140.0, so a change could call an API added after 1.95 and no check would fail. `just check` now type-checks `src/` against the 1.95 typings as well.

## Deliverables

A new `just check-min-vscode` step, run by `just check` (and so by the CI static job):

```text
tsconfig.vscode-min.json   maps "vscode" -> node_modules/@types/vscode-min (npm:@types/vscode@1.95.0)
package.json               devDependency "@types/vscode-min": "npm:@types/vscode@1.95.0"
                           script check:min-vscode = tsc --noEmit -p tsconfig.vscode-min.json
```

The main build keeps `@types/vscode` 1.140.0. Proof: the step passes on the current `src/`, and fails with TS2339 when `src/extension.ts` uses `vscode.lm.registerMcpServerDefinitionProvider` (an API from 1.101) while the main type-check accepts it; the probe was removed.

## Blast radius

Grade: **1**. Development tooling only; `git revert` restores the previous state.

## Autonomous decisions

- The 1.95 typings come from an exact-pinned npm alias (`@types/vscode-min`) of the existing registry, so the main `@types/vscode` is untouched.
- No requirements (SwRS) entry: this is tooling, not product behaviour.
- `@types/vscode-min` is added to the `--reject` list of `just update` so it is not bumped past the minimum.

## Known gaps

- `just check` stops at an unrelated unit test (`tableBreakout`, "Auto measures a table again on a real resize while a cell is edited") seen failing in one local run; this change touches no `src/`. Not run on the base, so a flake is unconfirmed.

<details>
<summary>Details</summary>

## Changes

- `tsconfig.vscode-min.json` (new), `package.json`, `package-lock.json`, `justfile` (recipe `check-min-vscode`, added to `check`; `update` rejects the alias), `CONTRIBUTING.md` (describes the step and says to raise the alias with `engines.vscode`).

## Impacts

Contributors: a use of an API newer than 1.95 now fails `just check` locally and in CI. No visual or runtime change.

## Test plan

- [ ] New or changed tests: No behaviour change (a tooling check; proven by the failing probe above)
- [ ] Local gates at `<sha7>`: `just check-min-vscode`, `just format` pass
- [ ] Evidence: none, no visible change
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-336 (nothing protects the engines.vscode minimum); archive under `.agents/changes/5-archives/261117-0959-336-check-against-minimum-vscode-types/`.

</details>
