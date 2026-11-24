# test_live_ready fails when NO_COLOR=1 is set

Two tests in test_live_ready.py fail when the session's shell sets NO_COLOR=1, also on the main checkout.

Reported by the Foreman of batch-31 with CR-480 (2026-11-24). Make the tests independent of the environment (unset NO_COLOR in the test, or have the code under test not depend on it), and check that no other test reads NO_COLOR.
