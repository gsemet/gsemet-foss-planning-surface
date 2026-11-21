
## Settled by the Chief of Staff, 2026-11-21

No behaviour change: the behaviour is the owner's CR-455 decisions (real-file side scrolls the preview; staged and timeline diffs open the working-tree preview with no scroll following, decision 5). This CR closes the test gaps CR-455 left:
- a real-window test of diff-to-preview scroll in the inline diff layout (CR-455 tested side by side only);
- the real-window step T6 dropped by CR-455 (staged-like diff, no `file:` side: the button opens the working-tree preview, no scroll following), made reliable this time;
- if a step proves impossible in a real window because of VS Code, it is written as a known limitation with the reason, never a skipped test left silent.

Owner, 2026-11-21: "mets tous les inbox dans le batch en cours" then "Griller puis batch": joins the running batch-07.
