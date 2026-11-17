# Review round 1 — stress dispatch inputs (CR 205)

Inspector, 2026-10-31. Scope: `git diff` in `markdown-okf-schema-studio-wt-205`
(`.github/workflows/ci.yml`, `justfile`, `test/build/test_workflows.py`).
Gate run: `uv run pytest test/build/test_workflows.py` → 64 passed. `just --dry-run ci-stress`
renders `STUDIO_STRESS_REPEAT="20"`.

## What is good

- **Defaults unchanged.** On push (no `inputs`), and on a dispatch that leaves both fields empty,
  `inputs.stress_repeat || '20'` gives `20` and `STUDIO_STRESS_SCENARIOS` is empty, so all
  scenarios run. That is the same as before. Calling `just ci-stress` locally without the variable
  still gives 20, and `just ci-stress 5` still works.
- **No workflow-level injection.** Both inputs reach the step through `env:`. The `run:` line has
  no `${{ }}` expression. This is the pattern GitHub recommends.
- **CI guidelines respected.** The job still makes the two calls `just dev-ci` and
  `just ci-stress`, plus a display server (rule 3). It has no inline script. Rule 1 holds.
- **Scenarios are safe.** `STUDIO_STRESS_SCENARIOS` is never interpolated by just. It reaches
  `stressPlan.ts` as an env var and is checked against the known names there.
- **New test** pins the input types, the empty defaults, the env wiring and the unchanged `run:`
  line. It fails on the old workflow because the inputs are missing.

## Findings

### 1. Shell injection through `{{ REPEAT }}` (required)

`REPEAT=env("STUDIO_STRESS_REPEAT", "20")` turns the dispatch input into a just parameter. just
then pastes it as text into the shebang script, in two places:
`export ... STUDIO_STRESS_REPEAT="{{ REPEAT }}"` and the `echo "ci-stress: passed ({{ REPEAT }} rounds)"`
line. This undoes the env-var protection that the workflow sets up. I reproduced it with just
outside the repo:

```text
STUDIO_STRESS_REPEAT='1"; echo INJECTED; "' just t   →  prints INJECTED
```

The real-world risk is low: only someone with write access can dispatch, and that person could
also edit the workflow. The job's token is `contents: read`. But the code is the standard
injection pattern. It is also in the one recipe that takes free-form text from the GitHub UI, and
it would look like a non-issue to anyone who later adds a secret to this job. The fix is small, so
it must be fixed. Either of these works:

- `export STUDIO_STRESS_REPEAT={{ quote(REPEAT) }}` (just's `quote()` escapes for the shell), and
  use `$STUDIO_STRESS_REPEAT` in the final echo; or
- add the `[positional-arguments]` attribute and read `"$1"`.

### 2. Range check comes late (required, same edit)

The 1–100 check exists (`test/shared/stressPlan.ts`, `MAX_STRESS_REPEAT`). It only runs inside the
VS Code extension host (`realInput/run.ts:70`). That is after `npm run compile`, `bundle` and the
VS Code launch. A typo like `60x` or `150` costs minutes and ends in a test-host failure instead of
a clear recipe error. Check the value at the start of the recipe, after quoting:
`[[ "$STUDIO_STRESS_REPEAT" =~ ^[0-9]+$ ]] && (( STUDIO_STRESS_REPEAT >= 1 && STUDIO_STRESS_REPEAT <= 100 ))`,
else `echo "ci-stress: REPEAT must be an integer from 1 to 100, got ..." >&2; exit 2`. This
follows the style of `ci-report STAGES`. With this check in place, finding 1 can no longer be
exploited either. Keep the quoting anyway.

### 3. Time limits for 100 rounds (advisory, document it)

Today 20 rounds × 15 trusted scenarios take about 18 minutes. Each window has a launch deadline of
26 minutes (`STUDIO_LAUNCH_TIMEOUT_MS=1560000`), and the job timeout is 30 minutes. That is about
3.6 s per scenario-round:

- `alert-dropdown` alone × 100 rounds is about 6–10 minutes plus setup. It fits.
- **All scenarios × 100 rounds is about 90 minutes.** The launch watchdog would kill it at 26
  minutes and the job would time out at 30. Rule 11 says not to raise the timeouts, and they
  should not be raised.

Add a note to the `stress_repeat` description, for example "above 20 rounds, narrow
stress_scenarios", and to the recipe comment. That way a dispatch of 100 rounds without a scenario
filter is not mistaken for a flake or a hang.

### 4. Doc of the dispatch command (nice to have)

CI rule 13 in `.agents/guidelines/ci.guidelines.md` lists the heavy dispatch command. Add an
example there:
`gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=60 -f stress_scenarios=alert-dropdown`.
Without it, nobody will find the knob. The input does nothing without `heavy=true`, and the
description already says so.

### 5. Test coverage of the recipe (nice to have)

The new test covers the workflow side only. Add an assertion that the `ci-stress` body does not
contain a bare `"{{ REPEAT }}"`, or that it uses `quote(`. Finding 1 would then be locked in.

## Verdict

CHANGES REQUIRED

1. Stop raw text interpolation of `REPEAT` in the `ci-stress` body: use `{{ quote(REPEAT) }}`, or
   positional arguments, and use the shell variable in the final echo.
2. Check that `REPEAT` is an integer from 1 to 100 at the start of the recipe, with a clear
   `ci-stress:` error and a non-zero exit.
3. In the `stress_repeat` input description and the recipe comment, say that above about 20 rounds
   `stress_scenarios` must be narrowed to stay within the 26-minute launch deadline and the
   30-minute job timeout.
