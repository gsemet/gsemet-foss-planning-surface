# `verdict VERIFIED` refuses a verify note that does not name the head

Filed 2026-11-15 by the Chief of Staff from batch-18's retro (kept by the retro critic, reshaped by a Fable review), on the user's word "lance le tout dans le batch actuel".

Problem: workers still replied out of format after CR-256 (an Inspector "APPROVED" with no head, Verifiers that did not record their verdict so their Drivers ran `verdict` themselves, a conflict-resolver "Placeholder"); about 12 "restart: reply out of format" notes in batch-18; it recurs from batch-17. worker.md already says the Verifier runs `verdict` before replying; the CLI knows no role and cannot refuse "a Driver".

Fix (CLI, role-free refusal): `verdict <cr> VERIFIED` refuses when the CR's `work/verify.md` has no `Head:` line equal to the CR's recorded head, so the Verifier is corrected inside its own run. First check which card text the workers after CR-256's merge (2026-11-14 ~23:34) actually read; if they read the old one, say so in the spec and keep the change to the refusal. Neutral on host and forge.
