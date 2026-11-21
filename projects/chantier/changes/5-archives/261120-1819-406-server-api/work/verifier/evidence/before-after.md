# before-after, CR-406

Head (after): fea5a03bd671c27f60d1b14fae37a40b22c8d1a6. Base (before): origin/main daec1986.

No before/after pair was captured: the change has no picture ("No visual change", docs_screenshots not run) and the API did not exist at the base, so a "before" would only show the old routes, which claim 5 of verify.md shows gone at the head. The text logs of the head are `work/verifier/real-process-1.log` and `real-process-2.log` (reproduce with `probe.py.log`, a throwaway board started with `chantier board --host 127.0.0.1 --port 0` over a scratch project).
