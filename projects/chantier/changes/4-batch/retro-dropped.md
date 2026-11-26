
## 2026-11-23: CR-463, CR-464

1. [chantier] CR-463's first Driver ended on `blocked waits: CI` at about 118k tokens, a fresh Driver needed: dropped, the rule already exists (driver.md, "Means: CI" and its context rule); once, $0.2, no user-visible defect.
2. [chantier] a second `take` is refused while the lease is live, so a cut-short skeleton is lost: dropped, not measured (once, 36 s, no defect).
3. [chantier] a release took three Release drivers: dropped, no problem and no fix proposed; it ran as the card says.

## 2026-11-26: CR-465, CR-466, CR-467, CR-468, CR-469, CR-470, CR-471, CR-472, CR-473, CR-474, CR-475, CR-476, CR-477, CR-478, CR-479, CR-480, CR-481, CR-482, CR-483, CR-484, CR-485, CR-486, CR-487, CR-488, CR-489, CR-490, CR-491, CR-492, CR-493, CR-494, CR-495, CR-496, CR-497, CR-498, CR-499, CR-500, CR-501, CR-502, CR-503, CR-504, CR-505, CR-506, CR-507, CR-508, CR-509, CR-510, CR-511, CR-512, CR-513, CR-514

1. [chantier] 14 `blocked context:` hand-backs, many at closing: dropped, open items already hold the fix (`context-limits-of-the-drivers-configurab`, `driver-checkpoint-and-a-ready-restart-br`, `drivers-compact-not-hand-back`); only one more after O-161.
2. [project] Local Windows long gate red on the machine's state (port 8765): dropped, CR-472 fixed it in this batch and open inbox items cover the rest.
5. [chantier] Long `lease not confirmed` and a stale stack lease: dropped, the lease card gives `lease hold` and an open inbox item covers the stack lease.
8. [chantier] Driver no-op messages and re-reports wake the Foreman: dropped, one no-op message on record, the Foreman's wake cost cannot be put down to them and `foreman-idle-wakes` covers it.
9. [chantier] Repeated stack-ready-to-merge asks for one stack link: dropped, `ready-asks` supersedes the earlier unread ask and each added newly ready CRs.
11. [chantier] A merge that swaps cards and CLI under a running Driver: dropped, once, the Foreman held the fast-forward, no defect reached the user.
13. [chantier] Foreman steering slips (an ask to the owner after O-173, badly worded notes, a missed escalation): dropped, each once with no measured cost.
14. [chantier] The watcher row says Monitor with no timeout against a 30-minute host cap: dropped, nothing in the batch records the cap or wakes from it.
15. [chantier] The classifier refused a Coder's temporary Edit of `brief.py`: dropped, once, not retried, the gap is named in Known gaps.
16. [project] CR-497's CI scenario red on exact-output checks after its last round: dropped, once, the long gate caught it before the merge as designed.
