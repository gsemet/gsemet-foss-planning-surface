# Campaign 215 — what in the QA skill did not work as written

First real use of the skill as merged in #237 and #239. Foreman notes first; Driver SKILL lines are
appended when the returns arrive.

## Foreman (scope, prepare, smoke)

| # | Step | What happened | Suggested fix |
| --- | --- | --- | --- |
| F1 | Scope: `new-features.py` | It lists only PRs merged after the baseline date (#240). PRs merged before the baseline that the previous campaign did not cover (#223 Agents window) are invisible. The Foreman has to know them. | Also read the previous index's new-feature table and carry its TODO or "not run" rows forward. |
| F2 | Scope: `coverage-map.py` | 4 host files changed for radio lists (`src/core/edits/sourceEdits.ts`, protocol files, `src/session/features/sourceEdits.ts`) map to area `?`. | Map `src/core/edits`, `src/core/protocol` and `src/session/features` to areas. |
| F3 | Prepare: `doctor` | Run right after `q run observe.mjs &`, it prints `WARN observer: not running`, so the observer has not attached yet. The smoke still passed. | `doctor` waits a second for the observer, or the doc says to wait. |
| F4 | Budgets: window check | `doctor` reports `msq- processes (all sessions): 7` for one window. `pgrep -fl msq-` counts helper processes, not windows, so it cannot check the 2–3 windows budget. | Count main processes only (for example the `--user-data-dir` arg), or add `q sessions`. |
| F5 | Prepare: smoke shot | The doc says the shot confirms "a real workbench", but the smoke shot is clipped to the preview. | Say "a rendered preview", or take a full-window shot. |

## Driver A (C1, C2)

| # | Where | What happened | What the agent did |
| --- | --- | --- | --- |
| A1 | scenario-format.md | No `comment` step; an unknown step fails the whole scenario. | Dropped the comments. |
| A2 | scenario-format.md | An `eval` step is one expression; `;` gives a SyntaxError, and the doc does not say so. | Wrapped the code in an IIFE. |
| A3 | Shell use | zsh noclobber blocks overwriting a scenario file; `env QA_SESSION=x $Q …` stored in a variable fails. | `\rm -f` first; `export QA_SESSION`. |
| A4 | Open With editor, side preview also open | Cmd+Z with focus in the Open With webview did not undo. **Re-checked by C7b: not a product defect.** With Open With only, Cmd+Z undoes a paragraph commit and a radio click, with or without a click on empty preview space first (diff against mark empty). UX-03 (paragraph only) stays fixed. | Undo only after Meta+1 into the side preview. |
| A5 | Open With editor | "Reopen Editor With…" leaves a text tab, the custom editor and the side preview all open; Go to Line hits the wrong editor. | Worked around it. |
| A6 | `q frames` / `q box` | With Open With and the side preview both visible, only one webview is listed, so the Open With webview cannot be driven. harness-pitfalls.md says both are reachable. | Not covered. |
| A7 | `q launch --untrusted` | It only sets `security.workspace.trust.enabled`; the ws path inherits trust, so no restricted window. | Not covered; the skill should say how to untrust. |
| A8 | Narrow pane | The toolbar is collapsed, so `[data-sphinx-preview-theme-toggle]` has size 0; click `button[aria-label='Show view controls']` first. Not documented. | Clicked it first. |
| A9 | Replay fixtures | A replay needs its synth fixture; C1 copied `synth/radio-c1.md` into the skill's `assets/synth` in the worktree (not committed). | Must be promoted with the scenario. |

## Driver A2 (C7, C7b)

| # | Where | What happened | What the agent did |
| --- | --- | --- | --- |
| A10 | `setup-workspace.sh --clone` | A clone made before a fixture was added to `assets/synth` lacks it (`radio-c1.md`); `crlf-source.md` is called `crlf.md`. | Copied by hand. |
| A11 | harness-pitfalls.md | The palette-mode `<select>` is native: arrows and Enter do not change it. | Focus it, type the first letter, Enter. |
| A12 | scenario-format.md | `peval` works as a check or command only, not as a step. The default `diff` check applies `maxLines` per side, so a radio click (-2/+2) needs `maxLines: 2`. | Adjusted. |
| A13 | `clicksel` | It scrolls the element into view, and that scroll can close an open editor (it hid finding c7-1 at first). Boxes move when an editor opens. | Re-box after every editor change. |
| A14 | Scenarios | A click on the already-selected radio is a no-op that looks like a refused write. | Read the selection first (about 6 calls lost). |
| A15 | Inline editor | Escape cancels a paragraph edit; only Meta+Enter commits. Not stated where scenarios are described. | Used Meta+Enter. |
| A16 | `open` step | Quick Open needs `wait: 2500` before the palette step; a missing file fails as "quick pick row not found", which hides the cause. | Added waits. |
| A17 | Untrusted window | `q launch --untrusted --workspace <dir outside the trusted parent>` (for example `$TMPDIR/msq-untrusted-c7`) does give Restricted Mode. Supersedes A7 as the documented method. | Used it. |

## Driver B (C0, C3, C4, C5, C6)

| # | Where | What happened | What the agent did |
| --- | --- | --- | --- |
| B1 | `noop-sweep.mjs` | A click on a radio or checkbox counts as CHANGED (a false positive on `74-radio-plan.md`). | Ignored by hand; `PICK_POINT` should skip `[role=radio]`, checkboxes and `.myst-radio`. |
| B2 | SKILL.md §3 | No shipped scenario opens a document in the side preview with edit mode on. Focus then stays in the preview, so `latency-probe` returns 5000 ms. | Wrote `open.json`; added Meta+1 and an Enter in the source. |
| B3 | SKILL.md §3 | "3–5 chapters in 30 min" does not fit: 60 blocks plus cells of one chapter take more than 4 min. | Used `--limit/--from` (should be stated as mandatory). |
| B4 | `editor` check | It wants the suffix as the editor reports it (`chapters/08-…`), not the workspace path (`book/chapters/08-…`). | Adjusted. |
| B5 | `q scenario --var` | A value with a space (`t=3. Quoted`) did not override the variable. | Generated the scenario with python. |
| B6 | Agents window | Opens with `code --user-data-dir=… --extensions-dir=…/ext --agents <ws>` as a second CDP page (`sessions.html`); `connect()` takes the first `/workbench/` page, so `q` never targets it. The isolated profile shows "Sign in to use Agents", and the window listed the user's real folders. | Blocked; needs `--page sessions` and a signed-in profile. |
| B7 | After navigation | A scenario that follows a link leaves the window dirty; "Open Preview to Side" does not reset it, and Back is hidden in the collapsed toolbar. | Relaunched with a fresh clone. |
| B8 | Scenarios | Without `--keep-going` the first failing action stops the scenario; undo after a preview edit needs Meta+1 then Meta+z. | Used both. |
| B9 | Collapsed toolbar | The Comments button is 0×0 until "Show view controls" is pressed, and `clicksel` then silently does nothing (same root as A8). In `feval`, `document` is the outer iframe; use `D`. | Worked around it. |
| B10 | Shell / env | `q stop` chained with `pkill` was denied by the auto-mode classifier; `QA_CHANGES_ROOT` has no effect on launch/scenario; `sed -i ''` behaves as GNU sed. | `q stop` alone. |
| B11 | Evidence privacy | The Agents-window shot showed the user's real folder names. | Foreman deleted it. The skill should warn that windows outside the QA workspace may show private paths. |
