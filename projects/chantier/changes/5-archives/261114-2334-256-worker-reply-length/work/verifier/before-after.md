# Before and after: verdict refusal
Command: verdict 999 APPROVED --batch batch-18 (word check runs before the CR lookup)
- Before, base 4ecc7cdbed4dc0b870732aac4d4b2f6542f6b448 (detached worktree): exit 1, error: verdict <cr> VERIFIED | "NOT VERIFIED"
- After, head 97e7df76352d48f1c497d301cd8a1efdd55fe188: exit 1, error: verdict: "APPROVED" is not a verdict: the accepted words are VERIFIED and "NOT VERIFIED"
Command: verdict 999 verified: base and head both pass the word check and stop at "unknown CR CR-999" (exit 2); VERIFIED is accepted.
