# Stress: the alert type list loses its editor once in 20 rounds

Severity Low · Observed twice · Area GitHub alerts, type list · Real-window stress · P1

The release run 41704023642 (1.3.1, `main` 01b1e292) failed its stress job at round 7 of 20,
scenario `alert-dropdown`: "Timed out waiting for Warning to change the type". The block editor of
the alert committed at 648 ms with the focus on `body` (`related=none`), right after the type list
opened (682 ms in the scenario steps), so the Warning click at 740 ms found no editor. The same
scenario passed every round of the stress job on the fix branch twice (runs 41692594254 and
41698052929, same code).

Second occurrence: release run 41711901580 (1.3.2, `main` 42cd340a), integration job, same step.
The page trace shows no mousedown for the Warning click at all; the text box blurs to nowhere at
page time 610 ms with the page still focused, and the page itself blurs 3 ms later (613 ms). So the
VS Code window lost the focus during the click and the click never reached the page. The redo rule
of the scenario (BLOCK-047 "commit to nowhere in an unfocused page") misses this order: the text
box blur comes a few ms before the page blur, while `pageFocus` is still true.

Likely fix: in `witnessPress` (test/integration/realInput), also accept a commit to nowhere followed
within a few ms by the page blur when no mousedown reached the page.

Earlier hypothesis: a blur of the alert's text box while the type list takes the focus, during a page
that briefly lost the window focus, commits the editor instead of keeping it open.

**Next step.** Re-run `just ci-stress 40` on the fix branch, or locally with
`STUDIO_REAL_INPUT_SCENARIO=stress`, and capture the page editor trace of the failing round.

## Moved to P1 (owner, 2026-11-04)

A version push makes `stress` blocking, so this flake can stop a tag. It failed on 2026-11-04 in
round 8 of 20 of CI run 41830004503, and once in a local `just preflight`: `Timed out waiting for
Warning to change the type`.

