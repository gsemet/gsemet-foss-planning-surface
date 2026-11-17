# Possible flake: "linked target replaced by a rename (atomic save)"

Seen during CR 241 on 2026-11-03, filed by the owner. The unit test failed once and did not
reproduce. Check whether it depends on timing or file-system events, and make it deterministic.
