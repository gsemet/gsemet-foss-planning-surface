# A grid or card inside a blockquote maps every source line one too early

Found by the CR 209 Inspector (2026-10-31). A `{grid}` / `{card}` nested in a blockquote maps its
title and body lines one line too early, so the block editor opens on the line above. This was
already true for the card itself before CR 209 (#229). Reproduce with a render-level test first.
