# Verify CR-256
Head: 97e7df76352d48f1c497d301cd8a1efdd55fe188
1. git diff --stat origin/main..HEAD at 97e7df76352d48f1c497d301cd8a1efdd55fe188: only run_scenario.py, driver.md, worker.md, delivery.py (4 files).
2. git grep -n at 97e7df76352d48f1c497d301cd8a1efdd55fe188: worker.md has the templates (lines 23, 51, 140); driver.md:102-104 has the long-reply paragraph and the `long reply: <role>:` note.
3. Refusal before/after: see before-after.md (exit 1 both, new one-line message at head).
4. Not run: a recorded VERIFIED on a scratch CR (used a nonexistent CR); my own verdict on the real CR records it. Scenario and CI green per caller.
Result: VERIFIED
