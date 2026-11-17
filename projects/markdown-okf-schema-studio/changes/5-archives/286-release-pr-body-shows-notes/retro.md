# Retro — 286-release-pr-body-shows-notes

| What happened | Root cause | Process fix |
| --- | --- | --- |
| CI red on the first push (checks, static, static-windows): `test_guideline_isolation.py` rejects the word "driver" in a project guideline | Run in direct mode by the Chief of Staff, pushed after a snippet test only; the local gate (`just check`, or at least `release-tests`) was not run because the change was "text only" | A text-only change still runs the local gate: project tests read the guidelines. Recorded in the Chief of Staff's memory; the retro step (CR 287) makes this review systematic |
| Auto-fix repaired it in one amend, no owner question | Works as intended (owner, 2026-11-11: "parfait comme use case de mini correction automatisée") | None |
| Release images are Git LFS: `raw.githubusercontent.com` serves the pointer | Found while testing the snippet | Written in the guideline (media.githubusercontent.com) |
