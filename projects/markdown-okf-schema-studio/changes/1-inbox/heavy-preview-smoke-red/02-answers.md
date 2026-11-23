Short name: `heavy-red`

Grilled by the Chief of Staff on 2026-11-23 (bug day, batch-09). This is a routine regression fix:
the expected behaviour is that of 1.12.0, already approved, so there is no owner question.

1. heavy-red-Q1 (expected): **as in 1.12.0 / d9b3cd6b.** The real preview renders admonitions
   (and everything `preview-smoke` asserts), and both heavy jobs are green on the fixed head.
2. heavy-red-Q2 (product or test): **the cause decides.** The Driver proves the cause first, for
   example with a heavy run at d9b3cd6b and at each suspect commit, or with a local real window. A
   product regression is fixed in the product, with a test that would have caught it outside the
   heavy jobs where possible. A test that drifted is fixed in the test, and the PR says why the product is
   right. No assertion is weakened to turn the run green.
3. heavy-red-Q3 (place): **the bottom of batch-09's stack, on `main`, beside CR-477**, so that
   CR-475, CR-476, CR-477 and the release CR-478 can each be heavy-run on top of it. It ships in
   1.12.1, with a CHANGELOG line only if the product changed.
4. heavy-red-Q4 (scope): only this failure, plus any other heavy failure it was hiding (the steps
   after `preview-smoke` never ran), each one named in the PR. A hidden failure that needs a
   behaviour decision is reported to the Chief of Staff, not decided by the Driver.
