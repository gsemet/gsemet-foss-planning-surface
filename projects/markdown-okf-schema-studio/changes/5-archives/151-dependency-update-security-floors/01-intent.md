# Update every dependency, with minimum-version floors for security fixes

Type: chore · Priority: P1 · Requested 2026-10-27 by the user

## Intent (user, translated)

"There are many vulnerabilities on Dependabot; I suppose we need a dependency update with
minimum-version guards. Add a CR that updates all dependencies, in the stack."

## Open Dependabot alerts (checked 2026-10-27 23:45 with `gh api …/dependabot/alerts`)

| Repository | Severity | Package | Manifest | First patched |
| --- | --- | --- | --- | --- |
| this repository | high | `@azure/msal-node` (dev, transitive via `@vscode/vsce`) 6.0.1 | `package-lock.json` | 7.1.0 |
| gsemet/okf-schema (not this repository) | 2 high, 1 medium | `urllib3` | `uv.lock` | 2.8.0 |
| gsemet/okf-schema (not this repository) | 2 medium | `soupsieve` | `uv.lock` | 2.9.0 |

This repository's `uv.lock` already has `urllib3` 2.8.0. The okf-schema alerts are handled in that
repository, outside this stack.

## Expected

- **npm**: update every direct dependency and dev dependency to its latest version compatible with
  the code (`npm outdated` before/after in the PR). Major upgrades are allowed when the code and
  the tests follow; a major that needs real work is left out and listed with its reason.
  `package-lock.json` regenerated.
- **Python** (`pyproject.toml` / `uv.lock`, use `UV_NO_CONFIG=1`): `uv lock --upgrade`; keep
  `okf-schema` pinned to the version CI uses unless 0.15.0 is on PyPI (CR 122 depends on it).
- **Minimum-version floors** so a resolver can never go back to a vulnerable version:
  - npm: `overrides` for vulnerable transitive packages (`"@azure/msal-node": ">=7.1.0"` and any
    other alert found by `npm audit`), next to the existing `csv-parse` and `markdown-it` ones;
  - Python: `[tool.uv] constraint-dependencies` (for example `urllib3>=2.8.0`, `soupsieve>=2.9.0`)
    for transitive packages, and lower bounds on direct dependencies.
  - A comment next to each floor names the advisory (GHSA id) it guards against.
- `npm audit` (and `uv`'s audit, or `pip-audit` through `uvx` if available) shows **no high or
  critical** issue; remaining low/medium ones are listed with the reason.
- If CR 135's T9 already added an `npm audit` step in CI, keep it green; otherwise do not add CI
  steps here.
- Full gates: `just check`, the e2e suites, heavy CI on the branch; the VSIX still packages and its
  size is reported before/after. The bundled page runtime (Mermaid, PlantUML, KaTeX, Shiki, Vega)
  renders the README showcase documents unchanged (screenshot comparison).

## Proof

`npm audit` and the Python audit before/after in the PR body, `npm outdated` before/after, the list
of floors with their advisories, all gates green, rendering screenshots unchanged.
