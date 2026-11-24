Short name: `foreman-wake`

1. foreman-wake-Q1: **Scope.** B (not the recommended A): the timer (30 to 55 min on Claude Code) plus a watcher for the Foreman, which subscribes to the events (merge, CI red, wait met) instead of having them relayed. AGENTS.md's rule that the watcher is the Chief of Staff's is rewritten. Order: after `watcher-runs-through-several-events-inst` (watcher-limit) and after CR-471. Duplicates the paused inbox item `foreman-idle-wakes`.
Destination: next batch (3-ready): it touches `hosts/claude-code.md`, `foreman.md` (cut by CR-471) and the defaults file; it comes after `watcher-runs-through-several-events-inst`.
2. foreman-wake-Q2: **Who records a merge the user made, in Foreman mode.** A: the Foreman checks the forge, then runs `order merged <cr> --epoch <n>`; the Chief of Staff only tells the user, and keeps recording when the Foreman's watcher does not run.

Defaults taken on the spec-writer's other open questions (2026-11-24, no new question asked):
3. foreman-wake-D1: the Suspect threshold (one full heartbeat interval with no Driver activity) follows the wake to 55 minutes.
4. foreman-wake-D2: while the batch is paused with no Driver running, the Foreman's watcher keeps running (as watcher-limit-Q1 A does for the Chief of Staff's), so it catches the merge of a PR handed back ready.
5. foreman-wake-D3: a 55m default with the 60-minute limit kept; the CLI does not also refuse values below 30 or above 55.
Destination: running batch batch-31 (the user, 2026-11-24: "tout passer les ready dans le batch en cours"); after CR-476 (watcher-limit) and CR-471.
