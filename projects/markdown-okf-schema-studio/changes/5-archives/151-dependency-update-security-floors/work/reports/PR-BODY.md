## Summary

Updates the npm and Python dependencies to their latest compatible versions and adds minimum-version
floors so a resolver can never fall back to a version with a known advisory. `npm audit` goes from
3 findings (2 high) to 0.

## Deliverables

### Versions, before and after

| Package | Before | After |
| --- | --- | --- |
| katex | 0.19.0 | 0.19.1 |
| myst-parser / myst-to-html | 1.7.4 | 1.7.5 |
| markdown-it-myst (transitive) | 1.0.18 | 1.0.19 |
| @azure/msal-node (transitive, dev) | 6.0.1 | 7.1.2 |
| qs (transitive) | 6.16.0 | 6.17.0 |
| okf-schema | 0.13.0 | 0.15.1 |
| commitizen | 4.19.2 | 4.19.3 |
| playwright | 1.64.0 | 1.64.1 |
| pytest | 9.1.1 | 9.2.0 |
| sphinx | 9.1.0 | 9.1.1 / 9.2.0 (per Python marker) |
| pluggy, sphinxcontrib-jsmath, tomlkit, wcwidth | 1.6.0, 1.0.1, 0.15.1, 0.9.2 | 1.7.0, 2.0.0, 0.15.2, 0.9.4 |

About 15 further transitive patch bumps are in the lock file. The VSIX grows from 7,430,035 to
7,430,331 bytes (+296 B).

### Audit counts

| Audit | Before | After |
| --- | --- | --- |
| `npm audit` | 3 (2 high, 1 moderate) | 0 |
| `pip-audit` on the exported lock | no finding | no finding |

### Floors

| Where | Floor | Advisory |
| --- | --- | --- |
| npm `overrides` | `@azure/msal-node >=7.1.0` | GHSA-xcx6-jx8p-x3h5 (high) |
| npm `overrides` | `qs >=6.17.0` | GHSA-6pq8-jhm2-2vcw (moderate) |
| uv `constraint-dependencies` | `urllib3>=2.8.0` | GHSA-vxq7-64xx-v4gw, GHSA-8988-9cw3-xx77 (high), GHSA-gh4c-6fx4-qh6g (medium) |
| uv `constraint-dependencies` | `soupsieve>=2.9.0` | GHSA-gjv8-xp57-g29c, GHSA-j934-xhv5-fg8f (medium) |

The npm floors are documented in the `//overrides` key of `package.json` (JSON has no comments);
the Python ones in comments in `pyproject.toml`. Lower bounds of direct Python dependencies were
raised to the locked versions.

### Held-back upgrades

- `@types/node` stays on `^24`: Node 24 is the pinned runtime, the types must match it.
- `dependency-cruiser` stays on 18.7.0: it is already the newest release (the registry's "latest"
  tag is stale).

## Changes

- `package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`: bumps, overrides, floors.
- `scripts/patch-myst-imports.mjs`: version guards moved to `myst-to-html` 1.7.5 and
  `markdown-it-myst` 1.0.19 (the patched code is identical; the patch still applies).
- `test/build/mystTightnessPatch.test.ts`: comment only; assertions unchanged.
- `SwRS-MDOKFSTUDIO-CORE-070`: the refusal scenario names the new guarded version.

## Impacts

Only katex and the MyST packages changed among the bundled renderers. Rendering of the showcase
documents is expected unchanged; the screenshot comparison is left to the on-demand heavy CI run.
CI now uses okf-schema 0.15.1 (from the lock); `requirements-lint` is green, with new informational
notices only.

Blast radius: 2 (build tooling, lock files, bundled renderers).

## Test plan

- `just check` green: 2918 unit tests, contracts, boundaries, limits, markers, settings,
  dependency-cruiser, requirements lint and coverage.
- `npm run package` produces the VSIX.
- Real-window integration and rendering comparison: run the heavy CI job on this branch.

## Autonomous decisions

- Installs and upgrades were allowed by the change request; `npm ci` ran in the worktree.
- The corporate Python index was unreachable, so `UV_NO_CONFIG=1` against public PyPI was used.
- okf-schema was raised to 0.15.1 (on PyPI, requirements lint green) instead of staying on 0.13.0.
- Real-window tests were not run locally (screen locked overnight).
- The okf-schema repository's own alerts are out of scope (another repository).

## Internal references

Change request 151, stacked above 149/150.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
