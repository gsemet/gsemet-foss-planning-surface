# Heavy CI red: the trusted suite exceeds its launch deadline

Make the heavy CI (the real VS Code jobs, run on every push to `main` and on demand) green again,
by fixing why the `trusted-suite.js` launch exceeds its deadline and the second failure seen once
on the open-at-line test.

Why: `main` has been red since 4a47151e (2026-11-25 morning), so a heavy run no longer proves
anything about a pull request, and the batch's later merges go to `main` without that proof.

In scope: the cause of the launch timeout; the `locator.count` timeout of the open-at-line test;
a heavy run green at the pull request's head.

Out of scope: new tests, new product behaviour, the acceptance job of CR-505.
