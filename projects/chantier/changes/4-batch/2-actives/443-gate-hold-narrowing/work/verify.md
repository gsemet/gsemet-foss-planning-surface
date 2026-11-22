# Verify CR-443

Head: a13f35f4006ac7f66e10d585237f964f090df05a

Judged at a13f35f (pushed head, `gh pr view 416` headRefOid). The restack moved the base widely, so the claims are judged again from the in-process suite at this head, not carried by hand probes of 1353bbd.

- Full CLI suite at a13f35f, `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests -q -n 4`: `1740 passed, 20 skipped in 194.07s`. It holds the gate refusals (free command and unknown name exit 1, no entry exit 2 with the three lines, bad key exit 2 before the name check, `--stop`/`--first` unchanged, surface-layer commands ignored with parallel merged: `test_gate_refusals.py`), the hold limits (45 default, 90 max, 0/91 and `-- cmd` exit 1, renewal never shortens, no `.lease-hold.*` file: `test_lease_hold.py`, `test_leases.py`, lease-late after a lapse), the shipped files (root `chantier.yaml`, `AGENTS.md`, eval kit) and `test_startup_manifest.py` (cr-driver byte limit). PASS.
- Targeted rerun `-k "hold or named or free or long_gate or gate_refus or ignored or shipped or startup_manifest"`: `234 passed, 1 skipped`; `test_gate_refusals.py test_leases.py test_startup_manifest.py`: `76 passed`. PASS.
- Fingerprint (`git show HEAD -- board/fingerprint.py`): `HOLDS` use and the `fnmatch` import removed from `counts_for`; spec section 3, last hold leftover ("`board/fingerprint.py`: `HOLDS = ".lease-hold.*.run"` and its comment go"), asks for exactly this, and `core/files.py` `IGNORED` keeps `".lease-hold.*.run"` (`grep -rn "lease-hold\|HOLDS" skills/.../src`: only `core/files.py:216`). Intended. PASS.
- Long suite at a13f35f: pipeline `just scenario (ubuntu-latest)` completed success, `just check` ubuntu and macos success, `just eval-dry-run` success (`gh run view 45001040991`, same run `gh pr checks 416`); `just check (windows-latest)` was still in progress when read. The scenario covers the hold lapse, "not confirmed" and the stack `lease-late`. PASS (Windows check open).
- Hold writes no file: `scenario/run_scenario.py:1020` asserts no `.lease-hold.*` after a hold; the scenario passed at head.

## PR description (`gh pr view 416`, head a13f35f)

Renders (Summary, Deliverables, fold, no images); Summary, Deliverables and Changes match the diff (fingerprint's `holds` removal is listed under `board/fingerprint.py`); Before-you-update, API change and `sandbox.py reset --yes` present; Known gaps matches. Note for the Driver: the Test plan boxes still name `1353bbd` (Review, Verified, CI, local gates); refresh them to a13f35f (or carry with the restack reason) before the ready line. No evidence images.

VERIFIED
