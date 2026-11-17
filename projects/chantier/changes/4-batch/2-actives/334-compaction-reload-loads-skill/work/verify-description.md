Head: 6cb7984413b39a8aa03bb2e19f36fe536d8a52ae

Description-only pass (second), judged at 6cb7984. VERIFIED.

- Rendering: `gh pr view 293 --json body` shows sections, table, code block and a closed-form `<details>` fold; no images. Clean.
- Consistency: `git diff <base>...HEAD --stat` lists 11 files; the Changes section now names all 11 (hooks/register.tsx, register.test.tsx, three skills, session-start.md, claude-code.md, copilot.md, root README.md, status SKILL.md, types/index.d.ts). The status/types edits match the diff (sync-failure wording shortened; "reload line" -> "reload message"). No delivered change unmentioned, none claimed missing.
- Known gaps: carries the UNVERIFIED trial claims, the pane reset and the shortened wording; not "None".
- Review box: `chantier log 334` has "r2 approved at 47abe26, committed as 6cb79844" and the inspector approval at 47abe26. Matches.
- Test plan SHAs: gates note at 6cb7984 (just check 455 pass, just mod 65 pass), CI 5 jobs pass at 6cb7984 in the log.
- Role names: only product terms (Chief of Staff, Griller) of the change itself; Internal references holds the CR line. No STALE mark. No images.
