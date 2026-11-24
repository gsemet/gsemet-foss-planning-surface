# Verify, CR-481

Head: 007aa019c42db53b8261b854e35578769a491db6

All claims judged at 007aa019c42db53b8261b854e35578769a491db6 unless noted.

1. New pytest file red at base, green at head.
   Base c155c897 (test file copied in): `3 failed` (`KeyError: 'services'`).
   Head: `uv run --locked --group dev pytest -q skills/chantier/scripts/cli/tests/test_status_index_services.py` -> `3 passed in 2.64s`.
   The tests assert merged (newest first, cost), created, counts, services (server pid/url/build_note, hub/writer null, watchers), `server` null with no server, and neither key text nor `?k=` in the written STATUS.json.
2. `just mod` at head: `94 pass, 0 fail` (includes the pane tests: batch of merged CRs shown, each state shown, figures line, Backlog/Merged/Services folded, Services fold, links with keys from server.json, no server.json gives keyless links plus one line, older index shape draws as before).
3. Gate pass cited: gate log first line `gate CR-481 branch ... head 007aa019c42db53b8261b854e35578769a491db6`, last line `result: pass at 007aa019c42db53b8261b854e35578769a491db6` (work/gates/20261124-173321.log); `$CHANTIER log` shows `gate result=pass head=007aa019... name=scenario`.
4. CI at head (`gh pr view 457`): just check ubuntu/macos/windows, just scenario ubuntu, just eval-dry-run all SUCCESS.
5. Driver's note: `just check`, `just eval-dry-run`, `just mod` pass at 007aa01 (log, 16:33:18Z). Review notes: approved at c155c897 and 84246818, committed as 007aa019 (log 16:22:54Z, 16:23:00Z).
6. PR description (posted body at head 007aa019): renders, sections and fold present, Summary/Deliverables/Changes match the diff (14 files: views, write, links, address, register, types, tests, CONTRIBUTING, boards.md, orders_apply import, three test updates). Known gaps names the missing screenshot, the published services, the snapshot age. The Test plan boxes still hold `<sha7>` placeholders for the Driver to fill at ready; no image is attached.
7. Not proved: the pane in a real Claude Code session (screenshot); it is a Known gap, not a failure. The live planning folder was not written; STATUS.json proof is the in-test write.

VERIFIED
