# SC20 evidence: links, topics.json and names

Run: `work/coder3/checks_drivers.py`. Full output in `work/coder3/checks.out`.

```
## links
forward trouble-worker.md ../concepts.md
unresolved: []
## topics.json
load_topics ok 55
## trigger in card
part rows (reached from their parent row, not named in a card): ['ci-beside-gate', 'ci-no-check', 'conflicts-early-push', 'conflicts-local-gate', 'cr-prompt', 'cr-proof', 'handback-gate-draft', 'handback-refused', 'pr-gitlab', 'pr-images', 'refused-push-answer', 'retake-notes', 'retake-stack', 'stack-gate', 'stack-record', 'trouble-gate', 'trouble-git', 'trouble-remote', 'trouble-worker']
## forbidden
```

- Links: every relative link of the four cards and their topics resolves, but the one forward link `../concepts.md` of `topics/trouble-worker.md`. The files that child 23 moves (`concepts.md`, `pr-template.md`, `release-template.md`, `forges/`) are exceptions: they are not links to check yet.
- `help <name>` names: each one is a row of topics.json (checked by the script, "unresolved: []").
- topics.json: `load_topics` accepts it (55 rows: PART 1's 9 and SC20's). Every reading exists; every role is a name of `roles.yaml`; every `review_by` is `X.Y.Z` ("0.16.0" on trouble-gate, trouble-git, pr-gitlab, matrix, the incident rows).
- Trigger check: each card names its topics as `` `name` (trigger) `` with the trigger of topics.json; the part rows are reached from their parent row and named in no card (listed above). The script printed no "no line".
- Forbidden strings (`CR-<n>`, `batch-<n>`, `epoch`, a date) in the four cards, the topics and topics.json: none (the "## forbidden" section is empty). LF, no BOM: the script prints BAD for a file that has either, none.
