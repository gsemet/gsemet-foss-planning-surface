# CR 288 evidence (round 3, head 601e0bf1)

| Pair | Shows | Reproduce |
| --- | --- | --- |
| toolbar-before-cream / toolbar-after-cream (https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c0ddf112cff4f2e2ed17081b13903996a81f44fa/) | main row goes from 3 to 4 buttons (Refresh, Edit, Export, collapse); checked by viewing the after image: matches the head toolbar, not stale | npm run visual:render; capture.py --group toolbar-navigation |
| toolbar-before-dark / toolbar-after-dark | same, dark | same |
| export-file-cream / export-file-dark | exported file, JS off | capture.py --scenario toolbar-navigation/v42-export-html-cream-900 (and v43 dark) |

Local after-captures: out/reports/visual/screenshots and out/reports/visual/pages/*.export.html in worktree 288 (v42, v43 passed).
Before images are taken on the base with the same fixture (PR body statement); not re-taken by the Verifier.
