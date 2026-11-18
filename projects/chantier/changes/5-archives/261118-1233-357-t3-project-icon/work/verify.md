# Verify CR-357

Head: 1ed038919603387200db21974d264e450ef80b68

All claims judged at 1ed0389 (pushed head, PR 319 headRefOid equals it).

1. t3.json keys and values: python -I json.load -> `{'$schema': 'https://t3.codes/schema/t3.json', 'iconPath': 'docs/logo.svg'}`, keys exactly [$schema, iconPath]: True; ends with newline, no BOM, two-space indent (cat). PASS.
2. iconPath tracked and inside repo: `git ls-files docs/logo.svg t3.json` -> both printed; resolved path is_relative_to repo root: True. PASS.
3. logo.svg: ElementTree root `{http://www.w3.org/2000/svg}svg`, viewBox `0 0 64 64`, width=height=64, elements {svg, path, rect}; regex for font-family, href, data:, external URL -> []; 520 bytes. PASS.
4. Render: evidence/logo-256-and-16px.png opened: crane, hanging load, red cone on amber ground, legible at 256 px; the 16 px copy shows the same shapes (small but distinguishable). No path, username or home folder in the image. PASS.
5. `just check`: CI at the head, `gh pr check 319`: just check macos/ubuntu/windows pass, eval-dry-run pass, `just scenario (ubuntu-latest)` pass. Not re-run locally. PASS.
6. PR description (gh pr view 319): renders; JSON blocks, logo source and image present; Changes match the diff (two new files, `git diff --stat origin/main...HEAD`: docs/logo.svg, t3.json); scripts proposal matches spec; Known gaps "None" with no UNVERIFIED claim; no STALE; the image has no paths. Review box `approved at 1ed0389` backed by the Driver note "r1 committed as 1ed0389; inspector approved at bdd27e0f (body re-inspection approved too)" in `chantier log`. Remaining `<sha7>` placeholders in Verified and CI lines are for the Driver to fill. PASS.

VERIFIED
