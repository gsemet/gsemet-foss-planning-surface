# 053 — dependabot-security

Dependabot reports 40 open alerts on `uv.lock` (development dependencies only, docs group):

- `pillow` 12.3.0: 39 advisories (4 critical, 23 high, 12 medium), all fixed in 13.0.0.
- `certifi` 2026.7.22: 1 critical, fixed in 2026.10.19.

Dependabot security updates fail
([run](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39996023227)):
"Filtered out pillow 13.0.0 because python requirement >= 3.11 is not satisfied by python 3.10.20".
Cause: `pyproject.toml` declares `requires-python = ">=3.10"` while Pillow 13 needs Python 3.11 or later.

## Decisions (user, 2026-10-23)

1. Raise `requires-python` to `>=3.11` (check that no script or CI job relies on 3.10). Set
   `pillow>=13.0.0` in the docs group and relock so `certifi>=2026.10.19` too. Lock with the
   public index (`UV_NO_CONFIG=1`, the corporate index is unreachable); this CR may download the
   new wheels into the uv cache.
2. Check the Pillow 13 changelog for breaking changes against our uses (`scripts/version.py`,
   `scripts/release_notes.py`, `scripts/generate-readme-images.py`, `test/visual/capture.py`,
   `test/build/test_release.py`) and adapt if needed.
3. Make future Dependabot updates work: after merge, the alerts close and no Dependabot update run
   fails for this reason. If the repo has no `.github/dependabot.yml`, do not add version updates
   (security updates only, as today) unless needed for the fix; say so in the PR.
4. Gates: `just check`, `just visual`, and the Python tests (`uv run --group docs pytest test/build`).
   No real VS Code run needed (no extension code change).
5. Branch `changes-requests/053-dependabot-security`. No assets branch (no screenshots).
6. Speed: Opus everywhere, reviewer on the round diff, ready when `checks` is green. Rounds: 3.
   PR for an external reader; commit trailer `Assisted-by: Claude:Opus-5.5`.
