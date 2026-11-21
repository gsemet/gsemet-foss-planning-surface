# Verify CR-418

Head: a391c1ebe7bb8bc21b4cbc2d2ba729a2d5354963

Claims at a391c1e:
- Move since 800bd85 is one test regex (`git diff 800bd85 a391c1eb --stat`: test_live_link.py, 1 line, `lease 0\d:\d\d` -> `lease \d\d:\d\d`). Other claims carried from 800bd85 (see the previous judgment: refusals, pins, imports, docs, 1423 passed gate): no source file touched.
- Live tests at the head, after `uv sync --locked --project .`: `pytest test_live_link.py test_live_model.py -q` -> `17 passed in 5.49s` (ws and http, --once, lease).
- PR description as posted: Summary, Deliverables (capture at 800bd85, SHAs named), Changes, Test plan filled and consistent with the diff; capture shows made-up paths (/tmp/live-demo), `grep -ci gaeta evidence/live-once.txt` -> 0; Known gaps names the one gap (live screen not seen in a real terminal). Review box: log has `r2 approved at 4ed0d56, committed as 800bd85`, matching the box's 800bd85.
- CI at a391c1e as seen: all 5 checks pending (`gh pr checks 392`); not a proof. Remaining boxes "Verified" and "CI green" are the Driver's to tick.

VERIFIED
