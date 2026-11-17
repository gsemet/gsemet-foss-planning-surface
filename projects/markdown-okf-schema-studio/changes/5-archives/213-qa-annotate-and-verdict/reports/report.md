# CR 213 — report (Driver)

Commit `ed239750` on `c1399a18` (branch change-requests/213-qa-annotate-and-verdict, worktree
markdown-okf-schema-studio-wt-213). Not pushed, no PR (Foreman assembles the stack on #237).

| Round | Coder (sonnet) | Inspector (opus) |
| --- | --- | --- |
| 1 | annotate feature, Parts 2/3/3b, proof | CHANGES: label measured before attach covered the text; collisions; clip bounds; 0x0 boxes ([review](../reviews/round-1-inspector.md)) |
| 2 | all fixes + nits, clean proof retaken | CHANGES: 12 px selector clip forces labels inside; doc limit; wrong example ([review](../reviews/round-2-inspector.md)) |
| 3 | 34 px padding when annotating, docs, nits, clip proof | CHANGES (doc only, non-blocking): one sentence ([review](../reviews/round-3-inspector.md)) |

Proof (one real window, session cr213, synth/admon.md, `q doctor` no FAIL, stopped, QA_ROOT deleted):
[cr213-annotated-proof.jpg](cr213-annotated-proof.jpg), [cr213-annotated-proof-clip.jpg](cr213-annotated-proof-clip.jpg).
Printed boxes matched `q box` (797,294,290,22 and 797,330,290,66).

Gates: node --check 8/8, Python parse 4/4, bash -n 2/2, scenarios JSON 22/22, links 18 with 1 broken
(pre-existing placeholder harness-pitfalls.md:83, not in diff).

Open point (rounds exhausted): `references/qa-bug-template.md` lines 172–175, a 140-char line that also
says the 34 px padding applies to every `--clip SELECTOR`; it applies only when the shot has `--annotate`.
Nits: stale comment on `drawAnnotations`; unknown colour in the `{at, color}` object form not warned.
