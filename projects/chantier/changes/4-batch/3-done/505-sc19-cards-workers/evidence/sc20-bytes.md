# SC20 evidence: bytes against targets

Run: `work/coder3/checks_drivers.py` (output kept in `work/coder3/checks.out`), LF bytes, at the worktree's head plus the uncommitted SC20 files.

| card | target | bytes | result |
| --- | --- | --- | --- |
| cr-driver | 4096 | 3280 | within |
| stack-driver | 4096 | 3232 | within |
| release-driver | 3072 | 3056 | within |
| qa-driver | 2048 | 1337 | within |

| topic | target | bytes | result |
| --- | --- | --- | --- |
| checkpoints | 1536 | 965 | within |
| ci | 1536 | 1589 | over by 53 |
| ci-beside-gate | 1536 | 2052 | over by 516 |
| ci-no-check | 1536 | 1063 | within |
| closing | 1536 | 1888 | over by 352 |
| conflicts | 1536 | 2238 | over by 702 |
| conflicts-early-push | 1536 | 951 | within |
| conflicts-local-gate | 1536 | 1189 | within |
| cr-handback | 1536 | 1506 | within |
| cr-prompt | 1536 | 1391 | within |
| cr-proof | 1536 | 1044 | within |
| cr-rounds | 1536 | 2037 | over by 501 |
| cr-ship | 1536 | 2413 | over by 877 |
| cr-workers | 1536 | 1624 | over by 88 |
| handback-gate-draft | 1536 | 1341 | within |
| handback-other | 1536 | 2030 | over by 494 |
| handback-refused | 1536 | 1004 | within |
| lease | 1536 | 1385 | within |
| matrix | 1536 | 1347 | within |
| pr-extras | 1536 | 1898 | over by 362 |
| pr-gitlab | 1536 | 651 | within |
| pr-images | 1536 | 1882 | over by 346 |
| qa-results | 1536 | 946 | within |
| refused-push | 1536 | 1544 | over by 8 |
| refused-push-answer | 1536 | 1077 | within |
| release-end | 1536 | 976 | within |
| release-merged | 1536 | 2575 | over by 1039 |
| release-notes | 1536 | 1991 | over by 455 |
| release-ship | 1536 | 2306 | over by 770 |
| restart | 1536 | 1176 | within |
| retake | 1536 | 2328 | over by 792 |
| retake-notes | 1536 | 1871 | over by 335 |
| retake-stack | 1536 | 1818 | over by 282 |
| stack-changes | 1536 | 2354 | over by 818 |
| stack-gate | 1536 | 1176 | within |
| stack-hold | 1536 | 2232 | over by 696 |
| stack-joins | 1536 | 1470 | within |
| stack-make | 1536 | 1742 | over by 206 |
| stack-record | 1536 | 1233 | within |
| stack-restack | 1536 | 1832 | over by 296 |
| steering-messages | 1536 | 1295 | within |
| trouble-gate | 1536 | 1421 | within |
| trouble-git | 1536 | 906 | within |
| trouble-remote | 1536 | 1582 | over by 46 |
| trouble-worker | 1536 | 2173 | over by 637 |

Targets are targets: the cards are all within; 23 of the 45 Driver topic files are over 1,536 bytes, the worst release-merged (+1,039), cr-ship (+877), stack-changes (+818), retake (+792), release-ship (+770). They are listed in Known gaps of work/r3.md. No topic file has CR numbers, batch names, dates, CRLF or a BOM (sc20-links.md).

## `just test`

SC20 adds 0 seconds to `just test`: no test is added or changed, and no test reads `skills/chantier/cards-next/` (the files are cards and topics only, and `topics.json` rows are read by `load_topics` in PART 1's check, not by the suite).
