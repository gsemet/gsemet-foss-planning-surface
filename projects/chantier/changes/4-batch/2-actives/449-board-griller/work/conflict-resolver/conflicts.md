# Conflicts: CR-449 restack onto CR-439 head 870bae2e
- AGENTS.md (commit 1): kept HEAD's text (lease-hold sentence dropped upstream), added the board's Griller run to the network list.
- board/api/ops.py import list: kept both `griller` and `history_page` (sorted).
- board/context.py: kept both `history` and `griller` fields.
- board/api/protocol.json: regenerated with `just protocol-schema` (holds history and griller ops/topics).
Fast gate: none run, per the Driver's instruction (no `just check`).
