# Forge hub missed a merge: the watcher never saw it

Relayed from markdown-okf-schema-studio's Chief of Staff, on the owner's word (2026-11-24).

## What happened

- batch-09 of markdown-okf-schema-studio, parallel shape. The surface server (`serve --host 0.0.0.0`, the forge hub, PID 29916) wrote `merged@1` for CR-480 (https://github.com/gsemet/markdown-okf-schema-studio/pull/498, merged 14:19:17Z; journal seq 63 at 14:19:36Z).
- CR-481 (https://github.com/gsemet/markdown-okf-schema-studio/pull/499) merged at 15:49:21Z (merge commit 60daaef). The hub wrote no event for it: `changes/forge-journal.jsonl` still ends at seq 63 hours later.
- The Chief of Staff's watcher (`watch --after 63`) was running at 15:49 and later ended with "no event for batch-09 in 2 h". The owner found the merge by hand and asked "tu ne reçois pas les événements ?". The Chief of Staff ran `order merged CR-481` by hand.
- `status` at the time said `forge hub: PID 29916, the surface server, idle (no client subscribed)`. Not verified whether the hub was polling at 15:49, nor why it would be idle with a watcher running. The watcher had been restarted several times on its 2 h timeout.
- Side note seen in the same `status`: `forge-journal.jsonl: line 62 is of type arrived@1, unknown to this chantier: update it`, although the plugin copy in use wrote that line itself (`file`/`triage` of an inbox item). Probably unrelated, since seq 63 after it was delivered.

## Expected

1. Find why the hub missed the merge of #499 (idle hub, a watcher restart that did not subscribe again, a PR the hub did not know, or something else) and fix it.
2. A safety net: when the watcher ends on its quiet timeout, or when the hub is idle, it checks the batch's open PRs on the forge itself. A merge the journal missed is reported, not lost.
3. `status` names a CR whose PR is merged on the forge while the journal has no `merged` event for it.

## Seen again (2026-11-24)

CR-483 (https://github.com/gsemet/markdown-okf-schema-studio/pull/500) merged at 18:28:15Z: no `merged@1` event either, with a watcher (`watch --after 63`) running. Two missed merges in a row; recorded by hand with `order merged`.
