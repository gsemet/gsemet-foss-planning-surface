# Before / after, CR-321

Before: no receipt on the Costs page (base = the CR-319 branch); not captured, the receipt is new. The
reference is the approved mock-up. After: head 89d43b134414099a54d501f654d6c4468deed091 (all images recaptured at 89d43b1; caption each with 89d43b1).

| File | Shows |
| --- | --- |
| `mockup-pc.png`, `mockup-phone.png` | `final-costs.html`, `final-costs-phone.html` rendered (Chromium) |
| `after-full-pc.png`, `after-full-phone.png` | real Costs page of the demo's `mobile-app` batch-02 (full receipt), 1400px and 375px |
| `after-norecord-pc.png`, `after-norecord-phone.png` | same batch with `cost_receipt` null: "roles not recorded", shown once |
| `after-notcomputed-pc.png`, `after-notcomputed-phone.png` | demo `shop-api` running batch-03, no transcripts: pill "running", live error, Recompute in the receipt |

Reproduce: `uv run --script work/verifier/shots.py <worktree> <evidence folder> <mock-up folder>` from the worktree
(demo copied to a scratch surface, board on loopback, clock fixed). Paths on screen are made up
(`C:\vfdemo`, `/home/demo`); no username.

Differences from the mock-up: Steering label "Foreman" (demo batch is Foreman; mock-up is a direct batch,
"Chief of Staff"); Outside the budget on two lines (Q9; mock-up one line); demo figures, not batch-22's.
Not captured: a paused batch (same code path as running).
