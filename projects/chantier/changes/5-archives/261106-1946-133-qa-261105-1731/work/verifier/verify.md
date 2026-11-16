# verify.md, CR-133

Head: 3a69ea351ab8e88f4f75c234326f9f807ba8f4d5. Windows run; Linux and macOS are CI's. Evidence in evidence/ (before.txt, after.txt, docs-after.txt, before-after.md).

Findings:
1. file existing slug: fixed, `file X` twice -> exit 2, names `--slug <other>`.
2. triage backlog: fixed, P2 -> P3 exit 0; same priority exit 2 "already P3"; README.md/dir exit 1 naming the expected folders.
3. order drop twice / `101`: fixed, second drop exit 2 "already dropped", no new order; `order drop 101` accepted; `101x` exit 1.
4. applied orders shown pending: fixed, `status` has two lines (applied O-1,O-2; pending O-3 qa); `land` exit 2 names `order done <O-k>`; `order done` x3 then `land` exit 0.
5. dropped shows cancelled: docs now say so (docs/use-cases.md); `status` shows `cancelled`. `order note` on cancelled: exit 2.
6. order rounds / budget errors: fixed, `rounds --note 0` with a CR, no CR, `budget --note -5` all exit 1 with usage and reason.
7. QA folder open: fixed, exit 2 "QA report ... not to open".
8. cost/close on fresh batch: still refuse (exit 2), as wanted; docs now say it. `close` on a queued-CR batch exit 2, after land exit 2 "cannot be priced"; nothing deleted.
9. open output: fixed, `next:` plus `src -> dest` per CR; 8 CRs = 10 lines, next and all 8 CRs present.
Not replayed: `--batch` needed with several batches (not in the spec's fixes).

Unchanged and holding: close and close --yes exit 2 nothing deleted; order qa then status shows pending qa; cost fresh exit 2; order rounds on cancelled CR exit 0.
docs/use-cases.md changed sentences match the real answers (cancelled in status, "already dropped", two status lines, `order done` lets land pass, close needs a Foreman, `no open batch` after landing with `--batch <name>` working).

VERIFIED
