# Catch real-window failures before the version commit

Filed 2026-11-03 by the main session from the owner's request: "Je veux vraiment que ça soit
beaucoup plus stable la prochaine release."

## Owner decision (2026-11-04)

This decision replaces the proposal below, which stays as history.

- The real VS Code jobs stay on `main`: no heavy jobs on pull requests.
- At release time, the guideline runs the procedure and makes sure it passes: a green heavy run on
  `main` HEAD before the version commit.
- Stacking the release commit on top of a lot of development is probably the mistake. A release
  should be planned by the Foreman: the development lands first, then the release runs on its own.

What is left to do: say in the release process and lifecycle guidelines how the Foreman plans a
release, and what stops merging during it. The heavy run on `main` before the version commit is
already in the release driver's steps (CR 256).

Not retained: heavy jobs on pull requests, the nightly run (owner, 2026-11-04) and the bump gate in
`scripts/version.py`.

## What happened

> [!WARNING]
> 1.3.0 and 1.3.1 were never tagged: on both version pushes the real VS Code jobs (`integration`,
> `stress`) went red, so 1.3 ships as 1.3.2 after three fix PRs (#306, #309 and the test fix
> 14c706cf).

| Version push | Red job | Cause |
| --- | --- | --- |
| 1.3.0 (run 41686091727) | integration `wide-table-tab` | real bug: a cell editor left view when its table left the breakout (fixed in #306) |
| 1.3.0 | stress `incoming-changes` | stale helper: waited for a stored edit mode nothing writes since "preview first" |
| 1.3.1 (run 41704023642) | integration, stress | two more real-window scenarios still assumed a document opens in edit mode (#309) |

Common root: the heavy jobs run only on a manual dispatch or on the version push (CI rules 13 and
14). Rule 13 asks for a heavy run before merging a change to the host, the webview or the
real-window tests, but nothing enforces it, so the "preview first" change and the table breakout
change merged with only the simulated jobs, and the release push was the first real-window run.

## Goal

The version push is never the first heavy run of its code. A red real-window scenario shows up
on the PR that causes it, or at the latest the next morning, never at release time.

## Proposal (recommended, to grill)

1. **Heavy jobs on PRs that need them, automatically.** In `ci.yml`, run `integration` (and a
   short `stress`, e.g. 3 rounds) on a pull request whose diff touches `src/host-*`, `src/page/`,
   `src/session/`, `test/integration/` or `package.json` contributions. Advisory first (one week),
   then required in `checks`. Cost: about +20 min on those PRs only.
2. **Nightly heavy run on `main`** (`schedule`, e.g. 03:00 UTC, skipped when `main` did not change
   since the last green nightly). A red nightly opens or updates a GitHub issue "main is red on
   real VS Code".
3. **Release gate before the version PR.** `scripts/version.py` (`just bump-version`) refuses to
   bump unless `origin/main` HEAD has a green heavy run (nightly, dispatch or PR run of that exact
   commit), checked with `gh run list --commit`; `--force` documented for emergencies. The release
   process guideline gets a step 0: "dispatch `gh workflow run ci.yml --ref main -f heavy=true`
   and wait for green".
4. **Stress flake budget.** Keep the flaky stress items (P3 backlog) visible on the board; a release
   waits for none of them, but the nightly records the flake rate per scenario.

## Open questions for the owner

- Advisory then required for PR heavy jobs, or required at once? (recommended: advisory one week)
- Nightly time and whether a red nightly may open an issue automatically (recommended: yes).
- Keep the version push's own heavy run as the final gate (recommended: yes, it stays rule 14).

## Split (2026-11-03)

The procedure part (heavy run on `main` before the version commit, run by a release driver) is CR
256 `release-driver`, decided by the owner. This item keeps the CI changes: heavy jobs on PRs, the
nightly run and the bump gate in `scripts/version.py`.
