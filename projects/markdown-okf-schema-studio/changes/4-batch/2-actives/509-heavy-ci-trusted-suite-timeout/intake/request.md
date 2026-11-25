# Heavy CI red: the trusted suite exceeds its launch deadline

The heavy CI (the real VS Code jobs) is red: the `trusted-suite.js` launch of the `integration` job exceeds its 900000 ms deadline. Make it green again.

Observed (2026-11-25, GitHub Actions, workflow `ci.yml`):

- Push to `main` at 4a47151e, run 45580228461: `integration` failed, `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms deadline (STUDIO_LAUNCH_TIMEOUT_MS); last heartbeat step: lifecycle, marker: step started (suite trusted-suite, host pid 4864)`; a hang dump is in the `e2e-integration-attempt-1` artifact.
- Manual heavy run 45706313890 at 1f209e1 (the batch's stack top before its merge): attempt 1 failed on the same launch timeout; attempt 3 too, last heartbeat step `side-preview-jump`; attempt 2 failed on a `locator.count` timeout in the open-at-line test, not diagnosed.
- Earlier manual runs on the CR-503 branch also failed (45625193289 at 124a348, 45617988132 at 4404b98); cause not read.
- Last green push to `main`: 63ef752, run 45476952370 (2026-11-24T20:04Z).
- Push to `main` at 17b779d (after the merge of CR-508, CR-506, CR-502, CR-503), run 45713440510: still running when this was filed.

Not verified: the suite may simply have grown past its deadline (the last step differs between failures), or one step may stall.
