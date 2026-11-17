# CR 206 — integration hang after coexistence: reproduction attempts (not reproduced)

Result: the real hang did not occur. The loop harness never got past round 2, so only 4 clean
rounds (round 1 of run 1, x4 shards) count; 0 hangs. Not a serious enough attempt to close the item.

| Run | Ref / commit | Setup | Outcome |
| --- | --- | --- | --- |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41145896019 | proof/206-integration-hang, 7c03827d | 4 shards x 25 rounds, delay 0 | all 4 shards: round 1 clean; `checkbox-toggle#2` step timeout (180 s, "waiting for the first checkbox render"). Cause: state left by round 1 (dirty feature-contract.md, extra tabs, Studio preview of tasks.md). |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41148069155 | proof/206-integration-hang-2, 4ac0cb08 (per-round reset) | same | all 4 shards: reset works (1 group, 1 tab each round), round 1 clean, `checkbox-toggle#2` fails in ~11 s: "Timed out waiting for edit mode." Deterministic: checkbox-toggle is not repeatable in one window (most likely the persisted per-document edit mode left ON by round 1, so the round-2 toggle turns it OFF). |

Side results:
- The #193 hang watchdog, hang dump, kill and artifact upload worked in a real CI run (run 1).
- Round-2 dump of run 1 (`Studio · tasks.md` active in group 2, no active text editor, first
  checkbox render never ready) is kept as a lead in the backlog item.

Decision (Foreman, 2026-10-31): stop here. 3 of 3 Coder/Inspector rounds used; the loop knob
(local commit 4ac0cb08) is NOT landed (not repeatable; Inspector round 3 had 3 blocking items).
The backlog item stays OPEN at P2 with these findings. Next attempt, if any: use a repeatable
next scenario (`table-empty-column`) or reset the persisted edit mode between rounds, wrap the reset
in a `loop-reset#N` step, and rerun 4x25.
