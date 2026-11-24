# Verify CR-480

Head: b728c7150dab3b40c4d259e878595a81bc9a71b8

Claims, each judged at b728c71:

1. Behaviours of the spec (add, add-known unchanged, remove, remove-absent, slug, 3-ready path, batch path, number, target by slug, --note slug, unknown ref exit 2 naming the three forms, cycle exit 2 list untouched, exclusive forms exit 1, --add on `order note` exit 1, shared slug exit 2 with both ids, note recorded as ids or `-`):
   `uv run --no-sync python -m pytest tests/test_order_after.py -q` (in skills/chantier/scripts/cli) -> `21 passed in 7.05s`.
2. Absolute path and trailing separators (not in the test file): probe of `resolve_ref` on `C:/Users/user/p/changes/4-batch/1-pending/2-gamma-thing`, the same with backslashes and a trailing backslash, `3-ready/gamma-thing`, `gamma-thing`, `2`, `CR-1` -> all resolve to the right CR (CR-2, CR-2, CR-2, CR-2, CR-2, CR-1).
3. Scenario steps on the real CLI: gate log `work/gates/20261124-141927.log`, first line `gate CR-480 branch ... head b728c7150dab3b40c4d259e878595a81bc9a71b8`, last line `result: pass at b728c7150dab3b40c4d259e878595a81bc9a71b8`; the diff holds the two steps (--remove then --add by slug).
4. CI at head: `gh pr view 454` -> head b728c715, checks check (ubuntu, macos, windows), scenario (ubuntu), eval-dry-run all SUCCESS.
5. Cards and concepts.md lines match the spec (diff read at the head).
6. PR description, judged again at b728c71 (second pass, claims 1-5 carried from the first pass at the same head b728c71, nothing moved): `gh pr view 454 --json body` diffed against work/pr-body.md -> identical but a trailing newline. Known gaps says "None" (the stale UNVERIFIED bullet is gone; claim 3 shows the long gate passed). Test plan carries `b728c71` SHAs, no placeholders; the unticked boxes are the tests line (tests/test_order_after.py exists in the diff, 21 pass, claim 1) and Verified (set by this verdict). Review box `approved at b728c71`: `chantier log CR-480` -> `2026-11-24T13:00:44Z driver note note=r1 approved at a94085d..., committed as b728c71`, matches. Summary, Deliverables and Changes match the diff stat (flags, orders.py, orders_after.py new, orders_apply/word, cards, concepts, scenario, test). No images.

7. Description pass again at b728c71: `gh pr view 454 --repo gsemet/chantier` read against `git diff --stat origin/main...HEAD` (10 files) and the diff of orders_after.py, cards, scenario: Summary, Deliverables, Changes match; Known gaps None (no UNVERIFIED claim, evidence none stated); Review box matches the log note `committed as b728c71`; no images, no role names outside Internal references. Minor: Blast radius says 'two lines of cards' while the diff touches three card files (about nine lines); the Tests box is unticked though the test file exists (claim 1); neither fails the description.

VERIFIED
