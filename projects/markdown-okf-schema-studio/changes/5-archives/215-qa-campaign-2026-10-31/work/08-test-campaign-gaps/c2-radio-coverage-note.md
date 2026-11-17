# C2 radio groups: coverage note

Exercised (all PASS unless a finding is named): click in reading and edit mode writes two lines with no editor opened; arrows write nothing; Space writes; Light, Dark, White, Cream themes (border contrast 3.1 to 6.3 against the item background, noClip, inViewport at 393 px); two previews of one file (Open With plus side) stay in sync after a click; external rewrite while a radio is focused re-renders correctly (focus lost: c2-1).

Gap in the harness, not the product: `q launch --untrusted` produced a trusted folder (the Workspace Trust dialog says "You trust this folder"), so untrusted and read-only refusals were not exercised.
