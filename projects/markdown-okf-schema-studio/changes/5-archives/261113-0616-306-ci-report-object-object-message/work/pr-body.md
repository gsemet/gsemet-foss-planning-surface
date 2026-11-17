## Summary

When the visual stage failed, the CI `report` job printed `FAILED visual: [object Object]; [object Object]`, so the log did not say which page or check failed. It now prints `FAILED visual: <page>: <detail>; ...`.

## Deliverables

The failure text of a visual manifest, before and after:

| Manifest failures | Before | After |
| --- | --- | --- |
| `{page: "home", detail: "blank"}`, `{page: "toc", detail: "overflow"}` | `[object Object]; [object Object]` | `home: blank; toc: overflow` |
| `"first"`, `"second"` | `first; second` | `first; second` |

```js
function failureText(failure) {
  if (typeof failure === "string") return failure;
  if (failure && typeof failure === "object" && "page" in failure) return `${failure.page}: ${failure.detail}`;
  return JSON.stringify(failure);
}
```

## Changes

- `scripts/e2e-campaign.mjs`: `failureText` formats each failure; `stageFrom` maps the failures through it. The manifest's `error` keeps its priority, and the JUnit file carries the new text through `stage.error`.
- `test/site/e2eCampaign.test.ts`: a test for object and string failures.
- SwRS-MDOKFSTUDIO-CORE-076: a boundary row for the failure text, plus a requirements log entry.

## Impacts

No visual change: only the text of a CI log line and of the JUnit error changes.

Before (origin/main, the new test run against it): `FAILED visual: [object Object]; [object Object]`.
After (this branch): `FAILED visual: home: blank; toc: overflow`.

## Blast radius

Grade: **1**. One helper in a CI reporting script, no workflow file changes; a plain `git revert` restores the previous text.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [ ] Local gates: `just check`, `just requirements-lint`, `just requirements-update` (no diff); the local `just preflight` ci-static and ci-visual stages pass, its real VS Code integration stage failed on a window-geometry step unrelated to this change (proof is the branch heavy run)
- [x] Review
- [x] CI green (including the heavy run: integration and stress)

No user-facing change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
