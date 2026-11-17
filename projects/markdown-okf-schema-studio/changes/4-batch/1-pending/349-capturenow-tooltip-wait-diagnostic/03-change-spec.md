# Name the stuck tooltip when the capture helper's tooltip wait times out

Short name: `tooltip-wait-diag`. Origin: verbal (owner, 2026-11-17, « 3. ok »). No issue.
Repository: gsemet/markdown-okf-schema-studio.

## Goal

When a real-window capture waits for the toolbar tooltips to hide and they never do, the failure
must say which toolbar button still shows its tooltip, and why it is shown (hovered or focused), and
it must fail in a bounded time it states. Today the wait uses Playwright's 30 s default and its
error carries no such detail: CR-337 saw this timeout 3 times in the CI `stress` job
(incoming-changes scenario, intermediate heads of PR #402's branch) and could not tell which button
held it. This change is a diagnostic only: it fixes no flake and changes no product behaviour.

## Background (CR-337)

The investigation is in the planning folder:
`changes/6-trash/261117-1018-337-stress-incoming-changes-wait-timeout/evidence/investigation.md`.
In short: the only `frame.waitForFunction` on the incoming-changes path is the tooltip wait of the
shared capture helper, reached by `scenarioIncomingChanges` at the `r03` and `r07` captures through
`captureNow` (`test/integration/realWindowGaps.ts`); the failing runs show the wait ran the full
30 s; the stress runs on `main` and on the merged head have not reproduced it since (more than 80
rounds). The owner chose this diagnostic over closing with no change.

## What changes

One file: `test/integration/realInput/harness.ts`, the `capture` method of the object returned by
`createEvidence` (the helper `captureNow` in `test/integration/realWindowGaps.ts` calls it through
`withCurrentFrame`). Today, after moving the pointer to the frame's bottom-left corner and blurring
the toolbar buttons, it runs (around line 622):

```ts
await frame.waitForFunction(() => Array.from(document.querySelectorAll("[data-sphinx-preview-toolbar] button[data-tooltip]"))
  .every((element) => { /* ::after content none/normal, or visibility hidden, or opacity 0 */ }));
```

After the change:

1. **One page-side probe.** A single in-page function lists the toolbar buttons
   (`[data-sphinx-preview-toolbar] button[data-tooltip]`) whose `::after` is shown, by the same
   test as today (shown = `content` is neither `none` nor `normal`, and `visibility` is not `hidden`,
   and `Number(opacity)` is not 0). For each it returns: the `data-tooltip` text, whether the button
   matches `:hover`, whether it matches `:focus-visible`, and the computed `content`, `visibility` and
   `opacity` of its `::after`. The wait and the report use this same probe (one definition of the
   condition, not two copies): for example a module-level function passed to `frame.evaluate`, and
   the wait written as its result being empty. The condition itself does not change: a capture that
   passes today passes after the change.

2. **Explicit timeout: 10 000 ms**, as a named constant (for example
   `TOOLTIP_HIDE_TIMEOUT_MS = 10_000`) passed as `{ timeout }` to `frame.waitForFunction`.
   Reason: the toolbar tooltip has `transition: none`
   (`src/core/preview/styles/pageChromeStyles.ts`), so once the pointer has moved off and the buttons
   are blurred it hides at once; a tooltip still shown after 10 s is stuck, not slow. 10 s is the
   harness's usual bound for one page condition (`withCurrentFrame`'s default, the waits of
   `clickRouting.ts`), and it fails 20 s sooner than today in a CI job that repeats scenarios.

3. **On timeout, a message that names the cause.** When the wait throws a Playwright timeout error
   (`error.name === "TimeoutError"`), the helper runs the probe once more and throws a new `Error`
   with the original as `cause`. Message form (settled here; one line, so the `stress` wrapper in
   `test/integration/realInput/run.ts`, which prefixes `stress round N/M, scenario <name>: `, keeps
   it whole):

   ```
   capture <id>: toolbar tooltip still shown after 10000 ms: "<data-tooltip>" (hover: yes, focus-visible: no, ::after content "...", visibility visible, opacity 1); "<next>" (...)
   ```

   where `<id>` is the capture id (`review-annotations/r03-incoming-change-bars` for instance).
   Reason for the form: the capture id locates the step, the tooltip text names the button the way a
   reader sees it, hover versus focus-visible separates the two causes the helper tries to remove
   (pointer not moved off, focus not cleared), and the three computed values show which hiding rule
   failed.
   Edge cases:
   - The probe finds no shown tooltip on the second read (it hid just after the deadline): the
     message says so: `capture <id>: toolbar tooltips hid only after the 10000 ms wait timed out`.
   - The second probe itself throws (frame gone): rethrow the original timeout error unchanged, so
     `withCurrentFrame`'s detached-frame retry still sees it.
   - Any error that is not a timeout is rethrown unchanged.
   - The new message must not match `detachedFrameError` (`harness.ts` line 45:
     `/frame.*detach|execution context was destroyed|cannot find context with specified id/iu`), so
     `withCurrentFrame` never retries a stuck tooltip as a detached frame. The fixed words above do not;
     keep them that way.

4. **Doc comment.** The doc comment of `capture` (it already says it moves the pointer and blurs the
   toolbar) gains one sentence: it waits up to 10 s for the toolbar tooltips to hide and, if one stays
   shown, fails with the button's tooltip text and its hover and focus state.

The file stays far under the 1 500-line limit of `test/` (739 lines today).

## Out of scope

- Any fix of the flake itself: CR-337 found nothing to fix on the code now on `main`.
- The two other copies of this tooltip wait, in `test/integration/checkboxToggle.test.ts` (line ~82)
  and `test/integration/previewEditing.test.ts` (lines ~136 and ~208): the intake names the shared
  helper only, and the observed failures were on its path. They keep their behaviour; a later CR may
  share the probe with them.
- `src/`, the requirements bundle, the writing skill, CI workflows and justfile targets: no change.
- No new capture, no new scenario, no change to the stress plan.

## Requirements

No SwRS changes: the change is in test-harness code with no `@implements_req` or `@tests_req`
marker, and no product behaviour changes. No entry in `requirements/tiers/log.md`. The Driver
confirms with `just requirements-lint` (part of `just preflight`) that nothing moved.

## Commit and pull request

One commit, type `test` without a scope (the allowed scopes are for `feat` and `fix` only), for
example `test: name the stuck toolbar tooltip when a capture's wait times out`, per
`.agents/guidelines/git-commit-message.guidelines.md`. The pull request body links CR-337's finding
in plain words (stress flake of the incoming-changes scenario, not reproduced since PR #402) and
says this is a diagnostic only.

## Evidence

1. `just check` passes (TypeScript, formatting, file size, unused exports): the harness compiles and
   no new export is left unused.
2. `just preflight` passes (on Windows, its static stage; CI runs the others), per the constitution.
3. One heavy CI dispatch on the branch, so the real-window jobs run the changed helper:
   `gh workflow run ci.yml --ref <branch> -f heavy=true`. The `integration` and `stress` jobs pass;
   the pull request names that run. This proves the unchanged condition still lets every capture
   through within 10 s.
4. The timeout path cannot run locally (the real VS Code window runs in CI only) and is not forced in
   CI: the Driver shows it by the code itself in the pull request (the probe, the timeout, the
   message), and states that the path is proven only on the next real recurrence. A test that forces
   a stuck tooltip is not asked for: it would need a hover held across a real window, the very
   instability this diagnoses.

## Open questions

None.
