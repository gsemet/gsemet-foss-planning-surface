# Verify CR-470 (PR 447)

Head: 79713ceea10ef8e193bef85c180cdb718b0ae32a

All claims judged at 79713ce (merge base f4c1bcc = origin/main), in the CR worktree.

- Section 1 byte-identical: awk of `## 1.` to `## 2.` of `git show f4c1bccd:skills/chantier/references/session-start.md` and of the head file, both md5 d5a9c486614adcd65940903b5072fd6f (3271 bytes). PASS.
- Forge wording: `grep -nE '\b(gh|glab)\b'` over session-start.md, session-start-*.md, titles.md, sync-checkout.md: no match. Section 4 and the board paragraph read "forge's own command-line tool (its reference in `forges/`)". PASS.
- Rule words: `read the file of the role the seat gives you, again when the role changes` in session-start.md (line 7); the two SKILL.md Startup cores carry the pointer "then your role's file there, again when the role changes" (declared in the PR). PASS.
- Sizes (LF bytes): session-start.md 29428 -> 12270; chief-of-staff 10925; griller 571; titles 2660; sync-checkout 4801. Match the PR table. PASS.
- Byte budget: `pytest test_startup_manifest.py -s` startup-bytes: chief-of-staff claude 11636/12527 (copilot 11642/12533), griller 11197/12088, status 11385/12276, router 11135/12026, foreman 7740/8631; all under 12544. Match the PR. Declared deviation: Foreman +19 bytes (manifest grew); it exceeds the spec's "Foreman unchanged" and chief-of-staff/griller are +13 over v0.15.1, both disclosed in the PR's Autonomous decisions. ACCEPTED.
- Manifest: diff shows chief-of-staff gains session-start-chief-of-staff.md and titles.md, board = concepts.md + session-start-chief-of-staff.md, new `sync` action, session-start/route/reload unchanged; no worker/Driver/Foreman reading names the new files (test_session_start_split passes). PASS.
- Citations: no remaining `6. Sync the checkout` / `3. Titles` reference outside the tests' MOVED_OUT rows; launch paragraph in the four SKILL.md says `sync-checkout.md`; CONTRIBUTING and docs/forge-connectors.md step 4 updated. PASS.
- Tests: `pytest tests/test_startup_manifest.py test_session_start_split.py test_launch_modes.py test_command_names.py test_plugin_files.py test_stack_shape.py test_code_targets.py`: 183 passed. CI at 79713ce: 5 checks SUCCESS (`gh pr view 447`).
- PR description: posted body equals work/pr-body.md (one extra blank line); Summary, Deliverables, Changes match the diff; Known gaps names the owed Fable reading. Test plan boxes still hold `<sha7>` placeholders, to be filled by the Driver; note for the Review box: the inspector's approval note (`log CR-470`) cites f4c1bcc (the base, before the commit), not 79713ce, so the box needs a carried or fresh note. Minor wording: forges/github.md reads "PR (pull request)s" (cosmetic).
- Not run: the long gate `scenario` (no pass at this head per `ship`'s off line; CI scenario job green).

VERIFIED
