# Run the long gate on main after batch-17 and fix what it finds

Filed 2026-11-14 by the Chief of Staff, on the user's word: "finaliser ce batch le plus vite
possible quite à fixer les CI longue par la suite".

From about 12:50 on 2026-11-14, batch-17's PRs were merged without the local long gate
(`just scenario` on Windows, GitHub and GitLab): GitHub CI green at the head was accepted in its
place (`just check` on Linux, macOS and Windows, `just scenario` on Linux, `just eval-dry-run`).
Each waived CR records it, and its hand-back carries `--no-gate`.

What this CR does once batch-17 is merged: run the long gate (`just check`, `just scenario`) on
main on Windows, the GitHub and the GitLab scenarios, and fix any failure, one commit per cause.
Done when the long gate passes on main.
