# Toolbar load hint not seen when the preview opens

Type: fix · Priority: P3 · Filed 2026-10-28 from the user's manual test of #175 (VSIX in their VS Code)

## Observed

- In a real VS Code window, the unroll and roll-up of the collapsed floating toolbar work and look
  right (`interpolate-size` / `transition-behavior: allow-discrete` confirmed in practice).
- The load hint (the collapsed toolbar briefly unrolls rows 2 to 5, then rolls them up) is not seen
  when the preview opens. The user rates it "not very serious".

## Leads (to check first, nothing confirmed)

- The hint plays once per panel (`viewToolbarHintShown` in the webview state,
  `src/page/modules/toolbarCollapse.ts`). VS Code restores webview state for panels that survive a
  reload, so panels open before the install never replay it; new panels should.
- It starts two frames after load and lasts 700 ms (`HINT_OPEN_MS`): it may run while the page is
  still covered by the pending overlay or before the first real render, so nobody sees it.
- It needs the toolbar collapsed and reduced motion off (macOS "Reduce motion" is off on the user's
  machine).

## Expected

- Opening a preview with a collapsed toolbar shows the hint visibly, once the content is painted.
  Grill decision for CR 162: "À chaque ouverture" (every time a preview opens).

Proof: real-window recording or frame sheet of the hint after opening a new preview; unit test of
the start condition.
