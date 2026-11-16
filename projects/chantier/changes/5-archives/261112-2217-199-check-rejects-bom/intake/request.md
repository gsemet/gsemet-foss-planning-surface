batch-14 retro: CR-191 round 3's Coder wrote a UTF-8 BOM into evals/kit/dry_run.py on Windows and a whole round existed only to strip it. Fix: just check rejects a byte-order mark in any tracked text file, so a BOM is red at the gate, not at review.

Also seen in real-direct run 1 (2026-11-12, PR 137): conflict resolutions twice left a UTF-8 BOM in files. Besides the gate, the conflict-resolver and Coder cards repeat the no-BOM rule.
