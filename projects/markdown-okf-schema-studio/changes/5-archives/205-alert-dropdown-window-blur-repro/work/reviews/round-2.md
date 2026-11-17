# Review round 2 — stress dispatch inputs (CR 205)

Inspector, 2026-10-31. Scope: `git diff` in `markdown-okf-schema-studio-wt-205`
(`.agents/guidelines/ci.guidelines.md`, `.github/workflows/ci.yml`, `justfile`,
`test/build/test_workflows.py`). Nothing is committed yet; the worktree has only these 4 files
modified.

## Gate

`just check` was run once in the foreground: **exit 0**.

- Node tests: 3258 passed, 0 failed, 0 skipped (and a second suite with 71 passed, 0 failed).
- pytest: 139 passed (12 warnings).
- check-boundaries passed (310 modules), check-limits passed (882 files), check-settings passed
  (19 settings). Requirement indexes, OKF projections and coverage: 0 changes.
- The `okfreq lint` `W2 Broken cross-link` warnings also show up on files this change does not
  touch. They are warnings and they do not fail the gate.

## Round 1 required changes

### 1. Injection through `{{ REPEAT }}`: fixed

The recipe now sets `repeat={{ quote(REPEAT) }}` and uses only `"$repeat"` after that, in the
export, the error message and the final echo. No bare `{{ REPEAT }}` is left. I tested it against
the real recipe, both as an argument and through `STUDIO_STRESS_REPEAT`:

| Input | Result |
| --- | --- |
| `1"; echo INJECTED; "` | exit 2, the text is printed back as-is, no `INJECTED` line |
| `1'; echo INJECTED; '` | exit 2, the text is printed back as-is |
| `$(echo INJECTED)` | exit 2, nothing runs |
| `` `echo INJECTED` `` | exit 2, nothing runs |

`quote()` puts the value in single quotes, so the shell never parses it. Inside double quotes,
the shell does not run `$(...)` that sits in a variable's value. The error echo is safe too.

### 2. Early range check: fixed

`0`, `101`, `150`, `60x`, `-5`, `' 5'`, an empty string and `99999999999999999999` all stop at
once with `ci-stress: REPEAT must be an integer from 1 to 100, got …` and **exit 2**. Nothing is
compiled and no VS Code window opens. The style follows `ci-report STAGES`.

### 3. Time limit note: fixed

The `stress_repeat` input description says "Above about 20, narrow stress_scenarios or the run
exceeds the time limits". The recipe comment explains the 3.6 s per scenario-round figure, the
26-minute launch deadline and the job limit. The timeouts did not change, which matches rule 11.

## Nice-to-haves from round 1

- **4. Dispatch doc:** done. CI rule 13 now shows
  `-f heavy=true -f stress_repeat=60 -f stress_scenarios=alert-dropdown`.
- **5. Recipe test:** done. `test_ci_stress_recipe_quotes_and_validates_repeat` checks for
  `quote(REPEAT)`, no bare `{{ REPEAT }}`, the error text and `exit 2`.

## Defaults unchanged

- `env -u STUDIO_STRESS_REPEAT just --dry-run ci-stress` renders `repeat='20'`.
- `just --dry-run ci-stress 5` renders `repeat='5'`. `STUDIO_STRESS_REPEAT=60` renders
  `repeat='60'`.
- Workflow: a push, or a dispatch with an empty field, gets `inputs.stress_repeat || '20'`, which
  is `20`. `STUDIO_STRESS_SCENARIOS` is empty, so all scenarios run. The `run:` line has no
  `${{ }}` and is still `xvfb-run --auto-servernum just ci-stress`. The job still makes the two
  `just` calls from rule 3.

## New findings (advisory, not blocking)

### A. A 20-digit number gets past the recipe check (advisory)

Bash arithmetic is 64-bit and wraps silently. `18446744073709551621` (2^64 + 5) matches
`^[0-9]+$` and is read as `5` in `(( ... ))`, so it passes the recipe check. The run then compiles
and launches VS Code. `stressPlan.ts` still rejects it, because it uses `Number.isSafeInteger` and
the 1–100 range, so this is not a correctness or security hole. It only means one silly value
fails late instead of with exit 2. Locally, the run got as far as the VS Code launch (it failed
there for an unrelated local reason: `bad option: --user-data-dir`). A one-character fix would
close it: `^[0-9]{1,3}$`.

### B. Line wrap in the guideline (nit)

`.agents/guidelines/ci.guidelines.md` line 80 is now 133 characters. The project wraps prose at
100. Move `Run them before merging…` to the next line.

## Verdict

APPROVE

All three required changes from round 1 are fixed and verified by hand. The two nice-to-haves are
done. `just check` passes with exit 0. Findings A and B are optional cleanups. They can go into
this branch if the Coder touches it again, otherwise they can be dropped.
