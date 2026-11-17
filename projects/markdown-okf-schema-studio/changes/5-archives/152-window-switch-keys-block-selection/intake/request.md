# 152 — Keyboard block selection works again after a window switch (heavy integration fix)

Type: fix · Priority: P1 · From the user, 2026-10-28 11:00 (hotfix, fix forward, no revert)

## Intent

Heavy CI integration fails on `main` (6df062d3 and later) in
`test/integration/windowSwitchKeys.test.ts`, step "margin: the keyboard to select a block": after a
window switch, two ArrowDown presses in edit mode select no block (expected exactly one selected).
Runs: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40657976144 and
https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40658224831. The same branch
before the last merge (CR 142 tip) passed twice (runs 40640637221, 40645287945). The only product
commit in between is "feat: pasting a URL makes a link, an image URL an image" (#153, CR 145, touches
block-editor keyboard/paste handling): probable cause, not proven.

## Decisions (user)

- One independent PR on `main`, from fresh `origin/main`; fix forward, no revert of #153.
- Reproduce first (heavy CI on the branch before the fix, or a local real window if the screen is
  unlocked); the failing step must pass after the fix.
- Requirements traceability as usual (SwRS, `@implements_req` / `@tests_req`, `just requirements-update`).
- Gate: `just check` green and heavy CI integration green on the branch; stress is ignored.

## Autonomous decisions

- CR number 152 (next free), branch `change-requests/152-window-switch-keys-block-selection`.
