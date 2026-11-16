# Description check, PR 181 at af970ea (head confirmed by gh pr view)

Result: NOT VERIFIED

Passed
- Diff: 2 files (chief-of-staff.md +76, status-layout.md +2/-2); `git diff origin/main --stat`. One commit af970ea. Changes section matches, no code.
- Floor terms, cut paragraph, report bullet, "When the time will not hold", Hard rule, Never bullet, status-layout Notes lines, Completion gets none: all present in the diff.
- Autonomous decision (CI unknown -> gate alone, `CI time unknown, not counted`): in the diff.
- Gate run 20261113-190315-26164: events.jsonl shows gate events ending 2026-11-13T18:27:15Z; start 19:03:15 local = 18:03:15Z, 24 min. Arithmetic 13x24=312 min, 6x34.4=206.4 min correct.
- `gh pr checks 181`: five checks pass (run 43578762102, head af970ea).
- Layout/order of sections, fold, blank lines, nothing after `</details>`, Internal references last: correct. No Issues References (no issue line assumed).

Failed
1. Internal reference outside Internal references: Deliverables quotes the card example with "CR-221 -> CR-237 -> CR-222 -> CR-225 -> CR-226 -> CR-228" (CR numbers). Rule: no CR number outside Internal references. Replace with placeholders or generic ids. (Also the Changes/Details text is fine; "Chief of Staff" is a product term of the changed card, allowed.)
2. Test plan: "latest passed CI run 10.4 min" is not the latest. `gh run list` shows the latest passed run (af970ea, 09:04:08Z-09:12:29Z) took about 8.4 min; 10.4 min is run on head 8566cca (08:27:14Z-08:37:38Z). Say "a recent passed run (8566cca) 10.4 min" or use 8.4 min and recompute (6 x 32.4 = 194.4 min; lock term still binds).
