# Verification, CR-212, head ab84b5d (round 1): VERIFIED
1. HEAD is "release: v0.9.0"; version.py show = 0.9.0; the commit touches version files, agent/skill version lines and docs/release-notes/2026-11-13-v0.9.0/ only.
2. release_notes.py --check ok; --scan on release-notes.md and tweet.md rc 0.
3. N=92 = rev-list --no-merges --count v0.8.0..HEAD~1. 69 feat/fix commits, all 69 in 04-commit-map.md; notes sections match the map. Minor: restore (in cd1a89a) is not named in the notes, as the map admits.
4. No CR number, slug, batch number or .agents path in notes or tweet; images are bare file names. The three PNGs show sandbox batch-01 data only, no personal data.
5. PR body as posted (gh api): UTF-8, no BOM, same length as pr-body.md; notes then tweet after --- rules; image URLs use ab84b5dba9fb64788c0ae70974887920e4128443/docs/release-notes/2026-11-13-v0.9.0/; head sha matches; draft.
