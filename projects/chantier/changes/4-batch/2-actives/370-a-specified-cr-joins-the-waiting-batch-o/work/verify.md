Head: b2ae16d3d294e20015e3009683455124bb74a71a

Method: the CLI of the CR worktree (`uv run --no-sync --project <worktree> chantier`, not the
prompt's main-checkout line, which lacks `--factory`) in two scratch repositories (p, q), each with its own
bare remote, `--project` unset, cwd = the scratch repo. Raw logs: `verifier/run1.log` .. `run8.log` (paths made up).
All judged at b2ae16d3 (the pushed head).

1. `open` with no CR is a factory, born paused (run1.log): `opened batch-01 on claude: no CR, paused, 4 slots,
   parallel, steering foreman, factory`; `next:` line with the factory clause; `3-ready holds 1 CRs not joined`
   line; `events.jsonl` open event has `factory: true`; `status` says `factory: on`, `no CR yet: triage <folder>
   --ready joins one on its own`, and the `factory: 3-ready holds ...` line. PASS.
2. `triage --ready` joins in a factory batch (run1.log): prints `triaged ...`, the order line O-1, `added CR-101, queued`,
   `stays paused`, `factory batch-01: CR-101 joined on its own ...`; `order` event carries `origin: "triage --ready"`. PASS.
3. Refused join (run3.log): depends.json naming an unknown slug: stderr `not joined batch-01: ... the CR waits in
   3-ready (...)`, exit 2, `triaged 3-ready/delta` on stdout, no new order event (count stays 4). PASS.
4. No join on a non-factory batch (run6.log, run5.log): plain `open` with a CR, `triage two --ready`: only `triaged`, zero orders. PASS.
   Also after factory off (run5.log): zeta triaged, no order added. PASS.
5. `order factory off|on` (run2.log, run6.log): off/on recorded done at once and applied (batch.json orders), events `factory`
   + `order`, brief token `Factory: off.`, already-in-state refusals (exit 2), bad usage (exit 1), `on` prints the 3-ready line,
   `on` turns any open batch into a factory (q). PASS.
6. Release joining turns factory off (run4.log): `order add --release` prints `factory off: the release CR CR-103 joined ...`;
   then `order factory on` refused `a release CR is in batch-01: it ends the factory ...` (exit 2). PASS.
   `open --factory --release 1` refused with the reason and way out (run6.log). PASS.
7. End of last CR in a factory batch (run7.log): `next: factory batch-01 waits for its next ready CR ...: no retro and no close now`. PASS.
   `order factory off` on a paused, all-ended batch adds `every CR is merged or cancelled: next: the retro ...` (run8.log). PASS.
8. Not run by hand: `open --factory` with CRs, `order factory off` at a batch that never held a CR (the
   `no CR ever joined` line): covered by test_opening_and_restore.py / test_factory.py (not re-proved here).
9. Tests at head: `pytest test_factory.py test_open_empty_batch.py test_batch_end.py` -> 43 passed.
10. Shipped words: README `## Factory mode` present; docs/use-cases*.md sentences present; batch-lifecycle-texts.md three
    additions; board i18n `batch.factory_on`, `batch.no_cr_yet_factory` in en and fr. PASS (read in the diff).
    SVG docs/batch-lifecycle.svg: well-formed XML (python minidom); not rendered (no renderer on this machine); the diff
    is coordinates only, the grown rect (y 558..616) holds the two added text lines (y 597, 610). Looks right by reading.
Second pass (description only, head b2ae16d3d294e20015e3009683455124bb74a71a unchanged): claims 1-10 carried
from b2ae16d: no code move (only the PR body changed).

11. PR description (gh pr view 342 --json body, judged at b2ae16d3):
    - Fixed: Changes bullet now names `commands/factory.py` (grep -n "def set_factory" -> commands/factory.py:24,
      ready_not_joined :44). PASS.
    - Fixed: Human decisions now says the README advises stack/4; README.md:124 "usual opening is `--mode stack --slots 4`". PASS.
    - Summary, Deliverables, Changes match the diff (52 files, factory.py new, README, cards, board web, svg). PASS.
    - Review box `approved at 1908533`: `log 370` note "r2 inspector approved at 19085335ea..." and "r2 approved at 19085335, committed as b2ae16d3". PASS.
    - CI green at b2ae16d: log note "gh pr checks 342 at b2ae16d: all 5 pass". PASS.
    - FAIL: Test plan says "Local gates at b2ae16d: just check, just eval-dry-run, scenario direct unit". The log holds
      only `just check: pass; just eval-dry-run: pass (17 of 17)` at b2ae16d3; "scenario direct pass" is a round-1 note at
      19085335, and `ship` says `no long gate passed at b2ae16d`. The scenario claim at b2ae16d has no proof: narrow it
      (drop "scenario direct unit", or cite the ubuntu CI scenario job) or run it.

Third pass, head unchanged b2ae16d3d294e20015e3009683455124bb74a71a (claims 1-10 carried from b2ae16d: no code move).
12. PR description re-judged at b2ae16d3 (gh pr view 342 --json body): Test plan now reads "Local gates at `b2ae16d`: just check and
    just eval-dry-run pass (the scenario ran in the pipeline job, see CI)". Matches the log (just check pass; eval-dry-run pass 17/17).
    `gh pr checks 342`: just scenario (ubuntu-latest) pass, 3m43s, run 44385464582, whose headSha is b2ae16d3d294e20015e3009683455124bb74a71a.
    The item-11 FAIL is fixed. Rest of the description unchanged. PASS.

VERIFIED

Fourth pass (description only), head unchanged b2ae16d3d294e20015e3009683455124bb74a71a (claims 1-12 carried: no code move).
13. PR description re-judged at b2ae16d3 (gh pr view 342 --json body, headRefOid b2ae16d3d294e20015e3009683455124bb74a71a):
    only change is the Test plan box "Verified at `b2ae16d`" now ticked, backed by this file's VERIFIED at that head. Renders
    (sections, mermaid, fold), no image (no username or home path), SHAs b2ae16d and 1908533 match the log notes (item 11),
    Known gaps (SVG hand-edited, not rendered) matches item 10, no internal role name outside Internal references. PASS.

VERIFIED
