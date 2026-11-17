# Verify description CR-234

Head: 756a3878794c3e6737cc1d1d0c82a4ef5507302b
Verdict: VERIFIED

Code verified at 756a387 (verify.md carried). Claims, each at 756a387:

1. Head and diff. `gh pr view 175 --json headRefOid` = 756a387...; `git diff --stat origin/<cr-237 branch>..HEAD`: 7 files (scenario/README.md, fake_gh.py, run_scenario.py, hosts/claude-code.md, delivery.py, forge_stack.py, permissions.py). The Changes list names exactly these; nothing missing, nothing extra.
2. Detection. permissions.py: `_gh_names_stack` runs `gh extension list` once (`GH_LIST_TIMEOUT = 10`, `check=False`), true on exit 0 and `gh stack` or `*/gh-stack`; the XDG/LOCALAPPDATA folder test is removed; comment `# P10 counts these commands, not rules.` above SAMPLES. Matches.
3. Rebuild. forge_stack.py: `UNSTACK_TRIES = 5`, message `stack #n is still open after 5 unstack tries (the forge reads it back with #a #b)`, `EXIT_EXTERNAL` (4); `_rebuild` docstring added. Matches table and Autonomous decision.
4. Stale-SHA. delivery.py regex `\b(?=[0-9a-f]{0,39}[a-f])[0-9a-f]{7,40}\b`: letter a-f required. Matches.
5. Area 5 numbers. work/coder/area5-old-stack-base.log: 2 FAIL lines (texts equal the body's), `698/700`; area5-current.log `700/700`; long gate 700/700 at 756a387 per verify.md.
6. Real preflight. work/preflight-real-settings.log: `P10 warn 2 of 16 commands`; `gh extension list` here prints `gh stack	github/gh-stack	v0.3.0`. Matches (the 16 breakdown is consistent with the card's samples; not recounted).
7. Test plan. `gh pr checks 175`: check (macos, ubuntu, windows), eval-dry-run, scenario all pass. STATUS notes: inspector approved at e54e299, committed as 756a387; verdict VERIFIED 756a387; long gate pass 756a387. Boxes true.
8. Template audit. Sections in order, fold with Details, Human decisions omitted (no grill decision shaping the change: acceptable per template), no Issues References (no issue line assumed), Internal references last and holding CR-234 and work paths. No CR name, batch, role or `.agents/changes/` path outside it. Known gaps present, Blast radius has one grade. Deliverables has a table and a log block with SHAs.

Observation, not a failure: Summary and Changes use the preflight rule id "P10" (a term of the product's own preflight output, named in the card), and "the specification's default" in Autonomous decisions is generic wording; neither is a CR/batch/role reference.
