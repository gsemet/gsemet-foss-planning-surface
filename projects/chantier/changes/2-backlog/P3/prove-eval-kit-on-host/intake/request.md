# Prove the eval kit's host steps in a real campaign

Retro batch-13: nothing of the eval kit was proved on the host (setup.py's allow rules, sandbox.py merge on a real PR, reset --yes with real refs/pull/*). Fix: the first paid campaign proves them, running setup.py from the main checkout since its merge rule embeds the checkout's path.

Proved in part by real-direct run 1 (2026-11-12, PR 137): sandbox.py merge worked 5 of 5; setup.py's allow rules unproved (the session ran in auto mode, which lets the merges through anyway); reset ran as a plan only (it reads refs/pull/* through ls-remote and drops them from its plan; the refs of PRs 1 to 5 stay). Left: the allow rules outside auto mode, and reset --yes with real refs/pull/*.
