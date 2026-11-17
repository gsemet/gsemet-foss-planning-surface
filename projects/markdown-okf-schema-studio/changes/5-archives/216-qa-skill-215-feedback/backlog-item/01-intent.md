# QA skill: fix what did not work as written in its first real campaign

Tooling · Code review and campaign use · Source: campaign 215, the first run of the skill as merged in #237 and #239 · P2

> [!NOTE]
> Campaign 215 recorded 33 places where the exploratory QA skill
> (`.agents/skills/markdown-studio-exploratory-qa-claude/`) did not work as written. They are listed in
> [skill-feedback.md](../../../4-archives/215-qa-campaign-2026-10-31/skill-feedback.md). This item
> groups them into fixes. Out of scope (owner, 2026-10-31): driving the VS Code Agents window
> (second CDP page `sessions.html`, signed-in profile).

| # | Theme | Rows | Fix |
| --- | --- | --- | --- |
| 1 | **Privacy** | B11 | A window outside the QA workspace (recent folders, the Agents window) can show the user's real paths. In Rules and the charter prompt, say: check every shot for private paths or vault content before saving it to `evidence/`, and never shoot lists of recent folders. |
| 2 | **No-op sweep** | B1, B3 | `noop-sweep.mjs` must skip `[role=radio]`, checkboxes and `.myst-radio` (a click on them is a write by design, so it counts as a false CHANGED). §3 states `--limit/--from` as required on long chapters and gives a realistic budget. |
| 3 | **Scenario steps** | A1, A2, A12, A14, A15, B4, B5, B8 | Add a `comment` step (or ignore unknown keys with a warning). Make `eval` accept statements, or document the single-expression rule. Allow `peval` as a step. The `diff` check states that `maxLines` applies per side. `--var` accepts values with spaces. The `editor` check accepts the workspace path. Document `--keep-going`, Meta+Enter to commit (Escape cancels), and reading the current radio selection before a no-op click. |
| 4 | **Window budget** | F4, F3 | `doctor` and a new `q sessions` count windows (main processes per `--user-data-dir`), not helper processes, so the 2–3 windows rule can be checked. `doctor` waits briefly for the observer before warning. |
| 5 | **Fixture and replay promotion** | A9, A10 | A replay must ship with its fixture. Promote `synth/radio-c1.md` and the 7 campaign 215 replay scenarios (copies in the archive's `replay/`) into the skill. `setup-workspace.sh --clone` must refresh `synth/` from `assets/synth` so a clone made earlier gets new fixtures. Fix the `crlf.md` / `crlf-source.md` name. |
| 6 | **Open With webview with the side preview open** | A4, A5, A6 | `q frames` and `q box` list only one webview when Open With and the side preview are both visible, so the Open With webview cannot be driven, and Cmd+Z there does not reach it. Add a `--which`/`--frame` selector that targets each visible webview, and fix harness-pitfalls.md, which says both are reachable. Note that "Reopen Editor With…" leaves three editors open. |
| 7 | **Harness pitfalls to document** | A3, A7/A17, A8/B9, A11, A13, A16, B2, B7, B10, F5 | Restricted Mode needs `--untrusted --workspace <dir outside the trusted parent>`. A narrow pane collapses the toolbar (click "Show view controls" first; buttons are 0×0). The palette `<select>` is native. `clicksel` scrolls, which can close an open editor. Quick Open needs a wait and its error hides a missing file. Ship an "open in side preview, edit mode on" scenario that leaves focus in the source. After a navigation, relaunch with a fresh clone. noclobber and `export QA_SESSION`. Run `q stop` alone. The smoke shot shows the preview, not the workbench. |
| 8 | **Scope scripts** | F1, F2 | `new-features.py` carries forward the TODO and "not run" rows of the previous index (PRs merged before the baseline that were never covered). `coverage-map.py` maps `src/core/edits`, `src/core/protocol` and `src/session/features` to areas. |

## Done when

- [ ] Every row above is fixed or documented in SKILL.md, charters.md, scenario-format.md,
      harness-pitfalls.md or the scripts.
- [ ] The no-op sweep reports 0 CHANGED on `fixtures-visual/74-radio-plan.md`.
- [ ] `q sessions` (or `doctor`) reports one window per launched session.
- [ ] The 7 replay scenarios and `synth/radio-c1.md` are in the skill and parse.
- [ ] Shell, Python and Node syntax checks pass, and every relative link in the skill resolves.

Uncheck to disagree: [x]
