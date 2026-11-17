# 216 — QA skill: fix what did not work as written in campaign 215

:::{important}
**Owner GO, via the Chief of Staff, 2026-10-31.** The first real QA campaign with the new skill (215)
found 33 places where it did not work as written. Fix them in the skill only: no product code. One
clean commit, one ready PR from `origin/main`, never merge.
:::

The grouped list is in [backlog-item/01-intent.md](../work/backlog-item/intent.md); the 33 raw rows are in
[skill-feedback.md](../../215-qa-campaign-2026-10-31/work/skill-feedback.md).

## Scope

| Must include (owner) | Out of scope (owner) |
| --- | --- |
| Privacy warning for shots (theme 1) | Driving the Agents window: second CDP page `sessions.html`, signed-in profile |
| No-op sweep skips radio and checkbox clicks (theme 2) | Any change under `src/` or `test/` |
| Missing and unclear scenario steps (theme 3) | |
| Window budget that can be checked (theme 4) | |
| Fixture and replay promotion: `synth/radio-c1.md` and the 7 replays from the archive's `replay/` (theme 5) | |
| Reaching the Open With webview while the side preview is open (theme 6) | |

Themes 7 and 8 (pitfalls to document, scope scripts) are in scope too.

> [!WARNING]
> No real VS Code window is needed to prove the doc changes. The script changes (`noop-sweep.mjs`,
> `qa.mjs` frame selection, `q sessions`, `setup-workspace.sh`) get one short local check each in at
> most one window, then stop it.

## Done when

- [ ] Every row of the backlog item is fixed or documented.
- [ ] `noop-sweep.mjs` reports 0 CHANGED on `fixtures-visual/74-radio-plan.md`.
- [ ] `q sessions` (or `doctor`) counts one window per launched session.
- [ ] The 7 replay scenarios and `synth/radio-c1.md` are in the skill and parse as JSON.
- [ ] `bash -n`, `node --check`, `python3 -m py_compile` pass on the changed scripts; relative links
      resolve; `just check` green; normal CI green.
